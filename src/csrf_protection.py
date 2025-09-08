"""
CSRF (Cross-Site Request Forgery) protection utilities.
Provides token generation and validation for form submissions.
"""

import secrets
import hmac
import hashlib
import time
from typing import Optional, Dict, Any
from itsdangerous import URLSafeTimedSerializer, BadSignature
from logging_config import app_logger
from config import config
from exceptions import ValidationError


class CSRFProtection:
    """CSRF protection implementation."""
    
    def __init__(self):
        """Initialize CSRF protection."""
        self.serializer = URLSafeTimedSerializer(
            config.security.csrf_secret_key,
            salt='csrf-token'
        )
        self.token_max_age = 3600  # 1 hour
    
    def generate_token(self, session_id: str) -> str:
        """Generate a CSRF token for a session."""
        try:
            # Create token data including timestamp and session
            token_data = {
                'session_id': session_id,
                'timestamp': int(time.time()),
                'nonce': secrets.token_urlsafe(16)
            }
            
            # Serialize and sign the token
            token = self.serializer.dumps(token_data)
            app_logger.debug(f"Generated CSRF token for session: {session_id}")
            return token
            
        except Exception as e:
            app_logger.error(f"Failed to generate CSRF token: {str(e)}")
            raise ValidationError("Failed to generate security token")
    
    def validate_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token."""
        if not token:
            app_logger.warning("Missing CSRF token")
            return False
        
        try:
            # Deserialize and verify the token
            token_data = self.serializer.loads(
                token,
                max_age=self.token_max_age
            )
            
            # Verify session matches
            if token_data.get('session_id') != session_id:
                app_logger.warning(f"CSRF token session mismatch: expected {session_id}, got {token_data.get('session_id')}")
                return False
            
            # Verify timestamp is recent
            token_timestamp = token_data.get('timestamp', 0)
            current_time = int(time.time())
            if current_time - token_timestamp > self.token_max_age:
                app_logger.warning("CSRF token expired")
                return False
            
            app_logger.debug(f"CSRF token validated for session: {session_id}")
            return True
            
        except BadSignature:
            app_logger.warning("Invalid CSRF token signature")
            return False
        except Exception as e:
            app_logger.error(f"CSRF token validation error: {str(e)}")
            return False
    
    def create_hidden_input(self, session_id: str) -> str:
        """Create hidden input HTML for CSRF token."""
        token = self.generate_token(session_id)
        return f'<input type="hidden" name="csrf_token" value="{token}" />'
    
    def verify_form_token(self, form_data: Dict[str, Any], session_id: str) -> bool:
        """Verify CSRF token from form data."""
        csrf_token = form_data.get('csrf_token')
        if not csrf_token:
            raise ValidationError("Missing CSRF protection token")
        
        if not self.validate_token(csrf_token, session_id):
            raise ValidationError("Invalid or expired security token")
        
        return True


# Global CSRF protection instance
csrf_protection = CSRFProtection()


def csrf_protect(func):
    """Decorator to add CSRF protection to form handlers."""
    def wrapper(*args, **kwargs):
        # Extract form data and session info
        # Note: This is a simplified implementation for NiceGUI
        # In a real web application, you'd extract these from the request
        
        form_data = kwargs.get('form_data', {})
        session_id = kwargs.get('session_id', 'anonymous')
        
        try:
            # Verify CSRF token
            csrf_protection.verify_form_token(form_data, session_id)
            
            # Remove CSRF token from form data before processing
            if 'csrf_token' in form_data:
                del form_data['csrf_token']
            
            return func(*args, **kwargs)
            
        except ValidationError as e:
            app_logger.warning(f"CSRF protection failed for {func.__name__}: {str(e)}")
            raise
    
    return wrapper


def get_csrf_token(session_id: str) -> str:
    """Get CSRF token for a session."""
    return csrf_protection.generate_token(session_id)


def validate_csrf_token(token: str, session_id: str) -> bool:
    """Validate CSRF token for a session."""
    return csrf_protection.validate_token(token, session_id)