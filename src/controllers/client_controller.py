from src.models.user import Role
from src.models.client import Client
from src.permissions.decorators import (
    check_is_authenticated,
    check_is_commercial,
    check_is_owner_or_gestion
)
from src.utils.logger import log_event, log_error

class ClientController:
    """Gère les opérations sur les clients."""

    def __init__(self, db, current_user=None):
        self.db = db
        self.current_user = current_user

    def get_all_clients(self):
        """Retourne tous les clients."""
        check_is_authenticated(self.current_user)
        return self.db.query(Client).all()

    def get_my_clients(self):
        """Retourne les clients du commercial connecté."""
        check_is_commercial(self.current_user)

        return self.db.query(Client).filter(
            Client.commercial_contact_id == self.current_user.id
        ).all()

    def create_client(self, full_name, email, phone, company_name=None):
        """Crée un client (COMMERCIAL uniquement)."""
        check_is_commercial(self.current_user)

        try:
            new_client = Client(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                commercial_contact_id=self.current_user.id
            )

            self.db.add(new_client)
            self.db.commit()
        
            # Logger
            log_event("client_created", {
                "client_id": new_client.id,
                "created_by": self.current_user.id
            })

            return new_client
    
        except Exception as e:
            log_error(e, {"action": "create_client", "email": email})
            raise


    def update_client(self, client_id, full_name=None, email=None,
                      phone=None, company_name=None):

        client = self.db.query(Client).filter(Client.id == client_id).first()

        if client is None:
            raise ValueError("Client non trouvé")

        # SUPPORT interdit
        if self.current_user.role == Role.SUPPORT:
            raise PermissionError("Le rôle SUPPORT ne peut pas modifier les clients")

        # Vérifier propriétaire ou admin
        check_is_owner_or_gestion(
            self.current_user,
            client,
            "commercial_contact_id"
        )

        if full_name:
            client.full_name = full_name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if company_name is not None:
            client.company_name = company_name

        self.db.commit()
        
        # Logger
        log_event("client_updated", {
            "client_id": client.id,
            "updated_by": self.current_user.id
        })
        return client

    def get_client_by_id(self, client_id):
        return self.db.query(Client).filter(Client.id == client_id).first()
