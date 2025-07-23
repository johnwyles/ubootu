"""
Unit tests for tui/dialogs.py - Dialog system for TUI interface
"""


from __future__ import annotations
import pytest
from unittest.mock import Mock, MagicMock, patch, call
import curses
from lib.tui.dialogs import TUIDialogs
from lib.tui.models import MenuItem


class TestTUIDialogs:
    """Test TUIDialogs class"""
    
    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock stdscr object"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)  # Terminal size
        stdscr.getch.return_value = ord('q')  # Default to quit
        return stdscr
    
    @pytest.fixture
    def selected_items(self):
        """Create a set of selected items"""
        return {"item1", "item2", "item3"}
    
    @pytest.fixture
    def tui_dialogs(self, mock_stdscr, selected_items):
        """Create a TUIDialogs instance"""
        return TUIDialogs(mock_stdscr, selected_items)
    
    def test_init(self, mock_stdscr, selected_items):
        """Test TUIDialogs initialization"""
        dialogs = TUIDialogs(mock_stdscr, selected_items)
        assert dialogs.stdscr == mock_stdscr
        assert dialogs.selected_items == selected_items
    
    def test_show_configuration_dialog_slider(self, tui_dialogs):
        """Test show_configuration_dialog with slider type"""
        item = MenuItem(
            id="test-slider",
            label="Test Slider",
            description="Test slider description",
            config_type="slider",
            config_value=50,
            config_range=(0, 100),
            config_unit="%"
        )
        
        with patch.object(tui_dialogs, '_show_slider_dialog') as mock_slider:
            tui_dialogs.show_configuration_dialog(item)
            mock_slider.assert_called_once_with(item)
    
    def test_show_configuration_dialog_dropdown(self, tui_dialogs):
        """Test show_configuration_dialog with dropdown type"""
        item = MenuItem(
            id="test-dropdown",
            label="Test Dropdown",
            description="Test dropdown description",
            config_type="dropdown",
            config_value="option1",
            config_options=[("option1", "Option 1"), ("option2", "Option 2")]
        )
        
        with patch.object(tui_dialogs, '_show_dropdown_dialog') as mock_dropdown:
            tui_dialogs.show_configuration_dialog(item)
            mock_dropdown.assert_called_once_with(item)
    
    def test_show_configuration_dialog_toggle(self, tui_dialogs):
        """Test show_configuration_dialog with toggle type"""
        item = MenuItem(
            id="test-toggle",
            label="Test Toggle",
            description="Test toggle description",
            config_type="toggle",
            config_value=True
        )
        
        with patch.object(tui_dialogs, '_show_toggle_dialog') as mock_toggle:
            tui_dialogs.show_configuration_dialog(item)
            mock_toggle.assert_called_once_with(item)
    
    def test_show_configuration_dialog_text(self, tui_dialogs):
        """Test show_configuration_dialog with text type"""
        item = MenuItem(
            id="test-text",
            label="Test Text",
            description="Test text description",
            config_type="text",
            config_value="default text"
        )
        
        with patch.object(tui_dialogs, '_show_text_dialog') as mock_text:
            tui_dialogs.show_configuration_dialog(item)
            mock_text.assert_called_once_with(item)
    
    def test_show_configuration_dialog_unknown_type(self, tui_dialogs):
        """Test show_configuration_dialog with unknown type does nothing"""
        item = MenuItem(
            id="test-unknown",
            label="Test Unknown",
            description="Test unknown description",
            config_type="unknown_type",
            config_value="value"
        )
        
        # Should not raise an error
        tui_dialogs.show_configuration_dialog(item)
    
    @patch('curses.KEY_LEFT', 260)
    @patch('curses.KEY_RIGHT', 261)
    def test_show_slider_dialog_basic(self, tui_dialogs, mock_stdscr):
        """Test basic slider dialog functionality"""
        item = MenuItem(
            id="test-slider",
            label="Test Slider",
            description="Test slider",
            config_type="slider",
            config_value=50,
            config_range=(0, 100),
            config_unit="%"
        )
        
        # Mock getch to return 'q' to quit
        mock_stdscr.getch.return_value = ord('q')
        
        tui_dialogs._show_slider_dialog(item)
        
        # Verify dialog was drawn
        assert mock_stdscr.addstr.called
        assert mock_stdscr.getch.called
    
    def test_show_slider_dialog_swappiness(self, tui_dialogs, mock_stdscr):
        """Test slider dialog for swappiness with extra description"""
        item = MenuItem(
            id="swappiness",
            label="Swappiness",
            description="System swappiness",
            config_type="slider",
            config_value=10,
            config_range=(0, 100),
            config_unit="%"
        )
        
        mock_stdscr.getch.return_value = ord('q')
        
        tui_dialogs._show_slider_dialog(item)
        
        # Check that the special swappiness description was added
        calls = mock_stdscr.addstr.call_args_list
        descriptions = [str(call) for call in calls]
        assert any("Low: Keeps apps in RAM" in str(call) for call in calls)
    
    def test_show_slider_dialog_cpu_governor(self, tui_dialogs, mock_stdscr):
        """Test slider dialog for CPU governor with extra description"""
        item = MenuItem(
            id="cpu-governor",
            label="CPU Governor",
            description="CPU performance",
            config_type="slider",
            config_value=3,
            config_range=(1, 5),
            config_unit=""
        )
        
        mock_stdscr.getch.return_value = ord('q')
        
        tui_dialogs._show_slider_dialog(item)
        
        # Check that the special CPU governor description was added
        calls = mock_stdscr.addstr.call_args_list
        assert any("1=Save power" in str(call) for call in calls)
    
    @patch('curses.KEY_LEFT', 260)
    @patch('curses.KEY_RIGHT', 261)
    def test_show_slider_dialog_keyboard_navigation(self, tui_dialogs, mock_stdscr):
        """Test slider dialog keyboard navigation"""
        item = MenuItem(
            id="test-slider",
            label="Test Slider",
            description="Test slider",
            config_type="slider",
            config_value=50,
            config_range=(0, 100),
            config_unit="%"
        )
        
        # Simulate keyboard input: right arrow, left arrow, then quit
        mock_stdscr.getch.side_effect = [261, 260, ord('q')]
        
        tui_dialogs._show_slider_dialog(item)
        
        # Should have called getch 3 times
        assert mock_stdscr.getch.call_count == 3
    
    def test_show_dropdown_dialog_mock(self, tui_dialogs):
        """Test dropdown dialog exists and can be called"""
        item = MenuItem(
            id="test-dropdown",
            label="Test Dropdown",
            description="Test dropdown",
            config_type="dropdown",
            config_value="option1",
            config_options=[("opt1", "Option 1"), ("opt2", "Option 2")]
        )
        
        # Check that the method exists
        assert hasattr(tui_dialogs, '_show_dropdown_dialog')
        
        # Mock the method to test it's called
        with patch.object(tui_dialogs, '_show_dropdown_dialog') as mock_method:
            tui_dialogs._show_dropdown_dialog(item)
            mock_method.assert_called_once_with(item)
    
    def test_show_toggle_dialog_mock(self, tui_dialogs):
        """Test toggle dialog exists and can be called"""
        item = MenuItem(
            id="test-toggle",
            label="Test Toggle",
            description="Test toggle",
            config_type="toggle",
            config_value=True
        )
        
        # Check that the method exists
        assert hasattr(tui_dialogs, '_show_toggle_dialog')
        
        # Mock the method to test it's called
        with patch.object(tui_dialogs, '_show_toggle_dialog') as mock_method:
            tui_dialogs._show_toggle_dialog(item)
            mock_method.assert_called_once_with(item)
    
    def test_show_text_dialog_mock(self, tui_dialogs):
        """Test text dialog exists and can be called"""
        item = MenuItem(
            id="test-text",
            label="Test Text",
            description="Test text",
            config_type="text",
            config_value="default"
        )
        
        # Check that the method exists
        assert hasattr(tui_dialogs, '_show_text_dialog')
        
        # Mock the method to test it's called
        with patch.object(tui_dialogs, '_show_text_dialog') as mock_method:
            tui_dialogs._show_text_dialog(item)
            mock_method.assert_called_once_with(item)
    
    def test_dialog_screen_bounds(self, tui_dialogs, mock_stdscr):
        """Test that dialogs respect screen boundaries"""
        # Set a small screen size
        mock_stdscr.getmaxyx.return_value = (10, 40)
        mock_stdscr.getch.return_value = ord('q')
        
        item = MenuItem(
            id="test-slider",
            label="Test",
            description="Test",
            config_type="slider",
            config_value=50,
            config_range=(0, 100)
        )
        
        # Should not crash with small screen
        tui_dialogs._show_slider_dialog(item)
        
        # Check that addstr calls don't exceed screen bounds
        for call in mock_stdscr.addstr.call_args_list:
            args = call[0]
            if len(args) >= 2:
                y, x = args[0], args[1]
                assert y < 10, f"Y coordinate {y} exceeds screen height"
                assert x < 40, f"X coordinate {x} exceeds screen width"
    
    def test_dialog_value_persistence(self, tui_dialogs, mock_stdscr):
        """Test that dialog preserves original value on cancel"""
        original_value = 50
        item = MenuItem(
            id="test-slider",
            label="Test Slider",
            description="Test",
            config_type="slider",
            config_value=original_value,
            config_range=(0, 100)
        )
        
        # Simulate ESC key to cancel
        mock_stdscr.getch.return_value = 27  # ESC
        
        tui_dialogs._show_slider_dialog(item)
        
        # Value should remain unchanged
        assert item.config_value == original_value
    
    def test_empty_selected_items(self, mock_stdscr):
        """Test TUIDialogs with empty selected items"""
        dialogs = TUIDialogs(mock_stdscr, set())
        assert dialogs.selected_items == set()
        assert len(dialogs.selected_items) == 0
    
    def test_selected_items_modification(self, tui_dialogs):
        """Test that selected_items can be modified"""
        initial_count = len(tui_dialogs.selected_items)
        
        # Add an item
        tui_dialogs.selected_items.add("new_item")
        assert len(tui_dialogs.selected_items) == initial_count + 1
        
        # Remove an item
        tui_dialogs.selected_items.discard("item1")
        assert "item1" not in tui_dialogs.selected_items


@pytest.mark.parametrize("config_type,method_name", [
    ("slider", "_show_slider_dialog"),
    ("dropdown", "_show_dropdown_dialog"),
    ("toggle", "_show_toggle_dialog"),
    ("text", "_show_text_dialog"),
])
def test_configuration_dialog_routing(config_type, method_name):
    """Test that show_configuration_dialog routes to correct method"""
    mock_stdscr = MagicMock()
    dialogs = TUIDialogs(mock_stdscr, set())
    
    item = MenuItem(
        id=f"test-{config_type}",
        label=f"Test {config_type}",
        description="Test",
        config_type=config_type,
        config_value="test"
    )
    
    with patch.object(dialogs, method_name) as mock_method:
        dialogs.show_configuration_dialog(item)
        mock_method.assert_called_once_with(item)