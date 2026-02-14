from src.models.user import Role


def check_is_authenticated(current_user):
    if current_user is None:
        raise PermissionError("Vous devez être connecté.")


def check_is_gestion(current_user):
    check_is_authenticated(current_user)
    if current_user.role != Role.GESTION:
        raise PermissionError("Action réservée au rôle GESTION.")


def check_is_commercial(current_user):
    check_is_authenticated(current_user)
    if current_user.role != Role.COMMERCIAL:
        raise PermissionError("Action réservée au rôle COMMERCIAL.")


def check_is_support(current_user):
    check_is_authenticated(current_user)
    if current_user.role != Role.SUPPORT:
        raise PermissionError("Action réservée au rôle SUPPORT.")


def check_is_owner_or_gestion(current_user, entity, ownership_field):
    check_is_authenticated(current_user)

    if current_user.role == Role.GESTION:
        return

    owner_id = getattr(entity, ownership_field)

    if owner_id != current_user.id:
        raise PermissionError("Vous n'êtes pas le propriétaire.")
