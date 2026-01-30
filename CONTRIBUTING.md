# Contributing to wlfwifi

Thank you for your interest in contributing to wlfwifi! This document provides comprehensive guidelines for contributing to the project, whether you're fixing bugs, adding features, improving documentation, or helping with testing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Making Changes](#making-changes)
  - [Commit Guidelines](#commit-guidelines)
- [Code Standards](#code-standards)
  - [Python Style Guide](#python-style-guide)
  - [Type Hints](#type-hints)
  - [Documentation](#documentation)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Writing Tests](#writing-tests)
  - [Test Coverage](#test-coverage)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Project Architecture](#project-architecture)
- [License](#license)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

**Key principles:**
- Be respectful and inclusive
- No harassment, discrimination, or inappropriate behavior
- Provide constructive feedback
- Focus on what is best for the community

---

## Ways to Contribute

There are many ways to contribute to wlfwifi:

| Contribution Type | Description |
|-------------------|-------------|
| 🐛 **Bug Reports** | Report bugs with detailed reproduction steps |
| ✨ **Feature Requests** | Suggest new features or improvements |
| 📝 **Documentation** | Improve docs, README, docstrings, comments |
| 🧪 **Testing** | Add or improve test coverage |
| 🔧 **Bug Fixes** | Fix reported issues |
| 🚀 **New Features** | Implement approved feature requests |
| 🌐 **Translations** | Help translate documentation |
| 👀 **Code Review** | Review pull requests from others |

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed
- **Git** for version control
- **pip** for package management
- A GitHub account
- (Optional) A Linux system with wireless card for testing

### Development Setup

1. **Fork the Repository**
   
   Click the "Fork" button on the [wlfwifi GitHub page](https://github.com/yourusername/wlfwifi) to create your own copy.

2. **Clone Your Fork**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/wlfwifi.git
   cd wlfwifi
   ```

3. **Add Upstream Remote**
   
   ```bash
   git remote add upstream https://github.com/yourusername/wlfwifi.git
   ```

4. **Create Virtual Environment**
   
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   
   # Activate it
   # Linux/macOS:
   source .venv/bin/activate
   # Windows:
   .\.venv\Scripts\Activate.ps1
   ```

5. **Install Development Dependencies**
   
   ```bash
   # Install package in editable mode
   pip install -e .
   
   # Install dev tools
   pip install pytest black flake8 pytest-cov
   ```

6. **Verify Setup**
   
   ```bash
   # Run tests
   pytest -v
   
   # Run linting
   flake8 wlfwifi tests --max-line-length=120
   
   # Check formatting
   black --check wlfwifi tests
   ```

---

## Development Workflow

### Branching Strategy

We use a simplified Git flow:

| Branch | Purpose |
|--------|---------|
| `main` | Stable release branch |
| `develop` | Integration branch for features |
| `feature/*` | New features |
| `bugfix/*` | Bug fixes |
| `docs/*` | Documentation updates |
| `hotfix/*` | Urgent production fixes |

**Creating a Branch:**

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-123-fix-description
```

### Making Changes

1. **Keep Changes Focused**
   - One feature/fix per pull request
   - Small, incremental changes are easier to review

2. **Test Your Changes**
   ```bash
   # Run tests frequently
   pytest -v
   
   # Run specific tests
   pytest tests/test_utils.py -v
   ```

3. **Check Code Quality**
   ```bash
   # Format code
   black wlfwifi tests
   
   # Check for issues
   flake8 wlfwifi tests --max-line-length=120
   ```

### Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style (formatting, no logic change) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |

**Examples:**

```bash
# Feature
git commit -m "feat(attacks): add PMKID capture support"

# Bug fix
git commit -m "fix(utils): handle missing ifconfig gracefully"

# Documentation
git commit -m "docs(readme): add troubleshooting section"

# Tests
git commit -m "test(models): add edge case tests for Target class"
```

**Good Commit Messages:**
- ✅ `fix(config): validate channel range before scanning`
- ✅ `feat(utils): add MAC address validation function`
- ✅ `docs(contributing): add development setup instructions`

**Bad Commit Messages:**
- ❌ `fixed stuff`
- ❌ `updates`
- ❌ `WIP`

---

## Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

| Rule | Standard |
|------|----------|
| **Line Length** | Maximum 120 characters |
| **Indentation** | 4 spaces (no tabs) |
| **Quotes** | Double quotes for strings |
| **Imports** | Sorted, grouped (stdlib, third-party, local) |
| **Formatter** | Black |
| **Linter** | Flake8 |

**Import Order:**

```python
# Standard library
import os
import sys
from typing import Optional, List

# Third-party packages
import pytest
from unittest.mock import Mock, patch

# Local imports
from wlfwifi.models import Target
from wlfwifi.utils import remove_file
```

### Type Hints

All new code must include type hints:

```python
# Good
def get_target_by_bssid(targets: List[Target], bssid: str) -> Optional[Target]:
    """Find a target by its BSSID."""
    for target in targets:
        if target.bssid.upper() == bssid.upper():
            return target
    return None

# Bad (no type hints)
def get_target_by_bssid(targets, bssid):
    for target in targets:
        if target.bssid.upper() == bssid.upper():
            return target
    return None
```

### Documentation

#### Module Docstrings

Every module should have a docstring:

```python
"""
utils.py
--------
Utility functions for file operations, subprocess management,
time formatting, and other helpers used throughout wlfwifi.

Functions:
    rename: Safely renames files, handling cross-partition moves.
    remove_file: Removes a file if it exists.
    program_exists: Checks if a program is installed on the system.
    ...
"""
```

#### Function Docstrings

Use Google-style docstrings:

```python
def capture_handshake(target: Target, timeout: int = 120) -> Optional[CapFile]:
    """
    Capture a WPA/WPA2 handshake from the target network.
    
    Monitors the target network and attempts to capture a 4-way
    handshake by deauthenticating connected clients.
    
    Args:
        target: The Target object representing the network to attack.
        timeout: Maximum time in seconds to wait for handshake.
                 Defaults to 120 seconds.
    
    Returns:
        CapFile object if handshake captured successfully, None otherwise.
    
    Raises:
        ValueError: If target has no connected clients.
        TimeoutError: If no handshake captured within timeout.
    
    Example:
        >>> target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)
        >>> cap = capture_handshake(target, timeout=60)
        >>> if cap:
        ...     print(f"Captured {cap.handshakes} handshakes")
    """
```

#### Class Docstrings

```python
class Target:
    """
    Represents a wireless network target.
    
    This class stores information about a discovered wireless network
    including its identification, channel, encryption type, and WPS status.
    
    Attributes:
        bssid (str): The BSSID (MAC address) of the access point.
        essid (str): The ESSID (network name). May be empty for hidden networks.
        channel (int): The WiFi channel (1-14 for 2.4GHz, higher for 5GHz).
        encryption (str): Encryption type (WEP, WPA, WPA2, OPN).
        wps (bool): Whether WPS is enabled on the access point.
    
    Example:
        >>> target = Target(
        ...     bssid="00:11:22:33:44:55",
        ...     essid="MyNetwork",
        ...     channel=6,
        ...     encryption="WPA2",
        ...     wps=True
        ... )
        >>> print(f"Found {target.essid} on channel {target.channel}")
    """
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific test file
pytest tests/test_models.py

# Run specific test class
pytest tests/test_models.py::TestTarget

# Run specific test method
pytest tests/test_models.py::TestTarget::test_target_initialization

# Run tests matching a pattern
pytest -k "wps"

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l
```

### Writing Tests

**Test File Structure:**

```python
"""
test_example.py
---------------
Tests for the example module.
"""

from wlfwifi.example import some_function, SomeClass


class TestSomeFunction:
    """Tests for some_function."""
    
    def test_some_function_basic(self):
        """Test basic functionality."""
        result = some_function("input")
        assert result == "expected"
    
    def test_some_function_edge_case(self):
        """Test edge case with empty input."""
        result = some_function("")
        assert result is None
    
    def test_some_function_error(self):
        """Test that invalid input raises ValueError."""
        with pytest.raises(ValueError):
            some_function(None)


class TestSomeClass:
    """Tests for SomeClass."""
    
    def test_initialization(self):
        """Test class initialization."""
        obj = SomeClass(param="value")
        assert obj.param == "value"
```

**Test Naming Conventions:**

| Pattern | Example |
|---------|---------|
| Test file | `test_<module>.py` |
| Test class | `Test<ClassName>` |
| Test method | `test_<method>_<scenario>` |

**Mocking External Dependencies:**

```python
from unittest.mock import Mock, patch

class TestProgramExists:
    @patch("wlfwifi.utils.Popen")
    def test_program_exists_found(self, mock_popen):
        """Test when program is found."""
        mock_proc = Mock()
        mock_proc.communicate.return_value = (b"/usr/bin/python", b"")
        mock_popen.return_value = mock_proc
        
        result = utils.program_exists("python")
        
        assert result is True
```

### Test Coverage

We aim for >80% test coverage:

```bash
# Run with coverage
pytest --cov=wlfwifi --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Pull Request Process

1. **Ensure All Checks Pass**
   ```bash
   pytest -v
   flake8 wlfwifi tests --max-line-length=120
   black --check wlfwifi tests
   ```

2. **Update Documentation**
   - Update README if adding features
   - Add/update docstrings
   - Update CHANGELOG.md

3. **Create Pull Request**
   - Use a descriptive title
   - Reference related issues (`Fixes #123`)
   - Describe what changed and why
   - Include testing instructions

4. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes.
   
   ## Related Issue
   Fixes #123
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation
   - [ ] Refactoring
   
   ## Testing
   Describe how you tested your changes.
   
   ## Checklist
   - [ ] Tests pass locally
   - [ ] Linting passes
   - [ ] Documentation updated
   - [ ] Changelog updated
   ```

5. **Code Review**
   - Respond to feedback promptly
   - Make requested changes
   - Keep discussion constructive

---

## Issue Guidelines

### Bug Reports

Include:
- Python version (`python --version`)
- Operating system
- Wireless card model (if relevant)
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

**Template:**
```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
1. Run `python3 wlfwifi.py -i wlan0`
2. Select target...
3. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: Kali Linux 2024.1
- Python: 3.11.2
- Wireless Card: Alfa AWUS036ACH

**Logs**
```
Paste error output here
```
```

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)
- Alternatives considered

---

## Project Architecture

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

**Quick Overview:**

```
wlfwifi/
├── config.py    # CLI parsing, RunConfig
├── core.py      # Main engine, workflow
├── models.py    # Data classes (Target, Client, CapFile)
├── attacks.py   # Attack implementations
└── utils.py     # Helper functions
```

**Key Classes:**
- `RunConfig`: Runtime configuration from CLI args
- `Target`: Represents a wireless network
- `Attack`: Abstract base class for attacks

---

## License

By contributing to wlfwifi, you agree that your contributions will be licensed under the **GNU General Public License v2.0** (GPL-2.0).

---

## Questions?

- Check existing [issues](https://github.com/yourusername/wlfwifi/issues)
- Open a new issue with the `question` label
- Join our discussions

---

Thank you for contributing to wlfwifi! 🎉
