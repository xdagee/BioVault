from nicegui import ui  # type: ignore
from typing import Callable, Tuple, Any, Dict, Optional
from pathlib import Path
from image_handler import validate_image_file, process_and_save_image
from logging_config import app_logger


def registration_form(on_submit: Callable[[], None]) -> Tuple[Any, Any, Any, Any, Any, Any, Any]:
    """
    Create a registration form with Material Design responsive styling, proper input validation, and image upload.
    
    Args:
        on_submit: Callback function to execute when form is submitted
        
    Returns:
        Tuple containing form container and input elements for external access
    """
    # Create form container with Material Design responsive spacing
    with ui.column().classes('w-full space-y-4 md:space-y-6 px-4 sm:px-6 md:px-8 pb-6 md:pb-8') as form:
        # Material Design input styling with proper contrast and touch targets
        input_style = '''
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            color: #1a1a1a !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            line-height: 1.5 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            min-height: 48px !important;
        '''
        
        focus_style = '''
            border-color: #a855f7 !important;
            box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
            outline: none !important;
            background: rgba(255, 255, 255, 0.98) !important;
        '''
        
        name_input = ui.input('Full Name').classes('w-full').props('type=text')
        name_input.style(input_style)
        name_input.on('focus', lambda: name_input.style(focus_style))
        name_input.on('blur', lambda: name_input.style(input_style))
        
        email_input = ui.input('Email Address').classes('w-full').props('type=email')
        email_input.style(input_style)
        email_input.on('focus', lambda: email_input.style(focus_style))
        email_input.on('blur', lambda: email_input.style(input_style))
        
        phone_input = ui.input('Phone Number').classes('w-full').props('type=tel')
        phone_input.style(input_style)
        phone_input.on('focus', lambda: phone_input.style(focus_style))
        phone_input.on('blur', lambda: phone_input.style(input_style))
        
        age_input = ui.input('Age').classes('w-full').props('type=number')
        age_input.style(input_style)
        age_input.on('focus', lambda: age_input.style(focus_style))
        age_input.on('blur', lambda: age_input.style(input_style))
        
        password_input = ui.input('Password').classes('w-full').props('type=password')
        password_input.style(input_style)
        password_input.on('focus', lambda: password_input.style(focus_style))
        password_input.on('blur', lambda: password_input.style(input_style))
        
        # Image upload section with Material Design typography
        ui.html('<div class="text-base sm:text-lg md:text-xl font-semibold text-purple-300 mb-3 md:mb-4">Profile Image (Optional)</div>')
        
        # Image preview container with responsive spacing
        image_preview_container = ui.column().classes('w-full mb-4 md:mb-6')
        
        # Store uploaded image data with proper typing
        uploaded_image_data: Dict[str, Optional[str]] = {'path': None, 'filename': None}
        
        def handle_image_upload(e):
            """Handle image upload."""
            try:
                app_logger.info(f"Image upload started: {e.name}")
                
                # Validate image
                is_valid, error_msg = validate_image_file(e.content.read(), e.name)
                if not is_valid:
                    ui.notify(f"Image validation failed: {error_msg}", color="red")
                    return
                
                # Reset file pointer
                e.content.seek(0)
                
                # Process and save image
                image_path = process_and_save_image(e.content.read(), e.name)
                if image_path:
                    uploaded_image_data['path'] = image_path
                    uploaded_image_data['filename'] = e.name
                    
                    # Show preview
                    show_image_preview(image_path, e.name)
                    ui.notify("Image uploaded successfully!", color="green")
                    app_logger.info(f"Image uploaded successfully: {image_path}")
                else:
                    ui.notify("Failed to save image. Please try again.", color="red")
                    
            except Exception as ex:
                app_logger.error(f"Error handling image upload: {str(ex)}")
                ui.notify("Error uploading image. Please try again.", color="red")
        
        def show_image_preview(image_path: str, filename: str):
            """Show image preview with Material Design responsive layout."""
            image_preview_container.clear()
            with image_preview_container:
                ui.html(f'''
                    <div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20">
                        <div class="flex items-center space-x-3 md:space-x-4">
                            <img src="/uploads/{Path(image_path).name}" 
                                 alt="Preview" 
                                 class="w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20 rounded-lg object-cover border border-purple-400/30">
                            <div>
                                <p class="text-purple-300 font-semibold text-sm sm:text-base md:text-lg">Image uploaded</p>
                                <p class="text-gray-400 text-xs sm:text-sm md:text-base">{filename}</p>
                            </div>
                        </div>
                    </div>
                ''')
        
        # Image upload component with Material Design styling and proper touch targets
        image_upload = ui.upload(
            on_upload=handle_image_upload,
            auto_upload=False,
            max_file_size=5 * 1024 * 1024,  # 5MB
            multiple=False
        ).classes('w-full').props('accept=image/*')
        
        # Style the upload component with Material Design principles
        image_upload.style('''
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px dashed rgba(168, 85, 247, 0.4) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            color: #1a1a1a !important;
            font-size: 16px !important;
            min-height: 64px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        ''')

        # Submit Button with Material Design touch targets and responsive sizing
        ui.button('Create Identity', on_click=on_submit).classes('''
            w-full py-3 sm:py-4 bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-500 hover:to-pink-600 
            text-white font-bold text-base sm:text-lg md:text-xl rounded-xl shadow-lg hover:shadow-pink-500/25 
            transition-all duration-300 transform hover:scale-105 border border-pink-400/30
            min-h-[48px] flex items-center justify-center
        ''')
    
    # Return the form container and inputs for external access
    return form, name_input, email_input, phone_input, age_input, password_input, uploaded_image_data

