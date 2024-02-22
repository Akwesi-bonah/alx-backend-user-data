#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
        for k in kwargs.keys():
            if k not in User.__table__.columns.keys():
                raise InvalidRequestError
        query = self._session.query(User).filter_by(**kwargs).first()
        if query is None:
            raise NoResultFound
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user’s attributes as passed in the arguments
        """
        user = self.find_user_by(id=user_id)
        for k in kwargs.keys():
            if k not in User.__table__.columns.keys():
                raise ValueError
        for k, v in kwargs.items():
            setattr(user, k, v)
        self._session.commit()
