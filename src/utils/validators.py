import re
from email_validator import validate_email, EmailNotValidError


# Vérifier un email
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


# Vérifier un numéro de téléphone
def is_valid_phone(phone):
    pattern = r'^\+?[\d\s\-]{8,20}$'
    return bool(re.match(pattern, phone))


# Vérifier la force du mot de passe
def is_valid_password(password):
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True


# Vérifier un montant
def is_valid_amount(amount):
    return amount > 0


# Vérifier le nombre de participants
def is_valid_attendees(attendees):
    return attendees > 0
