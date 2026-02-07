"""
attacks.py
----------
Implements attack logic for WEP, WPA, and WPS, including attack classes and helper functions.

Functions and Classes:
    wps_check_targets: Checks if targets support WPS using tshark.
    Attack: Abstract base class for attacks.
    WPAAttack, WEPAttack, WPSAttack: Concrete attack implementations.
    wpa_crack: Attempts to crack WPA handshakes.
"""

import os
import re
import abc
import logging
from typing import List, Any
from subprocess import Popen, PIPE
from wlfwifi.utils import program_exists
from wlfwifi.models import Target


def wps_check_targets(
    targets: List[Target], cap_file: str, verbose: bool = True
) -> None:
    try:
        if not program_exists("tshark"):
            return
        if len(targets) == 0 or not os.path.exists(cap_file):
            if verbose:
                logging.warning(
                    "[wps_check_targets] No targets or cap file does not exist."
                )
            return
        if verbose:
            logging.info(" [+] checking for WPS compatibility...")
        cmd = [
            "tshark",
            "-r",
            cap_file,
            "-n",
            "-Y",
            "wps.wifi_protected_setup_state && wlan.da == ff:ff:ff:ff:ff:ff",
            "-T",
            "fields",
            "-e",
            "wlan.ta",
            "-e",
            "wps.ap_setup_locked",
            "-E",
            "separator=,",
        ]
        proc_tshark = Popen(cmd, stdout=PIPE, stderr=PIPE)
        proc_tshark.wait()
        tshark_stdout, _ = proc_tshark.communicate()
        bssid_regex = re.compile(r"([A-F0-9\:]{17})", re.IGNORECASE)
        bssids = [
            bssid.upper()
            for bssid in bssid_regex.findall(tshark_stdout.decode(errors="ignore"))
        ]
        for t in targets:
            t.wps = t.bssid.upper() in bssids
        if verbose:
            logging.info("done")
    except Exception as e:
        logging.error(f"[wps_check_targets] Error: {e}")


class Attack(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def RunAttack(self) -> Any:
        """Run the attack. Must be implemented by subclasses."""
        raise NotImplementedError("RunAttack() must be implemented by subclasses.")

    @abc.abstractmethod
    def EndAttack(self) -> Any:
        """End the attack. Must be implemented by subclasses."""
        raise NotImplementedError("EndAttack() must be implemented by subclasses.")

