"""
Utility functions for the application.
Contains shared functions that don't have circular dependencies.
"""

import bcrypt
from typing import Optional


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    if not password or not hashed_password:
        return False
    
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False
