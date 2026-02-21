import pytest
from src.controllers.auth_controller import AuthController
from src.utils.auth import create_access_token


def test_login_success(db, admin_user):
    """Test une connexion réussie."""
    controller = AuthController(db)
    
    result = controller.login("admin@test.com", "Admin123!")
    
    assert "token" in result
    assert "user" in result
    assert result["user"].email == "admin@test.com"
    assert result["user"].id == admin_user.id


def test_login_wrong_email(db):
    """Test avec un email qui n'existe pas."""
    controller = AuthController(db)
    
    with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
        controller.login("inexistant@test.com", "Password123!")


def test_login_wrong_password(db, admin_user):
    """Test avec un mauvais mot de passe."""
    controller = AuthController(db)
    
    with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
        controller.login("admin@test.com", "MauvaisPassword")


def test_verify_token_valid(db, admin_user):
    """Test la vérification d'un token valide."""
    controller = AuthController(db)
    
    token = create_access_token(admin_user.id, admin_user.role.value)
    user = controller.verify_token(token)
    
    assert user.id == admin_user.id
    assert user.email == "admin@test.com"


def test_verify_token_invalid(db):
    """Test avec un token invalide."""
    controller = AuthController(db)
    
    with pytest.raises(ValueError):
        controller.verify_token("token_completement_invalide")


def test_set_current_user(db, admin_user):
    """Test la définition de l'utilisateur courant."""
    controller = AuthController(db)
    
    token = create_access_token(admin_user.id, admin_user.role.value)
    user = controller.set_current_user(token)
    
    assert controller.current_user is not None
    assert controller.current_user.id == admin_user.id