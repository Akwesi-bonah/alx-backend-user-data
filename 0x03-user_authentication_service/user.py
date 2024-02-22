#!/usr/bin/env python3
"""
SQLAlchemy model named User for a database table named users
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    '''SQLAlchemy model named User'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        '''returns class attributes'''
        return "<User(name='%s', email='%s', session_id='%s')>" % (
                             self.name, self.email, self.session_id)
