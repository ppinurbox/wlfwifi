"""
test_attacks.py
---------------
Comprehensive unit tests for the attacks module (Attack, wps_check_targets, etc.).
Tests cover abstract class behavior, WPS checking, mocking subprocess calls, and edge cases.
"""

import pytest
from unittest.mock import Mock, patch
from wlfwifi.attacks import Attack, wps_check_targets
from wlfwifi.models import Target


class TestAttackAbstractClass:
    """Tests for the Attack abstract base class."""

    def test_attack_cannot_instantiate_directly(self):
        """Test that Attack cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Attack()

    def test_attack_subclass_must_implement_methods(self):
        """Test that subclass must implement abstract methods."""

        class IncompleteAttack(Attack):
            pass

        with pytest.raises(TypeError):
            IncompleteAttack()

    def test_attack_subclass_run_attack(self):
        """Test that subclass can implement RunAttack."""

        class ConcreteAttack(Attack):
            def RunAttack(self):
                return "attack running"

            def EndAttack(self):
                return "attack ended"

        attack = ConcreteAttack()
        assert attack.RunAttack() == "attack running"

    def test_attack_subclass_end_attack(self):
        """Test that subclass can implement EndAttack."""

        class ConcreteAttack(Attack):
            def RunAttack(self):
                return "attack running"

            def EndAttack(self):
                return "attack ended"

        attack = ConcreteAttack()
        assert attack.EndAttack() == "attack ended"

    def test_attack_super_run_raises(self):
        """Test that calling super().RunAttack() raises NotImplementedError."""

        class DummyAttack(Attack):
            def RunAttack(self):
                return super().RunAttack()

            def EndAttack(self):
                return "ended"

        attack = DummyAttack()
        with pytest.raises(NotImplementedError):
            attack.RunAttack()

    def test_attack_super_end_raises(self):
        """Test that calling super().EndAttack() raises NotImplementedError."""

        class DummyAttack(Attack):
            def RunAttack(self):
                return "running"

            def EndAttack(self):
                return super().EndAttack()

        attack = DummyAttack()
        with pytest.raises(NotImplementedError):
            attack.EndAttack()


class TestWpsCheckTargets:
    """Tests for the wps_check_targets function."""

    @patch("wlfwifi.attacks.program_exists")
    def test_wps_check_targets_no_tshark(self, mock_program_exists):
        """Test wps_check_targets when tshark is not installed."""
        mock_program_exists.return_value = False
        targets = [
            Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)
        # Should return early without modifying targets

    @patch("wlfwifi.attacks.program_exists")
    def test_wps_check_targets_empty_list(self, mock_program_exists):
        """Test wps_check_targets with empty target list."""
        mock_program_exists.return_value = True
        wps_check_targets([], "/tmp/test.cap", verbose=True)
        # Should return early

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    def test_wps_check_targets_cap_file_not_exists(
        self, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets when cap file doesn't exist."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = False
        targets = [
            Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False),
        ]
        wps_check_targets(targets, "/nonexistent.cap", verbose=True)
        # Should return early

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_with_wps_enabled(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets marks WPS-enabled targets."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (
            b"00:11:22:33:44:55,0\n11:22:33:44:55:66,1\n",
            b"",
        )
        mock_popen.return_value = mock_proc

        targets = [
            Target("00:11:22:33:44:55", "TestNet1", 6, "WPA2", False),
            Target("11:22:33:44:55:66", "TestNet2", 11, "WPA2", False),
            Target("22:33:44:55:66:77", "TestNet3", 1, "WPA2", False),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)
        assert targets[0].wps is True
        assert targets[1].wps is True
        assert targets[2].wps is False

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_no_wps(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets when no targets have WPS."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (b"", b"")
        mock_popen.return_value = mock_proc

        targets = [
            Target("00:11:22:33:44:55", "TestNet1", 6, "WPA2", True),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)
        assert targets[0].wps is False

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_case_insensitive(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets handles case-insensitive BSSIDs."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (b"AA:BB:CC:DD:EE:FF,0\n", b"")
        mock_popen.return_value = mock_proc

        targets = [
            Target("aa:bb:cc:dd:ee:ff", "TestNet", 6, "WPA2", False),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)
        assert targets[0].wps is True

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_verbose_false(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets with verbose=False."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (b"00:11:22:33:44:55,0\n", b"")
        mock_popen.return_value = mock_proc

        targets = [
            Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=False)
        assert targets[0].wps is True

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_exception_handling(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets handles exceptions gracefully."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_popen.side_effect = Exception("tshark error")

        targets = [
            Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False),
        ]
        # Should not raise
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)

    @patch("wlfwifi.attacks.program_exists")
    @patch("wlfwifi.attacks.os.path.exists")
    @patch("wlfwifi.attacks.Popen")
    def test_wps_check_targets_malformed_output(
        self, mock_popen, mock_path_exists, mock_program_exists
    ):
        """Test wps_check_targets handles malformed tshark output."""
        mock_program_exists.return_value = True
        mock_path_exists.return_value = True
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (b"malformed output here", b"")
        mock_popen.return_value = mock_proc

        targets = [
            Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False),
        ]
        wps_check_targets(targets, "/tmp/test.cap", verbose=True)
        assert targets[0].wps is False


class TestConcreteAttackImplementations:
    """Tests for concrete attack implementations."""

    def test_wpa_attack_implementation(self):
        """Test WPA attack implementation pattern."""

        class WPAAttack(Attack):
            def __init__(self, target: Target):
                self.target = target
                self.running = False

            def RunAttack(self):
                self.running = True
                return f"Attacking {self.target.essid}"

            def EndAttack(self):
                self.running = False
                return f"Stopped attacking {self.target.essid}"

        target = Target("00:11:22:33:44:55", "TestWPA", 6, "WPA2", False)
        attack = WPAAttack(target)
        assert attack.RunAttack() == "Attacking TestWPA"
        assert attack.running is True
        assert attack.EndAttack() == "Stopped attacking TestWPA"
        assert attack.running is False

    def test_wep_attack_implementation(self):
        """Test WEP attack implementation pattern."""

        class WEPAttack(Attack):
            def __init__(self, target: Target):
                self.target = target
                self.ivs_collected = 0

            def RunAttack(self):
                self.ivs_collected = 10000
                return f"Collected {self.ivs_collected} IVs"

            def EndAttack(self):
                return f"Attack complete with {self.ivs_collected} IVs"

        target = Target("00:11:22:33:44:55", "TestWEP", 6, "WEP", False)
        attack = WEPAttack(target)
        assert "10000" in attack.RunAttack()
        assert "10000" in attack.EndAttack()

    def test_wps_attack_implementation(self):
        """Test WPS attack implementation pattern."""

        class WPSAttack(Attack):
            def __init__(self, target: Target):
                self.target = target
                self.pin = None

            def RunAttack(self):
                if self.target.wps:
                    self.pin = "12345670"
                    return f"Found PIN: {self.pin}"
                return "WPS not enabled"

            def EndAttack(self):
                return f"WPS attack ended, PIN: {self.pin}"

        target_with_wps = Target("00:11:22:33:44:55", "TestWPS", 6, "WPA2", True)
        attack = WPSAttack(target_with_wps)
        assert "12345670" in attack.RunAttack()

        target_without_wps = Target("00:11:22:33:44:55", "TestNoWPS", 6, "WPA2", False)
        attack2 = WPSAttack(target_without_wps)
        assert attack2.RunAttack() == "WPS not enabled"


class TestAttackLifecycle:
    """Tests for attack lifecycle management."""

    def test_attack_start_stop_cycle(self):
        """Test complete attack start/stop cycle."""

        class LifecycleAttack(Attack):
            def __init__(self):
                self.state = "idle"
                self.attempts = 0

            def RunAttack(self):
                self.state = "running"
                self.attempts += 1
                return self.state

            def EndAttack(self):
                self.state = "stopped"
                return self.state

        attack = LifecycleAttack()
        assert attack.state == "idle"
        attack.RunAttack()
        assert attack.state == "running"
        assert attack.attempts == 1
        attack.EndAttack()
        assert attack.state == "stopped"

    def test_attack_multiple_runs(self):
        """Test running attack multiple times."""

        class CountingAttack(Attack):
            def __init__(self):
                self.run_count = 0

            def RunAttack(self):
                self.run_count += 1
                return self.run_count

            def EndAttack(self):
                return self.run_count

        attack = CountingAttack()
        for i in range(5):
            assert attack.RunAttack() == i + 1
        assert attack.run_count == 5


class TestAttackWithCapFile:
    """Tests for attacks using capture files."""

    def test_attack_with_capture_file(self):
        """Test attack that uses capture file."""
        from wlfwifi.models import CapFile

        class CaptureAttack(Attack):
            def __init__(self, target: Target, cap_file: CapFile):
                self.target = target
                self.cap_file = cap_file

            def RunAttack(self):
                return f"Reading {self.cap_file.path}"

            def EndAttack(self):
                return f"Captured {self.cap_file.handshakes} handshakes"

        target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)
        cap = CapFile("/tmp/test.cap", 2)
        attack = CaptureAttack(target, cap)
        assert "/tmp/test.cap" in attack.RunAttack()
        assert "2 handshakes" in attack.EndAttack()
