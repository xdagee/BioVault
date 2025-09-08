"""
Custom exceptions for the application.
Provides structured error handling with specific exception types.
"""

from typing import Optional, Dict, Any


class BioAppException(Exception):
    """Base exception for the Bio App."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BioAppException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR", details)


class AuthenticationError(BioAppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class AuthorizationError(BioAppException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTHZ_ERROR", details)


class DatabaseError(BioAppException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, operation: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.operation = operation
        super().__init__(message, "DATABASE_ERROR", details)


class UserNotFoundError(BioAppException):
    """Raised when a user is not found."""
    
    def __init__(self, email: str, details: Optional[Dict[str, Any]] = None):
        self.email = email
        super().__init__(f"User with email '{email}' not found", "USER_NOT_FOUND", details)


class UserAlreadyExistsError(BioAppException):
    """Raised when trying to create a user that already exists."""
    
    def __init__(self, email: str, details: Optional[Dict[str, Any]] = None):
        self.email = email
        super().__init__(f"User with email '{email}' already exists", "USER_EXISTS", details)


class SessionError(BioAppException):
    """Raised when session operations fail."""
    
    def __init__(self, message: str, session_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.session_id = session_id
        super().__init__(message, "SESSION_ERROR", details)


class ConfigurationError(BioAppException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.config_key = config_key
        super().__init__(message, "CONFIG_ERROR", details)
