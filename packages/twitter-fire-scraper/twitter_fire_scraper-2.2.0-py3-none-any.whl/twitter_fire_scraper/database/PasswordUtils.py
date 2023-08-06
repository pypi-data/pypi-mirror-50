from werkzeug.security import generate_password_hash


def hash_password(password) -> str:
    """Standardized way to hash a password."""
    return generate_password_hash(password, method='pbkdf2:sha512', salt_length=128)