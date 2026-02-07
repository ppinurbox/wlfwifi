"""
models.py
-----------
Data models for wireless targets, clients, and capture files used by wlfwifi.

Classes:
        Target: Represents a wireless network target.
        Client: Represents a client device connected to a target.
        CapFile: Represents a capture file containing handshake or packet data.
"""


class Target:
    """
    Represents a wireless network target.
    Attributes:
            bssid (str): The BSSID of the target.
            essid (str): The ESSID (network name) of the target.
            channel (int): The channel the target is operating on.
            encryption (str): The encryption type (WEP, WPA, WPA2, etc.).
            wps (bool): Whether WPS is enabled.
    """

    bssid: str
    essid: str
    channel: int
    encryption: str
    wps: bool

    def __init__(
        self, bssid: str, essid: str, channel: int, encryption: str, wps: bool
    ) -> None:
        self.bssid = bssid
        self.essid = essid
        self.channel = channel
        self.encryption = encryption
        self.wps = wps


class Client:
    """
    Represents a client device connected to a target.
    Attributes:
            mac (str): The MAC address of the client.
            target_bssid (str): The BSSID of the associated target.
    """

    mac: str
    target_bssid: str

    def __init__(self, mac: str, target_bssid: str) -> None:
        self.mac = mac
        self.target_bssid = target_bssid


class CapFile:
    """
    Represents a capture file containing handshake or packet data.
    Attributes:
            path (str): The file path to the capture file.
            handshakes (int): Number of handshakes or packets captured.
    """

    path: str
    handshakes: int

    def __init__(self, path: str, handshakes: int) -> None:
        self.path = path
        self.handshakes = handshakes
