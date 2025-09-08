from nicegui import ui
from pages.home import home_page
from pages.registrants import registrants_page
from pages.login import login_page
from pages.register import register_page
from database import init_db
from database_migrations import run_database_migrations
from logging_config import setup_logging, app_logger
from config import config
from monitoring import health_checker
from middleware import apply_middleware, apply_auth_middleware
from pathlib import Path

# Setup logging
setup_logging(
    log_level=config.logging.level,
    log_file=config.logging.log_file
)

# Initialize database
try:
    init_db()
    app_logger.info("Database initialized successfully")
    
    # Run database migrations
    if run_database_migrations():
        app_logger.info("Database migrations completed successfully")
    else:
        app_logger.warning("Database migrations failed, but continuing...")
        
except Exception as e:
    app_logger.error(f"Failed to initialize database: {str(e)}")
    raise

# Setup static file serving for uploaded images
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
# Note: Static file serving handled differently in newer NiceGUI versions
# Files are served from the uploads directory automatically

# Define routes with middleware
@ui.page("/")
def home():
    return apply_middleware(home_page)()

@ui.page("/login")
def login():
    return apply_auth_middleware(login_page)()

@ui.page("/register")
def register():
    return apply_auth_middleware(register_page)()

@ui.page("/registrants")
def registrants():
    return apply_middleware(registrants_page)()

# Health check endpoint
@ui.page("/health")
def health_check():
    """Health check endpoint for monitoring."""
    health_status = health_checker.get_application_health()
    return health_status

# Metrics endpoint
@ui.page("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    from nicegui import response
    metrics_data = health_checker.get_metrics()
    response.headers['Content-Type'] = 'text/plain; version=0.0.4; charset=utf-8'
    return metrics_data

# Run the app
if __name__ in {"__main__", "__mp_main__"}:
    app_logger.info(f"Starting application on {config.host}:{config.port}")
    ui.run(host=config.host, port=config.port)
