
import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 8


def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Vérifie un mot de passe contre son hash.
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(user_id: int, role: str) -> str:
    """
    Crée un token JWT pour un utilisateur.
    """
    now = datetime.now(timezone.utc)
    
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": now + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": now
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    """
    Décode et vérifie un token JWT.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expiré. Veuillez vous reconnecter.")
    except jwt.InvalidTokenError:
        raise ValueError("Token invalide. Veuillez vous reconnecter.")