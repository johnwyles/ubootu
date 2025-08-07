#!/usr/bin/env python3
"""
Functional tests for sudo_dialog module
Tests sudo password dialog functionality
"""

import curses
from unittest.mock import MagicMock, Mock, patch

import pytest

# Mock curses constants that aren't available without initscr
if not hasattr(curses, 'ACS_ULCORNER'):
    curses.ACS_ULCORNER = ord('+')
    curses.ACS_URCORNER = ord('+')
    curses.ACS_LLCORNER = ord('+')
    curses.ACS_LRCORNER = ord('+')
    curses.ACS_HLINE = ord('-')
    curses.ACS_VLINE = ord('|')
    curses.A_BOLD = 1
    curses.A_DIM = 2
    curses.A_REVERSE = 4
    curses.KEY_BACKSPACE = 263
    curses.KEY_DC = 330

from lib.tui.sudo_dialog import SudoDialog


class TestSudoDialogFunctional:
    """Test SudoDialog functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch.return_value = ord('\n')

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_init(self, mock_noecho, mock_echo, mock_curs_set):
        """Test SudoDialog initialization"""
        dialog = SudoDialog(self.stdscr)
        
        assert dialog.stdscr == self.stdscr
        assert dialog.height == 24
        assert dialog.width == 80

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_enter(self, mock_noecho, mock_echo, mock_curs_set):
        """Test getting password with Enter key"""
        dialog = SudoDialog(self.stdscr)
        
        # Simulate typing "pass" then Enter
        self.stdscr.getch.side_effect = [
            ord('p'), ord('a'), ord('s'), ord('s'), ord('\n')
        ]
        
        password = dialog.get_password()
        
        assert password == "pass"
        mock_noecho.assert_called()
        mock_echo.assert_called()
        mock_curs_set.assert_called()

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_escape(self, mock_noecho, mock_echo, mock_curs_set):
        """Test cancelling password entry with ESC"""
        dialog = SudoDialog(self.stdscr)
        
        # Simulate ESC key
        self.stdscr.getch.return_value = 27
        
        password = dialog.get_password()
        
        assert password is None

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_with_message(self, mock_noecho, mock_echo, mock_curs_set):
        """Test getting password with custom message"""
        dialog = SudoDialog(self.stdscr)
        
        self.stdscr.getch.side_effect = [ord('t'), ord('e'), ord('s'), ord('t'), ord('\n')]
        
        password = dialog.get_password(message="Custom sudo prompt:")
        
        assert password == "test"
        # Check that custom message was drawn
        addstr_calls = [str(call) for call in self.stdscr.addstr.call_args_list]
        assert any("Custom sudo prompt:" in str(call) for call in addstr_calls)

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_backspace(self, mock_noecho, mock_echo, mock_curs_set):
        """Test backspace handling in password entry"""
        dialog = SudoDialog(self.stdscr)
        
        # Type "test", backspace, then "s" and Enter
        self.stdscr.getch.side_effect = [
            ord('t'), ord('e'), ord('s'), ord('t'),
            curses.KEY_BACKSPACE,
            ord('s'), ord('\n')
        ]
        
        password = dialog.get_password()
        
        assert password == "tess"

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_delete_key(self, mock_noecho, mock_echo, mock_curs_set):
        """Test delete key handling in password entry"""
        dialog = SudoDialog(self.stdscr)
        
        # Type "test", delete, then Enter
        self.stdscr.getch.side_effect = [
            ord('t'), ord('e'), ord('s'), ord('t'),
            curses.KEY_DC,
            ord('\n')
        ]
        
        password = dialog.get_password()
        
        # Delete key typically doesn't work in password mode
        assert password == "test"

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_with_title(self, mock_noecho, mock_echo, mock_curs_set):
        """Test password dialog with custom title"""
        dialog = SudoDialog(self.stdscr)
        
        self.stdscr.getch.side_effect = [ord('p'), ord('w'), ord('d'), ord('\n')]
        
        password = dialog.get_password(title="Admin Access Required")
        
        assert password == "pwd"
        # Check that title was drawn
        addstr_calls = self.stdscr.addstr.call_args_list
        assert any("Admin Access" in str(call) for call in addstr_calls)

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_max_length(self, mock_noecho, mock_echo, mock_curs_set):
        """Test password max length handling"""
        dialog = SudoDialog(self.stdscr)
        
        # Try to type a very long password
        long_input = [ord('a')] * 100 + [ord('\n')]
        self.stdscr.getch.side_effect = long_input
        
        password = dialog.get_password()
        
        # Should truncate to reasonable length
        assert len(password) <= 256

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_special_chars(self, mock_noecho, mock_echo, mock_curs_set):
        """Test password with special characters"""
        dialog = SudoDialog(self.stdscr)
        
        # Type password with special chars
        self.stdscr.getch.side_effect = [
            ord('P'), ord('@'), ord('$'), ord('$'), 
            ord('!'), ord('2'), ord('3'), ord('\n')
        ]
        
        password = dialog.get_password()
        
        assert password == "P@$$!23"

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_empty(self, mock_noecho, mock_echo, mock_curs_set):
        """Test empty password entry"""
        dialog = SudoDialog(self.stdscr)
        
        # Just press Enter
        self.stdscr.getch.return_value = ord('\n')
        
        password = dialog.get_password()
        
        assert password == ""

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_with_error(self, mock_noecho, mock_echo, mock_curs_set):
        """Test password dialog with error message"""
        dialog = SudoDialog(self.stdscr)
        
        self.stdscr.getch.side_effect = [ord('t'), ord('e'), ord('s'), ord('t'), ord('\n')]
        
        password = dialog.get_password(error_msg="Authentication failed. Try again.")
        
        assert password == "test"
        # Check that error message was displayed
        addstr_calls = self.stdscr.addstr.call_args_list
        assert any("Authentication failed" in str(call) for call in addstr_calls)

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_draw_password_box(self, mock_noecho, mock_echo, mock_curs_set):
        """Test drawing the password dialog box"""
        dialog = SudoDialog(self.stdscr)
        
        dialog.draw_password_box("Enter Password:", "")
        
        # Check that box corners were drawn
        self.stdscr.addch.assert_any_call(9, 20, curses.ACS_ULCORNER)
        self.stdscr.addch.assert_any_call(9, 59, curses.ACS_URCORNER)
        self.stdscr.addch.assert_any_call(14, 20, curses.ACS_LLCORNER)
        self.stdscr.addch.assert_any_call(14, 59, curses.ACS_LRCORNER)

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_get_password_handles_curses_error(self, mock_noecho, mock_echo, mock_curs_set):
        """Test that curses errors are handled gracefully"""
        dialog = SudoDialog(self.stdscr)
        
        # Make addstr raise curses.error
        self.stdscr.addstr.side_effect = curses.error
        self.stdscr.getch.side_effect = [ord('t'), ord('e'), ord('s'), ord('t'), ord('\n')]
        
        # Should not raise exception
        password = dialog.get_password()
        
        assert password == "test"

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_validate_sudo_password(self, mock_noecho, mock_echo, mock_curs_set):
        """Test sudo password validation"""
        dialog = SudoDialog(self.stdscr)
        
        # Mock subprocess to simulate successful sudo
        with patch('lib.tui.sudo_dialog.subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = dialog.validate_sudo_password("testpass")
            
            assert result is True
            mock_run.assert_called_once()

    @patch('lib.tui.sudo_dialog.curses.curs_set')
    @patch('lib.tui.sudo_dialog.curses.echo')
    @patch('lib.tui.sudo_dialog.curses.noecho')
    def test_validate_sudo_password_fail(self, mock_noecho, mock_echo, mock_curs_set):
        """Test sudo password validation failure"""
        dialog = SudoDialog(self.stdscr)
        
        # Mock subprocess to simulate failed sudo
        with patch('lib.tui.sudo_dialog.subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            
            result = dialog.validate_sudo_password("wrongpass")
            
            assert result is False