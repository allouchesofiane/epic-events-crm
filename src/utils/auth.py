import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


# Hash d’un mot de passe
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


# Vérifier un mot de passe et son hash
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# Créer un token JWT
def create_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# Lire un token JWT
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
