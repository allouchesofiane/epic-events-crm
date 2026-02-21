import pytest
from src.permissions.decorators import (
    check_is_authenticated,
    check_is_gestion,
    check_is_commercial
)


def test_authenticated_with_user(admin_user):
    """Test avec un utilisateur connecté."""
    check_is_authenticated(admin_user)


def test_authenticated_without_user():
    """Test sans utilisateur connecté."""
    with pytest.raises(PermissionError):
        check_is_authenticated(None)


def test_gestion_with_admin(admin_user):
    """Test qu'un admin a les droits GESTION."""
    check_is_gestion(admin_user)


def test_gestion_with_commercial(commercial_user):
    """Test qu'un commercial n'a pas les droits GESTION."""
    with pytest.raises(PermissionError):
        check_is_gestion(commercial_user)


def test_commercial_with_commercial(commercial_user):
    """Test qu'un commercial a les droits COMMERCIAL."""
    check_is_commercial(commercial_user)