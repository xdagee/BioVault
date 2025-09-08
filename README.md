# BioVault - Secure Digital Identity Management

A secure user registration and management application built with Python, NiceGUI, and enterprise-grade security features.

## 🎯 Overview

BioVault is designed for developers and system administrators who need a robust, secure user registration system with comprehensive authentication, monitoring, and protection against common web vulnerabilities.

## 📋 Quick Reference

### Essential Commands
```bash
# First time setup (after cloning)
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python src/app.py

# Daily development
git pull origin main
venv\Scripts\activate  # Windows
python src/app.py

# Making changes
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "Add: my new feature"
git push origin feature/my-feature
```

### Repository URLs
- **HTTPS Clone**: `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git`
- **SSH Clone**: `git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git`
- **Application URL**: `http://localhost:8080`
- **Health Check**: `http://localhost:8080/health`
- **Metrics**: `http://localhost:8080/metrics`

## 🚀 Quick Start - GitHub Integration

### 📤 Push Your Project to GitHub

1. **Create a new repository on GitHub:**
   - Go to [GitHub](https://github.com) and click "New repository"
   - Name your repository (e.g., "biovault" or "bio-app")
   - Choose visibility (Public or Private)
   - **Don't** initialize with README, .gitignore, or license (we already have these)

2. **Initialize Git and push from your local directory:**
```bash
# Navigate to your project directory
cd c:\Users\twentytwo\Documents\bio

# Initialize git repository (if not already done)
git init

# Add all files to git
git add .

# Create initial commit
git commit -m "Initial commit: BioVault secure identity management app"

# Add your GitHub repository as remote origin
# Replace YOUR_USERNAME and YOUR_REPOSITORY with your actual GitHub info
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# Push to GitHub
git branch -M main
git push -u origin main
```

3. **Alternative: Using GitHub CLI (if installed):**
```bash
# Navigate to project directory
cd c:\Users\twentytwo\Documents\bio

# Create repository and push in one command
gh repo create biovault --public --source=. --remote=origin --push
```

### 📥 Clone and Setup on Any Computer

#### **For New Contributors/Users:**

1. **Clone the repository:**
```bash
# Clone using HTTPS
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

# Or clone using SSH (if you have SSH keys set up)
git clone git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

2. **Set up Python environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

3. **Initialize the application:**
```bash
# Run the application (database will be created automatically)
python src/app.py
```

4. **Access the application:**
   - Open your browser to `http://localhost:8080`
   - The application is now ready to use!

#### **For Existing Contributors:**

1. **Pull latest changes:**
```bash
# Navigate to your project directory
cd path/to/your/biovault

# Pull latest changes from GitHub
git pull origin main

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Update dependencies (if requirements.txt changed)
pip install -r requirements.txt

# Run the application
python src/app.py
```

### 🔄 Development Workflow

#### **Making Changes and Contributing:**

1. **Create a new branch for your feature:**
```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

2. **Make your changes and test:**
```bash
# Run tests to ensure everything works
pytest

# Check code quality
mypy src/

# Run the application to test
python src/app.py
```

3. **Commit and push your changes:**
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "Add: new feature description" 
# or
git commit -m "Fix: bug description"
# or 
git commit -m "Update: improvement description"

# Push to GitHub
git push origin feature/your-feature-name
```

4. **Create Pull Request:**
   - Go to your GitHub repository
   - Click "Compare & pull request"
   - Add description of your changes
   - Submit the pull request

#### **Staying Up to Date:**

```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Update your feature branch (if working on one)
git checkout feature/your-feature-name
git merge main
```

### 🛠️ Environment Setup Variations

#### **Using Conda (Alternative to venv):**
```bash
# Create conda environment
conda create -n biovault python=3.11
conda activate biovault

# Install dependencies
pip install -r requirements.txt

# Run application
python src/app.py
```

#### **Using Poetry (Alternative dependency manager):**
```bash
# Initialize poetry (if not already done)
poetry init

# Install dependencies
poetry install

# Run in poetry environment
poetry run python src/app.py
```

#### **Using Docker (Containerized setup):**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
EXPOSE 8080

CMD ["python", "src/app.py"]
```

Build and run:
```bash
# Build image
docker build -t biovault .

# Run container
docker run -p 8080:8080 biovault
```

### 📋 Pre-requisites for Contributors

**Required Software:**
- **Python 3.11+** ([Download here](https://www.python.org/downloads/))
- **Git** ([Download here](https://git-scm.com/downloads))
- **GitHub Account** ([Sign up here](https://github.com))

**Optional but Recommended:**
- **GitHub CLI** ([Download here](https://cli.github.com/)) - for easier repository management
- **VS Code** with Python extension - for development
- **GitHub Desktop** - for GUI-based Git operations

### 🔧 Troubleshooting Setup Issues

#### **Common Issues and Solutions:**

**1. Python not found:**
```bash
# Verify Python installation
python --version
# or try
python3 --version

# If not found, download from python.org and ensure it's in PATH
```

**2. Git not found:**
```bash
# Verify Git installation
git --version

# If not found, download from git-scm.com
```

**3. Permission denied (Windows):**
```bash
# Run PowerShell as Administrator
# Or use Git Bash instead of Command Prompt
```

**4. Virtual environment issues:**
```bash
# On Windows, if execution policy prevents activation:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv
venv\Scripts\activate
```

**5. Dependencies installation fails:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install dependencies one by one to identify issues
pip install nicegui
pip install bcrypt
# ... continue with other packages
```

**6. Port already in use:**
```bash
# Run on different port
PORT=3000 python src/app.py

# Or kill process using port 8080
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8080 | xargs kill
```

## ✨ Features

### Core Functionality
- **Secure User Registration**: Multi-step registration with image upload support
- **JWT Authentication**: Token-based authentication with session management
- **User Management**: View and manage registered users (authenticated access)
- **Real-time Monitoring**: Health checks and Prometheus metrics
- **Admin Dashboard**: User list with search and filtering capabilities

### Security Features
- **Password Security**: bcrypt hashing with strength requirements
- **Session Management**: In-memory sessions with automatic cleanup
- **Rate Limiting**: Configurable limits for authentication and general endpoints
- **CSRF Protection**: Token-based protection for all forms
- **Input Sanitization**: XSS protection using bleach
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Session Security**: Automatic regeneration to prevent fixation attacks

### Enterprise Features
- **Comprehensive Logging**: Structured logging with configurable levels
- **Error Handling**: Custom exception hierarchy with detailed error tracking
- **Health Monitoring**: `/health` endpoint for system status
- **Metrics Exposure**: Prometheus-compatible `/metrics` endpoint
- **Simple Deployment**: No external dependencies for basic operation

## 🛠️ Technology Stack

- **Backend**: Python 3.11, NiceGUI
- **Database**: PostgreSQL (recommended) or SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose, bcrypt password hashing
- **Session Storage**: In-memory with automatic cleanup
- **Security**: CSRF protection (itsdangerous), input sanitization (bleach)
- **Rate Limiting**: SlowAPI with memory backend
- **Monitoring**: Prometheus metrics, structured logging (psutil)
- **Testing**: pytest with coverage reporting
- **Code Quality**: mypy for type checking, optional flake8 and black

## 🚀 Local Development Setup

> **For GitHub setup and collaboration, see the [GitHub Integration section](#-quick-start---github-integration) above.**

### Prerequisites

- **Python 3.11+** (required)
- **Git** (for version control)
- **PostgreSQL** (optional, SQLite used by default)

### Installation & Setup

1. **If you already have the code locally:**
```bash
cd c:\Users\twentytwo\Documents\bio
pip install -r requirements.txt
```

2. **If cloning from GitHub:**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Basic Configuration (Development):**
```bash
# The app works out-of-the-box with defaults
# Optional: Create .env file for custom configuration
cp env.example .env
```

3. **Run the application:**
```bash
python src/app.py
```

4. **Access the application:**
   - Open your browser to `http://localhost:8080`
   - Register a new user or login with existing credentials
   - View registered users at `/registrants` (requires authentication)

### 📊 Monitoring Endpoints

- **Health Check**: `http://localhost:8080/health`
- **Metrics**: `http://localhost:8080/metrics` (Prometheus format)
- **Application**: `http://localhost:8080/` (main interface)

## ⚙️ Configuration

The application uses environment variables for configuration with sensible defaults for development.

### Development Setup (Minimal)

For local development, the app runs with built-in defaults:

```bash
# No .env file needed - just run:
python src/app.py
```

### Production Configuration

For production deployment, create a `.env` file:

```bash
# Security (Required for production)
SECRET_KEY=your-strong-secret-key-here
CSRF_SECRET_KEY=your-csrf-secret-key-here
DEBUG=false

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/bioapp

# Rate Limiting (Optional - enabled by default)
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE=10
RATE_LIMIT_BURST_SIZE=10

# Session & Security
SESSION_TIMEOUT_MINUTES=30
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

# Application
HOST=localhost
PORT=8080
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Auto-generated | JWT signing key (set for production) |
| `CSRF_SECRET_KEY` | Auto-generated | CSRF token signing key |
| `DATABASE_URL` | SQLite file | Database connection string |
| `RATE_LIMIT_ENABLED` | `true` | Enable/disable rate limiting |
| `DEBUG` | `false` | Enable debug mode |
| `HOST` | `localhost` | Server bind address |
| `PORT` | `8080` | Server port |

### Database Setup

**Automatic Setup:**
- Database tables are created automatically on first run
- No manual migrations required
- Supports both SQLite (default) and PostgreSQL

**PostgreSQL Setup (Optional):**
```bash
# Install PostgreSQL and create database
createdb bioapp

# Set environment variable
DATABASE_URL=postgresql://username:password@localhost:5432/bioapp
```

### Redis Setup (Optional but Recommended)

**Note: Redis has been removed from this application. Sessions are now handled in memory.**

**For High-Availability Deployments:**
If you need persistent sessions across server restarts, consider implementing database-backed sessions or using sticky sessions with a load balancer.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test modules
pytest tests/test_auth.py          # Authentication tests
pytest tests/test_database.py      # Database tests
pytest tests/test_validation.py    # Input validation tests

# Run tests with verbose output
pytest -v

# View coverage report
# Open htmlcov/index.html in your browser after running coverage
```

## 🔍 Code Quality

The project includes several code quality tools:

```bash
# Type checking (required)
mypy src/

# Linting (optional)
flake8 src/

# Code formatting (optional)
black src/

# Check all quality tools at once
mypy src/ && echo "Type checking passed"
```

## 🌐 API Endpoints

### Application Pages
- `GET /` - Registration form (home page)
- `GET /login` - User login form
- `GET /register` - User registration form
- `GET /registrants` - User management dashboard (requires authentication)

### Monitoring & Health
- `GET /health` - Health check endpoint (JSON response)
- `GET /metrics` - Prometheus metrics (text format)

### Security Features
- **Rate Limiting**: Applied to all endpoints
  - General endpoints: 60 requests/minute
  - Authentication endpoints: 10 requests/minute
- **CSRF Protection**: All forms include CSRF tokens
- **Session Management**: Automatic cleanup and Redis storage

## 📊 Monitoring & Observability

The application includes enterprise-grade monitoring:

### Health Checks
- **Database Connectivity**: Automatic database connection testing
- **System Resources**: Memory, CPU, and disk usage monitoring
- **Redis Status**: Session storage connectivity (if configured)
- **Application Status**: Overall health aggregation

### Metrics (Prometheus Compatible)
- **Request Metrics**: Count, duration, status codes by endpoint
- **Session Metrics**: Active sessions, creation/destruction rates
- **Database Metrics**: Connection pool status and query performance
- **System Metrics**: Memory usage, CPU usage, process information

### Logging
- **Structured Logging**: JSON format with configurable levels
- **Security Events**: Authentication attempts, rate limiting, CSRF violations
- **Error Tracking**: Comprehensive error logging with stack traces
- **Audit Trail**: User actions and system events

### Example Monitoring Setup
```bash
# View real-time health status
curl http://localhost:8080/health

# Get Prometheus metrics
curl http://localhost:8080/metrics

# Monitor logs (if file logging enabled)
tail -f logs/app.log
```

## 🔒 Security Considerations

### Authentication & Authorization
- **Password Security**: bcrypt hashing with configurable rounds
- **JWT Tokens**: Secure token generation with expiration
- **Session Management**: Redis-based sessions with automatic cleanup
- **Session Security**: Regeneration on login to prevent fixation attacks

### Input Security
- **Input Sanitization**: All user inputs sanitized using bleach
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: HTML content sanitization and CSP headers
- **CSRF Protection**: Token-based protection for all form submissions

### Rate Limiting & DoS Protection
- **Authentication Rate Limiting**: 10 attempts per minute per IP
- **General Rate Limiting**: 60 requests per minute per IP
- **Failed Attempt Tracking**: Automatic lockout after repeated failures
- **Distributed Rate Limiting**: Redis-based counters for horizontal scaling

### Production Security
- **HTTPS Required**: All production deployments must use HTTPS
- **Secure Headers**: Security headers via reverse proxy (recommended)
- **Environment Isolation**: Sensitive configuration via environment variables
- **Secret Management**: Automatic generation of secure secrets for development

### Security Audit
- **Regular Updates**: Keep dependencies updated
- **Security Scanning**: Run `pip-audit` to check for vulnerabilities
- **Log Monitoring**: Monitor authentication failures and rate limit violations
- **Access Logging**: Comprehensive audit trail of user actions

## 🚀 Deployment

### Development Deployment
```bash
# Simple development server
python src/app.py

# With debug mode
DEBUG=true python src/app.py

# Custom port
PORT=3000 python src/app.py
```

### Production Deployment

**Recommended Production Stack:**
- **Reverse Proxy**: Nginx or Apache for HTTPS and security headers
- **Process Manager**: systemd or supervisor
- **Database**: PostgreSQL for production workloads
- **Monitoring**: Prometheus + Grafana for metrics
- **Load Balancing**: For multiple instances (use sticky sessions)

**Example Production Setup:**

1. **Environment Configuration:**
```bash
# Production .env file
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@localhost/bioapp
RATE_LIMIT_ENABLED=true
LOG_LEVEL=INFO
```

2. **Systemd Service** (`/etc/systemd/system/bioapp.service`):
```ini
[Unit]
Description=Bio App
After=network.target

[Service]
Type=simple
User=bioapp
WorkingDirectory=/opt/bioapp
Environment=PATH=/opt/bioapp/venv/bin
EnvironmentFile=/opt/bioapp/.env
ExecStart=/opt/bioapp/venv/bin/python src/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Alternative Deployment Options

**Using Supervisor (Process Manager):**

1. **Install Supervisor:**
```bash
pip install supervisor
```

2. **Create supervisor config** (`/etc/supervisor/conf.d/bioapp.conf`):
```ini
[program:bioapp]
command=/opt/bioapp/venv/bin/python src/app.py
directory=/opt/bioapp
user=bioapp
autostart=true
autorestart=true
stderr_logfile=/var/log/bioapp/bioapp.err.log
stdout_logfile=/var/log/bioapp/bioapp.out.log
environment=PATH="/opt/bioapp/venv/bin"
```

3. **Start the service:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start bioapp
```

## 🛠️ Troubleshooting

### Common Issues

**1. Redis Connection Failed**
```bash
# Redis has been removed from this application
# Sessions are now handled in memory
# No action needed
```

**2. Database Connection Issues**
```bash
# For PostgreSQL
pg_isready -h localhost -p 5432

# For SQLite (default), no action needed
# Database file is created automatically
```

**3. Permission Errors**
```bash
# Ensure log directory exists
mkdir -p logs

# Check file permissions
ls -la logs/
```

**4. Rate Limiting Too Aggressive**
```bash
# Temporarily disable rate limiting
RATE_LIMIT_ENABLED=false python src/app.py

# Or increase limits
RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE=50 python src/app.py
```

**5. Module Import Errors**
```bash
# Ensure you're in the right directory
cd c:\Users\twentytwo\Documents\conda_envs\bio

# Install missing dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Health Check Commands

```bash
# Test application health
curl http://localhost:8080/health

# Test specific endpoints
curl http://localhost:8080/
curl http://localhost:8080/metrics

# Check logs
tail -f logs/app.log

# Monitor system resources
htop  # or Task Manager on Windows
```

## 📋 Contributing

### Development Setup

1. **Fork and clone the repository**
2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install development dependencies:**
```bash
pip install -r requirements.txt
pip install black flake8  # Optional formatting tools
```

4. **Run tests before making changes:**
```bash
pytest
mypy src/
```

5. **Make your changes and test:**
```bash
# Run specific tests
pytest tests/test_auth.py -v

# Check code quality
mypy src/
black --check src/
```

6. **Submit a pull request**

### Code Standards

- **Type Hints**: Required for all function signatures
- **Testing**: Add tests for new functionality
- **Documentation**: Update README for significant changes
- **Security**: Follow existing security patterns
- **Logging**: Use structured logging for new features

### Security Guidelines

- **Input Validation**: Always sanitize user inputs
- **Authentication**: Use existing auth patterns
- **Session Management**: Integrate with session_store
- **Rate Limiting**: Apply appropriate limits to new endpoints
- **Error Handling**: Use custom exception classes

## 📝 Changelog

### v2.0.0 (Latest) - Enhanced Security
- ✅ Implemented comprehensive rate limiting
- ✅ Added CSRF protection for all forms
- ✅ Centralized configuration management
- ✅ Enhanced session security with regeneration
- ✅ Improved monitoring and observability
- ✅ Simplified deployment (removed Redis dependency)
- ✅ Memory-based session storage with automatic cleanup

### v1.0.0 - Initial Release
- Basic user registration and authentication
- SQLAlchemy database integration
- JWT token authentication
- Basic security features

## 📜 Documentation

- **[Security Improvements](SECURITY_IMPROVEMENTS.md)** - Detailed security enhancement documentation
- **[API Documentation](docs/api.md)** - Detailed API reference (coming soon)
- **[Deployment Guide](docs/deployment.md)** - Production deployment guide (coming soon)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NiceGUI** - For the excellent Python web framework
- **SQLAlchemy** - For robust database ORM
- **Redis** - For scalable session storage
- **Prometheus** - For monitoring and metrics
- **bcrypt** - For secure password hashing

---

**Built with ❤️ for secure, scalable user management**
