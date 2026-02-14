from src.models.user import User, Role
from src.utils.auth import hash_password
from src.permissions.decorators import check_is_gestion


class UserController:
    """Gère les opérations sur les utilisateurs."""

    def __init__(self, db, current_user=None):
        self.db = db
        self.current_user = current_user

    def get_all_users(self):
        """Retourne tous les utilisateurs (GESTION uniquement)."""

        check_is_gestion(self.current_user)

        return self.db.query(User).all()

    def create_user(self, full_name, email, password, role):
        """Crée un nouvel utilisateur (GESTION uniquement)."""

        check_is_gestion(self.current_user)

        # Vérifier si l'email existe déjà
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError("Cet email est déjà utilisé")

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=Role[role.upper()]
        )

        self.db.add(new_user)
        self.db.commit()

        return new_user

    def get_user_by_id(self, user_id):
        """Retourne un utilisateur par son ID."""
        return self.db.query(User).filter(User.id == user_id).first()
