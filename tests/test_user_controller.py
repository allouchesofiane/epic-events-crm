import pytest
from src.controllers.user_controller import UserController


def test_get_all_users_as_admin(db, admin_user):
    """Test qu'un admin peut voir les utilisateurs."""
    controller = UserController(db, admin_user)
    users = controller.get_all_users()
    
    assert len(users) >= 1


def test_get_all_users_as_commercial(db, commercial_user):
    """Test qu'un commercial ne peut pas voir les utilisateurs."""
    controller = UserController(db, commercial_user)
    
    with pytest.raises(PermissionError):
        controller.get_all_users()


def test_create_user(db, admin_user):
    """Test la création d'un utilisateur."""
    controller = UserController(db, admin_user)
    
    new_user = controller.create_user(
        full_name="Nouvel Utilisateur",
        email="nouveau@test.com",
        password="Password123!",
        role="commercial"
    )
    
    assert new_user.id is not None
    assert new_user.email == "nouveau@test.com"