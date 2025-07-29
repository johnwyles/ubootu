#!/usr/bin/env python3
"""
Test menu structure to expose the real problem
Writing tests FIRST to identify what's actually broken
"""

import unittest
import sys
import os
import subprocess
from unittest.mock import MagicMock, patch

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Mock curses module before any imports that use it
sys.modules['curses'] = MagicMock()
import curses

# Set up curses constants that are used in the code
curses.ACS_ULCORNER = ord('┌')
curses.ACS_URCORNER = ord('┐')
curses.ACS_LLCORNER = ord('└')
curses.ACS_LRCORNER = ord('┘')
curses.ACS_HLINE = ord('─')
curses.ACS_VLINE = ord('│')
curses.KEY_UP = 259
curses.KEY_DOWN = 258
curses.KEY_LEFT = 260
curses.KEY_RIGHT = 261
curses.KEY_RESIZE = 410
curses.A_BOLD = 2097152
curses.A_REVERSE = 262144
curses.error = Exception
curses.curs_set = MagicMock(return_value=0)


class TestMenuStructureExists(unittest.TestCase):
    """Test that the menu structure can be loaded"""
    
    def test_can_import_unified_menu(self):
        """Test that UnifiedMenu can be imported"""
        try:
            from lib.tui.unified_menu import UnifiedMenu
            self.assertTrue(True, "UnifiedMenu imported successfully")
        except ImportError as e:
            self.fail(f"Cannot import UnifiedMenu: {e}")
    
    def test_can_instantiate_unified_menu(self):
        """Test that UnifiedMenu can be instantiated with mock stdscr"""
        from lib.tui.unified_menu import UnifiedMenu
        
        # Create mock stdscr
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        # This should not raise an exception
        try:
            menu = UnifiedMenu(mock_stdscr)
            self.assertIsNotNone(menu)
        except Exception as e:
            self.fail(f"Cannot instantiate UnifiedMenu: {e}")
    
    def test_menu_items_can_be_loaded(self):
        """Test that menu items can be loaded"""
        try:
            from lib.tui.menu_items import load_menu_structure
            items = load_menu_structure()
            self.assertIsInstance(items, list, "load_menu_structure should return a list")
            self.assertGreater(len(items), 0, "Menu should have at least one item")
        except ImportError as e:
            self.fail(f"Cannot import menu_items: {e}")
        except Exception as e:
            self.fail(f"Error loading menu structure: {e}")
    
    def test_unified_menu_can_load_structure(self):
        """Test that UnifiedMenu can load its menu structure"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        
        # This is where it might fail - loading menu structure
        try:
            menu.load_menu_structure()
            self.assertIsNotNone(menu.items)
            self.assertIsInstance(menu.items, list)
        except Exception as e:
            self.fail(f"Cannot load menu structure: {e}")


class TestScriptCanStart(unittest.TestCase):
    """Test that the main script can at least start"""
    
    def test_configure_standard_tui_imports(self):
        """Test that configure_standard_tui.py can be imported"""
        test_script = '''
import sys
import os

# Mock curses first
from unittest.mock import MagicMock
sys.modules['curses'] = MagicMock()

try:
    import configure_standard_tui
    print("SUCCESS: Script imported")
except Exception as e:
    print(f"FAIL: {e}")
    import traceback
    traceback.print_exc()
'''
        
        result = subprocess.run(
            [sys.executable, '-c', test_script],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        )
        
        self.assertIn("SUCCESS", result.stdout, 
                     f"Script import failed. stdout: {result.stdout}, stderr: {result.stderr}")
    
    def test_run_unified_tui_function_exists(self):
        """Test that run_unified_tui function exists and can be called with mock"""
        from configure_standard_tui import run_unified_tui
        
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        # Provide enough keypresses: q to quit, n to not save
        mock_stdscr.getch.side_effect = [ord('q'), ord('n')]
        
        # This should not crash
        try:
            result = run_unified_tui(mock_stdscr)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, int)
        except Exception as e:
            self.fail(f"run_unified_tui failed: {e}")


class TestMenuInitialization(unittest.TestCase):
    """Test the actual initialization that's failing"""
    
    @patch('sys.stdout.isatty')
    def test_script_startup_in_tty(self, mock_isatty):
        """Test what happens when script starts in a TTY"""
        mock_isatty.return_value = True
        
        # Run the script and capture what happens
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py', '--help'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        )
        
        # Help should work regardless
        self.assertEqual(result.returncode, 0, 
                        f"Script failed even with --help. stderr: {result.stderr}")
    
    def test_unified_menu_run_method(self):
        """Test that UnifiedMenu.run() can be called"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        # Provide enough key presses: q to quit, then n for "don't save"
        mock_stdscr.getch.side_effect = [ord('q'), ord('n')]
        
        menu = UnifiedMenu(mock_stdscr)
        
        # This is likely where it fails
        try:
            result = menu.run()
            self.assertIsInstance(result, int, "run() should return an int exit code")
        except Exception as e:
            self.fail(f"menu.run() failed: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)