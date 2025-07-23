"""
Unit tests for tui/app.py - Main TUI application.
"""

import curses
from unittest.mock import patch, Mock, MagicMock, call

import pytest

from lib.tui.app import UbootuTUI
from lib.tui.models import MenuItem


class TestUbootuTUIApp:
    """Test UbootuTUI application class."""
    
    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock curses screen."""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 100)  # height, width
        stdscr.getch.return_value = ord('q')  # Default to quit
        return stdscr
    
    @pytest.fixture
    def sample_menu_structure(self):
        """Create sample menu structure."""
        return {
            "root": MenuItem(
                "root", "Main Menu", "Root menu",
                is_category=True, children=["item1", "item2"]
            ),
            "item1": MenuItem(
                "item1", "Item 1", "First item",
                parent="root", default=True
            ),
            "item2": MenuItem(
                "item2", "Item 2", "Second item",
                parent="root", default=False
            ),
            "category1": MenuItem(
                "category1", "Category 1", "First category",
                is_category=True, children=["subitem1", "subitem2"]
            ),
            "subitem1": MenuItem(
                "subitem1", "Sub Item 1", "First sub item",
                parent="category1"
            ),
            "subitem2": MenuItem(
                "subitem2", "Sub Item 2", "Second sub item",
                parent="category1", default=True
            )
        }
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_initialization(self, mock_init_colors, mock_build_menu, mock_stdscr, sample_menu_structure):
        """Test UbootuTUI initialization."""
        mock_build_menu.return_value = sample_menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        assert tui.stdscr == mock_stdscr
        assert tui.menu_items == sample_menu_structure
        assert tui.current_menu == "root"
        assert tui.current_item == 0
        assert tui.scroll_offset == 0
        assert isinstance(tui.selected_items, set)
        assert tui.breadcrumb_stack == []
        assert tui.cancelled is False
        
        # Verify initialization calls
        mock_build_menu.assert_called_once()
        mock_init_colors.assert_called_once()
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    @patch('curses.curs_set')
    def test_init_curses(self, mock_curs_set, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test curses initialization."""
        mock_build_menu.return_value = {}
        
        tui = UbootuTUI(mock_stdscr)
        
        # Verify curses setup
        mock_curs_set.assert_called_once_with(0)  # Hide cursor
        mock_stdscr.keypad.assert_called_once_with(True)
        mock_stdscr.timeout.assert_called_once_with(50)
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    @patch('curses.curs_set', side_effect=Exception("Terminal doesn't support"))
    def test_init_curses_error_handling(self, mock_curs_set, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test curses initialization error handling."""
        mock_build_menu.return_value = {}
        
        # Should not raise exception
        tui = UbootuTUI(mock_stdscr)
        assert tui is not None
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_small_terminal(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test initialization with small terminal."""
        mock_stdscr.getmaxyx.return_value = (10, 40)  # Small terminal
        mock_build_menu.return_value = {}
        
        # Should not raise exception
        tui = UbootuTUI(mock_stdscr)
        assert tui is not None
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_apply_defaults(self, mock_init_colors, mock_build_menu, mock_stdscr, sample_menu_structure):
        """Test applying default selections."""
        mock_build_menu.return_value = sample_menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        # Check that defaults were applied
        assert "item1" in tui.selected_items  # default=True
        assert "subitem2" in tui.selected_items  # default=True
        assert "item2" not in tui.selected_items  # default=False
        
        # Check item states
        assert sample_menu_structure["item1"].selected is True
        assert sample_menu_structure["subitem2"].selected is True
        assert sample_menu_structure["item2"].selected is False
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_get_current_menu_items(self, mock_init_colors, mock_build_menu, mock_stdscr, sample_menu_structure):
        """Test getting current menu items."""
        mock_build_menu.return_value = sample_menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        # Root menu items
        items = tui.get_current_menu_items()
        assert len(items) == 2
        assert items[0].id == "item1"
        assert items[1].id == "item2"
        
        # Change to category1
        tui.current_menu = "category1"
        items = tui.get_current_menu_items()
        assert len(items) == 2
        assert items[0].id == "subitem1"
        assert items[1].id == "subitem2"
        
        # Menu with no children
        tui.current_menu = "item1"
        items = tui.get_current_menu_items()
        assert len(items) == 0
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_get_category_selection_status(self, mock_init_colors, mock_build_menu, mock_stdscr, sample_menu_structure):
        """Test category selection status calculation."""
        mock_build_menu.return_value = sample_menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        # Empty category (no items selected)
        status = tui.get_category_selection_status("category1")
        assert status == 'partial'  # subitem2 has default=True
        
        # Select all items
        tui.selected_items.add("subitem1")
        status = tui.get_category_selection_status("category1")
        assert status == 'full'
        
        # Deselect one item
        tui.selected_items.discard("subitem2")
        status = tui.get_category_selection_status("category1")
        assert status == 'partial'
        
        # Deselect all
        tui.selected_items.clear()
        status = tui.get_category_selection_status("category1")
        assert status == 'empty'
        
        # Non-existent category
        status = tui.get_category_selection_status("nonexistent")
        assert status == 'empty'
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_get_all_selectable_items(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test getting all selectable items in a category."""
        # Create nested structure
        menu_structure = {
            "root": MenuItem("root", "Root", "Root", is_category=True, children=["cat1"]),
            "cat1": MenuItem("cat1", "Cat1", "Category 1", is_category=True, children=["cat2", "item1"]),
            "cat2": MenuItem("cat2", "Cat2", "Category 2", is_category=True, children=["item2", "item3"]),
            "item1": MenuItem("item1", "Item1", "Item 1", parent="cat1"),
            "item2": MenuItem("item2", "Item2", "Item 2", parent="cat2"),
            "item3": MenuItem("item3", "Item3", "Item 3", parent="cat2")
        }
        
        mock_build_menu.return_value = menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        # Get items from cat1 (should include nested items)
        items = tui._get_all_selectable_items("cat1")
        assert len(items) == 3
        assert "item1" in items
        assert "item2" in items
        assert "item3" in items
        
        # Get items from cat2
        items = tui._get_all_selectable_items("cat2")
        assert len(items) == 2
        assert "item2" in items
        assert "item3" in items
        
        # Get items from leaf node
        items = tui._get_all_selectable_items("item1")
        assert len(items) == 0
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_run_normal(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test normal run of TUI."""
        mock_build_menu.return_value = {}
        mock_stdscr.getch.return_value = ord('q')  # Quit immediately
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 0
        assert not tui.cancelled
        
        # Verify display calls
        mock_stdscr.clear.assert_called_once()
        mock_stdscr.addstr.assert_called()
        mock_stdscr.refresh.assert_called_once()
        mock_stdscr.getch.assert_called_once()
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_run_keyboard_interrupt(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test run with keyboard interrupt."""
        mock_build_menu.return_value = {}
        mock_stdscr.getch.side_effect = KeyboardInterrupt()
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 1
        assert tui.cancelled
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_run_exception(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test run with general exception."""
        mock_build_menu.return_value = {}
        mock_stdscr.getch.side_effect = Exception("Test error")
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 1
        assert tui.cancelled


class TestSelectionLogic:
    """Test selection logic and state management."""
    
    @patch('lib.tui.app.build_menu_structure')
    @patch('lib.tui.app.init_colors')
    def test_recursive_category_selection(self, mock_init_colors, mock_build_menu, mock_stdscr):
        """Test recursive category selection status."""
        # Create deeply nested structure
        menu_structure = {
            "root": MenuItem("root", "Root", "Root", is_category=True, children=["level1"]),
            "level1": MenuItem("level1", "L1", "Level 1", is_category=True, children=["level2a", "level2b"]),
            "level2a": MenuItem("level2a", "L2A", "Level 2A", is_category=True, children=["item1", "item2"]),
            "level2b": MenuItem("level2b", "L2B", "Level 2B", is_category=True, children=["item3"]),
            "item1": MenuItem("item1", "Item1", "Item 1"),
            "item2": MenuItem("item2", "Item2", "Item 2"),
            "item3": MenuItem("item3", "Item3", "Item 3")
        }
        
        mock_build_menu.return_value = menu_structure
        
        tui = UbootuTUI(mock_stdscr)
        
        # Initially empty
        assert tui.get_category_selection_status("level1") == 'empty'
        
        # Select one item in level2a
        tui.selected_items.add("item1")
        assert tui.get_category_selection_status("level2a") == 'partial'
        assert tui.get_category_selection_status("level1") == 'partial'
        
        # Select all items in level2a
        tui.selected_items.add("item2")
        assert tui.get_category_selection_status("level2a") == 'full'
        assert tui.get_category_selection_status("level1") == 'partial'  # level2b still empty
        
        # Select item in level2b
        tui.selected_items.add("item3")
        assert tui.get_category_selection_status("level2b") == 'full'
        assert tui.get_category_selection_status("level1") == 'full'  # All items selected