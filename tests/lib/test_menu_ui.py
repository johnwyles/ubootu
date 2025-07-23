"""
Unit tests for menu_ui
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import curses

import lib.menu_ui
from lib.menu_ui import (
    SelectionMode, CategoryState, MenuItem, MenuCategory,
    SystemPreferences, show_menu, calculate_category_state,
    DropdownConfig, SliderConfig, MultiSelectConfig
)


class TestMenuUi:
    """Test MenuUi functionality"""
    
    @pytest.fixture
    def mock_stdscr(self):
        """Mock curses screen"""
        mock = MagicMock()
        mock.getmaxyx.return_value = (24, 80)
        mock.getch.return_value = ord('q')  # Default to quit
        return mock
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.menu_ui is not None
    
    def test_selection_mode_enum(self):
        """Test SelectionMode enum values"""
        assert SelectionMode.NAVIGATE.value == "navigate"
        assert SelectionMode.SELECT.value == "select"
        assert SelectionMode.CONFIGURE.value == "configure"
    
    def test_category_state_enum(self):
        """Test CategoryState enum values"""
        assert CategoryState.NONE == "none"
        assert CategoryState.PARTIAL == "partial"
        assert CategoryState.ALL == "all"
    
    def test_menu_item_creation(self):
        """Test MenuItem dataclass"""
        item = MenuItem(
            id="test-item",
            name="Test Item",
            description="Test description",
            parent="test-parent"
        )
        assert item.id == "test-item"
        assert item.name == "Test Item"
        assert item.selected is False  # Default value
        assert item.children == []  # Default value
    
    def test_menu_category_creation(self):
        """Test MenuCategory dataclass"""
        category = MenuCategory(
            id="test-cat",
            name="Test Category",
            description="Test category description",
            parent="root",
            children=["item1", "item2"]
        )
        assert category.id == "test-cat"
        assert len(category.children) == 2
    
    def test_system_preferences(self):
        """Test SystemPreferences dataclass"""
        prefs = SystemPreferences()
        assert prefs.username == ""
        assert prefs.full_name == ""
        assert prefs.timezone == "UTC"
        assert prefs.desktop_environment == "gnome"
    
    def test_config_classes(self):
        """Test configuration dataclasses"""
        # Test SliderConfig
        slider = SliderConfig(
            min_value=0,
            max_value=100,
            current_value=50,
            step=5,
            unit="%"
        )
        assert slider.min_value == 0
        assert slider.max_value == 100
        assert slider.current_value == 50
        
        # Test DropdownConfig
        dropdown = DropdownConfig(
            options=[("opt1", "Option 1"), ("opt2", "Option 2")],
            current_value="opt1"
        )
        assert len(dropdown.options) == 2
        assert dropdown.current_value == "opt1"
        
        # Test MultiSelectConfig
        multi = MultiSelectConfig(
            options=[("opt1", "Option 1", True), ("opt2", "Option 2", False)],
            max_selections=2
        )
        assert len(multi.options) == 2
        assert multi.max_selections == 2
    
    @patch('curses.wrapper')
    def test_show_menu_function(self, mock_wrapper):
        """Test show_menu function exists and is callable"""
        # Verify function exists
        assert hasattr(lib.menu_ui, 'show_menu')
        assert callable(lib.menu_ui.show_menu)
        
        # Test calling it (will be mocked)
        result = show_menu(None)
        mock_wrapper.assert_called_once()
    
    def test_calculate_category_state(self):
        """Test calculate_category_state function"""
        # All items selected
        items = [
            MenuItem("1", "Item 1", "", "cat", selected=True),
            MenuItem("2", "Item 2", "", "cat", selected=True)
        ]
        state = calculate_category_state(items, "cat")
        assert state == CategoryState.ALL
        
        # No items selected
        items = [
            MenuItem("1", "Item 1", "", "cat", selected=False),
            MenuItem("2", "Item 2", "", "cat", selected=False)
        ]
        state = calculate_category_state(items, "cat")
        assert state == CategoryState.NONE
        
        # Some items selected
        items = [
            MenuItem("1", "Item 1", "", "cat", selected=True),
            MenuItem("2", "Item 2", "", "cat", selected=False)
        ]
        state = calculate_category_state(items, "cat")
        assert state == CategoryState.PARTIAL
