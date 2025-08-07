#!/usr/bin/env python3
"""
Integration tests for the complete TUI flow
"""

import curses
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, Mock, call, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))


class TestFullUserJourney(unittest.TestCase):
    """Test complete user journey through the TUI"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.temp_config = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml")

    def tearDown(self):
        """Clean up temp files"""
        try:
            os.unlink(self.temp_config.name)
        except:
            pass

    def test_complete_flow_no_drops(self):
        """Start to finish without console drops"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)

        # Simulate user journey:
        # 1. Navigate to development tools
        # 2. Select some items
        # 3. Go to AI tools
        # 4. Select items
        # 5. Save and exit

        user_actions = [
            curses.KEY_DOWN,  # Navigate to dev tools
            ord("\n"),  # Enter dev tools
            ord(" "),  # Select first item
            curses.KEY_DOWN,  # Move down
            ord(" "),  # Select second item
            27,  # ESC to go back
            curses.KEY_DOWN,  # Navigate to AI tools
            ord("\n"),  # Enter AI tools
            ord(" "),  # Select item
            27,  # ESC to go back
            ord("s"),  # Save
            ord("q"),  # Quit
        ]

        self.stdscr.getch.side_effect = user_actions

        # Run the menu
        result = menu.run()

        # Should complete without exceptions
        self.assertIsNotNone(result)

        # Should have saved selections
        self.assertGreater(len(menu.selections), 0)

    def test_all_menu_transitions(self):
        """Every menu transition stays in TUI"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        # Test transitioning through all categories
        categories = [item for item in menu.items if item.get("is_category")]

        for category in categories:
            # Enter category
            menu.current_menu = "root"
            menu.enter_submenu(category["id"])
            self.assertEqual(menu.current_menu, category["id"])

            # Go back
            menu.go_back()
            self.assertEqual(menu.current_menu, "root")

            # No exceptions should occur

    @patch("lib.tui.sudo_dialog.SudoDialog.get_password")
    @patch("subprocess.run")
    def test_sudo_integration(self, mock_run, mock_get_password):
        """Test sudo password prompt integration"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)

        # Mock password entry
        mock_get_password.return_value = "testpass"
        mock_run.return_value.returncode = 0

        # Simulate applying configuration
        menu.apply_configuration()

        # Should have prompted for password
        mock_get_password.assert_called_once()

        # Should have run ansible with sudo
        mock_run.assert_called()
        ansible_call = mock_run.call_args[0][0]
        self.assertIn("ansible-playbook", " ".join(ansible_call))

    def test_help_overlay_integration(self):
        """Test F1 help overlay in menu flow"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)
        menu.items = [{"id": "vscode", "label": "VS Code", "help": "VS Code help text"}]

        # Navigate and press F1
        actions = [
            curses.KEY_F1,  # Show help
            ord("q"),  # Close help
            ord("q"),  # Quit menu
        ]

        self.stdscr.getch.side_effect = actions

        result = menu.run()

        # Should have shown help overlay
        help_calls = [call for call in self.stdscr.addstr.call_args_list if "VS Code help text" in str(call)]
        self.assertGreater(len(help_calls), 0)


class TestMenuStatePersistence(unittest.TestCase):
    """Test menu state persistence across sessions"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.config_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml")

    def tearDown(self):
        try:
            os.unlink(self.config_file.name)
        except:
            pass

    def test_save_selections(self):
        """Test saving selections to config file"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)
        menu.config_file = self.config_file.name

        # Make selections
        menu.selections = {"vscode": True, "python": True, "development": {"docker", "git", "nodejs"}}

        # Save
        menu.save_configuration()

        # Verify file was written
        with open(self.config_file.name, "r") as f:
            content = f.read()

        self.assertIn("vscode", content)
        self.assertIn("python", content)
        self.assertIn("docker", content)

    def test_load_selections(self):
        """Test loading selections from config file"""
        from lib.tui.unified_menu import UnifiedMenu

        # Write test config
        self.config_file.write(
            """
selected_items:
  - vscode
  - python
  - docker
configurable_items:
  swappiness:
    value: 10
"""
        )
        self.config_file.flush()

        menu = UnifiedMenu(self.stdscr)
        menu.config_file = self.config_file.name
        menu.load_configuration()

        # Should have loaded selections
        self.assertIn("vscode", menu.selections)
        self.assertIn("python", menu.selections)
        self.assertIn("docker", menu.selections)

        # Should have loaded configurable items
        self.assertEqual(menu.configurable_values.get("swappiness"), 10)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in TUI"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_terminal_resize(self):
        """Test handling terminal resize"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)

        # Simulate resize
        self.stdscr.getmaxyx.side_effect = [
            (24, 80),  # Initial size
            (30, 100),  # Resized
        ]

        # Simulate resize key
        self.stdscr.getch.side_effect = [curses.KEY_RESIZE, ord("q")]

        # Should handle gracefully
        menu.run()

        # Should have redrawn
        self.assertGreater(self.stdscr.clear.call_count, 1)

    def test_invalid_terminal_size(self):
        """Test handling too small terminal"""
        from lib.tui.unified_menu import UnifiedMenu

        # Very small terminal
        self.stdscr.getmaxyx.return_value = (10, 40)

        menu = UnifiedMenu(self.stdscr)
        self.stdscr.getch.return_value = ord("q")

        # Should show error message
        menu.run()

        error_calls = [
            call
            for call in self.stdscr.addstr.call_args_list
            if "Terminal too small" in str(call) or "minimum" in str(call).lower()
        ]
        self.assertGreater(len(error_calls), 0)


class TestMenuNavigation(unittest.TestCase):
    """Test menu navigation features"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_breadcrumb_navigation(self):
        """Test breadcrumb display"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)

        # Navigate deep into menus
        menu.breadcrumb = ["Root", "Development", "Languages", "Python"]
        menu.render()

        # Should show breadcrumb
        breadcrumb_calls = [
            call for call in self.stdscr.addstr.call_args_list if "Development" in str(call) and "Python" in str(call)
        ]
        self.assertGreater(len(breadcrumb_calls), 0)

    def test_search_functionality(self):
        """Test search within menu"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)
        menu.items = [
            {"id": "vscode", "label": "Visual Studio Code"},
            {"id": "pycharm", "label": "PyCharm"},
            {"id": "vim", "label": "Vim"},
        ]

        # Press / to search
        search_chars = [ord("/"), ord("v"), ord("i"), ord("\n"), ord("q")]
        self.stdscr.getch.side_effect = search_chars

        menu.run()

        # Should have filtered to items containing 'vi'
        # (Implementation would filter to vscode and vim)


if __name__ == "__main__":
    unittest.main()
