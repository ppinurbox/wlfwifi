# Installation Guide

This comprehensive guide covers all installation methods for wlfwifi, from quick installation to advanced setup for development and specific Linux distributions.

---

## Table of Contents

- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
  - [Method 1: Direct Run (No Installation)](#method-1-direct-run-no-installation)
  - [Method 2: Pip Install (Recommended)](#method-2-pip-install-recommended)
  - [Method 3: Development Install](#method-3-development-install)
  - [Method 4: System-Wide Install](#method-4-system-wide-install)
- [Installing Dependencies](#installing-dependencies)
  - [Python Dependencies](#python-dependencies)
  - [External Tools](#external-tools)
- [Distribution-Specific Instructions](#distribution-specific-instructions)
  - [Kali Linux](#kali-linux)
  - [Ubuntu / Debian](#ubuntu--debian)
  - [Arch Linux / Manjaro](#arch-linux--manjaro)
  - [Fedora / RHEL / CentOS](#fedora--rhel--centos)
  - [Parrot OS](#parrot-os)
- [Wireless Card Setup](#wireless-card-setup)
- [Verifying Installation](#verifying-installation)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Troubleshooting Installation](#troubleshooting-installation)
- [Uninstallation](#uninstallation)

---

## Quick Start

For experienced users on Kali Linux:

```bash
# Clone and run
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi
sudo python3 wlfwifi.py -i wlan0
```

For detailed instructions, continue reading below.

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Linux (kernel 4.0+) |
| **Python** | Python 3.7 or higher |
| **RAM** | 512 MB minimum, 2 GB recommended |
| **Storage** | 100 MB for wlfwifi + captures |
| **Privileges** | Root access required |

### Wireless Requirements

| Requirement | Details |
|-------------|---------|
| **Wireless Card** | Must support monitor mode |
| **Packet Injection** | Required for deauth attacks |
| **Recommended Cards** | Alfa AWUS036ACH, AWUS036NHA, AWUS1900 |

### Checking Your Python Version

```bash
python3 --version
# Should output: Python 3.7.x or higher
```

If your Python version is too old:

```bash
# Ubuntu/Debian
sudo apt install python3.10

# Fedora
sudo dnf install python3.10

# Use pyenv for more control
curl https://pyenv.run | bash
pyenv install 3.11.0
pyenv global 3.11.0
```

---

## Installation Methods

### Method 1: Direct Run (No Installation)

The simplest method - just clone and run:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/wlfwifi.git

# 2. Navigate to directory
cd wlfwifi

# 3. Run directly
sudo python3 wlfwifi.py --help
```

**Pros:**
- No installation needed
- Easy to update (just `git pull`)
- No system modifications

**Cons:**
- Must run from the wlfwifi directory
- No `wlfwifi` command available globally

---

### Method 2: Pip Install (Recommended)

Install as a Python package for system-wide access:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# 2. Install with pip
sudo pip3 install .

# 3. Run from anywhere
sudo wlfwifi --help
```

**Pros:**
- `wlfwifi` command available globally
- Proper Python package installation
- Easy dependency management

**Cons:**
- Requires reinstallation after updates

**Updating:**

```bash
cd wlfwifi
git pull
sudo pip3 install . --upgrade
```

---

### Method 3: Development Install

For contributors and developers:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in editable mode with dev dependencies
pip install -e .
pip install pytest black flake8 pytest-cov

# 4. Verify installation
pytest -v  # Should show 170 tests passing
```

**Pros:**
- Changes to code take effect immediately
- Isolated environment
- Full development toolchain

**Cons:**
- Must activate virtual environment each time
- Requires sudo for actual wireless operations

---

### Method 4: System-Wide Install

For permanent system installation:

```bash
# 1. Clone to /opt
sudo git clone https://github.com/yourusername/wlfwifi.git /opt/wlfwifi

# 2. Install system-wide
cd /opt/wlfwifi
sudo pip3 install .

# 3. Create symlink (optional, for direct script access)
sudo ln -s /opt/wlfwifi/wlfwifi.py /usr/local/bin/wlfwifi

# 4. Test
wlfwifi --help
```

---

## Installing Dependencies

### Python Dependencies

wlfwifi has minimal Python dependencies. The core package runs with standard library only.

For development:

```bash
pip install pytest       # Testing framework
pip install black        # Code formatter
pip install flake8       # Linter
pip install pytest-cov   # Coverage reporting
```

### External Tools

wlfwifi requires several external tools for wireless operations.

#### Quick Install (Debian/Ubuntu/Kali)

```bash
# Required tools
sudo apt update
sudo apt install -y \
    aircrack-ng \
    tshark \
    reaver

# Optional but recommended
sudo apt install -y \
    macchanger \
    cowpatty \
    hashcat \
    pixiewps
```

#### Detailed Tool Information

| Tool | Version | Purpose | Required |
|------|---------|---------|----------|
| `aircrack-ng` | 1.6+ | WEP/WPA cracking suite | ✅ Yes |
| `airodump-ng` | (part of aircrack-ng) | Network scanning | ✅ Yes |
| `aireplay-ng` | (part of aircrack-ng) | Packet injection | ✅ Yes |
| `airmon-ng` | (part of aircrack-ng) | Monitor mode | ✅ Yes |
| `tshark` | 3.0+ | Packet analysis | ✅ Yes |
| `reaver` | 1.6.5+ | WPS attacks | ⚠️ For WPS |
| `bully` | 1.1+ | Alternative WPS | Optional |
| `macchanger` | 1.7+ | MAC spoofing | Optional |
| `cowpatty` | 4.6+ | WPA dictionary | Optional |
| `pyrit` | 0.5+ | GPU acceleration | Optional |
| `hashcat` | 6.0+ | Advanced cracking | Optional |
| `pixiewps` | 1.4+ | Pixie Dust attack | Optional |
| `hcxdumptool` | 6.0+ | PMKID capture | Optional |

---

## Distribution-Specific Instructions

### Kali Linux

Kali Linux comes with most tools pre-installed:

```bash
# Update and install any missing tools
sudo apt update
sudo apt full-upgrade -y

# Clone wlfwifi
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# Install
sudo pip3 install .

# Verify
wlfwifi --help
```

### Ubuntu / Debian

```bash
# 1. Add universe repository (Ubuntu only)
sudo add-apt-repository universe

# 2. Update package lists
sudo apt update

# 3. Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# 4. Install wireless tools
sudo apt install -y \
    aircrack-ng \
    tshark \
    reaver \
    macchanger

# 5. Install wlfwifi
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi
sudo pip3 install .
```

### Arch Linux / Manjaro

```bash
# 1. Update system
sudo pacman -Syu

# 2. Install dependencies
sudo pacman -S \
    python \
    python-pip \
    aircrack-ng \
    wireshark-cli \
    reaver \
    macchanger

# 3. Install from AUR (alternative)
yay -S reaver-wps-fork-t6x

# 4. Install wlfwifi
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi
sudo pip install .
```

### Fedora / RHEL / CentOS

```bash
# 1. Enable RPM Fusion (for extra packages)
sudo dnf install \
    https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

# 2. Install dependencies
sudo dnf install -y \
    python3 \
    python3-pip \
    aircrack-ng \
    wireshark-cli

# 3. Reaver (may need to compile from source)
git clone https://github.com/t6x/reaver-wps-fork-t6x.git
cd reaver-wps-fork-t6x/src
./configure
make
sudo make install

# 4. Install wlfwifi
cd ~
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi
sudo pip3 install .
```

### Parrot OS

Parrot OS (like Kali) includes most tools:

```bash
# Update
sudo apt update

# Install any missing
sudo apt install -y aircrack-ng reaver tshark

# Clone and install
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi
sudo pip3 install .
```

---

## Wireless Card Setup

### Checking Your Wireless Card

```bash
# List wireless interfaces
iwconfig

# Check if monitor mode is supported
iw list | grep -A 10 "Supported interface modes"
# Look for "monitor" in the output
```

### Enabling Monitor Mode Manually

```bash
# Method 1: Using airmon-ng (recommended)
sudo airmon-ng check kill  # Kill interfering processes
sudo airmon-ng start wlan0

# Method 2: Using iw
sudo ip link set wlan0 down
sudo iw wlan0 set monitor control
sudo ip link set wlan0 up

# Method 3: Using iwconfig
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
```

### Recommended Wireless Adapters

| Adapter | Chipset | Monitor Mode | Packet Injection | Price Range |
|---------|---------|--------------|------------------|-------------|
| Alfa AWUS036ACH | RTL8812AU | ✅ | ✅ | $50-60 |
| Alfa AWUS036NHA | Atheros AR9271 | ✅ | ✅ | $30-40 |
| Alfa AWUS1900 | RTL8814AU | ✅ | ✅ | $70-80 |
| Panda PAU09 | Ralink RT5572 | ✅ | ✅ | $20-30 |
| TP-Link TL-WN722N v1 | Atheros AR9271 | ✅ | ✅ | $15-20 |

> ⚠️ **Note**: TP-Link TL-WN722N v2 and v3 use different chipsets and may not support monitor mode without driver modifications.

---

## Verifying Installation

### Step 1: Check Python Installation

```bash
python3 --version
# Expected: Python 3.7.0 or higher
```

### Step 2: Check wlfwifi

```bash
# If installed via pip:
wlfwifi --help

# If running directly:
python3 wlfwifi.py --help
```

Expected output:
```
usage: wlfwifi [-h] [-i INTERFACE] [-c CHANNEL] [-v]

wlfwifi: Automated wireless auditor

options:
  -h, --help            show this help message and exit
  -i, --interface       Wireless interface to use
  -c, --channel         Channel to scan/attack
  -v, --verbose         Enable verbose output
```

### Step 3: Check External Tools

```bash
# Check all required tools
for tool in aircrack-ng airodump-ng aireplay-ng airmon-ng tshark reaver; do
    which $tool && echo "$tool: OK" || echo "$tool: NOT FOUND"
done
```

### Step 4: Run Tests (Development Install)

```bash
cd wlfwifi
source .venv/bin/activate  # If using virtual environment
pytest -v
# Should show: 170 passed
```

---

## Virtual Environment Setup

Using a virtual environment is recommended for development:

### Creating a Virtual Environment

```bash
# Navigate to wlfwifi directory
cd wlfwifi

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/macOS
# or
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Your prompt should now show (.venv)
```

### Installing in Virtual Environment

```bash
# With virtual environment activated:
pip install -e .  # Editable install
pip install pytest black flake8  # Dev tools
```

### Deactivating

```bash
deactivate
```

### Note on Sudo with Virtual Environments

When running wlfwifi with sudo, the virtual environment's Python might not be used. Options:

```bash
# Option 1: Use the venv's Python explicitly
sudo .venv/bin/python wlfwifi.py -i wlan0

# Option 2: Install system-wide for running
sudo pip3 install .
sudo wlfwifi -i wlan0
```

---

## Troubleshooting Installation

### "pip: command not found"

```bash
# Install pip
sudo apt install python3-pip  # Debian/Ubuntu
sudo dnf install python3-pip  # Fedora
sudo pacman -S python-pip     # Arch
```

### "externally-managed-environment" Error

On newer Debian/Ubuntu systems:

```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install .

# Option 2: Use pipx
sudo apt install pipx
pipx install .

# Option 3: Override (not recommended)
pip install . --break-system-packages
```

### "ModuleNotFoundError: No module named 'wlfwifi'"

```bash
# Ensure you're in the right directory
cd /path/to/wlfwifi

# Reinstall
pip install -e .
```

### Permission Denied Errors

```bash
# Install for current user only
pip install --user .

# Or use sudo
sudo pip install .
```

### Git Clone Errors

```bash
# If git isn't installed
sudo apt install git

# If HTTPS doesn't work, try SSH
git clone git@github.com:yourusername/wlfwifi.git

# Or download ZIP
wget https://github.com/yourusername/wlfwifi/archive/refs/heads/main.zip
unzip main.zip
cd wlfwifi-main
```

---

## Uninstallation

### Remove Pip Installation

```bash
sudo pip3 uninstall wlfwifi
```

### Remove Cloned Repository

```bash
rm -rf /path/to/wlfwifi
```

### Remove Virtual Environment

```bash
rm -rf /path/to/wlfwifi/.venv
```

### Remove System-Wide Installation

```bash
# Remove package
sudo pip3 uninstall wlfwifi

# Remove from /opt (if installed there)
sudo rm -rf /opt/wlfwifi

# Remove symlink (if created)
sudo rm /usr/local/bin/wlfwifi
```

---

## Next Steps

After installation:

1. Read the [Usage Guide](USAGE.md) for detailed examples
2. Check [README.md](README.md) for feature overview
3. See [ARCHITECTURE.md](ARCHITECTURE.md) for code structure
4. Review [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute

---

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting-installation) section above
2. Search existing [GitHub Issues](https://github.com/yourusername/wlfwifi/issues)
3. Open a new issue with:
   - Your OS and version
   - Python version
   - Full error message
   - Steps you've tried
