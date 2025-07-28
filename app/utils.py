
from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256."""
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return pbkdf2_sha256.verify(plain_password, hashed_password)

