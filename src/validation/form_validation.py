def validate_form(name: str, email: str, phone: str, age: str, password: str = None) -> list[str]:
    """Validate form inputs and return list of errors."""
    errors = []
    
    # Name validation
    if not name or not name.strip():
        errors.append("Name is required.")
    elif len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long.")
    
    # Email validation
    if not email or not email.strip():
        errors.append("Email is required.")
    elif "@" not in email or "." not in email:
        errors.append("A valid email is required.")
    
    # Phone validation
    if not phone or not phone.strip():
        errors.append("Phone number is required.")
    elif len(phone.replace("-", "").replace(" ", "")) != 10 or not phone.replace("-", "").replace(" ", "").isdigit():
        errors.append("Phone number must be 10 digits.")
    
    # Age validation
    if not age or not age.strip():
        errors.append("Age is required.")
    elif not age.isdigit():
        errors.append("Age must be a valid number.")
    elif int(age) < 18:
        errors.append("Age must be 18 or older.")
    elif int(age) > 120:
        errors.append("Age must be a reasonable number.")
    
    # Password validation (if provided)
    if password is not None:
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        elif not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        elif not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        elif not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number.")
    
    return errors
