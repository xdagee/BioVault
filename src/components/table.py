from nicegui import ui  # type: ignore
from typing import List, Dict, Any, Callable, Optional
from pathlib import Path
from data import update_user, delete_user
from logging_config import app_logger


def registrants_table(registrants: List[Dict[str, Any]], refresh_callback: Optional[Callable[[], None]] = None) -> None:
    """
    Display registrants in a Material Design responsive card layout with CRUD operations.
    
    Args:
        registrants: List of registrant dictionaries to display
        refresh_callback: Function to call when data needs to be refreshed
    """
    if not registrants:
        ui.html('''
            <div class="text-center py-8 md:py-12 lg:py-16">
                <div class="text-5xl md:text-6xl lg:text-7xl mb-4 md:mb-6">🔍</div>
                <h3 class="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-purple-300 mb-2 md:mb-4">No Identities Found</h3>
                <p class="text-sm sm:text-base md:text-lg text-gray-400 max-w-md mx-auto leading-relaxed">The vault is empty. Create the first digital identity to begin.</p>
            </div>
        ''')
        return
    
    # Create a responsive grid layout with Material Design cards
    with ui.column().classes('w-full space-y-4 md:space-y-6'):
        # Table header with responsive typography
        ui.html('<div class="text-base sm:text-lg md:text-xl lg:text-2xl font-semibold text-purple-300 mb-4 md:mb-6">Digital Identity Registry</div>')
        
        # Create responsive grid for larger screens, stacked cards for mobile
        with ui.column().classes('w-full space-y-4 md:space-y-6'):
            for registrant in registrants:
                with ui.card().classes('w-full bg-black/20 backdrop-blur-sm border border-purple-500/20 p-4 sm:p-6 md:p-8 rounded-xl md:rounded-2xl hover:bg-black/30 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20'):
                    with ui.row().classes('w-full items-start sm:items-center justify-between flex-col sm:flex-row gap-4 sm:gap-6'):
                        # User information with responsive layout
                        with ui.column().classes('flex-1 w-full sm:w-auto'):
                            # Get image path
                            image_path = registrant.get('image_path')
                            image_html = ""
                            if image_path:
                                image_html = f'''
                                    <img src="/uploads/{Path(image_path).name}" 
                                         alt="Profile" 
                                         class="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-full object-cover border border-purple-400/30 mr-3">
                                '''
                            
                            ui.html(f'''
                                <div class="space-y-2 md:space-y-3">
                                    <div class="flex items-center space-x-3 md:space-x-4">
                                        {image_html}
                                        <div>
                                            <span class="text-purple-300 font-semibold text-base sm:text-lg md:text-xl">{registrant.get('name', 'Unknown')}</span>
                                            <span class="text-gray-400 text-xs sm:text-sm md:text-base ml-2">ID: {registrant.get('id', 'N/A')}</span>
                                        </div>
                                    </div>
                                    <div class="text-gray-300 space-y-1 md:space-y-2 text-sm sm:text-base">
                                        <div class="flex items-center space-x-2">
                                            <span class="text-purple-400 text-base md:text-lg">📧</span>
                                            <span class="break-all">{registrant.get('email', 'No email')}</span>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-purple-400 text-base md:text-lg">📱</span>
                                            <span>{registrant.get('phone', 'No phone')}</span>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-purple-400 text-base md:text-lg">🔢</span>
                                            <span>Access Level: {registrant.get('age', 'Unknown')}</span>
                                        </div>
                                    </div>
                                </div>
                            ''')
                    
                        # Action buttons with Material Design touch targets and responsive layout
                        with ui.row().classes('space-x-2 sm:space-x-3 md:space-x-4 flex-shrink-0 w-full sm:w-auto justify-center sm:justify-end'):
                            # Edit button with Material Design styling
                            ui.button('Edit', on_click=lambda r=registrant: edit_user_dialog(r, refresh_callback)).classes('''
                                px-3 sm:px-4 md:px-6 py-2 sm:py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 
                                text-white font-semibold text-xs sm:text-sm md:text-base rounded-lg md:rounded-xl shadow-lg hover:shadow-blue-500/25 
                                transition-all duration-300 transform hover:scale-105 border border-blue-400/30
                                min-h-[40px] sm:min-h-[44px] md:min-h-[48px] flex items-center justify-center flex-1 sm:flex-none
                            ''')
                            
                            # Delete button with Material Design styling
                            ui.button('Delete', on_click=lambda r=registrant: delete_user_dialog(r, refresh_callback)).classes('''
                                px-3 sm:px-4 md:px-6 py-2 sm:py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 
                                text-white font-semibold text-xs sm:text-sm md:text-base rounded-lg md:rounded-xl shadow-lg hover:shadow-red-500/25 
                                transition-all duration-300 transform hover:scale-105 border border-red-400/30
                                min-h-[40px] sm:min-h-[44px] md:min-h-[48px] flex items-center justify-center flex-1 sm:flex-none
                            ''')


def edit_user_dialog(user: Dict[str, Any], refresh_callback: Optional[Callable[[], None]] = None):
    """Open Material Design responsive edit dialog for a user."""
    app_logger.info(f"Opening edit dialog for user: {user.get('email', 'Unknown')}")
    
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-sm sm:max-w-md md:max-w-lg bg-black/30 backdrop-blur-sm border border-purple-500/20 rounded-xl md:rounded-2xl m-4'):
        ui.html('<h3 class="text-xl sm:text-2xl md:text-3xl font-bold text-purple-300 mb-6 md:mb-8 text-center px-4 sm:px-6 md:px-8 pt-6 md:pt-8">Edit Digital Identity</h3>')
        
        # Form container with responsive padding
        with ui.column().classes('px-4 sm:px-6 md:px-8 pb-6 md:pb-8 space-y-4 md:space-y-6'):
            # Form inputs with current values and Material Design styling
            input_style = '''
                background: rgba(255, 255, 255, 0.95) !important;
                border: 2px solid rgba(168, 85, 247, 0.4) !important;
                border-radius: 12px !important;
                padding: 14px 18px !important;
                color: #1a1a1a !important;
                font-size: 16px !important;
                min-height: 48px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            '''
            
            name_input = ui.input('Full Name', value=user.get('name', '')).classes('w-full')
            name_input.style(input_style)
            
            email_input = ui.input('Email Address', value=user.get('email', '')).classes('w-full')
            email_input.style(input_style)
            
            phone_input = ui.input('Phone Number', value=user.get('phone', '')).classes('w-full')
            phone_input.style(input_style)
            
            age_input = ui.input('Age', value=str(user.get('age', ''))).classes('w-full')
            age_input.style(input_style)
        
        # Action buttons
        with ui.row().classes('w-full justify-end space-x-3'):
            ui.button('Cancel', on_click=dialog.close).classes('''
                px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-500 hover:to-gray-600 
                text-white font-semibold rounded-lg shadow-lg hover:shadow-gray-500/25 
                transition-all duration-300 transform hover:scale-105 border border-gray-400/30
            ''')
            
            def save_changes():
                try:
                    # Update user data
                    updated_user = update_user(
                        user['id'],
                        name_input.value,
                        email_input.value,
                        phone_input.value,
                        int(age_input.value) if age_input.value else 0
                    )
                    
                    if updated_user:
                        app_logger.info(f"User updated successfully: {email_input.value}")
                        ui.notify("Identity updated successfully!", color="green")
                        dialog.close()
                        if refresh_callback:
                            refresh_callback()
                    else:
                        ui.notify("Failed to update identity. Please try again.", color="red")
                        
                except Exception as e:
                    app_logger.error(f"Error updating user: {str(e)}")
                    ui.notify("An error occurred while updating the identity.", color="red")
            
            ui.button('Save Changes', on_click=save_changes).classes('''
                px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 
                text-white font-semibold rounded-lg shadow-lg hover:shadow-green-500/25 
                transition-all duration-300 transform hover:scale-105 border border-green-400/30
            ''')
    
    dialog.open()


def delete_user_dialog(user: Dict[str, Any], refresh_callback: Optional[Callable[[], None]] = None):
    """Open Material Design responsive delete confirmation dialog for a user."""
    app_logger.info(f"Opening delete dialog for user: {user.get('email', 'Unknown')}")
    
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-sm sm:max-w-md md:max-w-lg bg-black/30 backdrop-blur-sm border border-red-500/20 rounded-xl md:rounded-2xl m-4'):
        ui.html('<h3 class="text-xl sm:text-2xl md:text-3xl font-bold text-red-300 mb-6 md:mb-8 text-center px-4 sm:px-6 md:px-8 pt-6 md:pt-8">⚠️ Delete Digital Identity</h3>')
        
        # Content with responsive padding and typography
        with ui.column().classes('px-4 sm:px-6 md:px-8 pb-6 md:pb-8'):
            ui.html(f'''
                <div class="text-gray-300 mb-6 md:mb-8">
                    <p class="mb-4 md:mb-6 text-sm sm:text-base md:text-lg leading-relaxed">Are you sure you want to permanently delete this digital identity?</p>
                    <div class="bg-black/20 rounded-lg p-3 md:p-4 border border-red-500/20">
                        <p class="text-sm sm:text-base md:text-lg mb-2"><strong>Name:</strong> {user.get('name', 'Unknown')}</p>
                        <p class="text-sm sm:text-base md:text-lg mb-2"><strong>Email:</strong> {user.get('email', 'Unknown')}</p>
                        <p class="text-sm sm:text-base md:text-lg"><strong>Phone:</strong> {user.get('phone', 'Unknown')}</p>
                    </div>
                    <p class="mt-4 md:mt-6 text-red-400 font-semibold text-sm sm:text-base md:text-lg">This action cannot be undone!</p>
                </div>
            ''')
        
        # Action buttons
        with ui.row().classes('w-full justify-end space-x-3'):
            ui.button('Cancel', on_click=dialog.close).classes('''
                px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-500 hover:to-gray-600 
                text-white font-semibold rounded-lg shadow-lg hover:shadow-gray-500/25 
                transition-all duration-300 transform hover:scale-105 border border-gray-400/30
            ''')
            
            def confirm_delete():
                try:
                    # Delete user
                    success = delete_user(user['id'])
                    
                    if success:
                        app_logger.info(f"User deleted successfully: {user.get('email', 'Unknown')}")
                        ui.notify("Digital identity deleted successfully!", color="green")
                        dialog.close()
                        if refresh_callback:
                            refresh_callback()
                    else:
                        ui.notify("Failed to delete identity. Please try again.", color="red")
                        
                except Exception as e:
                    app_logger.error(f"Error deleting user: {str(e)}")
                    ui.notify("An error occurred while deleting the identity.", color="red")
            
            ui.button('Delete Forever', on_click=confirm_delete).classes('''
                px-6 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 
                text-white font-semibold rounded-lg shadow-lg hover:shadow-red-500/25 
                transition-all duration-300 transform hover:scale-105 border border-red-400/30
            ''')
    
    dialog.open()
