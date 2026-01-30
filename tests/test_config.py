"""
test_config.py
--------------
Comprehensive unit tests for the config module (argument parsing, RunConfig).
Tests cover initialization, validation, edge cases, and error handling.
"""

import sys
import pytest
from wlfwifi.config import parse_args, RunConfig


class TestRunConfig:
    """Tests for the RunConfig class."""

    def test_runconfig_default_initialization(self):
        """Test RunConfig with default parameters."""
        config = RunConfig()
        assert config.interface is None
        assert config.channel is None
        assert config.verbose is False

    def test_runconfig_with_interface(self):
        """Test RunConfig with interface set."""
        config = RunConfig(interface="wlan0")
        assert config.interface == "wlan0"
        assert config.channel is None
        assert config.verbose is False

    def test_runconfig_with_channel(self):
        """Test RunConfig with channel set."""
        config = RunConfig(channel=6)
        assert config.interface is None
        assert config.channel == 6
        assert config.verbose is False

    def test_runconfig_with_verbose(self):
        """Test RunConfig with verbose enabled."""
        config = RunConfig(verbose=True)
        assert config.interface is None
        assert config.channel is None
        assert config.verbose is True

    def test_runconfig_all_parameters(self):
        """Test RunConfig with all parameters set."""
        config = RunConfig(interface="wlan1", channel=11, verbose=True)
        assert config.interface == "wlan1"
        assert config.channel == 11
        assert config.verbose is True

    def test_runconfig_interface_validation_invalid_type(self):
        """Test RunConfig raises error for invalid interface type."""
        with pytest.raises(ValueError, match="interface must be a string or None"):
            RunConfig(interface=123)

    def test_runconfig_channel_validation_invalid_type(self):
        """Test RunConfig raises error for invalid channel type."""
        with pytest.raises(ValueError, match="channel must be an integer or None"):
            RunConfig(channel="six")

    def test_runconfig_interface_empty_string(self):
        """Test RunConfig with empty string interface."""
        config = RunConfig(interface="")
        assert config.interface == ""

    def test_runconfig_channel_zero(self):
        """Test RunConfig with channel zero."""
        config = RunConfig(channel=0)
        assert config.channel == 0

    def test_runconfig_channel_negative(self):
        """Test RunConfig with negative channel (edge case)."""
        config = RunConfig(channel=-1)
        assert config.channel == -1

    def test_runconfig_channel_high_value(self):
        """Test RunConfig with high channel value (5GHz)."""
        config = RunConfig(channel=165)
        assert config.channel == 165

    def test_runconfig_interface_special_name(self):
        """Test RunConfig with special interface name."""
        config = RunConfig(interface="wlan0mon")
        assert config.interface == "wlan0mon"

    def test_runconfig_interface_with_spaces(self):
        """Test RunConfig with interface name containing spaces."""
        config = RunConfig(interface="Wi-Fi Adapter")
        assert config.interface == "Wi-Fi Adapter"


class TestParseArgs:
    """Tests for the parse_args function."""

    def test_parse_args_no_arguments(self, monkeypatch):
        """Test parse_args with no command line arguments."""
        monkeypatch.setattr(sys, "argv", ["prog"])
        config = parse_args()
        assert isinstance(config, RunConfig)
        assert config.interface is None
        assert config.channel is None
        assert config.verbose is False

    def test_parse_args_interface_short(self, monkeypatch):
        """Test parse_args with short interface flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "-i", "wlan0"])
        config = parse_args()
        assert config.interface == "wlan0"

    def test_parse_args_interface_long(self, monkeypatch):
        """Test parse_args with long interface flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "--interface", "wlan1"])
        config = parse_args()
        assert config.interface == "wlan1"

    def test_parse_args_channel_short(self, monkeypatch):
        """Test parse_args with short channel flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "-c", "6"])
        config = parse_args()
        assert config.channel == 6

    def test_parse_args_channel_long(self, monkeypatch):
        """Test parse_args with long channel flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "--channel", "11"])
        config = parse_args()
        assert config.channel == 11

    def test_parse_args_verbose_short(self, monkeypatch):
        """Test parse_args with short verbose flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "-v"])
        config = parse_args()
        assert config.verbose is True

    def test_parse_args_verbose_long(self, monkeypatch):
        """Test parse_args with long verbose flag."""
        monkeypatch.setattr(sys, "argv", ["prog", "--verbose"])
        config = parse_args()
        assert config.verbose is True

    def test_parse_args_all_options(self, monkeypatch):
        """Test parse_args with all options set."""
        monkeypatch.setattr(sys, "argv", ["prog", "-i", "wlan0", "-c", "6", "-v"])
        config = parse_args()
        assert config.interface == "wlan0"
        assert config.channel == 6
        assert config.verbose is True

    def test_parse_args_mixed_short_long(self, monkeypatch):
        """Test parse_args with mixed short and long flags."""
        monkeypatch.setattr(
            sys, "argv", ["prog", "--interface", "eth0", "-c", "1", "--verbose"]
        )
        config = parse_args()
        assert config.interface == "eth0"
        assert config.channel == 1
        assert config.verbose is True

    def test_parse_args_interface_monitor_mode(self, monkeypatch):
        """Test parse_args with monitor mode interface."""
        monkeypatch.setattr(sys, "argv", ["prog", "-i", "wlan0mon"])
        config = parse_args()
        assert config.interface == "wlan0mon"

    def test_parse_args_high_channel(self, monkeypatch):
        """Test parse_args with high channel number."""
        monkeypatch.setattr(sys, "argv", ["prog", "-c", "149"])
        config = parse_args()
        assert config.channel == 149

    def test_parse_args_channel_zero(self, monkeypatch):
        """Test parse_args with channel zero."""
        monkeypatch.setattr(sys, "argv", ["prog", "-c", "0"])
        config = parse_args()
        assert config.channel == 0

    def test_parse_args_returns_runconfig(self, monkeypatch):
        """Test that parse_args returns a RunConfig instance."""
        monkeypatch.setattr(sys, "argv", ["prog"])
        config = parse_args()
        assert isinstance(config, RunConfig)

    def test_parse_args_order_independence(self, monkeypatch):
        """Test that argument order doesn't matter."""
        monkeypatch.setattr(sys, "argv", ["prog", "-v", "-c", "6", "-i", "wlan0"])
        config = parse_args()
        assert config.interface == "wlan0"
        assert config.channel == 6
        assert config.verbose is True


class TestParseArgsEdgeCases:
    """Edge case tests for parse_args."""

    def test_parse_args_duplicate_interface(self, monkeypatch):
        """Test parse_args with duplicate interface flags (last wins)."""
        monkeypatch.setattr(sys, "argv", ["prog", "-i", "wlan0", "-i", "wlan1"])
        config = parse_args()
        assert config.interface == "wlan1"

    def test_parse_args_duplicate_channel(self, monkeypatch):
        """Test parse_args with duplicate channel flags (last wins)."""
        monkeypatch.setattr(sys, "argv", ["prog", "-c", "6", "-c", "11"])
        config = parse_args()
        assert config.channel == 11

    def test_parse_args_negative_channel(self, monkeypatch):
        """Test parse_args with negative channel."""
        monkeypatch.setattr(sys, "argv", ["prog", "-c", "-1"])
        config = parse_args()
        assert config.channel == -1

    def test_parse_args_interface_with_numbers(self, monkeypatch):
        """Test parse_args with interface containing numbers."""
        monkeypatch.setattr(sys, "argv", ["prog", "-i", "wlan123"])
        config = parse_args()
        assert config.interface == "wlan123"
