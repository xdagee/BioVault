from nicegui import ui  # type: ignore
from components.table import registrants_table
from data import get_all_users
from logging_config import app_logger

def registrants_page():
    """Registrants page with authentication check and Material Design responsive layout."""
    app_logger.info("Registrants page accessed")
    
    # Check authentication (simplified - in production, use proper middleware)
    ui.run_javascript("""
        const sessionId = localStorage.getItem('session_id');
        if (!sessionId) {
            window.location.href = '/login';
        }
    """)
    
    # Main container with gradient background, Material Design spacing, and proper centering
    with ui.column().classes('w-full min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center'):
        
        # Header section with Material Design typography, responsive spacing, and center alignment
        with ui.column().classes('w-full flex items-center justify-center text-center py-8 sm:py-12 md:py-16 lg:py-20 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="mb-6 md:mb-8">
                    <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 md:mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight tracking-tight">
                        Digital Vault
                    </h1>
                    <p class="text-base sm:text-lg md:text-xl lg:text-2xl text-gray-300 mb-4 md:mb-6 font-light leading-relaxed">Identity Registry & Management</p>
                    <div class="w-12 sm:w-16 md:w-20 lg:w-24 h-1 bg-gradient-to-r from-purple-400 to-pink-400 mx-auto rounded-full"></div>
                </div>
            ''')
        
        # Action buttons section with Material Design touch targets and responsive spacing
        with ui.column().classes('w-full max-w-4xl lg:max-w-6xl xl:max-w-7xl mx-auto px-4 sm:px-6 md:px-8 mb-6 md:mb-8'):
            with ui.row().classes('w-full justify-center gap-3 sm:gap-4 md:gap-6 flex-wrap'):
                ui.link('Create New Identity', target='/').classes('''
                    px-4 sm:px-6 md:px-8 py-3 sm:py-4 bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-500 hover:to-pink-600 
                    text-white font-bold text-sm sm:text-base md:text-lg rounded-xl shadow-lg hover:shadow-pink-500/25 
                    transition-all duration-300 transform hover:scale-105 border border-pink-400/30
                    min-h-[48px] flex items-center justify-center
                ''')
                
                def logout():
                    ui.run_javascript("""
                        const sessionId = localStorage.getItem('session_id');
                        if (sessionId) {
                            localStorage.removeItem('session_id');
                        }
                        window.location.href = '/';
                    """)
                
                ui.button('Exit Vault', on_click=logout).classes('''
                    px-4 sm:px-6 md:px-8 py-3 sm:py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 
                    text-white font-bold text-sm sm:text-base md:text-lg rounded-xl shadow-lg hover:shadow-red-500/25 
                    transition-all duration-300 transform hover:scale-105 border border-red-400/30
                    min-h-[48px] flex items-center justify-center
                ''')
        
        # Table container with refresh functionality and responsive layout
        with ui.column().classes('w-full max-w-4xl lg:max-w-6xl xl:max-w-7xl mx-auto px-4 sm:px-6 md:px-8'):
            with ui.card().classes('w-full bg-black/30 backdrop-blur-sm border border-purple-500/20 shadow-2xl rounded-xl md:rounded-2xl'):
                ui.html('<h2 class="text-xl sm:text-2xl md:text-3xl font-bold text-center mb-6 md:mb-8 text-purple-300 px-4 sm:px-6 md:px-8 pt-6 md:pt-8">Registered Identities</h2>')
                
                # Container for the table that can be refreshed with responsive padding
                table_container = ui.column().classes('w-full px-4 sm:px-6 md:px-8 pb-6 md:pb-8')
                
                def refresh_table():
                    """Refresh the table with current data."""
                    table_container.clear()
                    with table_container:
                        users = get_all_users()
                        registrants_table(users, refresh_table)
                
                # Initial load
                refresh_table()
        
        # Footer with Material Design spacing, responsive text, and proper centering
        with ui.column().classes('w-full flex items-center justify-center text-center py-8 md:py-12 mt-12 md:mt-16 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="text-gray-400 text-xs sm:text-sm md:text-base">
                    <p class="mb-2 md:mb-3">🔍 Vault access granted - Identity registry active</p>
                    <p class="text-xs sm:text-sm opacity-75">BioVault Management System v2.1</p>
                </div>
            ''')
