"""
test_utils.py
-------------
Comprehensive unit tests for the utils module (utility functions).
Tests cover file operations, subprocess helpers, time formatting, MAC handling, and more.
"""

import os
import tempfile
from unittest.mock import Mock, patch
from wlfwifi import utils


class TestSecToHms:
    """Tests for sec_to_hms function."""

    def test_sec_to_hms_one_second(self):
        """Test conversion of 1 second."""
        assert utils.sec_to_hms(1) == "[0:00:01]"

    def test_sec_to_hms_one_minute(self):
        """Test conversion of 60 seconds (1 minute)."""
        assert utils.sec_to_hms(60) == "[0:01:00]"

    def test_sec_to_hms_one_hour(self):
        """Test conversion of 3600 seconds (1 hour)."""
        assert utils.sec_to_hms(3600) == "[1:00:00]"

    def test_sec_to_hms_complex(self):
        """Test conversion of complex time value."""
        assert utils.sec_to_hms(3661) == "[1:01:01]"

    def test_sec_to_hms_zero(self):
        """Test conversion of 0 seconds."""
        assert utils.sec_to_hms(0) == "[0:00:00]"

    def test_sec_to_hms_negative(self):
        """Test conversion of negative value (endless)."""
        assert utils.sec_to_hms(-1) == "[endless]"

    def test_sec_to_hms_large_value(self):
        """Test conversion of large value (10 hours)."""
        assert utils.sec_to_hms(36000) == "[10:00:00]"

    def test_sec_to_hms_59_seconds(self):
        """Test conversion of 59 seconds."""
        assert utils.sec_to_hms(59) == "[0:00:59]"

    def test_sec_to_hms_59_minutes(self):
        """Test conversion of 59 minutes 59 seconds."""
        assert utils.sec_to_hms(3599) == "[0:59:59]"

    def test_sec_to_hms_24_hours(self):
        """Test conversion of 24 hours."""
        assert utils.sec_to_hms(86400) == "[24:00:00]"


class TestAddCommas:
    """Tests for add_commas function."""

    def test_add_commas_zero(self):
        """Test formatting of zero."""
        assert utils.add_commas(0) == "0"

    def test_add_commas_small_number(self):
        """Test formatting of small number (no commas needed)."""
        assert utils.add_commas(123) == "123"

    def test_add_commas_thousands(self):
        """Test formatting of thousands."""
        assert utils.add_commas(1000) == "1,000"

    def test_add_commas_millions(self):
        """Test formatting of millions."""
        assert utils.add_commas(1000000) == "1,000,000"

    def test_add_commas_complex(self):
        """Test formatting of complex number."""
        assert utils.add_commas(123456789) == "123,456,789"

    def test_add_commas_edge_999(self):
        """Test formatting of 999 (no comma)."""
        assert utils.add_commas(999) == "999"

    def test_add_commas_edge_1000(self):
        """Test formatting of exactly 1000."""
        assert utils.add_commas(1000) == "1,000"

    def test_add_commas_large(self):
        """Test formatting of large number."""
        assert utils.add_commas(1234567890123) == "1,234,567,890,123"


class TestRemoveFile:
    """Tests for remove_file function."""

    def test_remove_file_exists(self):
        """Test removing an existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        assert os.path.exists(temp_path)
        utils.remove_file(temp_path)
        assert not os.path.exists(temp_path)

    def test_remove_file_not_exists(self):
        """Test removing a non-existent file (should not raise)."""
        utils.remove_file("/nonexistent/path/to/file.txt")

    def test_remove_file_empty_string(self):
        """Test removing empty string path (should not raise)."""
        utils.remove_file("")


class TestRename:
    """Tests for rename function."""

    def test_rename_same_partition(self):
        """Test renaming file on same partition."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".old") as f:
            old_path = f.name
            f.write(b"test content")
        new_path = old_path.replace(".old", ".new")
        utils.rename(old_path, new_path)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)
        with open(new_path, "rb") as f:
            assert f.read() == b"test content"
        os.remove(new_path)

    def test_rename_preserves_content(self):
        """Test that rename preserves file content."""
        content = b"test content with special chars: \x00\xff\n\t"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".old") as f:
            old_path = f.name
            f.write(content)
        new_path = old_path.replace(".old", ".new")
        utils.rename(old_path, new_path)
        with open(new_path, "rb") as f:
            assert f.read() == content
        os.remove(new_path)


class TestGenerateRandomMac:
    """Tests for generate_random_mac function."""

    def test_generate_random_mac_format(self):
        """Test that generated MAC has correct format."""
        old_mac = "00:11:22:33:44:55"
        new_mac = utils.generate_random_mac(old_mac)
        assert len(new_mac) == 17
        parts = new_mac.split(":")
        assert len(parts) == 6
        for part in parts:
            assert len(part) == 2

    def test_generate_random_mac_preserves_vendor(self):
        """Test that vendor portion is preserved."""
        old_mac = "00:11:22:33:44:55"
        new_mac = utils.generate_random_mac(old_mac)
        assert new_mac[:8] == old_mac[:8].lower()

    def test_generate_random_mac_different(self):
        """Test that generated MAC is different from original."""
        old_mac = "00:11:22:33:44:55"
        new_mac = utils.generate_random_mac(old_mac)
        assert new_mac != old_mac

    def test_generate_random_mac_lowercase(self):
        """Test that generated MAC is lowercase."""
        old_mac = "AA:BB:CC:DD:EE:FF"
        new_mac = utils.generate_random_mac(old_mac)
        assert new_mac == new_mac.lower()

    def test_generate_random_mac_randomness(self):
        """Test that multiple calls generate different MACs."""
        old_mac = "00:11:22:33:44:55"
        macs = set()
        for _ in range(10):
            macs.add(utils.generate_random_mac(old_mac))
        # Should have at least a few different MACs
        assert len(macs) > 1


class TestProgramExists:
    """Tests for program_exists function."""

    @patch("wlfwifi.utils.Popen")
    def test_program_exists_found(self, mock_popen):
        """Test program_exists when program is found."""
        mock_proc = Mock()
        mock_proc.communicate.return_value = (b"/usr/bin/python", b"")
        mock_popen.return_value = mock_proc
        result = utils.program_exists("python")
        assert result is True

    @patch("wlfwifi.utils.Popen")
    def test_program_exists_not_found(self, mock_popen):
        """Test program_exists when program is not found."""
        mock_proc = Mock()
        mock_proc.communicate.return_value = (b"", b"")
        mock_popen.return_value = mock_proc
        result = utils.program_exists("nonexistent_program")
        assert result is False

    @patch("wlfwifi.utils.Popen")
    def test_program_exists_with_error(self, mock_popen):
        """Test program_exists when error occurs."""
        mock_popen.side_effect = Exception("Command failed")
        result = utils.program_exists("python")
        assert result is False


class TestSendInterrupt:
    """Tests for send_interrupt function."""

    @patch("wlfwifi.utils.os.kill")
    def test_send_interrupt_success(self, mock_kill):
        """Test send_interrupt successfully sends signal."""
        mock_process = Mock()
        mock_process.pid = 1234
        utils.send_interrupt(mock_process)
        mock_kill.assert_called_once()

    @patch("wlfwifi.utils.os.kill")
    def test_send_interrupt_no_pid(self, mock_kill):
        """Test send_interrupt with process without pid."""
        mock_process = Mock(spec=[])  # No pid attribute
        utils.send_interrupt(mock_process)
        mock_kill.assert_not_called()

    @patch("wlfwifi.utils.os.kill")
    def test_send_interrupt_os_error(self, mock_kill):
        """Test send_interrupt handles OSError gracefully."""
        mock_kill.side_effect = OSError("Process not found")
        mock_process = Mock()
        mock_process.pid = 1234
        # Should not raise
        utils.send_interrupt(mock_process)


class TestGetMacAddress:
    """Tests for get_mac_address function."""

    @patch("wlfwifi.utils.Popen")
    def test_get_mac_address_success(self, mock_popen):
        """Test get_mac_address with valid output."""
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (
            b"eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n"
            b"        ether 00-11-22-33-44-55  txqueuelen 1000  (Ethernet)\n",
            b"",
        )
        mock_popen.return_value = mock_proc
        result = utils.get_mac_address("eth0")
        assert result == "00:11:22:33:44:55"

    @patch("wlfwifi.utils.Popen")
    def test_get_mac_address_not_found(self, mock_popen):
        """Test get_mac_address when MAC not found."""
        mock_proc = Mock()
        mock_proc.wait.return_value = None
        mock_proc.communicate.return_value = (b"eth0: device not found", b"")
        mock_popen.return_value = mock_proc
        result = utils.get_mac_address("eth0")
        assert result == ""

    @patch("wlfwifi.utils.Popen")
    def test_get_mac_address_error(self, mock_popen):
        """Test get_mac_address handles errors."""
        mock_popen.side_effect = Exception("Command failed")
        result = utils.get_mac_address("eth0")
        assert result == ""


class TestMacAnonymize:
    """Tests for mac_anonymize function."""

    def test_mac_anonymize_disabled(self):
        """Test mac_anonymize when DO_NOT_CHANGE_MAC is True."""
        mock_config = Mock()
        mock_config.DO_NOT_CHANGE_MAC = True
        # Should return early without any action
        utils.mac_anonymize(
            "wlan0", mock_config, "GR", "W", "O", Mock(), Mock()
        )
        # No assertions needed - just verify it doesn't crash

    @patch("wlfwifi.utils.program_exists")
    def test_mac_anonymize_no_ifconfig(self, mock_program_exists):
        """Test mac_anonymize when ifconfig not available."""
        mock_program_exists.return_value = False
        mock_config = Mock()
        mock_config.DO_NOT_CHANGE_MAC = False
        # Should return early without action
        utils.mac_anonymize(
            "wlan0", mock_config, "GR", "W", "O", Mock(), Mock()
        )


class TestMacChangeBack:
    """Tests for mac_change_back function."""

    def test_mac_change_back_empty_iface(self):
        """Test mac_change_back with empty interface."""
        mock_config = Mock()
        mock_config.ORIGINAL_IFACE_MAC = ("", "00:11:22:33:44:55")
        # Should return early
        utils.mac_change_back(mock_config, "GR", "W", Mock(), Mock())

    def test_mac_change_back_empty_mac(self):
        """Test mac_change_back with empty MAC."""
        mock_config = Mock()
        mock_config.ORIGINAL_IFACE_MAC = ("wlan0", "")
        # Should return early
        utils.mac_change_back(mock_config, "GR", "W", Mock(), Mock())


class TestRemoveAirodumpFiles:
    """Tests for remove_airodump_files function."""

    def test_remove_airodump_files_basic(self):
        """Test remove_airodump_files with temporary files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config = Mock()
            mock_config.temp = tmpdir + os.sep
            prefix = os.path.join(tmpdir, "test")
            # Create some files
            files = [
                prefix + "-01.cap",
                prefix + "-01.csv",
                prefix + "-01.kismet.csv",
                prefix + "-01.kismet.netxml",
            ]
            for f in files:
                with open(f, "w") as fh:
                    fh.write("test")
            # Remove them
            utils.remove_airodump_files(prefix, mock_config)
            # Check they're gone
            for f in files:
                assert not os.path.exists(f)


class TestPrintAndExec:
    """Tests for print_and_exec function."""

    @patch("subprocess.run")
    def test_print_and_exec_success(self, mock_run):
        """Test print_and_exec executes command."""
        mock_stdout = Mock()
        mock_dn = Mock()
        utils.print_and_exec(
            ["echo", "hello"], "O", "W", mock_stdout, mock_dn
        )
        mock_run.assert_called_once()
        mock_stdout.flush.assert_called()


class TestEdgeCases:
    """Edge case tests for utility functions."""

    def test_sec_to_hms_very_large(self):
        """Test sec_to_hms with very large value."""
        result = utils.sec_to_hms(360000)  # 100 hours
        assert result == "[100:00:00]"

    def test_sec_to_hms_negative_two(self):
        """Test sec_to_hms with -2 (still endless)."""
        result = utils.sec_to_hms(-2)
        assert result == "[endless]"

    def test_add_commas_one(self):
        """Test add_commas with single digit."""
        assert utils.add_commas(1) == "1"

    def test_add_commas_two_digits(self):
        """Test add_commas with two digits."""
        assert utils.add_commas(99) == "99"

    def test_generate_random_mac_with_dashes(self):
        """Test generate_random_mac with dash-separated MAC."""
        old_mac = "00-11-22-33-44-55"
        new_mac = utils.generate_random_mac(old_mac)
        assert ":" in new_mac  # Output uses colons

    def test_remove_file_with_tempdir(self):
        """Test remove_file in a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "testfile.txt")
            with open(filepath, "w") as f:
                f.write("test")
            assert os.path.exists(filepath)
            utils.remove_file(filepath)
            assert not os.path.exists(filepath)
