"""
utils.py
--------
Utility functions for file operations, subprocess management,
time formatting, and other helpers used throughout wlfwifi.

Functions:
    rename: Safely renames files, handling cross-partition moves.
    remove_file: Removes a file if it exists.
    program_exists: Checks if a program is installed on the system.
    sec_to_hms: Converts seconds to h:mm:ss format.
    send_interrupt: Sends an interrupt signal to a process.
    ...
"""

import os
import errno
import random
import time
import logging
from typing import Any
from shutil import copy
from subprocess import Popen, PIPE
from signal import SIGINT


def rename(old: str, new: str) -> None:
    """
    Renames file 'old' to 'new', works with separate partitions.
    """
    try:
        os.rename(old, new)
    except OSError as detail:
        if detail.errno == errno.EXDEV:
            try:
                copy(old, new)
            except Exception as e:
                try:
                    os.unlink(new)
                except Exception:
                    pass
                logging.error(f"[rename] Failed to copy {old} to {new}: {e}")
                raise
            try:
                os.unlink(old)
            except Exception as e:
                logging.warning(f"[rename] Failed to remove original file {old}: {e}")
        else:
            logging.error(f"[rename] Failed to rename {old} to {new}: {detail}")
            raise


def remove_file(filename: str) -> None:
    """
    Attempts to remove a file. Does not throw error if file is not found.
    """
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except Exception as e:
        logging.warning(f"[remove_file] Failed to remove {filename}: {e}")


def program_exists(program: str) -> bool:
    """
    Checks if a program is installed and available in the system PATH.
    """
    try:
        proc = Popen(["which", program], stdout=PIPE, stderr=PIPE)
        txt = proc.communicate()
        if txt[0].strip() == b"" and txt[1].strip() == b"":
            return False
        if txt[0].strip() != b"" and txt[1].strip() == b"":
            return True
        return not (txt[1].strip() == b"" or b"no %s in" % program.encode() in txt[1])
    except Exception as e:
        logging.error(f"[program_exists] Error checking for program '{program}': {e}")
        return False


def sec_to_hms(sec: int) -> str:
    """
    Converts integer sec to h:mm:ss format
    """
    if sec <= -1:
        return "[endless]"
    h = int(sec / 3600)
    sec %= 3600
    m = int(sec / 60)
    sec %= 60
    return "[%d:%02d:%02d]" % (h, m, sec)


def send_interrupt(process: Any) -> None:
    """
    Sends interrupt signal to process's PID.
    """
    try:
        os.kill(process.pid, SIGINT)
    except (OSError, TypeError, UnboundLocalError, AttributeError) as e:
        logging.warning(f"[send_interrupt] Failed to send interrupt: {e}")


def get_mac_address(iface: str) -> str:
    """
    Returns MAC address of "iface".
    """
    try:
        proc = Popen(["ifconfig", iface], stdout=PIPE, stderr=PIPE)
        proc.wait()
        mac = ""
        output = proc.communicate()[0].decode(errors="ignore")
        mac_regex = ("[a-zA-Z0-9]{2}-" * 6)[:-1]
        import re

        match = re.search(" (%s)" % mac_regex, output)
        if match:
            mac = match.groups()[0].replace("-", ":")
        return mac
    except Exception as e:
        logging.error(f"[get_mac_address] Failed to get MAC for {iface}: {e}")
        return ""


def generate_random_mac(old_mac: str) -> str:
    """
    Generates a random MAC address preserving the vendor prefix (first 3 octets).
    """
    random.seed()
    new_mac = old_mac[:8].lower().replace("-", ":")
    for i in range(0, 6):
        if i % 2 == 0:
            new_mac += ":"
        new_mac += "0123456789abcdef"[random.randint(0, 15)]
    if new_mac == old_mac.lower().replace("-", ":"):
        new_mac = generate_random_mac(old_mac)
    return new_mac


def mac_anonymize(
    iface: str, RUN_CONFIG: Any, GR: str, W: str, color_orange: str, stdout: Any, DN: Any
) -> None:
    """
    Randomizes the MAC address of an interface while preserving the vendor prefix.
    Stores the original MAC in RUN_CONFIG.ORIGINAL_IFACE_MAC for later restoration.
    """
    if RUN_CONFIG.DO_NOT_CHANGE_MAC:
        return
    if not program_exists("ifconfig"):
        return
    proc = Popen(["ifconfig", iface], stdout=PIPE, stderr=DN)
    proc.wait()
    old_mac = ""
    for word in proc.communicate()[0].decode(errors="ignore").split("\n")[0].split(" "):
        if word != "":
            old_mac = word
    RUN_CONFIG.ORIGINAL_IFACE_MAC = (iface, old_mac)
    new_mac = generate_random_mac(old_mac)
    import subprocess

    subprocess.run(["ifconfig", iface, "down"], check=True)
    print(
        f"{GR} [+]{W} changing {iface}'s MAC from {old_mac} to {new_mac}...",
        end="",
    )
    stdout.flush()
    proc = Popen(["ifconfig", iface, "hw", "ether", new_mac], stdout=PIPE, stderr=DN)
    proc.wait()
    subprocess.run(["ifconfig", iface, "up"], stdout=DN, stderr=DN, check=True)
    print("done")


def mac_change_back(RUN_CONFIG: Any, GR: str, W: str, stdout: Any, DN: Any) -> None:
    """
    Changes MAC address back to what it was before attacks began.
    """
    iface = RUN_CONFIG.ORIGINAL_IFACE_MAC[0]
    old_mac = RUN_CONFIG.ORIGINAL_IFACE_MAC[1]
    if iface == "" or old_mac == "":
        return
    print(
        f"{GR} [+]{W} changing {iface}'s mac back to {old_mac}...",
        end="",
    )
    stdout.flush()
    import subprocess

    subprocess.run(["ifconfig", iface, "down"], stdout=DN, stderr=DN, check=True)
    proc = Popen(["ifconfig", iface, "hw", "ether", old_mac], stdout=PIPE, stderr=DN)
    proc.wait()
    subprocess.run(["ifconfig", iface, "up"], stdout=DN, stderr=DN, check=True)
    print("done")


def add_commas(n: int) -> str:
    """
    Formats an integer with thousands separators (e.g., 1000000 -> "1,000,000").
    """
    strn = str(n)
    lenn = len(strn)
    i = 0
    result = ""
    while i < lenn:
        if (lenn - i) % 3 == 0 and i != 0:
            result += ","
        result += strn[i]
        i += 1
    return result


def print_and_exec(cmd: list[str], color_orange: str, W: str, stdout: Any, DN: Any) -> None:
    print("\r                                                        \r", end="")
    stdout.flush()
    print(color_orange + " [!] " + W + "executing: " + color_orange + " ".join(cmd) + W, end="")
    stdout.flush()
    import subprocess

    subprocess.run(cmd, stdout=DN, stderr=DN, check=True)
    time.sleep(0.1)


def remove_airodump_files(prefix: str, RUN_CONFIG: Any) -> None:
    remove_file(prefix + "-01.cap")
    remove_file(prefix + "-01.csv")
    remove_file(prefix + "-01.kismet.csv")
    remove_file(prefix + "-01.kismet.netxml")
    for filename in os.listdir(RUN_CONFIG.temp):
        if filename.lower().endswith(".xor"):
            remove_file(RUN_CONFIG.temp + filename)
    for filename in os.listdir("."):
        if filename.startswith("replay_") and filename.endswith(".cap"):
            remove_file(filename)
        if filename.endswith(".xor"):
            remove_file(filename)
