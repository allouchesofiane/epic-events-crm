from src.utils.auth import hash_password, verify_password, create_access_token


def test_hash_password():
    """Test le hashage du mot de passe."""
    password = "MonMotDePasse123!"
    hashed = hash_password(password)
    
    assert hashed != password


def test_verify_password_correct():
    """Test la vérification avec le bon mot de passe."""
    password = "MonMotDePasse123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) == True


def test_verify_password_incorrect():
    """Test la vérification avec le mauvais mot de passe."""
    password = "MonMotDePasse123!"
    hashed = hash_password(password)
    
    assert verify_password("MauvaisMotDePasse", hashed) == False


def test_create_token():
    """Test la création d'un token."""
    token = create_access_token(user_id=1, role="gestion")
    
    assert isinstance(token, str)
    assert len(token) > 50