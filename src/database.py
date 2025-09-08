"""
Database configuration and session management.
Handles database connection, models, and session management.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as OrmSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from typing import Optional
from logging_config import db_logger
from exceptions import DatabaseError, UserAlreadyExistsError

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bio_app.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class User(Base):
    """User model for storing registrant information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    password_hash = Column(String(255), nullable=False)
    image_path = Column(String(500), nullable=True)  # Path to uploaded image
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Session(Base):
    """Session model for storing user sessions."""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


def get_db() -> OrmSession:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_user_by_email(db: OrmSession, email: str) -> Optional[User]:
    """Get user by email."""
    try:
        db_logger.debug(f"Getting user by email: {email}")
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        if user:
            db_logger.info(f"User found: {user.email}")
        else:
            db_logger.info(f"User not found: {email}")
        return user
    except SQLAlchemyError as e:
        db_logger.error(f"Database error getting user by email {email}: {str(e)}")
        raise DatabaseError(f"Failed to get user by email: {str(e)}", "get_user_by_email")


def create_user(db: OrmSession, name: str, email: str, phone: str, age: int, password_hash: str, image_path: str = None) -> User:
    """Create a new user."""
    try:
        db_logger.info(f"Creating user: {email}")
        user = User(
            name=name,
            email=email,
            phone=phone,
            age=age,
            password_hash=password_hash,
            image_path=image_path
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db_logger.info(f"User created successfully: {user.id}")
        return user
    except IntegrityError as e:
        db_logger.error(f"Integrity error creating user {email}: {str(e)}")
        db.rollback()
        raise UserAlreadyExistsError(email)
    except SQLAlchemyError as e:
        db_logger.error(f"Database error creating user {email}: {str(e)}")
        db.rollback()
        raise DatabaseError(f"Failed to create user: {str(e)}", "create_user")


def get_session_by_id(db: OrmSession, session_id: str) -> Optional[Session]:
    """Get session by session ID."""
    return db.query(Session).filter(
        Session.session_id == session_id,
        Session.is_active == True
    ).first()


def create_session_record(db: OrmSession, session_id: str, user_id: int) -> Session:
    """Create a new session record."""
    session = Session(
        session_id=session_id,
        user_id=user_id
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def destroy_session_record(db: OrmSession, session_id: str) -> bool:
    """Destroy a session record."""
    session = get_session_by_id(db, session_id)
    if session:
        session.is_active = False
        db.commit()
        return True
    return False


def cleanup_expired_sessions(db: OrmSession, max_age_minutes: int = 30):
    """Clean up expired sessions."""
    from datetime import timedelta
    cutoff_time = datetime.utcnow() - timedelta(minutes=max_age_minutes)
    
    expired_sessions = db.query(Session).filter(
        Session.last_activity < cutoff_time,
        Session.is_active == True
    ).all()
    
    for session in expired_sessions:
        session.is_active = False
    
    db.commit()
    return len(expired_sessions)
