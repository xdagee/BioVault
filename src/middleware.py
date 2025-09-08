"""
Middleware for request/response processing.
Handles logging, metrics, security headers, and rate limiting.
"""

import time
from typing import Callable, Any
from logging_config import api_logger
from monitoring import record_request_metrics
from rate_limiter import rate_limiter, RateLimitExceeded
from csrf_protection import csrf_protection


def rate_limiting_middleware(func: Callable, limit_type: str = "general") -> Callable:
    """
    Middleware to apply rate limiting to endpoints.
    
    Args:
        func: The function to wrap
        limit_type: Type of rate limit to apply ('general' or 'auth')
        
    Returns:
        Wrapped function with rate limiting
    """
    def wrapper(*args, **kwargs):
        # Extract request information for rate limiting
        request_info = {
            'endpoint': func.__name__,
            'session_id': getattr(kwargs, 'session_id', 'anonymous'),
            'user_agent': 'NiceGUI-Client',
            'timestamp': time.time()
        }
        
        try:
            # Check rate limit
            allowed, retry_after = rate_limiter.is_allowed(request_info, limit_type)
            
            if not allowed:
                api_logger.warning(f"Rate limit exceeded for {func.__name__}: retry after {retry_after}s")
                raise RateLimitExceeded(retry_after, limit_type)
            
            # Execute the original function
            return func(*args, **kwargs)
            
        except RateLimitExceeded:
            # Re-raise rate limit errors
            raise
        except Exception as e:
            # Record failed attempts for auth endpoints
            if limit_type == "auth":
                rate_limiter.record_failed_attempt(request_info, limit_type)
            raise
    
    return wrapper


def request_logging_middleware(func: Callable) -> Callable:
    """
    Middleware to log HTTP requests and responses.
    
    Args:
        func: The function to wrap
        
    Returns:
        Wrapped function with logging
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Extract request information (simplified for NiceGUI)
        method = "GET"  # NiceGUI doesn't expose HTTP method directly
        endpoint = func.__name__
        
        try:
            api_logger.info(f"Request started: {method} {endpoint}")
            result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            status_code = 200  # Assume success for NiceGUI
            
            api_logger.info(f"Request completed: {method} {endpoint} - {status_code} - {duration:.3f}s")
            record_request_metrics(method, endpoint, status_code, duration)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            status_code = 500
            
            api_logger.error(f"Request failed: {method} {endpoint} - {status_code} - {duration:.3f}s - {str(e)}")
            record_request_metrics(method, endpoint, status_code, duration)
            
            raise
    
    return wrapper


def security_headers_middleware(func: Callable) -> Callable:
    """
    Middleware to add security headers.
    
    Args:
        func: The function to wrap
        
    Returns:
        Wrapped function with security headers
    """
    def wrapper(*args, **kwargs):
        # Note: NiceGUI doesn't provide direct access to response headers
        # In a real application, you would add security headers here
        # For now, we'll just log the security middleware execution
        
        api_logger.debug("Security headers middleware executed")
        return func(*args, **kwargs)
    
    return wrapper


def error_handling_middleware(func: Callable) -> Callable:
    """
    Middleware to handle errors gracefully.
    
    Args:
        func: The function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            api_logger.error(f"Unhandled error in {func.__name__}: {str(e)}")
            # In a real application, you would return a proper error response
            # For NiceGUI, we'll let the error propagate to be handled by the UI
            raise
    
    return wrapper


def apply_middleware(func: Callable, limit_type: str = "general") -> Callable:
    """
    Apply all middleware to a function.
    
    Args:
        func: The function to wrap
        limit_type: Type of rate limit to apply
        
    Returns:
        Function with all middleware applied
    """
    return request_logging_middleware(
        rate_limiting_middleware(
            security_headers_middleware(
                error_handling_middleware(func)
            ), limit_type
        )
    )


def apply_auth_middleware(func: Callable) -> Callable:
    """
    Apply middleware with authentication rate limiting.
    
    Args:
        func: The function to wrap
        
    Returns:
        Function with auth-specific middleware applied
    """
    return apply_middleware(func, "auth")
