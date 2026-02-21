import pytest
from src.controllers.contract_controller import ContractController
from src.models.contract import Contract
from src.models.user import Role



def test_get_all_contracts(db, commercial_user, contract):
    """Test récupération de tous les contrats."""
    controller = ContractController(db, commercial_user)
    contracts = controller.get_all_contracts()
    
    assert len(contracts) >= 1
    assert any(c.id == contract.id for c in contracts)


def test_get_all_contracts_not_authenticated(db):
    """Test sans authentification."""
    controller = ContractController(db, None)
    
    with pytest.raises(PermissionError):
        controller.get_all_contracts()


def test_get_unsigned_contracts(db, commercial_user, contract):
    """Test récupération des contrats non signés."""
    controller = ContractController(db, commercial_user)
    contracts = controller.get_unsigned_contracts()
    
    assert len(contracts) >= 1
    assert all(c.is_signed == False for c in contracts)


def test_get_unpaid_contracts(db, commercial_user, contract):
    """Test récupération des contrats non payés."""
    controller = ContractController(db, commercial_user)
    contracts = controller.get_unpaid_contracts()
    
    assert len(contracts) >= 1
    assert all(c.remaining_amount > 0 for c in contracts)


def test_create_contract_as_gestion(db, admin_user, client):
    """Test création d'un contrat par GESTION."""
    controller = ContractController(db, admin_user)
    
    new_contract = controller.create_contract(
        client_id=client.id,
        total_amount=15000.00,
        remaining_amount=10000.00
    )
    
    assert new_contract.id is not None
    assert new_contract.total_amount == 15000.00
    assert new_contract.remaining_amount == 10000.00
    assert new_contract.is_signed == False


def test_create_contract_default_remaining(db, admin_user, client):
    """Test création sans spécifier le montant restant."""
    controller = ContractController(db, admin_user)
    
    new_contract = controller.create_contract(
        client_id=client.id,
        total_amount=20000.00
    )
    
    # Le montant restant doit être égal au total
    assert new_contract.remaining_amount == 20000.00


def test_create_contract_as_commercial(db, commercial_user, client):
    """Test qu'un commercial ne peut pas créer de contrat."""
    controller = ContractController(db, commercial_user)
    
    with pytest.raises(PermissionError):
        controller.create_contract(
            client_id=client.id,
            total_amount=10000.00
        )


def test_create_contract_client_not_found(db, admin_user):
    """Test création avec un client inexistant."""
    controller = ContractController(db, admin_user)
    
    with pytest.raises(ValueError, match="Client non trouvé"):
        controller.create_contract(
            client_id=99999,  # ID qui n'existe pas
            total_amount=10000.00
        )


def test_sign_contract_as_owner(db, commercial_user, contract):
    """Test signature d'un contrat par le propriétaire."""
    controller = ContractController(db, commercial_user)
    
    signed = controller.sign_contract(contract.id)
    
    assert signed.is_signed == True


def test_sign_contract_as_gestion(db, admin_user, contract):
    """Test signature d'un contrat par GESTION."""
    controller = ContractController(db, admin_user)
    
    signed = controller.sign_contract(contract.id)
    
    assert signed.is_signed == True


def test_sign_contract_as_support(db, support_user, contract):
    """Test qu'un support ne peut pas signer."""
    controller = ContractController(db, support_user)
    
    with pytest.raises(PermissionError, match="SUPPORT ne peut pas signer"):
        controller.sign_contract(contract.id)


def test_sign_contract_not_found(db, commercial_user):
    """Test signature d'un contrat inexistant."""
    controller = ContractController(db, commercial_user)
    
    with pytest.raises(ValueError, match="Contrat non trouvé"):
        controller.sign_contract(99999)


def test_sign_already_signed_contract(db, commercial_user, contract):
    """Test qu'on ne peut pas re-signer un contrat."""
    controller = ContractController(db, commercial_user)
    
    # Signer une première fois
    controller.sign_contract(contract.id)
    
    # Essayer de re-signer
    with pytest.raises(ValueError, match="déjà signé"):
        controller.sign_contract(contract.id)


def test_get_contract_by_id(db, contract):
    """Test récupération d'un contrat par ID."""
    controller = ContractController(db, None)
    
    found = controller.get_contract_by_id(contract.id)
    
    assert found is not None
    assert found.id == contract.id


def test_get_contract_by_id_not_found(db):
    """Test récupération d'un contrat inexistant."""
    controller = ContractController(db, None)
    
    found = controller.get_contract_by_id(99999)
    
    assert found is None