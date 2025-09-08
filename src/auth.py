"""
Authentication and session management module.
Handles user authentication, password hashing, and session management.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from utils import verify_password
from config import config
from session_store import session_store
from logging_config import app_logger

# Use centralized configuration
SECRET_KEY = config.security.secret_key
ALGORITHM = config.security.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.security.access_token_expire_minutes


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user with email and password."""
    # Import locally to avoid circular imports
    from data import get_user_by_email_for_auth
    
    user = get_user_by_email_for_auth(email)
    if not user:
        return None
    
    if not verify_password(password, user['password']):
        return None
    
    return user


def create_session(user: Dict[str, Any]) -> str:
    """Create a new session for a user."""
    session_id = secrets.token_urlsafe(32)
    
    try:
        session_store.create_session(
            session_id=session_id,
            user_id=user['email'],
            data={'user_data': user}
        )
        app_logger.info(f"Session created for user: {user['email']}")
        return session_id
    except Exception as e:
        app_logger.error(f"Failed to create session for user {user['email']}: {str(e)}")
        raise


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session data by session ID."""
    try:
        return session_store.get_session(session_id)
    except Exception as e:
        app_logger.error(f"Failed to get session {session_id}: {str(e)}")
        return None


def destroy_session(session_id: str) -> bool:
    """Destroy a session."""
    try:
        result = session_store.destroy_session(session_id)
        if result:
            app_logger.info(f"Session destroyed: {session_id}")
        return result
    except Exception as e:
        app_logger.error(f"Failed to destroy session {session_id}: {str(e)}")
        return False


def get_current_user(session_id: str) -> Optional[Dict[str, Any]]:
    """Get current user from session."""
    session = get_session(session_id)
    if not session:
        return None
    
    # Import locally to avoid circular imports
    from data import get_user_by_email_for_auth
    
    user_id = session.get('user_id')
    if not user_id:
        return None
    
    user = get_user_by_email_for_auth(user_id)
    return user


def regenerate_session(old_session_id: str, user: Dict[str, Any]) -> str:
    """Regenerate session ID for security (prevents session fixation)."""
    # Destroy old session
    destroy_session(old_session_id)
    
    # Create new session
    new_session_id = create_session(user)
    
    app_logger.info(f"Session regenerated for user: {user['email']}")
    return new_session_id
