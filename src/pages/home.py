from nicegui import ui  # type: ignore
from nicegui import ui  # type: ignore
from logging_config import app_logger

def home_page():
    """Home page with engaging design and compelling story following Material Design guidelines."""
    app_logger.info("Home page accessed")
    
    # Main container with gradient background, Material Design spacing, and proper centering
    with ui.column().classes('w-full min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center'):
        
        # Header section with Material Design typography and spacing - properly centered
        with ui.column().classes('w-full flex items-center justify-center text-center py-16 sm:py-20 md:py-24 lg:py-32 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="mb-12 md:mb-16">
                    <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold mb-6 md:mb-8 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight tracking-tight">
                        BioVault
                    </h1>
                    <p class="text-lg sm:text-xl md:text-2xl lg:text-3xl text-gray-200 mb-6 md:mb-8 font-light leading-relaxed max-w-4xl mx-auto">Your Digital Identity Sanctuary</p>
                    <div class="w-24 sm:w-32 md:w-40 h-1 bg-gradient-to-r from-purple-400 to-pink-400 mx-auto rounded-full shadow-lg"></div>
                </div>
            ''')
        
        # Story section with Material Design typography, responsive spacing, and center alignment
        with ui.column().classes('w-full max-w-4xl lg:max-w-5xl xl:max-w-6xl mx-auto flex items-center justify-center px-4 sm:px-6 md:px-8 mb-16 md:mb-20 lg:mb-24'):
            ui.html('''
                <div class="bg-black/30 backdrop-blur-sm rounded-2xl md:rounded-3xl p-6 sm:p-8 md:p-10 lg:p-12 border border-purple-500/20 shadow-2xl">
                    <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-center mb-6 md:mb-8 lg:mb-10 text-purple-300 leading-tight tracking-tight">The Mystery of the Lost Identities</h2>
                    
                    <div class="text-base sm:text-lg md:text-xl lg:text-xl leading-relaxed space-y-4 md:space-y-6 text-gray-100">
                        <p class="text-center italic text-purple-200 mb-6 md:mb-8 text-lg sm:text-xl md:text-2xl lg:text-3xl font-light leading-relaxed">
                            "In the shadows of the digital realm, where data flows like whispers in the wind..."
                        </p>
                        
                        <p class="leading-7 md:leading-8">
                            <span class="text-purple-300 font-semibold">Dr. Elena Voss</span> was a brilliant cryptographer who discovered something that would change everything. 
                            Hidden within the depths of an ancient server farm, she found fragments of digital identities—not just data, but living memories, 
                            dreams, and secrets of thousands of people who had vanished from the digital world.
                        </p>
                        
                        <p class="leading-7 md:leading-8">
                            Each identity was a puzzle piece in a larger mystery. Some contained encrypted messages about a global conspiracy. 
                            Others held the keys to unlocking technologies that could revolutionize human consciousness. 
                            But the most chilling discovery was this: <span class="text-red-400 font-bold">the identities weren't just stored—they were waiting.</span>
                        </p>
                        
                        <p class="leading-7 md:leading-8">
                            Before Dr. Voss could complete her research, she disappeared without a trace. The only clue left behind was a cryptic message: 
                            <span class="text-yellow-300 italic">"The vault holds the truth, but only the worthy can unlock it. Your identity is your key."</span>
                        </p>
                        
                        <div class="bg-gradient-to-r from-purple-600/20 to-pink-600/20 rounded-xl md:rounded-2xl p-6 md:p-8 mt-6 md:mt-8 border border-purple-400/30 shadow-lg">
                            <p class="text-center text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-purple-200 leading-relaxed">
                                Now, the BioVault awaits your arrival. Will you be the one to unlock the mystery?
                            </p>
                        </div>
                    </div>
                </div>
            ''')
        
        # Features section with Material Design grid, responsive layout, and center alignment
        with ui.column().classes('w-full max-w-4xl lg:max-w-6xl xl:max-w-7xl mx-auto flex items-center justify-center px-4 sm:px-6 md:px-8 mb-16 md:mb-20 lg:mb-24'):
            ui.html('''
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
                    <div class="bg-black/20 backdrop-blur-sm rounded-xl md:rounded-2xl p-6 md:p-8 border border-purple-500/20 text-center hover:bg-black/30 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-500/20">
                        <div class="text-4xl md:text-5xl lg:text-6xl mb-4 md:mb-6">🔐</div>
                        <h3 class="text-lg sm:text-xl md:text-2xl font-bold text-purple-300 mb-3 md:mb-4 leading-tight">Secure Identity</h3>
                        <p class="text-sm sm:text-base text-gray-300 leading-relaxed">Military-grade encryption protects your digital persona</p>
                    </div>
                    <div class="bg-black/20 backdrop-blur-sm rounded-xl md:rounded-2xl p-6 md:p-8 border border-purple-500/20 text-center hover:bg-black/30 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-500/20">
                        <div class="text-4xl md:text-5xl lg:text-6xl mb-4 md:mb-6">🌐</div>
                        <h3 class="text-lg sm:text-xl md:text-2xl font-bold text-purple-300 mb-3 md:mb-4 leading-tight">Global Network</h3>
                        <p class="text-sm sm:text-base text-gray-300 leading-relaxed">Connect with others in the digital underground</p>
                    </div>
                    <div class="bg-black/20 backdrop-blur-sm rounded-xl md:rounded-2xl p-6 md:p-8 border border-purple-500/20 text-center hover:bg-black/30 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-500/20 sm:col-span-2 lg:col-span-1">
                        <div class="text-4xl md:text-5xl lg:text-6xl mb-4 md:mb-6">⚡</div>
                        <h3 class="text-lg sm:text-xl md:text-2xl font-bold text-purple-300 mb-3 md:mb-4 leading-tight">Instant Access</h3>
                        <p class="text-sm sm:text-base text-gray-300 leading-relaxed">Enter the vault and discover what awaits</p>
                    </div>
                </div>
            ''')
        
        # Call to action section with Material Design spacing, touch targets, and center alignment
        with ui.column().classes('w-full flex items-center justify-center text-center py-12 md:py-16 lg:py-20 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="mb-8 md:mb-12">
                    <h3 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-purple-300 mb-4 md:mb-6 leading-tight tracking-tight">Ready to Begin Your Journey?</h3>
                    <p class="text-gray-300 text-lg sm:text-xl md:text-2xl lg:text-3xl font-light leading-relaxed max-w-3xl mx-auto">Join the digital underground and unlock the mystery</p>
                </div>
            ''')
            
            # Navigation buttons with Material Design touch targets and proper centering
            with ui.row().classes('w-full flex items-center justify-center gap-4 sm:gap-6 md:gap-8 flex-wrap px-4'):
                ui.link('Enter the Vault', target='/login').classes('''
                    px-6 sm:px-8 md:px-10 py-3 sm:py-4 md:py-5 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 
                    text-white font-bold text-base sm:text-lg md:text-xl rounded-xl md:rounded-2xl shadow-xl hover:shadow-purple-500/30 
                    transition-all duration-300 transform hover:scale-105 border border-purple-400/30
                    min-w-[160px] sm:min-w-[180px] md:min-w-[200px] text-center min-h-[44px] flex items-center justify-center
                ''')
                
                ui.link('Create Identity', target='/register').classes('''
                    px-6 sm:px-8 md:px-10 py-3 sm:py-4 md:py-5 bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-500 hover:to-pink-600 
                    text-white font-bold text-base sm:text-lg md:text-xl rounded-xl md:rounded-2xl shadow-xl hover:shadow-pink-500/30 
                    transition-all duration-300 transform hover:scale-105 border border-pink-400/30
                    min-w-[160px] sm:min-w-[180px] md:min-w-[200px] text-center min-h-[44px] flex items-center justify-center
                ''')
        
        # Footer with Material Design spacing, responsive text, and proper centering
        with ui.column().classes('w-full flex items-center justify-center text-center py-8 md:py-12 mt-12 md:mt-16 px-4 sm:px-6 md:px-8'):
            ui.html('''
                <div class="text-gray-400 text-xs sm:text-sm md:text-base max-w-2xl mx-auto">
                    <p class="mb-2 md:mb-3">⚠️ Warning: Entering the BioVault may change your perception of reality</p>
                    <p class="text-xs sm:text-sm opacity-75 leading-relaxed">Dr. Elena Voss - Last seen: Unknown | Status: Missing | Location: Digital Void</p>
                </div>
            ''')
