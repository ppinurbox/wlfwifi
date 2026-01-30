"""
wlfwifi - Automated Wireless Network Security Auditor
======================================================

wlfwifi is a modern, modular Python tool for automated wireless network
security testing. It supports WEP, WPA/WPA2, and WPS attack vectors.

Package Structure
-----------------
- config: CLI argument parsing and runtime configuration
- core: Main engine and workflow orchestration
- models: Data classes (Target, Client, CapFile)
- attacks: Attack implementations and WPS checking
- utils: Utility functions for file ops, MAC handling, etc.

Quick Start
-----------
    from wlfwifi.core import main
    main()

Or run from command line:
    python -m wlfwifi -i wlan0

Modules
-------
config
    Configuration management and CLI argument parsing.
    
    Classes:
        RunConfig - Stores runtime configuration
    
    Functions:
        parse_args() - Parse CLI arguments into RunConfig

core
    Core engine logic and main entry point.
    
    Functions:
        main() - Entry point for wlfwifi

models
    Data models for wireless targets and captures.
    
    Classes:
        Target - Represents a wireless network
        Client - Represents a connected client device
        CapFile - Represents a capture file

attacks
    Attack logic for WEP, WPA, and WPS.
    
    Classes:
        Attack - Abstract base class for attacks
    
    Functions:
        wps_check_targets() - Check targets for WPS support

utils
    Utility functions used throughout wlfwifi.
    
    Functions:
        rename() - Safe file rename across partitions
        remove_file() - Remove file if exists
        program_exists() - Check if program is installed
        sec_to_hms() - Convert seconds to h:mm:ss
        generate_random_mac() - Generate random MAC address
        ... and more

License
-------
GNU General Public License v2.0 (GPL-2.0)

Copyright
---------
(C) 2011 Derv Merkler (original author)
Modernization: Mike and contributors

See Also
--------
- README.md: Project overview and features
- INSTALLATION.md: Detailed installation guide
- USAGE.md: Usage examples and workflows
- ARCHITECTURE.md: Technical architecture
- CONTRIBUTING.md: Contribution guidelines
"""

__version__ = "1.0.0"
__author__ = "derv82, ballastsec, Mike, and contributors"
__license__ = "GPL-2.0"

# Expose main entry point
from wlfwifi.core import main

# Expose key classes for convenient imports
from wlfwifi.models import Target, Client, CapFile
from wlfwifi.config import RunConfig, parse_args
from wlfwifi.attacks import Attack, wps_check_targets

__all__ = [
    "main",
    "Target",
    "Client", 
    "CapFile",
    "RunConfig",
    "parse_args",
    "Attack",
    "wps_check_targets",
    "__version__",
    "__author__",
    "__license__",
]
