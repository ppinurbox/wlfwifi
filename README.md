# wlfwifi

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/gpl-2.0)
[![Tests](https://img.shields.io/badge/tests-170%20passed-brightgreen.svg)](#testing)

**wlfwifi** is a modern, modular, and automated wireless network security auditing tool for Linux systems. It automates the process of scanning, capturing handshakes, and testing the security of WEP, WPA/WPA2, and WPS-protected Wi-Fi networks.

> ⚠️ **Legal Disclaimer**: This tool is intended for authorized security testing and educational purposes only. Unauthorized access to computer networks is illegal. Always obtain proper authorization before testing any network you do not own.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
  - [System Requirements](#system-requirements)
  - [Required External Tools](#required-external-tools)
  - [Optional Tools](#optional-tools)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [Development Install](#development-install)
  - [Installing External Tools](#installing-external-tools)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Command Line Options](#command-line-options)
  - [Examples](#examples)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Testing](#testing)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Authors & Acknowledgments](#authors--acknowledgments)

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **Automated Scanning** | Automatically discovers and lists nearby wireless networks |
| 🎯 **Target Selection** | Intelligent target selection based on signal strength and encryption |
| 🔓 **Multi-Protocol Support** | Attacks WEP, WPA/WPA2, and WPS-enabled networks |
| 🤝 **Handshake Capture** | Automated WPA handshake capture for offline cracking |
| 📡 **WPS PIN Attack** | Brute-force WPS PIN for vulnerable access points |
| 🎭 **MAC Anonymization** | Optional MAC address randomization for privacy |
| 📊 **Verbose Logging** | Detailed logging for debugging and analysis |
| 🐍 **Modern Python 3** | Clean, typed, modular Python 3.7+ codebase |
| ✅ **Fully Tested** | 170+ unit and integration tests |

---

## Requirements

### System Requirements

| Requirement | Details |
|-------------|---------|
| **Operating System** | Linux (Kali Linux, Parrot OS, Ubuntu, Debian recommended) |
| **Python Version** | Python 3.7 or higher |
| **Wireless Card** | Must support **monitor mode** and **packet injection** |
| **Privileges** | Root/sudo access required for wireless operations |

### Required External Tools

wlfwifi relies on several external tools that must be installed on your system:

| Tool | Purpose | Package Name (Debian/Ubuntu) |
|------|---------|------------------------------|
| `aircrack-ng` | WPA/WEP cracking suite | `aircrack-ng` |
| `airodump-ng` | Wireless network scanner | (part of aircrack-ng) |
| `aireplay-ng` | Packet injection tool | (part of aircrack-ng) |
| `airmon-ng` | Monitor mode control | (part of aircrack-ng) |
| `tshark` | Packet analysis (WPS detection) | `tshark` |
| `reaver` | WPS PIN brute-force | `reaver` |

### Optional Tools

| Tool | Purpose | Package Name (Debian/Ubuntu) |
|------|---------|------------------------------|
| `pyrit` | GPU-accelerated WPA cracking | `pyrit` |
| `cowpatty` | WPA dictionary attack | `cowpatty` |
| `macchanger` | MAC address spoofing | `macchanger` |
| `hashcat` | Advanced password cracking | `hashcat` |

---

## Installation

### Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# 2. (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS

# 3. Install wlfwifi
pip install -e .

# 4. Verify installation
wlfwifi --help
```

### Development Install

For contributors and developers who want to run tests and linting:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install with development dependencies
pip install -e .
pip install pytest black flake8

# 4. Run tests to verify
pytest -v

# 5. Run linting
flake8 wlfwifi tests --max-line-length=120
black --check wlfwifi tests
```

### Installing External Tools

#### Debian/Ubuntu/Kali Linux

```bash
# Update package lists
sudo apt update

# Install required tools
sudo apt install -y aircrack-ng tshark reaver

# Install optional tools
sudo apt install -y macchanger cowpatty pyrit hashcat
```

#### Arch Linux

```bash
sudo pacman -S aircrack-ng wireshark-cli reaver
```

#### From Source (aircrack-ng)

```bash
git clone https://github.com/aircrack-ng/aircrack-ng.git
cd aircrack-ng
autoreconf -i
./configure
make
sudo make install
```

---

## Usage

### Basic Usage

```bash
# Run with a specific wireless interface
sudo python3 wlfwifi.py -i wlan0

# Or if installed via pip
sudo wlfwifi -i wlan0
```

### Command Line Options

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-i` | `--interface` | Specify the wireless interface to use (e.g., `wlan0`, `wlan0mon`) |
| `-c` | `--channel` | Lock to a specific channel (1-14 for 2.4GHz, higher for 5GHz) |
| `-v` | `--verbose` | Enable verbose output for detailed logging |
| `-h` | `--help` | Display help message and exit |

### Examples

#### Example 1: Basic Scan on Interface wlan0

```bash
sudo python3 wlfwifi.py -i wlan0
```

This will:
1. Put `wlan0` into monitor mode
2. Scan for nearby wireless networks
3. Display discovered targets with encryption type, signal strength, and WPS status

#### Example 2: Target a Specific Channel

```bash
sudo python3 wlfwifi.py -i wlan0 -c 6
```

Useful when you already know the target network's channel. Reduces scan time and interference.

#### Example 3: Verbose Mode for Debugging

```bash
sudo python3 wlfwifi.py -i wlan0 -v
```

Outputs detailed information about:
- Commands being executed
- Process status
- Error messages
- Timing information

#### Example 4: Running as a Module

```bash
sudo python3 -m wlfwifi -i wlan0
```

---

## Project Structure

```
wlfwifi/
├── wlfwifi.py              # Main entry point script
├── wlfwifi/                # Core package directory
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Enables `python -m wlfwifi`
│   ├── config.py           # CLI argument parsing & configuration
│   ├── core.py             # Main engine and workflow coordination
│   ├── models.py           # Data models (Target, Client, CapFile)
│   ├── attacks.py          # Attack implementations (WEP, WPA, WPS)
│   └── utils.py            # Utility functions (file ops, MAC handling)
├── tests/                  # Test suite (170+ tests)
│   ├── test_models.py      # Tests for data models
│   ├── test_config.py      # Tests for configuration
│   ├── test_utils.py       # Tests for utilities
│   ├── test_attacks.py     # Tests for attack logic
│   ├── test_core.py        # Tests for core engine
│   └── test_integration.py # End-to-end integration tests
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── README.md               # This file
├── INSTALLATION.md         # Detailed installation guide
├── USAGE.md                # Detailed usage examples
├── ARCHITECTURE.md         # Developer architecture guide
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
├── CODE_OF_CONDUCT.md      # Community guidelines
├── LICENSE                 # GPL v2 license
├── setup.py                # Package installation script
├── pyproject.toml          # Modern Python packaging config
├── pytest.ini              # Pytest configuration
└── MANIFEST.in             # Package distribution manifest
```

---

## How It Works

### Workflow Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Parse Args    │────▶│  Enable Monitor │────▶│   Scan Networks │
│   (config.py)   │     │   Mode          │     │   (airodump-ng) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Crack/Analyze  │◀────│  Execute Attack │◀────│  Select Target  │
│  (aircrack-ng)  │     │  (attacks.py)   │     │  (user choice)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Core Components

1. **Configuration (`config.py`)**: Parses command-line arguments and creates a `RunConfig` object containing all runtime settings.

2. **Core Engine (`core.py`)**: Orchestrates the entire workflow - initializing the interface, running scans, managing attacks, and handling cleanup.

3. **Models (`models.py`)**: Data classes representing:
   - `Target`: A wireless network (BSSID, ESSID, channel, encryption, WPS status)
   - `Client`: A connected client device
   - `CapFile`: A capture file with handshake data

4. **Attacks (`attacks.py`)**: Attack implementations using an abstract `Attack` base class:
   - WPA/WPA2 handshake capture
   - WEP IV collection and cracking
   - WPS PIN brute-force

5. **Utilities (`utils.py`)**: Helper functions for:
   - File operations (rename, remove, cleanup)
   - MAC address handling (get, randomize, restore)
   - Process management (send signals, execute commands)
   - Time formatting

---

## Testing

wlfwifi includes a comprehensive test suite with **170 tests** covering all modules.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_models.py

# Run with coverage report
pytest --cov=wlfwifi --cov-report=html
```

### Test Categories

| Category | File | Tests | Description |
|----------|------|-------|-------------|
| Models | `test_models.py` | 22 | Target, Client, CapFile classes |
| Config | `test_config.py` | 32 | Argument parsing, validation |
| Utils | `test_utils.py` | 55 | Utility functions |
| Attacks | `test_attacks.py` | 21 | Attack logic, WPS checking |
| Core | `test_core.py` | 21 | Main function, logging |
| Integration | `test_integration.py` | 19 | End-to-end workflows |

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to submit issues and bug reports
- How to propose new features
- Code style guidelines
- Pull request process
- Development setup

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/wlfwifi.git
cd wlfwifi

# Create branch
git checkout -b feature/your-feature-name

# Make changes, then test
pytest -v
flake8 wlfwifi tests --max-line-length=120

# Commit and push
git add .
git commit -m "Add: description of your changes"
git push origin feature/your-feature-name

# Open a Pull Request on GitHub
```

---

## Troubleshooting

### Common Issues

#### "Interface not found"

```
Error: Interface 'wlan0' not found
```

**Solution**: Check available interfaces with `ip link show` or `iwconfig`. Your wireless interface might have a different name (e.g., `wlp2s0`).

#### "Permission denied"

```
Error: Operation not permitted
```

**Solution**: Run with `sudo`:
```bash
sudo python3 wlfwifi.py -i wlan0
```

#### "Monitor mode not supported"

```
Error: Failed to enable monitor mode
```

**Solution**: 
1. Ensure your wireless card supports monitor mode
2. Check with: `iw list | grep -A 10 "Supported interface modes"`
3. Consider using a compatible USB wireless adapter (e.g., Alfa AWUS036ACH)

#### "aircrack-ng not found"

```
Error: Required program 'aircrack-ng' not found
```

**Solution**: Install aircrack-ng:
```bash
sudo apt install aircrack-ng
```

#### "No networks found"

**Possible causes**:
1. Interface not in monitor mode
2. No networks in range
3. Wrong channel specified
4. Interference from NetworkManager

**Solution**:
```bash
# Stop NetworkManager (temporarily)
sudo systemctl stop NetworkManager

# Kill interfering processes
sudo airmon-ng check kill

# Try again
sudo python3 wlfwifi.py -i wlan0
```

### Getting Help

1. Check existing [GitHub Issues](https://github.com/yourusername/wlfwifi/issues)
2. Run with `-v` (verbose) for detailed output
3. Check the [USAGE.md](USAGE.md) for examples
4. Open a new issue with:
   - Your OS and Python version
   - Wireless card model
   - Full error output
   - Steps to reproduce

---

## License

This project is licensed under the **GNU General Public License v2.0** (GPL-2.0).

See [LICENSE](LICENSE) for the full license text.

---

## Authors & Acknowledgments

### Original Authors
- **derv82** - Original wlfwifi creator
- **ballastsec** - Ballast Security additions and maintenance

### Modernization Team
- **Mike** - Python 3 migration, modularization, testing framework

### Contributors
Thank you to all contributors who have helped improve wlfwifi!

### Acknowledgments
- The [aircrack-ng](https://www.aircrack-ng.org/) team for the amazing wireless security suite
- The Python community for excellent tooling
- All security researchers who responsibly disclose vulnerabilities

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

<p align="center">
  Made with ❤️ for the security research community
</p>
