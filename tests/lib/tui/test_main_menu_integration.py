#!/usr/bin/env python3
"""
Integration tests for main menu flow
Written BEFORE implementation to follow TDD
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

# Mock curses before import
sys.modules["curses"] = MagicMock()
import curses

# Set up curses constants
curses.KEY_UP = 259
curses.KEY_DOWN = 258
curses.KEY_ENTER = 10
curses.A_REVERSE = 262144
curses.KEY_RESIZE = 410
curses.error = Exception


# Mock curses.wrapper to avoid terminal requirements
def mock_wrapper(func):
    """Mock wrapper that calls function with mock stdscr"""
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (24, 80)
    return func(mock_stdscr)


curses.wrapper = mock_wrapper


class TestMainMenuIntegration(unittest.TestCase):
    """Test main menu integration"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()

    def test_main_menu_displays_all_options(self):
        """Main menu should show all 8 options"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)

        # Should have 8 menu items
        self.assertEqual(len(menu.menu_items), 8)

        # Check all options are present
        ids = [item["id"] for item in menu.menu_items]
        self.assertEqual(ids, ["1", "2", "3", "4", "5", "6", "7", "8"])

        # Check labels
        labels = [item["label"] for item in menu.menu_items]
        self.assertIn("Fresh Install", labels)
        self.assertIn("Modify Setup", labels)
        self.assertIn("Exit", labels)

    def test_arrow_keys_navigate_menu(self):
        """Arrow keys should move selection up/down"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)

        # Start at index 0
        self.assertEqual(menu.current_index, 0)

        # Down arrow should increment
        action = menu.navigate(curses.KEY_DOWN)
        self.assertEqual(action, "navigate")
        self.assertEqual(menu.current_index, 1)

        # Up arrow should decrement
        action = menu.navigate(curses.KEY_UP)
        self.assertEqual(action, "navigate")
        self.assertEqual(menu.current_index, 0)

        # Up at top should wrap to bottom
        action = menu.navigate(curses.KEY_UP)
        self.assertEqual(menu.current_index, 7)

    def test_number_keys_select_directly(self):
        """Pressing 1-8 should select that option"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)

        # Press '1' key
        action = menu.navigate(ord("1"))
        self.assertEqual(action, "select")
        self.assertEqual(menu.current_index, 0)

        # Press '8' key
        action = menu.navigate(ord("8"))
        self.assertEqual(action, "select")
        self.assertEqual(menu.current_index, 7)

    def test_esc_exits_application(self):
        """ESC should select exit option"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)

        # ESC should select exit
        action = menu.navigate(27)  # ESC key
        self.assertEqual(action, "select")
        self.assertEqual(menu.current_index, 7)  # Exit option

    def test_enter_selects_current_option(self):
        """Enter should select current option"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)
        menu.current_index = 0  # Fresh Install

        action = menu.navigate(ord("\n"))
        self.assertEqual(action, "select")

    def test_splash_screen_shows_before_menu(self):
        """Splash screen should display before main menu"""
        from lib.tui.main_menu import MainMenu

        menu = MainMenu(self.stdscr)

        # Mock getch to return '8' (exit) after splash
        self.stdscr.getch.return_value = ord("8")

        # Run should show splash then menu
        result = menu.run()

        # Should return '8' (exit)
        self.assertEqual(result, "8")

        # Should have drawn progress bar
        draw_calls = [str(call) for call in self.stdscr.addstr.call_args_list]
        self.assertTrue(any("█" in call for call in draw_calls))


class TestSectionSelectorIntegration(unittest.TestCase):
    """Test section selector integration"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_section_selector_shows_all_sections(self):
        """Section selector should show all 6 sections"""
        from lib.tui.section_selector import SectionSelector

        selector = SectionSelector(self.stdscr)

        # Should have 6 sections
        self.assertEqual(len(selector.sections), 6)

        # Check section IDs
        ids = [s["id"] for s in selector.sections]
        expected = ["desktop", "applications", "development", "security", "themes", "system"]
        self.assertEqual(ids, expected)

    def test_space_toggles_selection(self):
        """Space bar should toggle section selection"""
        from lib.tui.section_selector import SectionSelector

        selector = SectionSelector(self.stdscr)
        selector.current_index = 0

        # Initially nothing selected
        self.assertEqual(len(selector.selections), 0)

        # Space should toggle selection
        action = selector.navigate(ord(" "))
        self.assertEqual(action, "select")
        self.assertIn("desktop", selector.selections)

        # Space again should deselect
        action = selector.navigate(ord(" "))
        self.assertEqual(action, "select")
        self.assertNotIn("desktop", selector.selections)

    def test_select_all_and_clear_all(self):
        """A selects all, N clears all"""
        from lib.tui.section_selector import SectionSelector

        selector = SectionSelector(self.stdscr)

        # A should select all
        action = selector.navigate(ord("A"))
        self.assertEqual(action, "select_all")
        self.assertEqual(len(selector.selections), 6)

        # N should clear all
        action = selector.navigate(ord("N"))
        self.assertEqual(action, "deselect_all")
        self.assertEqual(len(selector.selections), 0)

    def test_esc_cancels_selection(self):
        """ESC should cancel and return empty list"""
        from lib.tui.section_selector import SectionSelector

        selector = SectionSelector(self.stdscr)

        # Make some selections
        selector.selections = {"desktop", "applications"}

        # ESC should cancel
        action = selector.navigate(27)
        self.assertEqual(action, "cancel")


class TestMenuFlowIntegration(unittest.TestCase):
    """Test complete menu flows"""

    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    @patch("lib.tui.dialogs.ConfirmDialog")
    def test_fresh_install_cancel_flow(self, mock_confirm):
        """Test cancelling fresh install returns to main menu"""
        from lib.tui.unified_menu import UnifiedMenu

        menu = UnifiedMenu(self.stdscr)

        # Simulate ESC press
        self.stdscr.getch.return_value = 27  # ESC

        # Run should return 1 (cancelled)
        exit_code = menu.run()
        self.assertEqual(exit_code, 1)

    @patch("curses.wrapper")
    def test_main_menu_wrapper_integration(self, mock_wrapper):
        """Test main menu through curses wrapper"""
        from lib.tui.main_menu import show_main_menu

        # Mock wrapper to call function directly with our mock stdscr
        mock_wrapper.side_effect = lambda func: func(self.stdscr)

        # Simulate selecting exit
        self.stdscr.getch.return_value = ord("8")

        # Should return '8'
        result = show_main_menu(self.stdscr)
        self.assertEqual(result, "8")

    @patch("curses.wrapper")
    def test_section_selector_wrapper_integration(self, mock_wrapper):
        """Test section selector through curses wrapper"""
        from lib.tui.section_selector import show_section_selector

        # Mock wrapper to call function directly
        mock_wrapper.side_effect = lambda func: func(self.stdscr)

        # Simulate ESC to cancel
        self.stdscr.getch.return_value = 27

        # Should return empty list
        result = show_section_selector(self.stdscr)
        self.assertEqual(result, [])


class TestImportCompatibility(unittest.TestCase):
    """Test that imports don't conflict"""

    def test_no_import_conflicts(self):
        """All TUI modules should import without conflicts"""
        try:
            from lib.tui.dialogs import ConfirmDialog, MessageDialog
            from lib.tui.main_menu import MainMenu
            from lib.tui.section_selector import SectionSelector
            from lib.tui.sudo_dialog import SudoDialog
            from lib.tui.unified_menu import UnifiedMenu

            # All imports successful
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == "__main__":
    unittest.main()
