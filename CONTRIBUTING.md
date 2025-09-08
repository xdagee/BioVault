# Contributing to BioVault

Thank you for your interest in contributing to BioVault! This document provides guidelines and instructions for contributing to the project.

## 🚀 Quick Start for Contributors

### First-time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork:**
```bash
git clone https://github.com/YOUR_USERNAME/biovault.git
cd biovault
```

3. **Set up development environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov mypy black flake8
```

4. **Add upstream remote:**
```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/biovault.git
```

## 🔄 Development Workflow

### Before Making Changes

1. **Sync with upstream:**
```bash
git checkout main
git pull upstream main
git push origin main
```

2. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### Making Changes

1. **Write your code** following our coding standards
2. **Add tests** for new functionality
3. **Update documentation** if needed
4. **Run tests locally:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src/

# Code formatting (optional)
black src/
flake8 src/
```

### Submitting Changes

1. **Commit your changes:**
```bash
git add .
git commit -m "Type: Brief description of changes"
```

**Commit Message Format:**
- `Add: new feature or functionality`
- `Fix: bug fix`
- `Update: improvement to existing feature`
- `Remove: deletion of feature or code`
- `Docs: documentation changes`
- `Test: test additions or modifications`
- `Refactor: code refactoring without functional changes`

2. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request:**
   - Go to GitHub and create a pull request
   - Provide clear description of changes
   - Reference any related issues
   - Wait for review and address feedback

## 📋 Coding Standards

### Python Code Style

- **Follow PEP 8** style guidelines
- **Use type hints** for all function signatures
- **Write docstrings** for all public functions and classes
- **Keep functions small** and focused on single responsibility
- **Use meaningful variable names**

### Example Code Style:

```python
def validate_user_email(email: str) -> bool:
    """
    Validate if the provided email address is in correct format.
    
    Args:
        email: The email address to validate
        
    Returns:
        True if email is valid, False otherwise
        
    Raises:
        ValueError: If email is None or empty
    """
    if not email:
        raise ValueError("Email cannot be empty")
    
    return "@" in email and "." in email
```

### Security Guidelines

- **Always sanitize user inputs** using bleach or similar
- **Use parameterized queries** (SQLAlchemy handles this)
- **Never log sensitive information** (passwords, tokens, etc.)
- **Follow existing authentication patterns**
- **Add rate limiting** to new endpoints if applicable

### Testing Requirements

- **Unit tests** for all new functions
- **Integration tests** for API endpoints
- **Test both success and failure cases**
- **Maintain test coverage** above 80%

Example test:
```python
def test_validate_user_email_valid():
    """Test email validation with valid email."""
    assert validate_user_email("user@example.com") is True

def test_validate_user_email_invalid():
    """Test email validation with invalid email."""
    assert validate_user_email("invalid-email") is False

def test_validate_user_email_empty():
    """Test email validation with empty email."""
    with pytest.raises(ValueError):
        validate_user_email("")
```

## 🐛 Bug Reports

### Before Reporting a Bug

1. **Check existing issues** to avoid duplicates
2. **Test with latest version** from main branch
3. **Reproduce the bug** consistently
4. **Gather relevant information:**
   - Python version
   - Operating system
   - Error messages
   - Steps to reproduce

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 
- OS: 
- Browser (if applicable):

## Error Messages
```
[Paste any error messages here]
```

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting a Feature

1. **Check existing issues** and discussions
2. **Consider if it fits** the project's scope and goals
3. **Think about implementation** and potential challenges

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why this feature would be valuable

## Proposed Implementation
High-level overview of how it could be implemented

## Alternatives Considered
Other ways to achieve the same goal

## Additional Context
Any other relevant information
```

## 🔍 Code Review Process

### For Contributors

- **Be responsive** to review feedback
- **Make requested changes** promptly
- **Ask questions** if feedback is unclear
- **Test your changes** after making updates

### Review Criteria

Your pull request will be reviewed for:

- **Code quality** and adherence to standards
- **Test coverage** and test quality
- **Security implications**
- **Performance impact**
- **Documentation updates**
- **Backward compatibility**

## 🏗️ Project Structure

```
biovault/
├── src/                    # Application source code
│   ├── components/         # Reusable UI components
│   ├── pages/             # Application pages
│   ├── validation/        # Input validation
│   ├── auth.py           # Authentication logic
│   ├── config.py         # Configuration management
│   ├── database.py       # Database models and operations
│   └── app.py            # Main application entry point
├── tests/                 # Test files
├── logs/                  # Application logs (created at runtime)
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── CONTRIBUTING.md       # This file
├── LICENSE               # Project license
└── .gitignore           # Git ignore patterns
```

## 🛡️ Security Considerations

### Reporting Security Issues

- **Do not** create public issues for security vulnerabilities
- **Email security issues** to: [your-security-email@domain.com]
- **Provide detailed information** about the vulnerability
- **Allow reasonable time** for fixes before public disclosure

### Security Best Practices

- **Input validation** on all user inputs
- **Output encoding** to prevent XSS
- **SQL injection prevention** using ORM
- **Rate limiting** on sensitive endpoints
- **Secure session management**
- **CSRF protection** on forms

## 🎯 Areas for Contribution

We welcome contributions in these areas:

### High Priority
- **Performance optimizations**
- **Additional security features**
- **Better error handling**
- **Mobile responsiveness**
- **API documentation**

### Medium Priority
- **Additional authentication methods** (OAuth, SAML)
- **User management features**
- **Audit logging enhancements**
- **Monitoring improvements**

### Low Priority
- **UI/UX improvements**
- **Additional themes**
- **Internationalization**
- **Plugin system**

## 📚 Resources

### Documentation
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [NiceGUI Documentation](https://nicegui.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Tools
- [pytest](https://pytest.org/) - Testing framework
- [mypy](http://mypy-lang.org/) - Static type checker
- [black](https://black.readthedocs.io/) - Code formatter
- [flake8](https://flake8.pycqa.org/) - Style guide enforcement

## ❓ Getting Help

- **General questions**: Create a GitHub discussion
- **Bug reports**: Create a GitHub issue
- **Feature requests**: Create a GitHub issue
- **Security issues**: Email privately
- **Contributing questions**: Ask in pull request comments

## 🙏 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors graph**

Thank you for contributing to BioVault! 🚀