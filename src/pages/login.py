from nicegui import ui  # type: ignore
from auth import authenticate_user, create_session
from logging_config import auth_logger
from exceptions import AuthenticationError, ValidationError

def login_page():
    """Login page with secure authentication and Material Design responsive layout."""
    auth_logger.info("Login page accessed")
    
    # Main container with gradient background, Material Design spacing, and proper centering
    with ui.column().classes('w-full min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center'):
        
        # Header section with Material Design typography, responsive spacing, and center alignment
        with ui.column().classes('w-full flex items-center justify-center text-center py-12 sm:py-16 md:py-20 lg:py-24 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="mb-8 md:mb-12">
                    <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 md:mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight tracking-tight">
                        Enter the Vault
                    </h1>
                    <p class="text-base sm:text-lg md:text-xl text-gray-300 mb-4 md:mb-6 font-light leading-relaxed">Access your digital identity</p>
                    <div class="w-16 sm:w-20 md:w-24 h-1 bg-gradient-to-r from-purple-400 to-pink-400 mx-auto rounded-full"></div>
                </div>
            ''')
        
        # Login form container with Material Design responsive layout
        with ui.column().classes('w-full max-w-sm sm:max-w-md md:max-w-lg mx-auto px-4 sm:px-6 md:px-8'):
            with ui.card().classes('w-full bg-black/30 backdrop-blur-sm border border-purple-500/20 shadow-2xl rounded-xl md:rounded-2xl'):
                ui.html('<h2 class="text-xl sm:text-2xl md:text-3xl font-bold text-center mb-6 md:mb-8 text-purple-300 px-4 sm:px-6 md:px-8 pt-6 md:pt-8">Authentication Required</h2>')
                
                # Form container with Material Design spacing
                with ui.column().classes('px-4 sm:px-6 md:px-8 pb-6 md:pb-8'):
                    # Form inputs with Material Design styling, proper contrast, and touch targets
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
                    '''
                    
                    email_input = ui.input('Email Address').classes('w-full mb-4 md:mb-6').props('type=email')
                    email_input.style(input_style)
                    email_input.on('focus', lambda: email_input.style(focus_style))
                    email_input.on('blur', lambda: email_input.style(input_style))
                    
                    password_input = ui.input('Password').classes('w-full mb-6 md:mb-8').props('type=password')
                    password_input.style(input_style)
                    password_input.on('focus', lambda: password_input.style(focus_style))
                    password_input.on('blur', lambda: password_input.style(input_style))

                    def on_login():
                        try:
                            email = email_input.value
                            password = password_input.value

                            auth_logger.info(f"Login attempt for email: {email}")

                            # Validate input
                            if not email or not password:
                                auth_logger.warning(f"Login attempt with missing credentials for: {email}")
                                ui.notify("Please enter both email and password.", color="red")
                                return

                            # Authenticate user with secure password verification
                            user = authenticate_user(email, password)
                            
                            if user:
                                # Create session
                                session_id = create_session(user)
                                # Store session in client storage (in a real app, use secure cookies)
                                ui.run_javascript(f"localStorage.setItem('session_id', '{session_id}')")
                                
                                auth_logger.info(f"Login successful for: {email}")
                                ui.notify("Access granted! Welcome to the vault.", color="green")
                                ui.run_javascript("window.location.href = '/registrants'")  # Redirect to registrants page
                            else:
                                auth_logger.warning(f"Login failed - invalid credentials for: {email}")
                                ui.notify("Access denied. Invalid credentials.", color="red")
                                
                        except AuthenticationError as e:
                            auth_logger.error(f"Authentication error: {str(e)}")
                            ui.notify(f"Authentication error: {e.message}", color="red")
                        except ValidationError as e:
                            auth_logger.error(f"Validation error during login: {str(e)}")
                            ui.notify(f"Validation error: {e.message}", color="red")
                        except Exception as e:
                            auth_logger.error(f"Unexpected error during login: {str(e)}")
                            ui.notify("An unexpected error occurred. Please try again.", color="red")

                    # Submit button with Material Design touch targets and responsive sizing
                    ui.button("Enter the Vault", on_click=on_login).classes('''
                        w-full py-3 sm:py-4 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 
                        text-white font-bold text-base sm:text-lg rounded-xl shadow-lg hover:shadow-purple-500/25 
                        transition-all duration-300 transform hover:scale-105 border border-purple-400/30 mb-4 md:mb-6
                        min-h-[48px] flex items-center justify-center
                    ''')
                    
                    # Navigation links with proper spacing and touch targets
                    with ui.column().classes('w-full text-center space-y-3 md:space-y-4'):
                        ui.link("Create New Identity", target="/register").classes('''
                            text-purple-300 hover:text-purple-200 transition-colors duration-300 text-base sm:text-lg
                            min-h-[44px] flex items-center justify-center
                        ''')
                        ui.link("Return to Home", target="/").classes('''
                            text-gray-400 hover:text-gray-300 transition-colors duration-300 text-sm sm:text-base
                            min-h-[44px] flex items-center justify-center
                        ''')
        
        # Footer with Material Design spacing and responsive text - properly centered
        with ui.column().classes('w-full flex items-center justify-center text-center py-8 md:py-12 mt-12 md:mt-16 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="text-gray-400 text-xs sm:text-sm md:text-base max-w-2xl mx-auto">
                    <p class="mb-2 md:mb-3">🔐 Secure authentication protocols active</p>
                    <p class="text-xs sm:text-sm opacity-75">BioVault Security System v2.1</p>
                </div>
            ''')
