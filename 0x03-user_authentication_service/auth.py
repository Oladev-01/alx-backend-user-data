#!/usr/bin/env python3
"""auth model"""
from cgitb import reset
import uuid
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt
from typing import Union
from user import User


def _hash_password(password: str) -> str:
    """"hash password"""
    if password is None or not isinstance(password, str):
        return None
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """generate a uuid"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validate credential"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """returns session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """It takes a single session_id string argument
        Returns a string or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys sessions"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except (InvalidRequestError, NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generate a new token"""
        try:
            user = self._db.find_user_by(email=email)
            new_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except (InvalidRequestError, NoResultFound):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """use reset token to update the user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (InvalidRequestError, NoResultFound):
            raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pwd,
                             reset_token=None)
        return None
