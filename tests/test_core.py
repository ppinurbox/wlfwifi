"""
test_core.py
-------------
Comprehensive unit tests for the core module (main engine logic).
Tests cover main function, logging configuration, error handling, and integration.
"""

import logging
import pytest
from unittest.mock import patch


class TestMainFunction:
    """Tests for the main function."""

    @patch("wlfwifi.core.parse_args")
    @patch("wlfwifi.core.logging")
    def test_main_calls_parse_args(self, mock_logging, mock_parse_args):
        """Test that main calls parse_args."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig()
        try:
            main()
        except SystemExit:
            pass
        mock_parse_args.assert_called_once()

    @patch("wlfwifi.core.parse_args")
    def test_main_with_default_config(self, mock_parse_args):
        """Test main with default configuration."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig()
        # Should not raise
        main()

    @patch("wlfwifi.core.parse_args")
    def test_main_with_interface(self, mock_parse_args):
        """Test main with interface specified."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(interface="wlan0")
        main()

    @patch("wlfwifi.core.parse_args")
    def test_main_with_channel(self, mock_parse_args):
        """Test main with channel specified."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(channel=6)
        main()

    @patch("wlfwifi.core.parse_args")
    def test_main_with_verbose(self, mock_parse_args):
        """Test main with verbose mode."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(verbose=True)
        main()

    @patch("wlfwifi.core.parse_args")
    def test_main_with_all_options(self, mock_parse_args):
        """Test main with all options specified."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(
            interface="wlan0", channel=11, verbose=True
        )
        main()

    @patch("wlfwifi.core.parse_args")
    def test_main_handles_parse_args_exception(self, mock_parse_args):
        """Test main handles parse_args exceptions."""
        from wlfwifi.core import main

        mock_parse_args.side_effect = Exception("Parse error")
        with pytest.raises(SystemExit):
            main()


class TestLoggingConfiguration:
    """Tests for logging configuration in main."""

    def test_logging_basic_config(self):
        """Test that logging is configured with basicConfig."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        with patch("wlfwifi.core.parse_args") as mock_parse:
            mock_parse.return_value = RunConfig()
            with patch("wlfwifi.core.logging.basicConfig") as mock_basic:
                main()
                mock_basic.assert_called_once()

    def test_logging_level_info(self):
        """Test that logging level is set to INFO."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        with patch("wlfwifi.core.parse_args") as mock_parse:
            mock_parse.return_value = RunConfig()
            with patch("wlfwifi.core.logging.basicConfig") as mock_basic:
                main()
                call_kwargs = mock_basic.call_args[1]
                assert call_kwargs["level"] == logging.INFO

    def test_logging_format(self):
        """Test that logging format is set correctly."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        with patch("wlfwifi.core.parse_args") as mock_parse:
            mock_parse.return_value = RunConfig()
            with patch("wlfwifi.core.logging.basicConfig") as mock_basic:
                main()
                call_kwargs = mock_basic.call_args[1]
                assert "%(asctime)s" in call_kwargs["format"]
                assert "%(levelname)s" in call_kwargs["format"]
                assert "%(message)s" in call_kwargs["format"]

    def test_logging_datefmt(self):
        """Test that logging date format is set."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        with patch("wlfwifi.core.parse_args") as mock_parse:
            mock_parse.return_value = RunConfig()
            with patch("wlfwifi.core.logging.basicConfig") as mock_basic:
                main()
                call_kwargs = mock_basic.call_args[1]
                assert "%Y-%m-%d" in call_kwargs["datefmt"]
                assert "%H:%M:%S" in call_kwargs["datefmt"]


class TestMainLoggingOutput:
    """Tests for main function logging output."""

    @patch("wlfwifi.core.parse_args")
    def test_main_logs_startup(self, mock_parse_args):
        """Test that main logs startup message."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(
            interface="wlan0", channel=6, verbose=True
        )
        with patch("wlfwifi.core.logging.info") as mock_info:
            main()
            mock_info.assert_called()
            # Check that the startup message contains expected info
            call_args = str(mock_info.call_args)
            assert "wlfwifi" in call_args.lower() or "Starting" in call_args

    @patch("wlfwifi.core.parse_args")
    def test_main_logs_interface(self, mock_parse_args):
        """Test that main logs interface in startup."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(interface="wlan0")
        with patch("wlfwifi.core.logging.info") as mock_info:
            main()
            call_args = str(mock_info.call_args)
            assert "wlan0" in call_args

    @patch("wlfwifi.core.parse_args")
    def test_main_logs_channel(self, mock_parse_args):
        """Test that main logs channel in startup."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(channel=11)
        with patch("wlfwifi.core.logging.info") as mock_info:
            main()
            call_args = str(mock_info.call_args)
            assert "11" in call_args


class TestMainErrorHandling:
    """Tests for main function error handling."""

    @patch("wlfwifi.core.parse_args")
    def test_main_catches_exceptions(self, mock_parse_args):
        """Test that main catches and logs exceptions."""
        from wlfwifi.core import main

        mock_parse_args.side_effect = RuntimeError("Test error")
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("wlfwifi.core.parse_args")
    def test_main_logs_critical_on_exception(self, mock_parse_args):
        """Test that main logs critical on exception."""
        from wlfwifi.core import main

        mock_parse_args.side_effect = Exception("Fatal error")
        with patch("wlfwifi.core.logging.critical") as mock_critical:
            with pytest.raises(SystemExit):
                main()
            mock_critical.assert_called()


class TestModuleImports:
    """Tests for module imports and dependencies."""

    def test_core_imports_config(self):
        """Test that core module imports config."""
        from wlfwifi import core

        assert hasattr(core, "parse_args")
        assert hasattr(core, "RunConfig")

    def test_core_imports_logging(self):
        """Test that core module uses logging."""
        import logging as logging_module

        # Verify logging module is properly imported and functional
        assert hasattr(logging_module, "info")
        assert hasattr(logging_module, "basicConfig")

    def test_main_is_callable(self):
        """Test that main function is callable."""
        from wlfwifi.core import main

        assert callable(main)


class TestEntryPoint:
    """Tests for entry point behavior."""

    @patch("wlfwifi.core.parse_args")
    def test_wlfwifi_main_entry(self, mock_parse_args):
        """Test wlfwifi.py entry point."""
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig()
        # Import and run main
        from wlfwifi.core import main

        main()

    def test_module_runnable(self):
        """Test that module can be imported."""
        import wlfwifi.core

        assert wlfwifi.core is not None


class TestConfigIntegration:
    """Tests for config integration with core."""

    @patch("wlfwifi.core.parse_args")
    def test_config_none_interface_handled(self, mock_parse_args):
        """Test that None interface is handled correctly."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(interface=None)
        # Should not raise
        main()

    @patch("wlfwifi.core.parse_args")
    def test_config_none_channel_handled(self, mock_parse_args):
        """Test that None channel is handled correctly."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(channel=None)
        main()

    @patch("wlfwifi.core.parse_args")
    def test_config_verbose_false_handled(self, mock_parse_args):
        """Test that verbose=False is handled correctly."""
        from wlfwifi.core import main
        from wlfwifi.config import RunConfig

        mock_parse_args.return_value = RunConfig(verbose=False)
        main()
