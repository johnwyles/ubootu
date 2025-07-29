#!/usr/bin/env python3
"""
Comprehensive tests for the unified TUI menu system
"""

import unittest
from unittest.mock import MagicMock, Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Mock curses module before importing anything that uses it
sys.modules['curses'] = MagicMock()
import curses
# Set up curses constants
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
curses.KEY_F1 = 265
curses.KEY_BACKSPACE = 263
curses.KEY_DC = 330
curses.KEY_HOME = 262
curses.KEY_END = 360
curses.KEY_PPAGE = 339
curses.KEY_NPAGE = 338
curses.KEY_RESIZE = 410
curses.A_BOLD = 2097152
curses.A_REVERSE = 262144
curses.error = Exception


class TestUnifiedMenu(unittest.TestCase):
    """Test the unified menu system for consistency"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()
        self.stdscr.keypad = MagicMock()
        
    @patch('curses.curs_set')
    def test_menu_rendering_consistency(self, mock_curs_set):
        """All menus use same box drawing characters"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.render()
        
        # Check that we're using single-line box characters
        calls = self.stdscr.addch.call_args_list
        box_chars = [call[0][2] for call in calls if len(call[0]) > 2]
        
        # Should use ACS characters for box drawing
        self.assertIn(curses.ACS_ULCORNER, box_chars)
        self.assertIn(curses.ACS_URCORNER, box_chars)
        self.assertIn(curses.ACS_LLCORNER, box_chars)
        self.assertIn(curses.ACS_LRCORNER, box_chars)
        self.assertIn(curses.ACS_HLINE, box_chars)
        self.assertIn(curses.ACS_VLINE, box_chars)
        
    def test_navigation_keys(self):
        """Arrow keys, space, enter work consistently"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.items = [
            {'id': 'item1', 'label': 'Item 1', 'children': []},
            {'id': 'item2', 'label': 'Item 2', 'children': []},
            {'id': 'item3', 'label': 'Item 3', 'children': []},
        ]
        menu.current_index = 0
        
        # Test down arrow
        menu.navigate(curses.KEY_DOWN)
        self.assertEqual(menu.current_index, 1)
        
        # Test up arrow
        menu.navigate(curses.KEY_UP)
        self.assertEqual(menu.current_index, 0)
        
        # Test space for selection
        menu.navigate(ord(' '))
        self.assertIn('item1', menu.selections)
        
        # Test enter for entering submenu
        result = menu.navigate(ord('\n'))
        self.assertEqual(result, 'enter')
        
    def test_selection_persistence(self):
        """Selections maintained across menu transitions"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        
        # Make some selections
        menu.selections = {'item1': True, 'item2': True, 'category1': {'subitem1', 'subitem2'}}
        
        # Transition to submenu and back
        menu.enter_submenu('category1')
        self.assertEqual(menu.current_menu, 'category1')
        
        menu.go_back()
        self.assertEqual(menu.current_menu, 'root')
        
        # Selections should be preserved
        self.assertIn('item1', menu.selections)
        self.assertIn('item2', menu.selections)
        self.assertEqual(menu.selections['category1'], {'subitem1', 'subitem2'})
        
    def test_help_system(self):
        """F1 shows help for current item"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.items = [
            {
                'id': 'vscode',
                'label': 'Visual Studio Code',
                'help': 'VS Code is a powerful editor'
            }
        ]
        menu.current_index = 0
        
        # Press F1
        result = menu.navigate(curses.KEY_F1)
        self.assertEqual(result, 'help')
        self.assertEqual(menu.get_current_help(), 'VS Code is a powerful editor')
        
    def test_no_console_drops(self):
        """Never drops to console except sudo"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        
        # Test all possible key inputs
        test_keys = [
            curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT,
            ord(' '), ord('\n'), ord('q'), ord('Q'), 27,  # ESC
            curses.KEY_F1, ord('h'), ord('H')
        ]
        
        for key in test_keys:
            result = menu.navigate(key)
            # Should return action strings, never raise or exit
            self.assertIsInstance(result, (str, type(None)))
            
    def test_selection_indicators(self):
        """Test category selection indicators"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        
        # Test no selection indicator
        indicator = menu.get_selection_indicator('category1', set())
        self.assertEqual(indicator, '○')
        
        # Test partial selection indicator
        menu.selections['category1'] = {'item1', 'item2'}
        menu.category_items['category1'] = {'item1', 'item2', 'item3', 'item4'}
        indicator = menu.get_selection_indicator('category1', menu.selections.get('category1', set()))
        self.assertEqual(indicator, '◐')
        
        # Test full selection indicator
        menu.selections['category1'] = {'item1', 'item2', 'item3', 'item4'}
        indicator = menu.get_selection_indicator('category1', menu.selections.get('category1', set()))
        self.assertEqual(indicator, '●')
        
    def test_menu_structure(self):
        """Test hierarchical menu structure"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Should have root items
        self.assertGreater(len(menu.items), 0)
        
        # Categories should have children
        categories = [item for item in menu.items if item.get('is_category')]
        self.assertGreater(len(categories), 0)
        
        for category in categories:
            self.assertIn('children', category)
            self.assertIsInstance(category['children'], list)


class TestMenuRendering(unittest.TestCase):
    """Test visual rendering of menus"""
    
    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        
    def test_box_drawing(self):
        """Test consistent box drawing across all menus"""
        from lib.tui.utils import draw_box
        
        draw_box(self.stdscr, 0, 0, 10, 40, "Test Menu")
        
        # Verify corners
        corner_calls = [
            ((0, 0, curses.ACS_ULCORNER),),
            ((0, 39, curses.ACS_URCORNER),),
            ((9, 0, curses.ACS_LLCORNER),),
            ((9, 39, curses.ACS_LRCORNER),),
        ]
        
        for call in corner_calls:
            self.stdscr.addch.assert_any_call(*call[0])
            
    def test_title_centering(self):
        """Test that titles are properly centered"""
        from lib.tui.utils import draw_box
        
        draw_box(self.stdscr, 0, 0, 10, 40, "🚀 Ubootu Configuration")
        
        # Check that title was written
        title_calls = [call for call in self.stdscr.addstr.call_args_list 
                      if "Ubootu Configuration" in str(call)]
        self.assertGreater(len(title_calls), 0)


class TestKeyboardHandling(unittest.TestCase):
    """Test keyboard input handling"""
    
    def setUp(self):
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        
    def test_vim_keys(self):
        """Test vim-style navigation keys"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.items = [{'id': f'item{i}'} for i in range(5)]
        menu.current_index = 2
        
        # j = down
        menu.navigate(ord('j'))
        self.assertEqual(menu.current_index, 3)
        
        # k = up
        menu.navigate(ord('k'))
        self.assertEqual(menu.current_index, 2)
        
    def test_escape_handling(self):
        """Test escape key handling"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.items = [{'id': 'test', 'label': 'Test'}]  # Add at least one item
        
        # ESC should go back/quit
        result = menu.navigate(27)  # ESC key
        self.assertEqual(result, 'back')
        
    def test_quit_keys(self):
        """Test quit key handling"""
        from lib.tui.unified_menu import UnifiedMenu
        
        menu = UnifiedMenu(self.stdscr)
        menu.items = [{'id': 'test', 'label': 'Test'}]  # Add at least one item
        
        # q should quit
        result = menu.navigate(ord('q'))
        self.assertEqual(result, 'quit')
        
        # Q should also quit
        result = menu.navigate(ord('Q'))
        self.assertEqual(result, 'quit')


if __name__ == '__main__':
    unittest.main()