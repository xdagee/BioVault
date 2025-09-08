"""
Input sanitization utilities.
Provides functions to clean and validate user input.
"""

import re
import bleach
from typing import Optional, List
from exceptions import ValidationError


def sanitize_string(value: str, max_length: Optional[int] = None, allow_html: bool = False) -> str:
    """Sanitize a string input."""
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")
    
    # Strip whitespace
    cleaned = value.strip()
    
    # Check length
    if max_length and len(cleaned) > max_length:
        raise ValidationError(f"String too long. Maximum length is {max_length} characters")
    
    # Remove HTML tags if not allowed
    if not allow_html:
        cleaned = bleach.clean(cleaned, tags=[], strip=True)
    
    return cleaned


def sanitize_email(email: str) -> str:
    """Sanitize and validate email address."""
    if not email:
        raise ValidationError("Email is required")
    
    # Basic sanitization
    cleaned_email = sanitize_string(email, max_length=255)
    
    # Email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, cleaned_email):
        raise ValidationError("Invalid email format")
    
    return cleaned_email.lower()


def sanitize_phone(phone: str) -> str:
    """Sanitize and validate phone number."""
    if not phone:
        raise ValidationError("Phone number is required")
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid 10-digit US phone number
    if len(digits_only) != 10:
        raise ValidationError("Phone number must be exactly 10 digits")
    
    if not digits_only.isdigit():
        raise ValidationError("Phone number must contain only digits")
    
    return digits_only


def sanitize_age(age: str) -> int:
    """Sanitize and validate age."""
    if not age:
        raise ValidationError("Age is required")
    
    # Remove whitespace
    cleaned_age = age.strip()
    
    # Check if it's a valid integer
    try:
        age_int = int(cleaned_age)
    except ValueError:
        raise ValidationError("Age must be a valid number")
    
    # Check age range
    if age_int < 18:
        raise ValidationError("Age must be 18 or older")
    if age_int > 120:
        raise ValidationError("Age must be a reasonable number")
    
    return age_int


def sanitize_password(password: str) -> str:
    """Sanitize and validate password."""
    if not password:
        raise ValidationError("Password is required")
    
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    
    # Check for required character types
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        raise ValidationError("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one number")
    
    # Check for common weak passwords
    weak_passwords = ['password', '12345678', 'qwerty123', 'admin123']
    if password.lower() in weak_passwords:
        raise ValidationError("Password is too common. Please choose a stronger password")
    
    return password


def sanitize_name(name: str) -> str:
    """Sanitize and validate name."""
    if not name:
        raise ValidationError("Name is required")
    
    # Basic sanitization
    cleaned_name = sanitize_string(name, max_length=100)
    
    # Check minimum length
    if len(cleaned_name) < 2:
        raise ValidationError("Name must be at least 2 characters long")
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-']+$", cleaned_name):
        raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes")
    
    return cleaned_name


def sanitize_form_data(data: dict) -> dict:
    """Sanitize all form data at once."""
    sanitized = {}
    errors = []
    
    try:
        if 'name' in data:
            sanitized['name'] = sanitize_name(data['name'])
    except ValidationError as e:
        errors.append(f"Name: {e.message}")
    
    try:
        if 'email' in data:
            sanitized['email'] = sanitize_email(data['email'])
    except ValidationError as e:
        errors.append(f"Email: {e.message}")
    
    try:
        if 'phone' in data:
            sanitized['phone'] = sanitize_phone(data['phone'])
    except ValidationError as e:
        errors.append(f"Phone: {e.message}")
    
    try:
        if 'age' in data:
            sanitized['age'] = sanitize_age(data['age'])
    except ValidationError as e:
        errors.append(f"Age: {e.message}")
    
    try:
        if 'password' in data:
            sanitized['password'] = sanitize_password(data['password'])
    except ValidationError as e:
        errors.append(f"Password: {e.message}")
    
    if errors:
        raise ValidationError("Validation failed", details={'errors': errors})
    
    return sanitized
