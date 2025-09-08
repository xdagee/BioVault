from nicegui import ui  # type: ignore
from pathlib import Path
from components.form import registration_form
from validation.form_validation import validate_form
from data import add_user
from logging_config import app_logger
from exceptions import ValidationError, UserAlreadyExistsError, DatabaseError

def register_page():
    """Registration page with form and verification step using Material Design responsive layout."""
    app_logger.info("Registration page accessed")
    
    # Main container with gradient background, Material Design spacing, and proper centering
    with ui.column().classes('w-full min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center'):
        
        # Header section with Material Design typography, responsive spacing, and center alignment
        with ui.column().classes('w-full flex items-center justify-center text-center py-12 sm:py-16 md:py-20 lg:py-24 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="mb-8 md:mb-12">
                    <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 md:mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight tracking-tight">
                        Create Identity
                    </h1>
                    <p class="text-base sm:text-lg md:text-xl text-gray-300 mb-4 md:mb-6 font-light leading-relaxed">Join the digital underground</p>
                    <div class="w-16 sm:w-20 md:w-24 h-1 bg-gradient-to-r from-purple-400 to-pink-400 mx-auto rounded-full"></div>
                </div>
            ''')
        
        # Container for the form with responsive width
        form_container = ui.column().classes('w-full max-w-sm sm:max-w-md md:max-w-lg mx-auto px-4 sm:px-6 md:px-8')
        
        # Verification container (initially hidden) with responsive width
        verification_container = ui.column().classes('w-full max-w-sm sm:max-w-md md:max-w-lg mx-auto px-4 sm:px-6 md:px-8').style('display: none')
    
    def on_submit():
        try:
            # Get input values from the form inputs
            name = name_input.value
            email = email_input.value
            phone = phone_input.value
            age = age_input.value
            password = password_input.value
            image_path = uploaded_image_data.get('path')

            app_logger.info(f"Registration attempt for email: {email}")

            # Validate form inputs
            errors = validate_form(name, email, phone, age, password)
            if errors:
                app_logger.warning(f"Validation errors for {email}: {errors}")
                ui.notify("\n".join(errors), color="red")
                return

            # Show verification step
            show_verification(name, email, phone, age, password, image_path)
                
        except ValidationError as e:
            app_logger.error(f"Validation error during registration: {str(e)}")
            ui.notify(f"Validation error: {e.message}", color="red")
        except Exception as e:
            app_logger.error(f"Unexpected error during registration: {str(e)}")
            ui.notify("An unexpected error occurred. Please try again.", color="red")

    def show_verification(name, email, phone, age, password, image_path):
        """Show verification step with user details."""
        # Hide form and show verification
        form_container.style('display: none')
        verification_container.style('display: block')
        
        # Clear verification container
        verification_container.clear()
        
        with verification_container:
            with ui.card().classes('w-full bg-black/30 backdrop-blur-sm border border-purple-500/20 shadow-2xl rounded-xl md:rounded-2xl'):
                ui.html('<h2 class="text-xl sm:text-2xl md:text-3xl font-bold text-center mb-6 md:mb-8 text-purple-300 px-4 sm:px-6 md:px-8 pt-6 md:pt-8">Identity Verification</h2>')
                ui.html('<p class="text-center text-gray-300 mb-6 md:mb-8 px-4 sm:px-6 md:px-8 text-sm sm:text-base">Please verify your digital identity details:</p>')
                
                # Display user details with Material Design spacing and responsive layout
                with ui.column().classes('space-y-3 md:space-y-4 mb-6 md:mb-8 px-4 sm:px-6 md:px-8'):
                    # Show image if uploaded with responsive sizing
                    if image_path:
                        ui.html(f'''
                            <div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20 text-center">
                                <img src="/uploads/{Path(image_path).name}" 
                                     alt="Profile Preview" 
                                     class="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-full object-cover border border-purple-400/30 mx-auto mb-2 md:mb-3">
                                <p class="text-purple-300 font-semibold text-sm sm:text-base">Profile Image</p>
                            </div>
                        ''')
                    
                    ui.html(f'<div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20"><span class="text-purple-300 font-semibold text-sm sm:text-base">Name:</span> <span class="text-white text-sm sm:text-base">{name}</span></div>')
                    ui.html(f'<div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20"><span class="text-purple-300 font-semibold text-sm sm:text-base">Email:</span> <span class="text-white text-sm sm:text-base">{email}</span></div>')
                    ui.html(f'<div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20"><span class="text-purple-300 font-semibold text-sm sm:text-base">Phone:</span> <span class="text-white text-sm sm:text-base">{phone}</span></div>')
                    ui.html(f'<div class="bg-black/20 rounded-lg p-3 md:p-4 border border-purple-500/20"><span class="text-purple-300 font-semibold text-sm sm:text-base">Age:</span> <span class="text-white text-sm sm:text-base">{age}</span></div>')
                
                # Action buttons with Material Design touch targets and responsive spacing
                with ui.row().classes('w-full justify-center gap-3 sm:gap-4 md:gap-6 px-4 sm:px-6 md:px-8 pb-6 md:pb-8 flex-wrap'):
                    ui.button('Confirm Identity', on_click=lambda: confirm_registration(name, email, phone, age, password, image_path)).classes('''
                        px-4 sm:px-6 md:px-8 py-3 sm:py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 
                        text-white font-bold text-sm sm:text-base md:text-lg rounded-xl shadow-lg hover:shadow-green-500/25 
                        transition-all duration-300 transform hover:scale-105 border border-green-400/30
                        min-h-[48px] flex items-center justify-center
                    ''')
                    ui.button('Edit Details', on_click=show_form).classes('''
                        px-4 sm:px-6 md:px-8 py-3 sm:py-4 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-500 hover:to-gray-600 
                        text-white font-bold text-sm sm:text-base md:text-lg rounded-xl shadow-lg hover:shadow-gray-500/25 
                        transition-all duration-300 transform hover:scale-105 border border-gray-400/30
                        min-h-[48px] flex items-center justify-center
                    ''')

    def confirm_registration(name, email, phone, age, password, image_path):
        """Confirm and complete registration."""
        try:
            # Add user to database
            user = add_user(name, email, phone, int(age), password, image_path)
            if user:
                app_logger.info(f"Registration successful for: {email}")
                ui.notify("Registration successful!", color="green")
                # Redirect to registrants page after successful registration
                ui.run_javascript("window.location.href = '/registrants'")
            else:
                app_logger.warning(f"Registration failed - user exists: {email}")
                ui.notify("User with this email already exists!", color="red")
                show_form()  # Show form again for editing
                
        except UserAlreadyExistsError as e:
            app_logger.warning(f"User already exists: {e.email}")
            ui.notify(f"User with email {e.email} already exists!", color="red")
            show_form()  # Show form again for editing
        except DatabaseError as e:
            app_logger.error(f"Database error during registration: {str(e)}")
            ui.notify("Registration failed due to a database error. Please try again.", color="red")
            show_form()  # Show form again for editing
        except Exception as e:
            app_logger.error(f"Unexpected error during registration: {str(e)}")
            ui.notify("An unexpected error occurred. Please try again.", color="red")
            show_form()  # Show form again for editing

    def show_form():
        """Show the registration form."""
        verification_container.style('display: none')
        form_container.style('display: block')

    # Render registration form and get input references
    with form_container:
        with ui.card().classes('w-full bg-black/30 backdrop-blur-sm border border-purple-500/20 shadow-2xl rounded-xl md:rounded-2xl'):
            ui.html('<h2 class="text-xl sm:text-2xl md:text-3xl font-bold text-center mb-6 md:mb-8 text-purple-300 px-4 sm:px-6 md:px-8 pt-6 md:pt-8">Digital Identity Creation</h2>')
            form, name_input, email_input, phone_input, age_input, password_input, uploaded_image_data = registration_form(on_submit)
            
            # Add back to home link with Material Design touch targets
            with ui.column().classes('w-full text-center mt-4 md:mt-6 pb-6 md:pb-8 px-4 sm:px-6 md:px-8'):
                ui.link("Return to Home", target="/").classes('''
                    text-gray-400 hover:text-gray-300 transition-colors duration-300 text-sm sm:text-base
                    min-h-[44px] flex items-center justify-center
                ''')
    
    # Footer with Material Design spacing, responsive text, and proper centering
    with ui.column().classes('w-full flex items-center justify-center text-center py-8 md:py-12 mt-12 md:mt-16 px-4 sm:px-6 md:px-8'):
        ui.html('''
            <div class="text-gray-400 text-xs sm:text-sm md:text-base">
                <p class="mb-2 md:mb-3">🛡️ Identity creation protocols active</p>
                <p class="text-xs sm:text-sm opacity-75">BioVault Identity System v2.1</p>
            </div>
        ''')
