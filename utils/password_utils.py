import hashlib
import os

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a random salt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        A string containing the salt and hashed password, separated by ':'
    """
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{pwd_hash}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        stored_password: The stored password hash (format: 'salt:hash')
        provided_password: The password to verify
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    try:
        salt, pwd_hash = stored_password.split(':')
        return pwd_hash == hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()
    except (ValueError, AttributeError):
        return False
