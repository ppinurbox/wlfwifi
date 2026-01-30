"""
test_models.py
---------------
Comprehensive unit tests for the models module (Target, Client, CapFile).
Tests cover initialization, attribute access, edge cases, and type handling.
"""

from wlfwifi.models import Target, Client, CapFile


class TestTarget:
    """Tests for the Target class."""

    def test_target_initialization(self):
        """Test basic Target initialization with valid parameters."""
        t = Target(
            bssid="00:11:22:33:44:55",
            essid="TestNet",
            channel=6,
            encryption="WPA2",
            wps=True,
        )
        assert t.bssid == "00:11:22:33:44:55"
        assert t.essid == "TestNet"
        assert t.channel == 6
        assert t.encryption == "WPA2"
        assert t.wps is True

    def test_target_wps_disabled(self):
        """Test Target with WPS disabled."""
        t = Target(
            bssid="AA:BB:CC:DD:EE:FF",
            essid="SecureNet",
            channel=11,
            encryption="WPA2",
            wps=False,
        )
        assert t.wps is False

    def test_target_wep_encryption(self):
        """Test Target with WEP encryption."""
        t = Target(
            bssid="11:22:33:44:55:66",
            essid="LegacyNet",
            channel=1,
            encryption="WEP",
            wps=False,
        )
        assert t.encryption == "WEP"

    def test_target_wpa_encryption(self):
        """Test Target with WPA encryption."""
        t = Target(
            bssid="22:33:44:55:66:77",
            essid="WpaNetwork",
            channel=3,
            encryption="WPA",
            wps=True,
        )
        assert t.encryption == "WPA"

    def test_target_empty_essid(self):
        """Test Target with empty ESSID (hidden network)."""
        t = Target(
            bssid="33:44:55:66:77:88",
            essid="",
            channel=9,
            encryption="WPA2",
            wps=False,
        )
        assert t.essid == ""

    def test_target_special_characters_essid(self):
        """Test Target with special characters in ESSID."""
        t = Target(
            bssid="44:55:66:77:88:99",
            essid="My Network!@#$%^&*()",
            channel=6,
            encryption="WPA2",
            wps=True,
        )
        assert t.essid == "My Network!@#$%^&*()"

    def test_target_unicode_essid(self):
        """Test Target with unicode characters in ESSID."""
        t = Target(
            bssid="55:66:77:88:99:AA",
            essid="カフェ WiFi",
            channel=11,
            encryption="WPA2",
            wps=False,
        )
        assert t.essid == "カフェ WiFi"

    def test_target_high_channel(self):
        """Test Target with high channel number (5GHz)."""
        t = Target(
            bssid="66:77:88:99:AA:BB",
            essid="5GHz_Network",
            channel=149,
            encryption="WPA2",
            wps=False,
        )
        assert t.channel == 149

    def test_target_channel_zero(self):
        """Test Target with channel 0 (edge case)."""
        t = Target(
            bssid="77:88:99:AA:BB:CC",
            essid="ZeroChannel",
            channel=0,
            encryption="WPA2",
            wps=False,
        )
        assert t.channel == 0

    def test_target_lowercase_bssid(self):
        """Test Target with lowercase BSSID."""
        t = Target(
            bssid="aa:bb:cc:dd:ee:ff",
            essid="LowerCase",
            channel=6,
            encryption="WPA2",
            wps=True,
        )
        assert t.bssid == "aa:bb:cc:dd:ee:ff"

    def test_target_mixed_case_encryption(self):
        """Test Target with mixed case encryption string."""
        t = Target(
            bssid="00:11:22:33:44:55",
            essid="MixedCase",
            channel=6,
            encryption="wpa2",
            wps=True,
        )
        assert t.encryption == "wpa2"


class TestClient:
    """Tests for the Client class."""

    def test_client_initialization(self):
        """Test basic Client initialization."""
        c = Client(mac="AA:BB:CC:DD:EE:FF", target_bssid="00:11:22:33:44:55")
        assert c.mac == "AA:BB:CC:DD:EE:FF"
        assert c.target_bssid == "00:11:22:33:44:55"

    def test_client_lowercase_mac(self):
        """Test Client with lowercase MAC address."""
        c = Client(mac="aa:bb:cc:dd:ee:ff", target_bssid="00:11:22:33:44:55")
        assert c.mac == "aa:bb:cc:dd:ee:ff"

    def test_client_mixed_case_mac(self):
        """Test Client with mixed case MAC address."""
        c = Client(mac="Aa:Bb:Cc:Dd:Ee:Ff", target_bssid="00:11:22:33:44:55")
        assert c.mac == "Aa:Bb:Cc:Dd:Ee:Ff"

    def test_client_empty_target_bssid(self):
        """Test Client with empty target BSSID."""
        c = Client(mac="AA:BB:CC:DD:EE:FF", target_bssid="")
        assert c.target_bssid == ""

    def test_client_same_mac_as_bssid(self):
        """Test Client where MAC equals target BSSID."""
        c = Client(mac="00:11:22:33:44:55", target_bssid="00:11:22:33:44:55")
        assert c.mac == c.target_bssid


class TestCapFile:
    """Tests for the CapFile class."""

    def test_capfile_initialization(self):
        """Test basic CapFile initialization."""
        cap = CapFile(path="/tmp/test.cap", handshakes=2)
        assert cap.path == "/tmp/test.cap"
        assert cap.handshakes == 2

    def test_capfile_zero_handshakes(self):
        """Test CapFile with zero handshakes."""
        cap = CapFile(path="/tmp/empty.cap", handshakes=0)
        assert cap.handshakes == 0

    def test_capfile_many_handshakes(self):
        """Test CapFile with many handshakes."""
        cap = CapFile(path="/tmp/busy.cap", handshakes=1000)
        assert cap.handshakes == 1000

    def test_capfile_relative_path(self):
        """Test CapFile with relative path."""
        cap = CapFile(path="./captures/test.cap", handshakes=1)
        assert cap.path == "./captures/test.cap"

    def test_capfile_absolute_path_windows(self):
        """Test CapFile with Windows absolute path."""
        cap = CapFile(path="C:\\Users\\test\\capture.cap", handshakes=1)
        assert cap.path == "C:\\Users\\test\\capture.cap"

    def test_capfile_spaces_in_path(self):
        """Test CapFile with spaces in path."""
        cap = CapFile(path="/tmp/my captures/test file.cap", handshakes=3)
        assert cap.path == "/tmp/my captures/test file.cap"

    def test_capfile_different_extensions(self):
        """Test CapFile with various extensions."""
        cap1 = CapFile(path="/tmp/test.pcap", handshakes=1)
        cap2 = CapFile(path="/tmp/test.pcapng", handshakes=2)
        assert cap1.path.endswith(".pcap")
        assert cap2.path.endswith(".pcapng")

    def test_capfile_negative_handshakes(self):
        """Test CapFile with negative handshakes (edge case)."""
        cap = CapFile(path="/tmp/test.cap", handshakes=-1)
        assert cap.handshakes == -1


class TestModelInteractions:
    """Tests for interactions between model classes."""

    def test_multiple_clients_same_target(self):
        """Test multiple clients associated with same target."""
        target = Target(
            bssid="00:11:22:33:44:55",
            essid="SharedNet",
            channel=6,
            encryption="WPA2",
            wps=True,
        )
        clients = [
            Client(mac="AA:BB:CC:DD:EE:01", target_bssid=target.bssid),
            Client(mac="AA:BB:CC:DD:EE:02", target_bssid=target.bssid),
            Client(mac="AA:BB:CC:DD:EE:03", target_bssid=target.bssid),
        ]
        for client in clients:
            assert client.target_bssid == target.bssid

    def test_target_capfile_association(self):
        """Test associating capture files with targets."""
        target = Target(
            bssid="00:11:22:33:44:55",
            essid="TestNet",
            channel=6,
            encryption="WPA2",
            wps=True,
        )
        cap = CapFile(path=f"/tmp/{target.bssid.replace(':', '')}.cap", handshakes=4)
        assert target.bssid.replace(":", "") in cap.path

    def test_wps_target_identification(self):
        """Test identifying WPS-enabled targets from a list."""
        targets = [
            Target("00:11:22:33:44:55", "WPS_On", 1, "WPA2", True),
            Target("11:22:33:44:55:66", "WPS_Off", 6, "WPA2", False),
            Target("22:33:44:55:66:77", "WPS_On_2", 11, "WPA", True),
        ]
        wps_targets = [t for t in targets if t.wps]
        assert len(wps_targets) == 2
        assert all(t.wps for t in wps_targets)
