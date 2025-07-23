"""
Unit tests for menu_ui
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import curses

import lib.menu_ui
from lib.menu_ui import MenuOption, MenuUI, SliderConfig, DropdownConfig, MultiSelectConfig, create_menu_ui


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
    
    def test_menu_option_class(self):
        """Test MenuOption class"""
        option = MenuOption(
            name="Test Option",
            key="t",
            description="Test description"
        )
        assert option.name == "Test Option"
        assert option.key == "t"
        assert option.description == "Test description"
    
    def test_menu_ui_initialization(self, mock_stdscr):
        """Test MenuUI class initialization"""
        with patch('curses.initscr', return_value=mock_stdscr):
            menu = MenuUI(title="Test Menu")
            assert menu.title == "Test Menu"
    
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
    
    def test_create_menu_ui_function(self):
        """Test create_menu_ui function"""
        assert hasattr(lib.menu_ui, 'create_menu_ui')
        assert callable(lib.menu_ui.create_menu_ui)
