#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user

        Returns:
            User: The created User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find a user in the database by specific attributes
        Args:
            **kwargs: Arbitrary keyword arguments representing the,
                      attributes of the user to search for

        Returns:
            User: The User object that matches the specified attributes

        Raises:
            NoResultFound: If no user with the specified attributes is found
            InvalidRequestError: If the query parameters are invalid
        """
        try:
            # Query the User model with the provided keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            # NoResultFound is raised when the .one(),
            # method doesn't find any matches
            raise NoResultFound()
        except InvalidRequestError:
            # InvalidRequestError is raised when the,
            # query parameters are invalid
            raise InvalidRequestError()
        # If a user was found and no exceptions were raised,
        # we return the user
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database

        Args:
            user_id (int): The id of the user to update
            **kwargs: Arbitrary keyword arguments representing,
                      the attributes to update

        Raises:
            ValueError: If an argument that does not correspond to,
                        a user attribute is passed
        """
        # Use find_user_by to locate the user to update
        user = self.find_user_by(id=user_id)

        # Check if any of the kwargs do not correspond to User attributes
        for key in kwargs:
            if not hasattr(user, key):
                raise ValueError()

        # Update the user's attributes and commit changes to the database
        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
