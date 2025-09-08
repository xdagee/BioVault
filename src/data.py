"""
Data access layer for the application.
Provides database operations and maintains backward compatibility.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database import get_db, User, get_user_by_email, create_user as db_create_user
from utils import hash_password
from logging_config import db_logger
from exceptions import DatabaseError, UserAlreadyExistsError, UserNotFoundError
from input_sanitizer import sanitize_form_data

# Backward compatibility - in-memory list for existing code
# This will be replaced with database operations
registrants: List[Dict[str, Any]] = []


def get_all_users() -> List[Dict[str, Any]]:
    """Get all users from database."""
    db = next(get_db())
    try:
        db_logger.info("Getting all users")
        users = db.query(User).filter(User.is_active == True).all()
        result = [
            {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'age': user.age,
                'image_path': user.image_path,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ]
        db_logger.info(f"Retrieved {len(result)} users")
        return result
    except Exception as e:
        db_logger.error(f"Error getting all users: {str(e)}")
        raise DatabaseError(f"Failed to get users: {str(e)}", "get_all_users")
    finally:
        db.close()


def add_user(name: str, email: str, phone: str, age: int, password: str, image_path: str = None) -> Optional[Dict[str, Any]]:
    """Add a new user to the database."""
    try:
        # Sanitize input data
        sanitized_data = sanitize_form_data({
            'name': name,
            'email': email,
            'phone': phone,
            'age': str(age),
            'password': password
        })
        
        db = next(get_db())
        try:
            # Check if user already exists
            existing_user = get_user_by_email(db, sanitized_data['email'])
            if existing_user:
                db_logger.warning(f"User already exists: {sanitized_data['email']}")
                return None
            
            # Hash password
            password_hash = hash_password(sanitized_data['password'])
            
            # Create user
            user = db_create_user(
                db, 
                sanitized_data['name'], 
                sanitized_data['email'], 
                sanitized_data['phone'], 
                sanitized_data['age'], 
                password_hash,
                image_path
            )
            
            # Also add to in-memory list for backward compatibility
            registrants.append({
                'name': sanitized_data['name'],
                'email': sanitized_data['email'],
                'phone': sanitized_data['phone'],
                'age': sanitized_data['age'],
                'password': password_hash
            })
            
            result = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'age': user.age,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            
            db_logger.info(f"User created successfully: {user.email}")
            return result
            
        finally:
            db.close()
            
    except Exception as e:
        db_logger.error(f"Error adding user: {str(e)}")
        raise


def get_user_by_email_for_auth(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email for authentication."""
    db = next(get_db())
    try:
        user = get_user_by_email(db, email)
        if user:
            return {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'age': user.age,
                'password': user.password_hash,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        return None
    finally:
        db.close()


def update_user(user_id: int, name: str, email: str, phone: str, age: int) -> Optional[Dict[str, Any]]:
    """Update an existing user in the database."""
    db = next(get_db())
    try:
        db_logger.info(f"Updating user with ID: {user_id}")
        
        # Get the user
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            db_logger.warning(f"User not found for update: {user_id}")
            return None
        
        # Sanitize input data
        sanitized_data = sanitize_form_data({
            'name': name,
            'email': email,
            'phone': phone,
            'age': str(age)
        })
        
        # Update user fields
        user.name = sanitized_data['name']
        user.email = sanitized_data['email']
        user.phone = sanitized_data['phone']
        user.age = sanitized_data['age']
        
        # Commit changes
        db.commit()
        
        result = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'age': user.age,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        db_logger.info(f"User updated successfully: {user.email}")
        return result
        
    except Exception as e:
        db_logger.error(f"Error updating user: {str(e)}")
        db.rollback()
        raise DatabaseError(f"Failed to update user: {str(e)}", "update_user")
    finally:
        db.close()


def delete_user(user_id: int) -> bool:
    """Delete a user from the database (soft delete by setting is_active to False)."""
    db = next(get_db())
    try:
        db_logger.info(f"Deleting user with ID: {user_id}")
        
        # Get the user
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            db_logger.warning(f"User not found for deletion: {user_id}")
            return False
        
        # Soft delete by setting is_active to False
        user.is_active = False
        
        # Commit changes
        db.commit()
        
        db_logger.info(f"User deleted successfully: {user.email}")
        return True
        
    except Exception as e:
        db_logger.error(f"Error deleting user: {str(e)}")
        db.rollback()
        raise DatabaseError(f"Failed to delete user: {str(e)}", "delete_user")
    finally:
        db.close()


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if user:
            return {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'age': user.age,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        return None
    finally:
        db.close()