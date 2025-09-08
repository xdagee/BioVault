"""
Configuration management for the application.
Handles environment variables and application settings.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
import secrets

# No .env loading; the app runs with built-in defaults and system env vars only


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 300


@dataclass
class RateLimitConfig:
    """Rate limiting configuration settings."""
    enabled: bool = True
    requests_per_minute: int = 60
    auth_requests_per_minute: int = 10
    burst_size: int = 10


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    session_timeout_minutes: int = 30
    csrf_secret_key: str = None
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str
    log_file: Optional[str] = None
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class AppConfig:
    """Main application configuration."""
    debug: bool
    host: str
    port: int
    database: DatabaseConfig
    security: SecurityConfig
    logging: LoggingConfig
    rate_limit: RateLimitConfig


def get_rate_limit_config() -> RateLimitConfig:
    """Get rate limiting configuration from environment variables."""
    return RateLimitConfig(
        enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
        requests_per_minute=int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60")),
        auth_requests_per_minute=int(os.getenv("RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE", "10")),
        burst_size=int(os.getenv("RATE_LIMIT_BURST_SIZE", "10"))
    )


def get_database_config() -> DatabaseConfig:
    """Get database configuration from environment variables."""
    return DatabaseConfig(
        url=os.getenv("DATABASE_URL", "sqlite:///./bio_app.db"),
        echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
        pool_pre_ping=os.getenv("DATABASE_POOL_PRE_PING", "true").lower() == "true",
        pool_recycle=int(os.getenv("DATABASE_POOL_RECYCLE", "300"))
    )


def get_security_config() -> SecurityConfig:
    """Get security configuration from environment variables.

    If SECRET_KEY is not provided, generate a secure random key at runtime
    so the application can run without a .env file.
    """
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        # Generate a strong random secret key for the current process
        secret_key = secrets.token_urlsafe(48)
        # Minimal notice without introducing logging dependencies here
        print("[config] SECRET_KEY not set; generated a temporary key for this run.")
    
    csrf_secret_key = os.getenv("CSRF_SECRET_KEY")
    if not csrf_secret_key:
        csrf_secret_key = secrets.token_urlsafe(32)
        print("[config] CSRF_SECRET_KEY not set; generated a temporary key for this run.")
    
    return SecurityConfig(
        secret_key=secret_key,
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        session_timeout_minutes=int(os.getenv("SESSION_TIMEOUT_MINUTES", "30")),
        csrf_secret_key=csrf_secret_key,
        max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
        lockout_duration_minutes=int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))
    )


def get_logging_config() -> LoggingConfig:
    """Get logging configuration from environment variables."""
    return LoggingConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "logs/app.log"),
        max_bytes=int(os.getenv("LOG_MAX_BYTES", str(10 * 1024 * 1024))),
        backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
    )


def get_app_config() -> AppConfig:
    """Get complete application configuration."""
    return AppConfig(
        debug=os.getenv("DEBUG", "false").lower() == "true",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", "8080")),
        database=get_database_config(),
        security=get_security_config(),
        logging=get_logging_config(),
        rate_limit=get_rate_limit_config()
    )


# Global configuration instance
config = get_app_config()
