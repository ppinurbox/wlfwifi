"""
test_integration.py
--------------------
Comprehensive integration tests for wlfwifi.
Tests cover end-to-end workflows, module interactions, and realistic scenarios.
"""

import sys
import os
import tempfile
import pytest
from unittest.mock import Mock, patch

from wlfwifi.models import Target, Client, CapFile
from wlfwifi.config import RunConfig, parse_args
from wlfwifi.attacks import Attack, wps_check_targets
from wlfwifi import utils


class TestFullWorkflowSimulation:
    """Integration tests simulating full attack workflows."""

    def test_target_discovery_to_attack_workflow(self):
        """Test complete workflow from target discovery to attack."""
        # 1. Create discovered targets
        targets = [
            Target("00:11:22:33:44:55", "HomeNetwork", 6, "WPA2", True),
            Target("11:22:33:44:55:66", "OfficeNet", 11, "WPA2", False),
            Target("22:33:44:55:66:77", "LegacyNet", 1, "WEP", False),
        ]

        # 2. Create associated clients
        clients = [
            Client("AA:BB:CC:DD:EE:01", targets[0].bssid),
            Client("AA:BB:CC:DD:EE:02", targets[0].bssid),
            Client("BB:CC:DD:EE:FF:01", targets[1].bssid),
        ]

        # 3. Create capture file (stored for potential use in attack)
        _ = CapFile("/tmp/capture.cap", 0)

        # 4. Create attack based on target properties
        class MockAttack(Attack):
            def __init__(self, target, clients):
                self.target = target
                self.clients = clients
                self.success = False

            def RunAttack(self):
                if self.target.wps:
                    return "WPS attack started"
                elif self.target.encryption == "WEP":
                    return "WEP attack started"
                else:
                    return "WPA attack started"

            def EndAttack(self):
                self.success = True
                return "Attack completed"

        # Test WPS-enabled target attack
        wps_attack = MockAttack(targets[0], [c for c in clients if c.target_bssid == targets[0].bssid])
        assert wps_attack.RunAttack() == "WPS attack started"
        assert len(wps_attack.clients) == 2

        # Test WPA target attack
        wpa_attack = MockAttack(targets[1], [c for c in clients if c.target_bssid == targets[1].bssid])
        assert wpa_attack.RunAttack() == "WPA attack started"

        # Test WEP target attack
        wep_attack = MockAttack(targets[2], [])
        assert wep_attack.RunAttack() == "WEP attack started"

    def test_config_to_attack_workflow(self):
        """Test workflow from config parsing to attack execution."""

        class WorkflowAttack(Attack):
            def __init__(self, config: RunConfig, target: Target):
                self.config = config
                self.target = target

            def RunAttack(self):
                if self.config.verbose:
                    return f"[VERBOSE] Attacking {self.target.essid} on channel {self.target.channel}"
                return f"Attacking {self.target.essid}"

            def EndAttack(self):
                return "Done"

        # Create config
        config = RunConfig(interface="wlan0", channel=6, verbose=True)
        target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)

        attack = WorkflowAttack(config, target)
        result = attack.RunAttack()
        assert "VERBOSE" in result
        assert "TestNet" in result
        assert "6" in result

    def test_multi_target_scanning_workflow(self):
        """Test scanning multiple targets and selecting best one."""
        targets = [
            Target("00:11:22:33:44:55", "WeakWEP", 1, "WEP", False),
            Target("11:22:33:44:55:66", "WPSEnabled", 6, "WPA2", True),
            Target("22:33:44:55:66:77", "StrongWPA", 11, "WPA2", False),
        ]

        # Priority: WEP > WPS > WPA
        def select_best_target(targets):
            for t in targets:
                if t.encryption == "WEP":
                    return t
            for t in targets:
                if t.wps:
                    return t
            return targets[0] if targets else None

        best = select_best_target(targets)
        assert best.encryption == "WEP"

        # Remove WEP target
        targets = [t for t in targets if t.encryption != "WEP"]
        best = select_best_target(targets)
        assert best.wps is True


class TestModuleIntegration:
    """Tests for integration between different modules."""

    def test_models_with_attacks(self):
        """Test that models work correctly with attacks module."""
        target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", True)
        cap = CapFile("/tmp/test.cap", 0)

        class CaptureAttack(Attack):
            def __init__(self, target, cap_file):
                self.target = target
                self.cap_file = cap_file

            def RunAttack(self):
                return f"Capturing for {self.target.bssid}"

            def EndAttack(self):
                self.cap_file.handshakes = 4
                return f"Captured {self.cap_file.handshakes} handshakes"

        attack = CaptureAttack(target, cap)
        attack.RunAttack()
        _ = attack.EndAttack()  # End attack triggers handshake count update
        assert cap.handshakes == 4

    def test_config_with_utils(self):
        """Test config integration with utility functions."""
        config = RunConfig(interface="wlan0", channel=6, verbose=True)

        # Use utility function
        time_str = utils.sec_to_hms(3661)
        assert time_str == "[1:01:01]"

        # Verify config works alongside utils
        assert config.interface == "wlan0"

    def test_utils_with_models(self):
        """Test utils integration with models."""
        target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)

        # Generate random MAC based on target's BSSID
        new_mac = utils.generate_random_mac(target.bssid)
        assert new_mac != target.bssid
        assert new_mac[:8] == target.bssid[:8].lower()


class TestCliIntegration:
    """Tests for CLI integration."""

    def test_cli_to_config(self, monkeypatch):
        """Test CLI arguments create correct config."""
        monkeypatch.setattr(sys, "argv", ["wlfwifi", "-i", "wlan0", "-c", "6", "-v"])
        config = parse_args()
        assert config.interface == "wlan0"
        assert config.channel == 6
        assert config.verbose is True

    def test_cli_minimal(self, monkeypatch):
        """Test minimal CLI invocation."""
        monkeypatch.setattr(sys, "argv", ["wlfwifi"])
        config = parse_args()
        assert config.interface is None
        assert config.channel is None
        assert config.verbose is False


class TestFileOperationsIntegration:
    """Tests for file operations integration."""

    def test_capfile_with_file_operations(self):
        """Test CapFile with actual file operations."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cap") as f:
            temp_path = f.name
            f.write(b"capture data")

        cap = CapFile(temp_path, 1)
        assert os.path.exists(cap.path)

        # Clean up
        utils.remove_file(temp_path)
        assert not os.path.exists(temp_path)

    def test_rename_with_capfile(self):
        """Test renaming capture files."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cap") as f:
            old_path = f.name
            f.write(b"test data")

        new_path = old_path.replace(".cap", "_renamed.cap")
        cap = CapFile(old_path, 2)

        utils.rename(cap.path, new_path)
        cap.path = new_path

        assert os.path.exists(new_path)
        assert not os.path.exists(old_path)

        # Clean up
        utils.remove_file(new_path)


class TestWpsCheckIntegration:
    """Tests for WPS check integration with targets."""

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_updates_targets(self, mock_popen, mock_exists, mock_prog):
        """Test that WPS check correctly updates target WPS status."""
        mock_prog.return_value = True
        mock_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (
            b"00:11:22:33:44:55,0\n22:33:44:55:66:77,0\n",
            b"",
        )
        mock_popen.return_value = mock_proc

        targets = [
            Target("00:11:22:33:44:55", "Net1", 1, "WPA2", False),
            Target("11:22:33:44:55:66", "Net2", 6, "WPA2", False),
            Target("22:33:44:55:66:77", "Net3", 11, "WPA2", False),
        ]

        wps_check_targets(targets, "/tmp/test.cap", verbose=False)

        assert targets[0].wps is True
        assert targets[1].wps is False
        assert targets[2].wps is True


class TestErrorHandlingIntegration:
    """Tests for error handling across modules."""

    def test_config_validation_error(self):
        """Test that config validation errors are raised correctly."""
        with pytest.raises(ValueError):
            RunConfig(interface=123)  # Should be string

        with pytest.raises(ValueError):
            RunConfig(channel="six")  # Should be int

    def test_attack_not_implemented_error(self):
        """Test that abstract attack methods raise NotImplementedError."""

        class IncompleteAttack(Attack):
            def RunAttack(self):
                return super().RunAttack()

            def EndAttack(self):
                return "ended"

        attack = IncompleteAttack()
        with pytest.raises(NotImplementedError):
            attack.RunAttack()


class TestRealWorldScenarios:
    """Tests simulating real-world usage scenarios."""

    def test_home_network_audit(self):
        """Simulate auditing a home network."""
        # Discover home network
        home_net = Target(
            bssid="00:11:22:33:44:55",
            essid="MyHomeWiFi",
            channel=6,
            encryption="WPA2",
            wps=True,
        )

        # Discover connected devices
        devices = [
            Client("AA:BB:CC:DD:EE:01", home_net.bssid),  # Phone
            Client("AA:BB:CC:DD:EE:02", home_net.bssid),  # Laptop
            Client("AA:BB:CC:DD:EE:03", home_net.bssid),  # Smart TV
        ]

        assert len(devices) == 3
        assert home_net.wps is True  # Potential vulnerability

    def test_enterprise_network_scan(self):
        """Simulate scanning an enterprise network."""
        networks = [
            Target("00:11:22:33:44:55", "Corp-Main", 1, "WPA2", False),
            Target("00:11:22:33:44:56", "Corp-Guest", 6, "WPA2", False),
            Target("00:11:22:33:44:57", "Corp-IoT", 11, "WPA2", True),
        ]

        # Enterprise networks typically have WPS disabled
        non_wps = [n for n in networks if not n.wps]
        wps_enabled = [n for n in networks if n.wps]

        assert len(non_wps) == 2
        assert len(wps_enabled) == 1
        assert wps_enabled[0].essid == "Corp-IoT"

    def test_channel_hopping_scenario(self):
        """Simulate channel hopping during scanning."""
        _ = RunConfig(interface="wlan0", verbose=True)  # Config for scan session

        # Simulate finding targets on different channels
        targets_per_channel = {
            1: [Target("00:11:22:33:44:55", "Net1", 1, "WPA2", False)],
            6: [
                Target("11:22:33:44:55:66", "Net2", 6, "WPA2", True),
                Target("22:33:44:55:66:77", "Net3", 6, "WEP", False),
            ],
            11: [Target("33:44:55:66:77:88", "Net4", 11, "WPA2", False)],
        }

        all_targets = []
        for channel, targets in targets_per_channel.items():
            all_targets.extend(targets)

        assert len(all_targets) == 4

    def test_long_running_attack_tracking(self):
        """Simulate tracking a long-running attack."""

        class TimedAttack(Attack):
            def __init__(self, target):
                self.target = target
                self.elapsed_seconds = 0

            def RunAttack(self):
                self.elapsed_seconds = 3661  # 1 hour 1 minute 1 second
                return utils.sec_to_hms(self.elapsed_seconds)

            def EndAttack(self):
                return f"Total time: {utils.sec_to_hms(self.elapsed_seconds)}"

        target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)
        attack = TimedAttack(target)
        result = attack.RunAttack()
        assert result == "[1:01:01]"


class TestConcurrencyScenarios:
    """Tests for concurrent operation scenarios."""

    def test_multiple_attacks_same_channel(self):
        """Test managing multiple attacks on same channel."""
        channel_6_targets = [
            Target("00:11:22:33:44:55", "Net1", 6, "WPA2", True),
            Target("11:22:33:44:55:66", "Net2", 6, "WPA2", False),
        ]

        class SequentialAttack(Attack):
            def __init__(self, targets):
                self.targets = targets
                self.current_index = 0
                self.completed = []

            def RunAttack(self):
                if self.current_index < len(self.targets):
                    target = self.targets[self.current_index]
                    return f"Attacking {target.essid}"
                return "No more targets"

            def EndAttack(self):
                if self.current_index < len(self.targets):
                    self.completed.append(self.targets[self.current_index])
                    self.current_index += 1
                return f"Completed {len(self.completed)} attacks"

        attack = SequentialAttack(channel_6_targets)
        assert attack.RunAttack() == "Attacking Net1"
        attack.EndAttack()
        assert attack.RunAttack() == "Attacking Net2"
        attack.EndAttack()
        assert len(attack.completed) == 2
