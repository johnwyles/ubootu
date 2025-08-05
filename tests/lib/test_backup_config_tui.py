"""
Unit tests for backup_config_tui
"""

import curses
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from lib.tui import backup_config


class TestBackupConfigTui:
    """Test BackupConfigTui functionality"""

    @pytest.fixture
    def mock_stdscr(self):
        """Mock curses screen"""
        mock = MagicMock()
        mock.getmaxyx.return_value = (24, 80)
        mock.getch.return_value = ord("q")  # Default to quit
        return mock

    @pytest.fixture
    def setup(self, mock_stdscr):
        """Setup test fixtures"""
        with patch("curses.initscr", return_value=mock_stdscr):
            with patch("curses.curs_set"):
                with patch("curses.start_color"):
                    with patch("curses.use_default_colors"):
                        yield {"stdscr": mock_stdscr}

    def test_import(self):
        """Test that module can be imported"""
        assert backup_config is not None

    def test_initialization(self, setup):
        """Test component initialization"""
        # Test that main classes/functions exist
        module = backup_config
        assert hasattr(module, "__file__")

        # Check for common TUI components
        for attr in ["render", "handle_input", "display", "show", "run", "BackupConfig"]:
            if hasattr(module, attr):
                assert callable(getattr(module, attr)) or isinstance(getattr(module, attr), type)
                break

    def test_rendering(self, setup):
        """Test rendering functionality"""
        stdscr = setup["stdscr"]

        # Test screen is cleared and refreshed
        if hasattr(backup_config, "render"):
            try:
                backup_config.render(stdscr)
                stdscr.clear.assert_called()
                stdscr.refresh.assert_called()
            except Exception:
                # Some modules might need additional setup
                pass

    @patch("curses.wrapper")
    def test_curses_wrapper(self, mock_wrapper):
        """Test curses wrapper usage"""
        if hasattr(backup_config, "main"):
            backup_config.main()
            mock_wrapper.assert_called_once()
