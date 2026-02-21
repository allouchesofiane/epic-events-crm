import src.models
import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.config import Base
from src.models.user import User, Role
from src.models.client import Client
from src.utils.auth import hash_password
from src.models.contract import Contract

@pytest.fixture
def db():
    """Crée une base de données de test en mémoire."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def admin_user(db):
    """Crée un utilisateur admin."""
    user = User(
        full_name="Admin Test",
        email="admin@test.com",
        password_hash=hash_password("Admin123!"),
        role=Role.GESTION
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def commercial_user(db):
    """Crée un utilisateur commercial."""
    user = User(
        full_name="Commercial Test",
        email="commercial@test.com",
        password_hash=hash_password("Commercial123!"),
        role=Role.COMMERCIAL
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def client(db, commercial_user):
    """Crée un client de test."""
    client = Client(
        full_name="Client Test",
        email="client@test.com",
        phone="+33612345678",
        company_name="Test Company",
        commercial_contact_id=commercial_user.id
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@pytest.fixture
def contract(db, client, commercial_user):
    """Crée un contrat de test."""
    contract = Contract(
        client_id=client.id,
        commercial_contact_id=commercial_user.id,
        total_amount=10000.00,
        remaining_amount=5000.00,
        is_signed=False
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


@pytest.fixture
def support_user(db):
    """Crée un utilisateur support pour les tests."""
    from src.models.user import User
    from src.utils.auth import hash_password
    
    user = User(
        full_name="Support Test",
        email="support@test.com",
        password_hash=hash_password("Support123!"),
        role=Role.SUPPORT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

