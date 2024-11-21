#!/usr/bin/env python3
"""Database module for user authentication.

This module provides the DB class to interact with the user database,
allowing for user creation and retrieval.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User  # Ensure User is imported


class DB:
    """DB class for managing database operations.

    This class handles the connection to the database and provides methods
    for adding and finding users.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.

        This method sets up the database engine and creates the necessary
        tables if they do not exist.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        This property returns a session object for interacting with the
        database, creating one if it does not already exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)  # Add the user to the session
        self._session.commit()
        return new_user  # Return the created User object

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        This method queries the database for a user matching the provided
        keyword arguments and returns the first matching user.

        Args:
            **kwargs: Arbitrary keyword arguments representing user attributes.

        Returns:
            User: The found User object.

        Raises:
            InvalidRequestError: If an invalid query argument is provided.
            NoResultFound: If no user matches the criteria.
        """
        session = self._session
        valid_columns = {column.name for column in User.__table__.columns}

        for key in kwargs.keys():
            if key not in valid_columns:
                raise InvalidRequestError(f"Invalid query argument: {key}")

        user = session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound("No user found matching the criteria.")

        return user
