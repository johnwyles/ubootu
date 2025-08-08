#!/usr/bin/env python3
"""Tests for lib/tui/sudo_dialog.py"""

import curses
import subprocess
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from lib.tui.sudo_dialog import SudoDialog


class TestSudoDialogInit:
    """Test SudoDialog initialization"""

    def test_init_basic(self):
        """Test basic initialization"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)

        assert dialog.stdscr == stdscr
        assert dialog.height == 24
        assert dialog.width == 80
        assert dialog.enable_caching is False
        assert dialog._cached_password is None


class TestGetPassword:
    """Test get_password method"""

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_enter_key(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test password entry with Enter key"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [ord("p"), ord("a"), ord("s"), ord("s"), ord("\n")]  # Type "pass"  # Press Enter

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()
        mock_curses.echo = MagicMock()
        mock_curses.KEY_BACKSPACE = 263
        mock_curses.KEY_DC = 330
        mock_curses.KEY_LEFT = 260
        mock_curses.KEY_RIGHT = 261
        mock_curses.KEY_HOME = 262
        mock_curses.KEY_END = 358

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password == "pass"
        stdscr.clear.assert_called()
        stdscr.refresh.assert_called()
        mock_curses.curs_set.assert_any_call(1)  # Enable cursor
        mock_curses.curs_set.assert_any_call(0)  # Disable cursor

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_escape_key(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test password entry cancelled with ESC key"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [ord("p"), ord("a"), 27]  # Type "pa"  # Press ESC

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password is None
        mock_curses.curs_set.assert_any_call(0)  # Disable cursor

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_with_backspace(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test password entry with backspace"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [
            ord("p"),
            ord("a"),
            ord("s"),
            ord("t"),  # Type "past"
            127,  # Backspace (remove 't')
            ord("s"),  # Type 's' to make "pass"
            ord("\n"),  # Press Enter
        ]

        mock_get_pos.return_value = (5, 10)
        mock_curses.KEY_BACKSPACE = 263
        mock_curses.curs_set = MagicMock()

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password == "pass"

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_cached(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test cached password retrieval"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        dialog.enable_caching = True
        dialog._cached_password = "cached_pass"

        password = dialog.get_password()

        assert password == "cached_pass"
        # Should not call clear/refresh when using cache
        stdscr.clear.assert_not_called()
        stdscr.refresh.assert_not_called()

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_keyboard_interrupt(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test password entry interrupted by KeyboardInterrupt"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = KeyboardInterrupt()

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password is None
        mock_curses.curs_set.assert_any_call(0)  # Disable cursor

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_get_password_with_navigation(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test password entry with cursor navigation"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [
            ord("p"),
            ord("a"),
            ord("s"),
            ord("s"),  # Type "pass"
            260,  # KEY_LEFT
            260,  # KEY_LEFT again
            ord("x"),  # Insert 'x' in middle to make "paxss"
            261,  # KEY_RIGHT
            330,  # KEY_DC (delete) to remove 's' making "paxs"
            358,  # KEY_END to go to end
            ord("t"),  # Add 't' at end to make "paxst"
            262,  # KEY_HOME to go to beginning
            ord("\n"),  # Press Enter
        ]

        mock_get_pos.return_value = (5, 10)
        mock_curses.KEY_BACKSPACE = 263
        mock_curses.KEY_DC = 330
        mock_curses.KEY_LEFT = 260
        mock_curses.KEY_RIGHT = 261
        mock_curses.KEY_HOME = 262
        mock_curses.KEY_END = 358
        mock_curses.curs_set = MagicMock()

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password == "paxst"

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_password_masking(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test that password is displayed as asterisks"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [ord("p"), ord("a"), ord("s"), ord("s"), ord("\n")]

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        # Check that asterisks were displayed
        asterisk_calls = [call for call in stdscr.addstr.call_args_list if len(call[0]) >= 3 and "*" in call[0][2]]
        assert len(asterisk_calls) > 0
        assert password == "pass"


class TestClearCache:
    """Test clear_cache method"""

    def test_clear_cache(self):
        """Test clearing cached password"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        dialog._cached_password = "some_password"

        dialog.clear_cache()

        assert dialog._cached_password is None


class TestExecuteWithSudo:
    """Test execute_with_sudo method"""

    @patch("lib.tui.sudo_dialog.subprocess.run")
    def test_execute_with_sudo_success(self, mock_run):
        """Test successful sudo command execution"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        dialog = SudoDialog(stdscr)
        dialog._cached_password = "test_pass"
        dialog.enable_caching = True

        result = dialog.execute_with_sudo("ls -la")

        assert result == mock_result
        mock_run.assert_called_once_with(
            ["sudo", "-S", "ls", "-la"], input="test_pass\n", text=True, capture_output=True
        )

    @patch("lib.tui.sudo_dialog.subprocess.run")
    def test_execute_with_sudo_password_cancelled(self, mock_run):
        """Test sudo command when password entry is cancelled"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        # Mock get_password to return None (cancelled)
        with patch.object(dialog, "get_password", return_value=None):
            result = dialog.execute_with_sudo("ls -la")

        assert result is None
        mock_run.assert_not_called()

    @patch("lib.tui.sudo_dialog.subprocess.run")
    @patch("lib.tui.dialogs.MessageDialog")
    def test_execute_with_sudo_command_failure(self, mock_msg_dialog, mock_run):
        """Test sudo command execution failure with error display"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Permission denied"
        mock_run.return_value = mock_result

        mock_dialog_instance = MagicMock()
        mock_msg_dialog.return_value = mock_dialog_instance

        dialog = SudoDialog(stdscr)
        dialog._cached_password = "test_pass"
        dialog.enable_caching = True

        result = dialog.execute_with_sudo("rm /protected/file", show_output=True)

        assert result == mock_result
        mock_dialog_instance.show.assert_called_once()
        call_args = mock_dialog_instance.show.call_args[0]
        assert call_args[0] == "Error"
        assert "Command failed" in call_args[1]
        assert call_args[2] == "error"

    @patch("lib.tui.sudo_dialog.subprocess.run")
    @patch("lib.tui.dialogs.MessageDialog")
    def test_execute_with_sudo_exception(self, mock_msg_dialog, mock_run):
        """Test sudo command execution with exception"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        mock_run.side_effect = Exception("Command not found")

        mock_dialog_instance = MagicMock()
        mock_msg_dialog.return_value = mock_dialog_instance

        dialog = SudoDialog(stdscr)
        dialog._cached_password = "test_pass"
        dialog.enable_caching = True

        result = dialog.execute_with_sudo("nonexistent_command")

        assert result is None
        mock_dialog_instance.show.assert_called_once()
        call_args = mock_dialog_instance.show.call_args[0]
        assert call_args[0] == "Error"
        assert "Failed to execute command" in call_args[1]


class TestTestSudoPassword:
    """Test test_sudo_password method"""

    @patch("lib.tui.sudo_dialog.subprocess.run")
    def test_test_sudo_password_valid(self, mock_run):
        """Test valid sudo password"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        is_valid = dialog.test_sudo_password("correct_pass")

        assert is_valid is True
        mock_run.assert_called_once_with(["sudo", "-S", "true"], input="correct_pass\n", text=True, capture_output=True)

    @patch("lib.tui.sudo_dialog.subprocess.run")
    def test_test_sudo_password_invalid(self, mock_run):
        """Test invalid sudo password"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        is_valid = dialog.test_sudo_password("wrong_pass")

        assert is_valid is False

    @patch("lib.tui.sudo_dialog.subprocess.run")
    def test_test_sudo_password_exception(self, mock_run):
        """Test sudo password test with exception"""
        mock_run.side_effect = Exception("Sudo not found")

        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)

        dialog = SudoDialog(stdscr)
        is_valid = dialog.test_sudo_password("any_pass")

        assert is_valid is False


class TestMessageWrapping:
    """Test message wrapping in get_password"""

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_long_message_wrapping(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test that long messages are wrapped correctly"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [ord("\n")]  # Just press Enter

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()
        mock_curses.KEY_BACKSPACE = 263
        mock_curses.KEY_DC = 330
        mock_curses.KEY_LEFT = 260
        mock_curses.KEY_RIGHT = 261
        mock_curses.KEY_HOME = 262
        mock_curses.KEY_END = 358

        dialog = SudoDialog(stdscr)
        long_message = (
            "This is a very long message that should be wrapped across multiple lines when displayed in the dialog box"
        )
        password = dialog.get_password(long_message)

        # Check that addstr was called multiple times for wrapped lines
        addstr_calls = [call for call in stdscr.addstr.call_args_list if len(call[0]) == 3]
        assert len(addstr_calls) > 1  # Message should be wrapped

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_narrow_screen_handling(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test dialog behavior on narrow screen"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 40)  # Narrow screen
        stdscr.getch.side_effect = [ord("\n")]  # Just press Enter

        mock_get_pos.return_value = (5, 2)
        mock_curses.curs_set = MagicMock()
        mock_curses.KEY_BACKSPACE = 263
        mock_curses.KEY_DC = 330
        mock_curses.KEY_LEFT = 260
        mock_curses.KEY_RIGHT = 261
        mock_curses.KEY_HOME = 262
        mock_curses.KEY_END = 358

        dialog = SudoDialog(stdscr)
        password = dialog.get_password("Enter password:")

        # Should adapt to narrow screen
        assert dialog.width == 40
        # Dialog should be created successfully
        assert password == ""

    @patch("lib.tui.sudo_dialog.draw_box")
    @patch("lib.tui.sudo_dialog.get_dialog_position")
    @patch("lib.tui.sudo_dialog.curses")
    def test_empty_password(self, mock_curses, mock_get_pos, mock_draw_box):
        """Test empty password handling"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.side_effect = [ord("\n")]  # Just press Enter

        mock_get_pos.return_value = (5, 10)
        mock_curses.curs_set = MagicMock()
        mock_curses.KEY_BACKSPACE = 263

        dialog = SudoDialog(stdscr)
        password = dialog.get_password()

        assert password == ""
