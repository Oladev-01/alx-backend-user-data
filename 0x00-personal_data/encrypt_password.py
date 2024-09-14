#!/usr/bin/env python3
"""hash password"""
from xmlrpc.client import boolean
import bcrypt


def hash_password(password: str) -> bytes:
    """returns hash"""
    get_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return get_hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check the validity of password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
