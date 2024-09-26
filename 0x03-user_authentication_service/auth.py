#!/usr/bin/env python3
"""auth model"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Any
from user import User


def _hash_password(password: str) -> str:
    """"hash password"""
    if password is None or not isinstance(password, str):
        return None
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError(f'User {email} already exists')
