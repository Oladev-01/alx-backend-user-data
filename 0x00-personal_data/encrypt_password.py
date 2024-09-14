#!/usr/bin/env python3
"""hash password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns hash"""
    get_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return get_hash
