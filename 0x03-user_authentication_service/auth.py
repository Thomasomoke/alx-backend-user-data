#!/usr/bin/env python3
"""Authentication module for user management.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    This method takes a password string, generates a salt,
    and returns the salted hash of the password.
    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
