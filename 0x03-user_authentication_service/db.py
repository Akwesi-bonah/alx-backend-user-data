#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base


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
        """returns a User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    
    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table
        """
        if kwargs is None:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise InvalidRequestError
        query = self._session.query(User).filter_by(**kwargs).first()
        if query is None:
            raise NoResultFound
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user’s attributes as passed in the arguments
        """
        if user_id is None and kwargs is None:
            raise InvalidRequestError

        user = self.find_user_by(id=user_id)
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise ValueError
        for key, v in kwargs.items():
            setattr(user, key, v)
        self._session.commit()
