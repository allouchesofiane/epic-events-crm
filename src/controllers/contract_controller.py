from src.models.user import Role
from src.models.contract import Contract
from src.models.client import Client
from src.permissions.decorators import (
    check_is_authenticated,
    check_is_gestion,
    check_is_owner_or_gestion
)
from src.utils.logger import log_event, log_error

class ContractController:
    """Gère les opérations sur les contrats."""

    def __init__(self, db, current_user=None):
        self.db = db
        self.current_user = current_user

    def get_all_contracts(self):
        check_is_authenticated(self.current_user)
        return self.db.query(Contract).all()

    def get_unsigned_contracts(self):
        check_is_authenticated(self.current_user)
        return self.db.query(Contract).filter(Contract.is_signed == False).all()

    def get_unpaid_contracts(self):
        check_is_authenticated(self.current_user)
        return self.db.query(Contract).filter(Contract.remaining_amount > 0).all()

    def create_contract(self, client_id, total_amount, remaining_amount=None):
        check_is_gestion(self.current_user)

        client = self.db.query(Client).filter(Client.id == client_id).first()
        if client is None:
            raise ValueError("Client non trouvé")

        if remaining_amount is None:
            remaining_amount = total_amount

        new_contract = Contract(
            client_id=client_id,
            commercial_contact_id=client.commercial_contact_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=False
        )

        self.db.add(new_contract)
        self.db.commit()
        
        log_event("contract_created", {
            "contract_id": new_contract.id,
            "client_id": client_id,
            "created_by": self.current_user.id
})

        return new_contract

    def sign_contract(self, contract_id):

        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if contract is None:
            raise ValueError("Contrat non trouvé")

        # SUPPORT interdit
        if self.current_user.role == Role.SUPPORT:
            raise PermissionError("Le rôle SUPPORT ne peut pas signer de contrats")

        check_is_owner_or_gestion(
            self.current_user,
            contract,
            "commercial_contact_id"
        )

        if contract.is_signed:
            raise ValueError("Ce contrat est déjà signé")

        contract.is_signed = True
        self.db.commit()

        log_event("contract_signed", {
            "contract_id": contract.id,
            "signed_by": self.current_user.id
        })
        return contract

    def get_contract_by_id(self, contract_id):
        return self.db.query(Contract).filter(Contract.id == contract_id).first()
