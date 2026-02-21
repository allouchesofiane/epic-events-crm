import pytest
from src.controllers.client_controller import ClientController


def test_get_all_clients(db, commercial_user, client):
    """Test la récupération de tous les clients."""
    controller = ClientController(db, commercial_user)
    clients = controller.get_all_clients()
    
    assert len(clients) >= 1


def test_create_client(db, commercial_user):
    """Test la création d'un client."""
    controller = ClientController(db, commercial_user)
    
    new_client = controller.create_client(
        full_name="Nouveau Client",
        email="nouveau@client.com",
        phone="+33698765432"
    )
    
    assert new_client.id is not None
    assert new_client.full_name == "Nouveau Client"


def test_update_client(db, commercial_user, client):
    """Test la modification d'un client."""
    controller = ClientController(db, commercial_user)
    
    updated = controller.update_client(
        client.id,
        full_name="Nom Modifié"
    )
    
    assert updated.full_name == "Nom Modifié"