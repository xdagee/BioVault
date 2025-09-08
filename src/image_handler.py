"""
Image upload and handling utilities.
Provides secure image upload, validation, and storage functionality.
"""

import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import io
from logging_config import app_logger


# Configuration
UPLOAD_DIR = Path("uploads/images")
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DIMENSIONS = (800, 800)  # Max width and height


def ensure_upload_directory():
    """Ensure the upload directory exists."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    app_logger.info(f"Upload directory ensured: {UPLOAD_DIR}")


def validate_image_file(file_content: bytes, filename: str) -> Tuple[bool, str]:
    """
    Validate uploaded image file.
    
    Args:
        file_content: The file content as bytes
        filename: The original filename
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            return False, f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit"
        
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        
        # Validate image with PIL
        try:
            image = Image.open(io.BytesIO(file_content))
            image.verify()  # Verify it's a valid image
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
        
        # Check dimensions
        image = Image.open(io.BytesIO(file_content))  # Reopen after verify
        width, height = image.size
        if width > MAX_DIMENSIONS[0] or height > MAX_DIMENSIONS[1]:
            return False, f"Image dimensions {width}x{height} exceed maximum {MAX_DIMENSIONS[0]}x{MAX_DIMENSIONS[1]}"
        
        return True, ""
        
    except Exception as e:
        app_logger.error(f"Error validating image file: {str(e)}")
        return False, f"Error validating image: {str(e)}"


def process_and_save_image(file_content: bytes, filename: str) -> Optional[str]:
    """
    Process and save uploaded image.
    
    Args:
        file_content: The file content as bytes
        filename: The original filename
        
    Returns:
        The saved file path or None if failed
    """
    try:
        ensure_upload_directory()
        
        # Generate unique filename
        file_ext = Path(filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Process image (resize if needed)
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize if too large
        if image.size[0] > MAX_DIMENSIONS[0] or image.size[1] > MAX_DIMENSIONS[1]:
            image.thumbnail(MAX_DIMENSIONS, Image.Resampling.LANCZOS)
        
        # Save image
        image.save(file_path, 'JPEG', quality=85, optimize=True)
        
        app_logger.info(f"Image saved successfully: {file_path}")
        return str(file_path)
        
    except Exception as e:
        app_logger.error(f"Error processing and saving image: {str(e)}")
        return None


def delete_image(image_path: str) -> bool:
    """
    Delete an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            app_logger.info(f"Image deleted successfully: {image_path}")
            return True
        return False
    except Exception as e:
        app_logger.error(f"Error deleting image {image_path}: {str(e)}")
        return False


def get_image_url(image_path: str) -> str:
    """
    Get the URL for serving an image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        URL for serving the image
    """
    if not image_path:
        return "/static/default-avatar.png"  # Default avatar
    
    # Convert file path to URL path
    return f"/uploads/{Path(image_path).name}"
