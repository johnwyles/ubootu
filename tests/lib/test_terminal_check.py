"""
Unit tests for terminal_check module
"""

from __future__ import annotations

import curses
import os
import sys
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from lib.terminal_check import (can_run_tui, check_terminal_capabilities,
                                print_compatibility_report, test_curses_basic)


class TestCheckTerminalCapabilities:
    """Test the check_terminal_capabilities function."""

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", return_value=("en_US", "UTF-8"))
    def test_ideal_terminal(self, mock_locale, mock_size, mock_isatty):
        """Test with ideal terminal conditions."""
        mock_size.return_value = Mock(columns=120, lines=40)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert warnings == []

    @patch("sys.stdout.isatty", return_value=False)
    @patch.dict(os.environ, {}, clear=True)
    def test_not_tty_without_force(self, mock_isatty):
        """Test when not in TTY and FORCE_TUI not set."""
        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Output may not be connected to terminal" in warnings

    @patch("sys.stdout.isatty", return_value=False)
    @patch.dict(os.environ, {"FORCE_TUI": "1"}, clear=True)
    def test_not_tty_with_force(self, mock_isatty):
        """Test when not in TTY but FORCE_TUI is set."""
        issues, warnings = check_terminal_capabilities()

        # Should not warn about TTY when FORCE_TUI is set
        assert not any("connected to terminal" in w for w in warnings)

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {}, clear=True)
    def test_no_term_variable(self, mock_isatty):
        """Test when TERM environment variable is not set."""
        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "TERM environment variable not set" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "dumb"}, clear=True)
    def test_dumb_terminal(self, mock_isatty):
        """Test with dumb terminal."""
        issues, warnings = check_terminal_capabilities()

        assert "Terminal type is 'dumb' - no advanced features supported" in issues
        assert len(issues) == 1

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "obscure-term"}, clear=True)
    @patch("os.get_terminal_size")
    def test_uncommon_terminal(self, mock_size, mock_isatty):
        """Test with uncommon terminal type."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Uncommon terminal type: obscure-term" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size")
    def test_small_terminal(self, mock_size, mock_isatty):
        """Test with small terminal size."""
        mock_size.return_value = Mock(columns=60, lines=20)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Terminal width may be too small (60 columns)" in warnings
        assert "Terminal height may be too small (20 lines)" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size", side_effect=Exception("Cannot get size"))
    def test_terminal_size_error(self, mock_size, mock_isatty):
        """Test when terminal size cannot be determined."""
        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Cannot determine terminal size - will try anyway" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", return_value=(None, None))
    def test_no_locale(self, mock_locale, mock_size, mock_isatty):
        """Test with no locale set."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "No character encoding set in locale" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", return_value=("en_US", "ISO-8859-1"))
    def test_non_utf_locale(self, mock_locale, mock_size, mock_isatty):
        """Test with non-UTF locale."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Non-UTF locale detected: ISO-8859-1" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", side_effect=Exception("Locale error"))
    def test_locale_error(self, mock_locale, mock_size, mock_isatty):
        """Test when locale cannot be determined."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Cannot determine locale settings" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(
        os.environ, {"TERM": "xterm", "SSH_CLIENT": "192.168.1.1 22 22"}, clear=True
    )
    @patch("os.get_terminal_size")
    def test_ssh_session(self, mock_size, mock_isatty):
        """Test in SSH session."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Running over SSH - some features may not work correctly" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(os.environ, {"TERM": "xterm", "SSH_TTY": "/dev/pts/1"}, clear=True)
    @patch("os.get_terminal_size")
    def test_ssh_tty(self, mock_size, mock_isatty):
        """Test with SSH_TTY set."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Running over SSH - some features may not work correctly" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(
        os.environ, {"TERM": "screen", "STY": "12345.pts-0.hostname"}, clear=True
    )
    @patch("os.get_terminal_size")
    def test_gnu_screen(self, mock_size, mock_isatty):
        """Test inside GNU Screen."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Running inside GNU Screen" in warnings

    @patch("sys.stdout.isatty", return_value=True)
    @patch.dict(
        os.environ,
        {"TERM": "tmux-256color", "TMUX": "/tmp/tmux-1000/default"},
        clear=True,
    )
    @patch("os.get_terminal_size")
    def test_tmux(self, mock_size, mock_isatty):
        """Test inside tmux."""
        mock_size.return_value = Mock(columns=100, lines=30)

        issues, warnings = check_terminal_capabilities()

        assert issues == []
        assert "Running inside tmux" in warnings


class TestTestCursesBasic:
    """Test the test_curses_basic function."""

    @patch("curses.wrapper")
    def test_success_interactive(self, mock_wrapper):
        """Test successful curses test in interactive mode."""
        mock_wrapper.return_value = None

        success, error = test_curses_basic(interactive=True)

        assert success is True
        assert error is None
        mock_wrapper.assert_called_once()

    @patch("curses.wrapper")
    def test_success_non_interactive(self, mock_wrapper):
        """Test successful curses test in non-interactive mode."""
        mock_wrapper.return_value = None

        success, error = test_curses_basic(interactive=False)

        assert success is True
        assert error is None
        mock_wrapper.assert_called_once()

    @patch("curses.wrapper", side_effect=Exception("Curses error"))
    def test_curses_failure(self, mock_wrapper):
        """Test when curses fails."""
        success, error = test_curses_basic(interactive=False)

        assert success is False
        assert error == "Curses error"

    @patch("curses.has_colors", return_value=True)
    @patch("curses.start_color")
    @patch("curses.init_pair")
    @patch("curses.curs_set")
    @patch("curses.wrapper")
    def test_curses_screen_operations(self, mock_wrapper, mock_curs_set, mock_init_pair, mock_start_color, mock_has_colors):
        """Test that curses operations are performed correctly."""
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (30, 100)

        # Mock wrapper to call the function and simulate success
        def mock_wrapper_func(func):
            result = func(mock_stdscr)
            # Return None to simulate successful completion
            return result

        mock_wrapper.side_effect = mock_wrapper_func

        success, error = test_curses_basic(interactive=False)

        assert success is True
        assert error is None

        # Verify curses operations were called
        mock_stdscr.keypad.assert_called_once_with(True)
        mock_stdscr.clear.assert_called_once()
        mock_stdscr.box.assert_called_once()
        mock_stdscr.addstr.assert_any_call(1, 1, "Terminal Test")
        mock_stdscr.addstr.assert_any_call(2, 1, "[OK] Basic functionality working")
        mock_stdscr.refresh.assert_called_once()

        # In non-interactive mode, should not wait for key
        mock_stdscr.getch.assert_not_called()

    @patch("curses.wrapper")
    @patch("curses.curs_set")
    @patch("curses.has_colors", return_value=True)
    @patch("curses.start_color")
    @patch("curses.init_pair")
    def test_curses_with_colors(
        self,
        mock_init_pair,
        mock_start_color,
        mock_has_colors,
        mock_curs_set,
        mock_wrapper,
    ):
        """Test curses with color support."""
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (30, 100)

        def capture_func(func):
            func(mock_stdscr)
            return None

        mock_wrapper.side_effect = capture_func

        success, error = test_curses_basic(interactive=False)

        assert success is True
        assert error is None

        # Verify color initialization
        mock_has_colors.assert_called_once()
        mock_start_color.assert_called_once()
        mock_init_pair.assert_called_once_with(
            1, curses.COLOR_GREEN, curses.COLOR_BLACK
        )


class TestCanRunTUI:
    """Test the can_run_tui function."""

    @patch("lib.terminal_check.check_terminal_capabilities", return_value=([], []))
    @patch("lib.terminal_check.test_curses_basic", return_value=(True, None))
    def test_can_run_ideal(self, mock_curses_test, mock_check_caps):
        """Test when everything is ideal."""
        can_run, issues, warnings = can_run_tui()

        assert can_run is True
        assert issues == []
        assert warnings == []

    @patch(
        "lib.terminal_check.check_terminal_capabilities",
        return_value=(["Terminal is dumb"], ["SSH detected"]),
    )
    @patch("lib.terminal_check.test_curses_basic", return_value=(True, None))
    def test_cannot_run_with_issues(self, mock_curses_test, mock_check_caps):
        """Test when there are critical issues."""
        can_run, issues, warnings = can_run_tui()

        assert can_run is False
        assert issues == ["Terminal is dumb"]
        assert warnings == ["SSH detected"]

        # Should not test curses if there are issues
        mock_curses_test.assert_not_called()

    @patch(
        "lib.terminal_check.check_terminal_capabilities",
        return_value=([], ["SSH detected"]),
    )
    @patch(
        "lib.terminal_check.test_curses_basic", return_value=(False, "Curses failed")
    )
    def test_cannot_run_curses_failure(self, mock_curses_test, mock_check_caps):
        """Test when curses test fails."""
        can_run, issues, warnings = can_run_tui()

        assert can_run is False
        assert issues == ["Curses test failed: Curses failed"]
        assert warnings == ["SSH detected"]

    @patch(
        "lib.terminal_check.check_terminal_capabilities",
        return_value=([], ["Warning 1", "Warning 2"]),
    )
    @patch("lib.terminal_check.test_curses_basic", return_value=(True, None))
    def test_can_run_with_warnings(self, mock_curses_test, mock_check_caps):
        """Test when there are only warnings."""
        can_run, issues, warnings = can_run_tui()

        assert can_run is True
        assert issues == []
        assert warnings == ["Warning 1", "Warning 2"]


class TestPrintCompatibilityReport:
    """Test the print_compatibility_report function."""

    @patch("lib.terminal_check.can_run_tui", return_value=(True, [], []))
    @patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", return_value=("en_US", "UTF-8"))
    def test_compatible_terminal(self, mock_locale, mock_size, mock_can_run, capsys):
        """Test report for compatible terminal."""
        mock_size.return_value = Mock(columns=120, lines=40)

        exit_code = print_compatibility_report()

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Terminal Compatibility Check" in captured.out
        assert "Terminal: xterm-256color" in captured.out
        assert "Size: 120x40" in captured.out
        assert "[OK] Terminal appears compatible with TUI" in captured.out

    @patch(
        "lib.terminal_check.can_run_tui",
        return_value=(False, ["Terminal type is 'dumb'"], ["SSH detected"]),
    )
    @patch.dict(os.environ, {"TERM": "dumb"}, clear=True)
    @patch("os.get_terminal_size", side_effect=Exception("No size"))
    @patch("locale.getlocale", return_value=("en_US", "UTF-8"))
    def test_incompatible_terminal(self, mock_locale, mock_size, mock_can_run, capsys):
        """Test report for incompatible terminal."""
        exit_code = print_compatibility_report()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Terminal Compatibility Check" in captured.out
        assert "Terminal: dumb" in captured.out
        assert "Size: unknown" in captured.out
        assert "[CRITICAL ISSUES]" in captured.out
        assert "✗ Terminal type is 'dumb'" in captured.out
        assert "[WARNINGS]" in captured.out
        assert "! SSH detected" in captured.out
        assert "[FAIL] Terminal is not compatible with TUI" in captured.out
        assert "Suggestions:" in captured.out

    @patch(
        "lib.terminal_check.can_run_tui",
        return_value=(True, [], ["SSH detected", "Small terminal"]),
    )
    @patch.dict(os.environ, {"TERM": "xterm"}, clear=True)
    @patch("os.get_terminal_size")
    @patch("locale.getlocale", return_value=(None, None))
    def test_terminal_with_warnings(self, mock_locale, mock_size, mock_can_run, capsys):
        """Test report with warnings only."""
        mock_size.return_value = Mock(columns=70, lines=20)

        exit_code = print_compatibility_report()

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "[WARNINGS]" in captured.out
        assert "! SSH detected" in captured.out
        assert "! Small terminal" in captured.out
        assert "[OK] Terminal appears compatible with TUI" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
