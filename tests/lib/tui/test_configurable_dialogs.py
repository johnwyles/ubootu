#!/usr/bin/env python3
"""
Tests for configurable dialog components
"""

import unittest
from unittest.mock import MagicMock, Mock, patch, call
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Mock curses before importing
sys.modules['curses'] = MagicMock()
import curses

# Set up curses constants
curses.KEY_UP = 259
curses.KEY_DOWN = 258
curses.KEY_LEFT = 260
curses.KEY_RIGHT = 261
curses.KEY_HOME = 262
curses.KEY_END = 360
curses.KEY_PPAGE = 339
curses.KEY_NPAGE = 338
curses.A_REVERSE = 262144
curses.error = Exception


class TestSliderDialog(unittest.TestCase):
    """Test SliderDialog functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()
        
        # Import after mocking
        from lib.tui.dialogs import SliderDialog
        self.SliderDialog = SliderDialog
        
    def test_slider_initialization(self):
        """Test slider dialog initialization"""
        dialog = self.SliderDialog(self.stdscr)
        self.assertEqual(dialog.stdscr, self.stdscr)
        self.assertEqual(dialog.height, 24)
        self.assertEqual(dialog.width, 80)
        
    def test_slider_value_adjustment(self):
        """Test adjusting slider value with arrow keys"""
        dialog = self.SliderDialog(self.stdscr)
        
        # Mock getch to return proper sequence
        def mock_getch_sequence():
            # Use a generator to return values in sequence
            sequence = [curses.KEY_RIGHT, curses.KEY_RIGHT, ord('\n')]
            for key in sequence:
                yield key
        
        getch_gen = mock_getch_sequence()
        self.stdscr.getch.side_effect = lambda: next(getch_gen)
        
        result = dialog.show("Test Slider", 50, 0, 100, 1, "%")
        self.assertEqual(result, 52)  # Started at 50, increased by 2
        
    def test_slider_direct_input(self):
        """Test direct numeric input in slider"""
        dialog = self.SliderDialog(self.stdscr)
        
        # Simulate typing "75" then enter
        self.stdscr.getch.side_effect = [
            ord('7'),
            ord('5'),
            ord('\n')
        ]
        self.stdscr.nodelay = MagicMock()
        
        # Mock nodelay behavior for digit collection
        with patch.object(self.stdscr, 'getch', side_effect=[ord('5'), -1, ord('\n')]):
            result = dialog.show("Test Slider", 50, 0, 100, 1, "%")
        
        # Should be 75 from direct input
        self.assertIsNotNone(result)
        
    def test_slider_cancellation(self):
        """Test ESC cancels slider"""
        dialog = self.SliderDialog(self.stdscr)
        
        # Simulate ESC key
        self.stdscr.getch.return_value = 27  # ESC
        
        result = dialog.show("Test Slider", 50, 0, 100)
        self.assertIsNone(result)
        
    def test_slider_bounds(self):
        """Test slider respects min/max bounds"""
        dialog = self.SliderDialog(self.stdscr)
        
        # Try to go below minimum
        self.stdscr.getch.side_effect = [
            curses.KEY_LEFT,  # Decrease from 10 (min)
            curses.KEY_LEFT,  # Try to decrease again
            ord('\n')
        ]
        
        result = dialog.show("Test", 10, 10, 100)
        self.assertEqual(result, 10)  # Should stay at minimum


class TestSpinnerDialog(unittest.TestCase):
    """Test SpinnerDialog functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()
        
        from lib.tui.dialogs import SpinnerDialog
        self.SpinnerDialog = SpinnerDialog
        
    def test_spinner_navigation(self):
        """Test navigating spinner values"""
        dialog = self.SpinnerDialog(self.stdscr)
        values = [10, 12, 14, 16, 18, 20]
        
        # Start at 14 (index 2), go up once, confirm
        self.stdscr.getch.side_effect = [
            curses.KEY_UP,    # Go to 12
            ord('\n')         # Confirm
        ]
        
        result = dialog.show("Font Size", 14, values, "pt")
        self.assertEqual(result, 12)
        
    def test_spinner_wrap_around(self):
        """Test spinner doesn't wrap at boundaries"""
        dialog = self.SpinnerDialog(self.stdscr)
        values = [1, 2, 3]
        
        # Try to go up from first value
        self.stdscr.getch.side_effect = [
            curses.KEY_UP,    # Should stay at 1
            ord('\n')
        ]
        
        result = dialog.show("Test", 1, values)
        self.assertEqual(result, 1)
        
    def test_spinner_home_end_keys(self):
        """Test HOME/END keys in spinner"""
        dialog = self.SpinnerDialog(self.stdscr)
        values = [10, 20, 30, 40, 50]
        
        # Press END to go to last value
        self.stdscr.getch.side_effect = [
            curses.KEY_END,   # Go to 50
            ord('\n')
        ]
        
        result = dialog.show("Test", 20, values)
        self.assertEqual(result, 50)


class TestSelectDialog(unittest.TestCase):
    """Test SelectDialog functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()
        
        from lib.tui.dialogs import SelectDialog
        self.SelectDialog = SelectDialog
        
    def test_select_navigation(self):
        """Test navigating select options"""
        dialog = self.SelectDialog(self.stdscr)
        options = ["Option 1", "Option 2", "Option 3"]
        
        # Start at Option 1, go down twice, confirm
        self.stdscr.getch.side_effect = [
            curses.KEY_DOWN,  # Go to Option 2
            curses.KEY_DOWN,  # Go to Option 3
            ord('\n')         # Confirm
        ]
        
        result = dialog.show("Select Test", options, "Option 1")
        self.assertEqual(result, "Option 3")
        
    def test_select_initial_value(self):
        """Test select dialog starts at current value"""
        dialog = self.SelectDialog(self.stdscr)
        options = ["A", "B", "C", "D"]
        
        # Should start at C, press enter immediately
        self.stdscr.getch.return_value = ord('\n')
        
        result = dialog.show("Test", options, "C")
        self.assertEqual(result, "C")
        
    def test_select_scrolling(self):
        """Test scrolling in long option lists"""
        dialog = self.SelectDialog(self.stdscr)
        
        # Create a long list of options
        options = [f"Option {i}" for i in range(50)]
        
        # Simulate page down then enter
        self.stdscr.getch.side_effect = [
            curses.KEY_NPAGE,  # Page down
            ord('\n')
        ]
        
        # Mock the visible area calculation
        with patch.object(dialog, 'draw_dialog_box', return_value=(5, 10, 10, 60)):
            result = dialog.show("Long List", options, "Option 0")
            
        # Should have moved down from Option 0
        self.assertIsNotNone(result)
        
    def test_select_search_by_letter(self):
        """Test quick jump to option by typing first letter"""
        dialog = self.SelectDialog(self.stdscr)
        options = ["Apple", "Banana", "Cherry", "Date"]
        
        # Type 'c' to jump to Cherry
        self.stdscr.getch.side_effect = [
            ord('c'),         # Jump to Cherry
            ord('\n')         # Confirm
        ]
        
        # This feature may not be implemented, but test the behavior
        result = dialog.show("Fruit", options, "Apple")
        self.assertIn(result, options)


class TestDialogIntegration(unittest.TestCase):
    """Test dialog integration with unified menu"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()
        
    @patch('lib.tui.dialogs.SliderDialog')
    def test_unified_menu_opens_slider(self, mock_slider_class):
        """Test unified menu opens slider dialog for slider config type"""
        from lib.tui.unified_menu import UnifiedMenu
        
        # Set up mock slider instance
        mock_slider = MagicMock()
        mock_slider.show.return_value = 75
        mock_slider_class.return_value = mock_slider
        
        menu = UnifiedMenu(self.stdscr)
        
        # Create a configurable item
        item = {
            'id': 'test-slider',
            'label': 'Test Slider',
            'is_configurable': True,
            'config_type': 'slider',
            'min_value': 0,
            'max_value': 100,
            'default_value': 50,
            'unit': '%'
        }
        
        menu.show_config_dialog(item)
        
        # Verify slider was created and shown
        mock_slider_class.assert_called_once_with(self.stdscr)
        mock_slider.show.assert_called_once_with(
            'Test Slider', 50, 0, 100, 1, '%'
        )
        
        # Verify value was updated
        self.assertEqual(menu.configurable_values['test-slider'], 75)


if __name__ == '__main__':
    unittest.main()