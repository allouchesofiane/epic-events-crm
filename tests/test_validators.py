from src.utils.validators import (
    validate_email_format,
    validate_phone,
    validate_password_strength
)


def test_email_valid():
    """Test un email valide."""
    assert validate_email_format("test@example.com") == True


def test_email_invalid():
    """Test un email invalide."""
    assert validate_email_format("pas_un_email") == False


def test_phone_valid():
    """Test un téléphone valide."""
    assert validate_phone("+33612345678") == True


def test_phone_invalid():
    """Test un téléphone invalide."""
    assert validate_phone("123") == False


def test_password_valid():
    """Test un mot de passe valide."""
    is_valid, message = validate_password_strength("Password123!")
    assert is_valid == True


def test_password_too_short():
    """Test un mot de passe trop court."""
    is_valid, message = validate_password_strength("Pass1")
    assert is_valid == False