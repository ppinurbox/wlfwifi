#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wlfwifi.__main__
----------------
Package entry point for running wlfwifi as a module.

This module enables the following invocation:

    python -m wlfwifi [options]

Which is equivalent to:

    python wlfwifi.py [options]

Example Usage:
    # Run with interface specification
    python -m wlfwifi -i wlan0

    # Run with verbose mode
    python -m wlfwifi -i wlan0 -v

    # Run with channel lock
    python -m wlfwifi -i wlan0 -c 6 -v

For help:
    python -m wlfwifi --help

See Also:
    wlfwifi.core.main: The main entry point function
    wlfwifi.config.parse_args: CLI argument parsing
"""

from .core import main

if __name__ == "__main__":
    main()
