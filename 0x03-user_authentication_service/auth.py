#!/usr/bin/env python3
"""auth model"""
import bcrypt
from typing import Any


def _hash_password(password: str) -> Any:
    """"hash password"""
    if password is None or not isinstance(password, str):
        return None
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
