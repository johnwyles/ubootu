#!/usr/bin/env python3
"""
Tests for the curses-based sudo dialog
"""

import curses
import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, call, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))


class TestSudoDialog(unittest.TestCase):
    """Test the sudo password dialog"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_password_masking(self):
        """Password input is masked with asterisks"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Mock user typing "password"
        password_chars = [ord("p"), ord("a"), ord("s"), ord("s"), ord("w"), ord("o"), ord("r"), ord("d"), ord("\n")]
        self.stdscr.getch.side_effect = password_chars

        password = dialog.get_password()

        # Check that asterisks were displayed
        displayed_calls = [call for call in self.stdscr.addstr.call_args_list if "*" in str(call)]
        self.assertGreater(len(displayed_calls), 0)

        # But actual password should be returned
        self.assertEqual(password, "password")

    def test_sudo_dialog_rendering(self):
        """Dialog appears as curses overlay"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Mock immediate enter press
        self.stdscr.getch.return_value = ord("\n")

        dialog.get_password("Enter sudo password:")

        # Should draw a box
        box_calls = [call for call in self.stdscr.addch.call_args_list if curses.ACS_ULCORNER in str(call)]
        self.assertGreater(len(box_calls), 0)

        # Should show the message
        msg_calls = [call for call in self.stdscr.addstr.call_args_list if "Enter sudo password:" in str(call)]
        self.assertGreater(len(msg_calls), 0)

    def test_sudo_caching(self):
        """Can cache sudo for session"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Enable caching
        dialog.enable_caching = True

        # First call should prompt
        self.stdscr.getch.side_effect = [ord("t"), ord("e"), ord("s"), ord("t"), ord("\n")]
        password1 = dialog.get_password()
        self.assertEqual(password1, "test")

        # Second call should return cached password without prompting
        self.stdscr.reset_mock()
        password2 = dialog.get_password()
        self.assertEqual(password2, "test")
        self.stdscr.getch.assert_not_called()

    def test_backspace_handling(self):
        """Test backspace key handling in password input"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Type "pass", backspace, then "sword"
        input_chars = [
            ord("p"),
            ord("a"),
            ord("s"),
            ord("s"),
            127,  # Backspace
            ord("w"),
            ord("o"),
            ord("r"),
            ord("d"),
            ord("\n"),
        ]
        self.stdscr.getch.side_effect = input_chars

        password = dialog.get_password()
        self.assertEqual(password, "password")

    def test_escape_cancellation(self):
        """Test ESC key cancels password input"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Press ESC
        self.stdscr.getch.return_value = 27  # ESC

        password = dialog.get_password()
        self.assertIsNone(password)

    def test_dialog_centering(self):
        """Test dialog is centered on screen"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)
        dialog.get_password()

        # Check that dialog was drawn in center area
        height, width = 24, 80
        expected_y = (height - 7) // 2  # Dialog height ~7
        expected_x = (width - 50) // 2  # Dialog width ~50

        # Should have drawn something near center
        center_calls = [
            call
            for call in self.stdscr.addstr.call_args_list
            if len(call[0]) >= 2 and abs(call[0][0] - expected_y) < 5 and abs(call[0][1] - expected_x) < 10
        ]
        self.assertGreater(len(center_calls), 0)

    def test_ctrl_c_handling(self):
        """Test Ctrl+C handling"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Simulate Ctrl+C
        self.stdscr.getch.side_effect = KeyboardInterrupt()

        password = dialog.get_password()
        self.assertIsNone(password)

    def test_empty_password(self):
        """Test empty password handling"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Just press enter
        self.stdscr.getch.return_value = ord("\n")

        password = dialog.get_password()
        self.assertEqual(password, "")


class TestSudoIntegration(unittest.TestCase):
    """Test sudo dialog integration with menu system"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    @patch("subprocess.run")
    def test_sudo_command_execution(self, mock_run):
        """Test executing commands with sudo"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Mock password input
        self.stdscr.getch.side_effect = [ord("p"), ord("a"), ord("s"), ord("s"), ord("\n")]

        # Execute sudo command
        result = dialog.execute_with_sudo("apt update")

        # Should have called subprocess with sudo
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "sudo")
        self.assertEqual(args[1], "-S")  # Read password from stdin

    def test_no_console_drop(self):
        """Ensure dialog never drops to console"""
        from lib.tui.sudo_dialog import SudoDialog

        dialog = SudoDialog(self.stdscr)

        # Test various edge cases
        test_cases = [
            [],  # Empty input
            [27],  # ESC
            [3],  # Ctrl+C
            [4],  # Ctrl+D
        ]

        for inputs in test_cases:
            self.stdscr.reset_mock()
            if inputs:
                self.stdscr.getch.side_effect = inputs + [ord("\n")]
            else:
                self.stdscr.getch.return_value = ord("\n")

            result = dialog.get_password()
            # Should return None or empty string, never crash
            self.assertIn(result, [None, ""])


if __name__ == "__main__":
    unittest.main()
