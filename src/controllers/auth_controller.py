from src.models.user import User
from src.utils.auth import verify_password, create_access_token, decode_access_token


class AuthController:
    """Gère l'authentification des utilisateurs."""

    def __init__(self, db):
        self.db = db
        self.current_user = None

    def login(self, email, password):
        """Authentifie un utilisateur."""

        # Chercher l'utilisateur
        user = self.db.query(User).filter(User.email == email).first()

        # Vérifier email + mot de passe
        if user is None:
            raise ValueError("Email ou mot de passe incorrect")

        if not verify_password(password, user.password_hash):
            raise ValueError("Email ou mot de passe incorrect")

        # Créer le token
        token = create_access_token(user.id, user.role.value)

        return {
            "token": token,
            "user": user
        }

    def verify_token(self, token):
        """Vérifie un token et retourne l'utilisateur."""

        payload = decode_access_token(token)

        user = self.db.query(User).filter(User.id == payload["user_id"]).first()

        if user is None:
            raise ValueError("Utilisateur non trouvé")

        return user

    def set_current_user(self, token):
        """Définit l'utilisateur connecté."""

        self.current_user = self.verify_token(token)
        return self.current_user
