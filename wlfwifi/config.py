"""
config.py
---------
Handles configuration, argument parsing, and runtime settings for wlfwifi.

Functions and Classes:
        parse_args: Parses command-line arguments and returns configuration.
        RunConfig: Stores runtime configuration and global state.
"""

import argparse
import logging
from typing import Optional


class RunConfig:
    """
    Stores runtime configuration and global state for wlfwifi.
    """

    interface: Optional[str]
    channel: Optional[int]
    verbose: bool

    def __init__(
        self,
        interface: Optional[str] = None,
        channel: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        if interface is not None and not isinstance(interface, str):
            logging.error("interface must be a string or None")
            raise ValueError("interface must be a string or None")
        if channel is not None and not isinstance(channel, int):
            logging.error("channel must be an integer or None")
            raise ValueError("channel must be an integer or None")
        self.interface = interface
        self.channel = channel
        self.verbose = verbose


def parse_args() -> RunConfig:
    """
    Parses command-line arguments and returns a RunConfig object.
    Returns:
            RunConfig: The runtime configuration object.
    """
    parser = argparse.ArgumentParser(description="wlfwifi: Automated wireless auditor")
    parser.add_argument("-i", "--interface", type=str, help="Wireless interface to use")
    parser.add_argument("-c", "--channel", type=int, help="Channel to scan/attack")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    try:
        args = parser.parse_args()
        return RunConfig(
            interface=args.interface, channel=args.channel, verbose=args.verbose
        )
    except Exception as e:
        logging.error(f"[parse_args] Error parsing arguments: {e}")
        parser.print_help()
        exit(1)


# Example function docstring template:
# def parse_args():
#     """
#     Parses command-line arguments and returns a configuration object.
#
#     Returns:
#         RunConfig: The runtime configuration object.
#     """
