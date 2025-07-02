# Contributing to KaliOSINT

We welcome contributions from the cybersecurity and OSINT community! This document provides guidelines for contributing to the KaliOSINT project.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. **Check existing issues** to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Follow coding standards** (see below)
5. **Add tests** if applicable
6. **Update documentation** as needed
7. **Submit a pull request**

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Keep line length under **88 characters**
- Use **meaningful variable names**

### Code Example

```python
def analyze_phone_number(phone: str, country_code: str = None) -> Dict[str, Any]:
    """
    Analyze a phone number for OSINT information.
    
    Args:
        phone: The phone number to analyze
        country_code: Optional country code for parsing
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If phone number format is invalid
    """
    # Implementation here
    pass
```

### File Structure

- Use **clear directory structure**
- Group related functionality
- Keep modules **focused and cohesive**
- Follow the existing project structure

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_phone_analysis.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests

- Write tests for **new features**
- Include **edge cases**
- Use **descriptive test names**
- Mock external API calls

```python
def test_phone_validation_with_valid_number():
    """Test phone validation with a valid international number."""
    result = validate_phone("+1234567890")
    assert result["valid"] is True
    assert result["country"] == "US"
```

## 📚 Documentation

### Updating Documentation

- Update **README.md** for major changes
- Add **docstrings** to new functions
- Update **API documentation**
- Include **usage examples**

### Documentation Style

- Use **clear, concise language**
- Include **code examples**
- Add **screenshots** where helpful
- Keep documentation **up to date**

## 🔒 Security Guidelines

### Responsible Disclosure

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. **Email** security@kaliosint.org
3. **Include** detailed information
4. **Wait** for acknowledgment before disclosure

### Security Best Practices

- **Never commit** API keys or secrets
- **Validate all inputs**
- **Use secure coding practices**
- **Follow OWASP guidelines**

## 🎯 Development Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to ensure everything works
python -m pytest tests/
```

### Development Dependencies

```bash
# Install additional development tools
pip install black flake8 mypy pre-commit pytest pytest-cov
```

## 📋 Pull Request Process

### Before Submitting

1. **Sync with main branch**: `git pull origin main`
2. **Run tests**: `python -m pytest`
3. **Check code style**: `black . && flake8`
4. **Update documentation** if needed
5. **Write descriptive commit messages**

### Pull Request Template

When submitting a PR, include:

- **Clear description** of changes
- **Motivation** for the changes
- **Testing** performed
- **Screenshots** if UI changes
- **Breaking changes** if any

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Merge** when approved

## 🏷️ Issue Labels

We use labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature request
- `documentation`: Documentation updates
- `good-first-issue`: Good for newcomers
- `help-wanted`: Extra attention needed
- `security`: Security-related issues

## 🎖️ Recognition

Contributors will be:

- **Listed** in CONTRIBUTORS.md
- **Mentioned** in release notes
- **Given credit** in documentation

## ❓ Questions

If you have questions about contributing:

- **Open a discussion** on GitHub
- **Join our community** channels
- **Email** the maintainers

## 📜 License

By contributing to KaliOSINT, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to KaliOSINT! 🎉**

*Together, we're building a powerful and ethical OSINT framework for the cybersecurity community.*
