"""Configuration de la base de données."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Charger les variables d'environnement
load_dotenv()

# Base pour les modèles
Base = declarative_base()

# URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///epic_events.db")

# Créer le moteur de base de données
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialise la base de données (crée les tables)."""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès !")


def get_db():
    """Générateur de session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()