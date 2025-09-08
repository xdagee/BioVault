"""
Rate limiting middleware for API endpoints.
Provides protection against brute force attacks and DoS attempts using memory storage.
"""

import time
import hashlib
from typing import Dict, Callable, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from logging_config import api_logger
from config import config
from exceptions import BioAppException


class RateLimitExceeded(BioAppException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: int, limit_type: str = "general"):
        self.retry_after = retry_after
        self.limit_type = limit_type
        super().__init__(
            f"Rate limit exceeded for {limit_type}. Try again in {retry_after} seconds.",
            "RATE_LIMIT_EXCEEDED",
            {"retry_after": retry_after, "limit_type": limit_type}
        )


class RateLimiter:
    """Memory-based rate limiter."""
    
    def __init__(self):
        """Initialize rate limiter."""
        # Memory storage for rate limiting
        self._memory_store: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "reset_time": 0})
        
    def _get_client_identifier(self, request_info: Dict) -> str:
        """Get client identifier for rate limiting."""
        # In a real application, you'd extract IP from request
        # For NiceGUI, we'll use a combination of session and endpoint
        session_id = request_info.get('session_id', 'anonymous')
        endpoint = request_info.get('endpoint', 'unknown')
        user_agent = request_info.get('user_agent', '')
        
        # Create a hash of identifiers
        identifier_str = f"{session_id}:{endpoint}:{user_agent}"
        return hashlib.sha256(identifier_str.encode()).hexdigest()[:16]
    
    def is_allowed(self, request_info: Dict, limit_type: str = "general") -> tuple[bool, Optional[int]]:
        """Check if request is allowed based on rate limits."""
        if not config.rate_limit.enabled:
            return True, None
        
        identifier = self._get_client_identifier(request_info)
        
        # Get rate limit configuration
        if limit_type == "auth":
            limit = config.rate_limit.auth_requests_per_minute
        else:
            limit = config.rate_limit.requests_per_minute
        
        window_seconds = 60  # 1 minute window
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        try:
            return self._check_memory_rate_limit(identifier, limit_type, limit, current_time, window_start)
        except Exception as e:
            api_logger.error(f"Rate limiting error: {str(e)}")
            # Allow request on error to avoid blocking legitimate users
            return True, None
    
    def _check_memory_rate_limit(self, identifier: str, limit_type: str, limit: int, current_time: int, window_start: int) -> tuple[bool, Optional[int]]:
        """Check rate limit using memory storage."""
        key = f"{limit_type}:{identifier}"
        rate_data = self._memory_store[key]
        
        # Reset if window has passed
        if current_time >= rate_data["reset_time"]:
            rate_data["count"] = 0
            rate_data["reset_time"] = current_time + 60
        
        if rate_data["count"] >= limit:
            retry_after = rate_data["reset_time"] - current_time
            return False, retry_after
        
        rate_data["count"] += 1
        return True, None
    
    def record_failed_attempt(self, request_info: Dict, limit_type: str = "auth"):
        """Record a failed authentication attempt."""
        if not config.rate_limit.enabled:
            return
        
        identifier = self._get_client_identifier(request_info)
        api_logger.warning(f"Failed {limit_type} attempt from {identifier}")


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit_middleware(limit_type: str = "general"):
    """Decorator for rate limiting endpoints."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Extract request info (simplified for NiceGUI)
            request_info = {
                'endpoint': func.__name__,
                'session_id': getattr(kwargs, 'session_id', 'anonymous'),
                'user_agent': 'NiceGUI-Client',
                'timestamp': time.time()
            }
            
            # Check rate limit
            allowed, retry_after = rate_limiter.is_allowed(request_info, limit_type)
            
            if not allowed:
                api_logger.warning(f"Rate limit exceeded for {func.__name__} from {request_info}")
                raise RateLimitExceeded(retry_after, limit_type)
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                # Record failed attempts for auth endpoints
                if limit_type == "auth" and isinstance(e, (ValueError, Exception)):
                    rate_limiter.record_failed_attempt(request_info, limit_type)
                raise
        
        return wrapper
    return decorator


def auth_rate_limit(func: Callable) -> Callable:
    """Rate limit decorator specifically for authentication endpoints."""
    return rate_limit_middleware("auth")(func)


def general_rate_limit(func: Callable) -> Callable:
    """Rate limit decorator for general endpoints."""
    return rate_limit_middleware("general")(func)