from src.models.user import User
from src.utils.auth import verify_password, create_access_token, decode_access_token
from src.utils.logger import log_event, log_error

class AuthController:
    """Gère l'authentification des utilisateurs."""

    def __init__(self, db):
        self.db = db
        self.current_user = None

    def login(self, email, password):
        """Authentifie un utilisateur."""
        try:
            # Chercher l'utilisateur
            user = self.db.query(User).filter(User.email == email).first()

            # Vérifier email + mot de passe
            if user is None:
                log_event("login_failed", {"email": email, "reason": "user_not_found"})
                raise ValueError("Email ou mot de passe incorrect")

            if not verify_password(password, user.password_hash):
                log_event("login_failed", {"email": email, "reason": "wrong_password"})
                raise ValueError("Email ou mot de passe incorrect")

            # Créer le token
            token = create_access_token(user.id, user.role.value)
        
            # Logger le succès
            log_event("login_success", {
                "user_id": user.id,
                "email": email,
                "role": user.role.value
            })
        
            return {
                "token": token,
                "user": user
            }
        except Exception as e:
            log_error(e, {"email": email})
            raise
        
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
