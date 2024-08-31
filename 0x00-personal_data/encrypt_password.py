#!/usr/bin/env python3
import bcrypt

def hash_password(password: str) -> bytes:
    """ Hash a password using bcrypt """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if the password is valid """
    return bcrypt.checkpw(password.encode(), hashed_password)
