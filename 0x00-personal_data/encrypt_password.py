#!/usr/bin/env python3
""" Defines hash_password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Creates a hash password using bcrypt """
    password = password.enode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates a hashed password"""
    passwordE = password.encode()
    return bcrypt.checkpw(passwordE, hashed_password)
