import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a password with a salt and returns the hashed password as bytes."""
    salt = bcrypt.gensalt()  # Generate a new salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password with the salt
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
