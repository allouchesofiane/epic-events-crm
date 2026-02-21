"""Utilitaires de validation des données."""
import re
from email_validator import validate_email, EmailNotValidError


def validate_email_format(email: str) -> bool:
    """
    Valide le format d'un email.
    """
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def validate_phone(phone: str) -> bool:
    """
    Valide le format d'un numéro de téléphone.
    
    """
    pattern = r'^\+?[\d\s\-\(\)]{8,20}$'
    return bool(re.match(pattern, phone))


def validate_password_strength(password: str) -> tuple:
    """
    Vérifie la force d'un mot de passe.
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    return True, ""


def validate_amount(amount: float) -> bool:
    """
    Valide un montant financier.
    """
    return amount > 0


def validate_attendees(attendees: int) -> bool:
    """
    Valide un nombre de participants.
    """
    return attendees > 0