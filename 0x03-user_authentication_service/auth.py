#!/usr/bin/env python3
"""Authentication module for user management.

Provides functions for user authentication, including registration.
"""

import bcrypt
from db import DB
from user import User  # Ensure User is imported
from auth import _hash_password  # Ensure _hash_password is imported
from sqlalchemy.orm.exc import NoResultFound  # Import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Takes a password string, generates a salt, and returns the salted hash.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password.

        Checks if a user with the given email exists. If not, hashes the
        password and saves the user to the database.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
