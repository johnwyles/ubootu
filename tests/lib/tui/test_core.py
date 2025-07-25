"""
Unit tests for tui/core.py - Main TUI orchestrator
"""

from __future__ import annotations

import curses
import os
import sys
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from lib.tui.core import UbootuTUI, main, run_tui
from lib.tui.models import MenuItem


class TestUbootuTUI:
    """Test the main UbootuTUI class."""

    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock curses screen."""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 100)
        stdscr.getch.return_value = -1
        return stdscr

    @pytest.fixture
    def mock_dependencies(self):
        """Mock all TUI dependencies."""
        with patch("lib.tui.core.MenuRegistry") as mock_registry, patch(
            "lib.tui.core.TUIConfigManager"
        ) as mock_config, patch("lib.tui.core.TUIRenderer") as mock_renderer, patch(
            "lib.tui.core.TUIDialogs"
        ) as mock_dialogs, patch(
            "lib.tui.core.TUIEventHandler"
        ) as mock_handler:

            # Setup menu registry
            mock_registry_instance = Mock()
            mock_registry_instance.builders = {}
            mock_registry.return_value = mock_registry_instance

            yield {
                "registry": mock_registry,
                "config": mock_config,
                "renderer": mock_renderer,
                "dialogs": mock_dialogs,
                "handler": mock_handler,
            }

    def test_initialization(self, mock_stdscr, mock_dependencies):
        """Test TUI initialization."""
        tui = UbootuTUI(mock_stdscr)

        assert tui.stdscr == mock_stdscr
        assert tui.selected_sections is None
        assert tui.cancelled is False
        assert isinstance(tui.menu_items, dict)
        assert "root" in tui.menu_items
        assert "actions" in tui.menu_items

    def test_initialization_with_sections(self, mock_stdscr, mock_dependencies):
        """Test TUI initialization with selected sections."""
        tui = UbootuTUI(mock_stdscr, selected_sections=["development", "desktop"])

        assert tui.selected_sections == ["development", "desktop"]
        root = tui.menu_items["root"]
        assert "development" in root.children
        assert "desktop" in root.children

    def test_build_menu_structure(self, mock_stdscr, mock_dependencies):
        """Test menu structure building."""
        tui = UbootuTUI(mock_stdscr)

        # Check root menu
        assert "root" in tui.menu_items
        root = tui.menu_items["root"]
        assert root.is_category
        assert len(root.children) >= 5  # At least 5 main sections

        # Check actions menu
        assert "actions" in tui.menu_items
        assert "action-install" in tui.menu_items
        assert "action-save" in tui.menu_items
        assert "action-reset" in tui.menu_items
        assert "action-exit" in tui.menu_items

    def test_themes_section_mapping(self, mock_stdscr, mock_dependencies):
        """Test that 'themes' section maps to 'desktop'."""
        tui = UbootuTUI(mock_stdscr, selected_sections=["themes"])

        root = tui.menu_items["root"]
        assert "desktop" in root.children
        assert "themes" not in root.children  # themes is mapped to desktop

    def test_setup_screen(self, mock_stdscr, mock_dependencies):
        """Test screen setup."""
        # Need to patch curses.curs_set since it's called in _setup_screen
        with patch("curses.curs_set"):
            tui = UbootuTUI(mock_stdscr)

        # Verify curses setup calls
        mock_stdscr.keypad.assert_called_once_with(True)
        mock_stdscr.timeout.assert_called_once_with(50)

    def test_setup_screen_small_terminal(self, mock_stdscr, mock_dependencies):
        """Test screen setup with small terminal."""
        mock_stdscr.getmaxyx.return_value = (10, 40)  # Too small

        # Should not raise exception
        tui = UbootuTUI(mock_stdscr)
        assert tui is not None

    def test_sync_component_state(self, mock_stdscr, mock_dependencies):
        """Test component state synchronization."""
        tui = UbootuTUI(mock_stdscr)

        # Set some state in config manager
        tui.config_manager.current_menu = "development"
        tui.config_manager.current_item = 2

        # Sync state
        tui._sync_component_state()

        # Verify state propagated to other components
        assert tui.renderer.current_menu == "development"
        assert tui.renderer.current_item == 2
        assert tui.event_handler.current_menu == "development"
        assert tui.event_handler.current_item == 2

    def test_run_main_loop(self, mock_stdscr, mock_dependencies):
        """Test main TUI loop."""
        tui = UbootuTUI(mock_stdscr)

        # Mock event handler to exit after first key
        tui.event_handler.handle_key.return_value = False
        mock_stdscr.getch.return_value = ord("q")

        exit_code = tui.run()

        assert exit_code == 0  # Normal exit
        mock_stdscr.clear.assert_called()
        tui.renderer.draw_header.assert_called()
        tui.renderer.draw_menu.assert_called()
        tui.event_handler.handle_key.assert_called()

    def test_run_with_keyboard_interrupt(self, mock_stdscr, mock_dependencies):
        """Test handling KeyboardInterrupt."""
        tui = UbootuTUI(mock_stdscr)

        # Make getch raise KeyboardInterrupt
        mock_stdscr.getch.side_effect = KeyboardInterrupt()

        exit_code = tui.run()

        assert exit_code == 1  # Cancelled
        assert tui.cancelled is True

    def test_run_with_exception(self, mock_stdscr, mock_dependencies):
        """Test handling general exceptions."""
        tui = UbootuTUI(mock_stdscr)

        # Make getch raise an exception
        mock_stdscr.getch.side_effect = Exception("Test error")

        exit_code = tui.run()

        assert exit_code == 1  # Cancelled
        assert tui.cancelled is True

    def test_draw_interface(self, mock_stdscr, mock_dependencies):
        """Test interface drawing."""
        tui = UbootuTUI(mock_stdscr)

        # Mock menu items
        tui.config_manager.get_current_menu_items.return_value = [
            MenuItem("item1", "Item 1", "Description")
        ]

        tui._draw_interface()

        tui.renderer.draw_header.assert_called_once()
        tui.renderer.draw_menu.assert_called_once()
        tui.renderer.draw_help.assert_called_once()
        tui.renderer.draw_stats.assert_called_once()
        mock_stdscr.refresh.assert_called_once()


class TestRunTUI:
    """Test the run_tui function."""

    @patch("curses.wrapper")
    def test_run_tui_basic(self, mock_wrapper):
        """Test basic run_tui call."""
        mock_wrapper.return_value = 0

        result = run_tui()

        assert result == 0
        mock_wrapper.assert_called_once()

    @patch("curses.wrapper")
    def test_run_tui_with_sections(self, mock_wrapper):
        """Test run_tui with selected sections."""
        mock_wrapper.return_value = 0

        result = run_tui(["development", "desktop"])

        assert result == 0
        mock_wrapper.assert_called_once()


class TestMain:
    """Test the main entry point."""

    @patch("sys.argv", ["configure_standard_tui.py", "--help"])
    def test_help_flag(self, capsys):
        """Test --help flag."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Ubootu Configuration Tool" in captured.out
        assert "Available sections:" in captured.out

    @patch("sys.stdout.isatty", return_value=False)
    @patch("os.environ.get", return_value=None)
    def test_not_in_terminal(self, mock_get, mock_isatty, capsys):
        """Test running outside terminal."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Not running in a terminal" in captured.out

    @patch("sys.stdout.isatty", return_value=False)
    @patch("os.environ.get", return_value="1")
    @patch("lib.tui.core.run_tui", return_value=0)
    def test_force_tui(self, mock_run_tui, mock_get, mock_isatty):
        """Test FORCE_TUI environment variable."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_run_tui.assert_called_once()

    @patch("sys.stdout.isatty", return_value=True)
    @patch(
        "lib.terminal_check.can_run_tui",
        return_value=(False, ["Terminal not compatible"], []),
    )
    def test_terminal_not_compatible(self, mock_can_run, mock_isatty, capsys):
        """Test terminal compatibility check failure."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Terminal is not compatible" in captured.out
        assert "Terminal not compatible" in captured.out

    @patch("sys.stdout.isatty", return_value=True)
    @patch("lib.terminal_check.can_run_tui", return_value=(True, [], ["SSH detected"]))
    @patch("lib.tui.core.run_tui", return_value=0)
    def test_terminal_warnings(self, mock_run_tui, mock_can_run, mock_isatty, capsys):
        """Test terminal compatibility warnings."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Warning: SSH detected" in captured.out
        mock_run_tui.assert_called_once()

    @patch("sys.argv", ["configure_standard_tui.py", "development", "desktop"])
    @patch("sys.stdout.isatty", return_value=True)
    @patch("lib.terminal_check.can_run_tui", return_value=(True, [], []))
    @patch("lib.tui.core.run_tui", return_value=0)
    def test_with_sections(self, mock_run_tui, mock_can_run, mock_isatty):
        """Test running with section arguments."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_run_tui.assert_called_once_with(["development", "desktop"])

    @patch("sys.stdout.isatty", return_value=True)
    @patch("lib.terminal_check.can_run_tui", side_effect=Exception("Check failed"))
    @patch("lib.tui.core.run_tui", return_value=0)
    def test_terminal_check_exception(
        self, mock_run_tui, mock_can_run, mock_isatty, capsys
    ):
        """Test when terminal check raises exception."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Warning: Could not check terminal compatibility" in captured.out
        mock_run_tui.assert_called_once()

    @patch("sys.stdout.isatty", return_value=True)
    @patch("lib.terminal_check.can_run_tui", return_value=(True, [], []))
    @patch("lib.tui.core.run_tui", side_effect=Exception("Curses error"))
    def test_run_tui_exception(self, mock_run_tui, mock_can_run, mock_isatty, capsys):
        """Test when run_tui raises exception."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Failed to run TUI" in captured.out
        assert "Curses error" in captured.out
