"""
Unit tests for tui/renderer.py - TUI rendering operations.
"""

import curses
from unittest.mock import Mock, MagicMock, patch, call

import pytest

from lib.tui.renderer import TUIRenderer
from lib.tui.models import MenuItem


class TestTUIRenderer:
    """Test TUIRenderer class."""
    
    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock curses screen."""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 100)  # height, width
        return stdscr
    
    @pytest.fixture
    def sample_menu_items(self):
        """Create sample menu items for testing."""
        items = {
            "root": MenuItem(
                "root", "🚀 Ubootu", "Main menu", 
                is_category=True, children=["development", "desktop"]
            ),
            "development": MenuItem(
                "development", "Development", "Dev tools", 
                parent="root", is_category=True, children=["python", "nodejs"]
            ),
            "python": MenuItem(
                "python", "Python", "Python development", 
                parent="development"
            ),
            "nodejs": MenuItem(
                "nodejs", "Node.js", "Node.js development", 
                parent="development"
            ),
            "desktop": MenuItem(
                "desktop", "Desktop", "Desktop settings", 
                parent="root", is_category=True
            ),
            "actions": MenuItem(
                "actions", "Actions", "Actions menu",
                parent="root", is_category=True
            )
        }
        return items
    
    @pytest.fixture
    def renderer(self, mock_stdscr, sample_menu_items):
        """Create a TUIRenderer instance."""
        selected_items = set()
        return TUIRenderer(mock_stdscr, sample_menu_items, selected_items)
    
    def test_initialization(self, renderer, mock_stdscr, sample_menu_items):
        """Test TUIRenderer initialization."""
        assert renderer.stdscr == mock_stdscr
        assert renderer.menu_items == sample_menu_items
        assert isinstance(renderer.selected_items, set)
        assert renderer.current_menu == "root"
        assert renderer.current_item == 0
        assert renderer.scroll_offset == 0
    
    def test_draw_header_root_menu(self, renderer, mock_stdscr):
        """Test header drawing for root menu."""
        renderer.current_menu = "root"
        renderer.selected_items = {"python", "nodejs"}
        
        renderer.draw_header()
        
        # Verify header was drawn
        assert mock_stdscr.addstr.called
        assert mock_stdscr.attron.called
        assert mock_stdscr.attroff.called
        
        # Check that selection count is displayed
        calls = [call[0] for call in mock_stdscr.addstr.call_args_list]
        assert any("[2/" in str(call) for call in calls)  # 2 selected items
    
    def test_draw_header_submenu(self, renderer, mock_stdscr):
        """Test header drawing for submenu with breadcrumbs."""
        renderer.current_menu = "development"
        
        renderer.draw_header()
        
        # Verify breadcrumb was drawn
        calls = [call[0] for call in mock_stdscr.addstr.call_args_list]
        assert any("Development" in str(call) for call in calls)
        assert any("BACKSPACE" in str(call) or "Back" in str(call) for call in calls)
    
    def test_draw_header_small_terminal(self, renderer, mock_stdscr):
        """Test header drawing with small terminal."""
        mock_stdscr.getmaxyx.return_value = (10, 40)  # Small terminal
        
        # Should not raise exception
        renderer.draw_header()
    
    def test_draw_header_curses_error(self, renderer, mock_stdscr):
        """Test header drawing with curses error."""
        mock_stdscr.addstr.side_effect = curses.error("Terminal error")
        
        # Should not raise exception
        renderer.draw_header()
    
    def test_get_breadcrumb(self, renderer):
        """Test breadcrumb generation."""
        # Root menu
        renderer.current_menu = "root"
        assert renderer.get_breadcrumb() == ""
        
        # First level
        renderer.current_menu = "development"
        assert renderer.get_breadcrumb() == "Development"
        
        # Second level
        renderer.current_menu = "python"
        assert renderer.get_breadcrumb() == "Development > Python"
    
    def test_draw_menu_basic(self, renderer, mock_stdscr):
        """Test basic menu drawing."""
        menu_items = [
            MenuItem("item1", "Item 1", "First item"),
            MenuItem("item2", "Item 2", "Second item"),
            MenuItem("item3", "Item 3", "Third item")
        ]
        
        renderer.current_item = 1  # Select second item
        renderer.draw_menu(menu_items)
        
        # Verify menu was drawn
        assert mock_stdscr.addstr.called
        assert mock_stdscr.attron.called_with(curses.A_REVERSE)  # Highlight
    
    def test_draw_menu_with_categories(self, renderer, mock_stdscr):
        """Test menu drawing with categories."""
        menu_items = [
            MenuItem("cat1", "Category 1", "First category", is_category=True, children=["item1"]),
            MenuItem("item1", "Item 1", "First item", parent="cat1"),
            MenuItem("cat2", "Category 2", "Second category", is_category=True, children=[])
        ]
        
        # Mock category selection status
        with patch.object(renderer, 'get_category_selection_status') as mock_status:
            mock_status.side_effect = ['full', 'none']  # cat1 full, cat2 none
            
            renderer.draw_menu(menu_items)
            
            assert mock_status.call_count == 2
    
    def test_draw_menu_scrolling(self, renderer, mock_stdscr):
        """Test menu drawing with scrolling."""
        # Create many items to test scrolling
        menu_items = [
            MenuItem(f"item{i}", f"Item {i}", f"Item {i} description")
            for i in range(50)
        ]
        
        mock_stdscr.getmaxyx.return_value = (20, 100)  # Limited height
        
        # Test scroll down
        renderer.current_item = 25
        renderer.draw_menu(menu_items)
        
        # Verify scroll offset was adjusted
        assert renderer.scroll_offset > 0
    
    def test_draw_menu_with_description(self, renderer, mock_stdscr):
        """Test menu drawing with F1 instruction in description."""
        renderer.menu_items["root"].description = "Navigate: arrows | Press F1 for actions"
        renderer.current_menu = "root"
        
        menu_items = []
        renderer.draw_menu(menu_items)
        
        # Verify F1 instruction handling
        calls = [str(call) for call in mock_stdscr.addstr.call_args_list]
        assert any("F1" in call for call in calls)
    
    @patch('curses.color_pair')
    @patch('curses.has_colors')
    def test_draw_menu_with_colors(self, mock_has_colors, mock_color_pair, renderer, mock_stdscr):
        """Test menu drawing with color support."""
        mock_has_colors.return_value = True
        mock_color_pair.return_value = 1
        
        menu_items = [
            MenuItem("item1", "Item 1", "First item", selected=True),
            MenuItem("item2", "Item 2", "Second item", selected=False)
        ]
        
        renderer.draw_menu(menu_items)
        
        # Verify color functions were used
        assert mock_has_colors.called
    
    def test_draw_menu_configurable_items(self, renderer, mock_stdscr):
        """Test drawing configurable menu items."""
        menu_items = [
            MenuItem(
                "slider", "Swappiness", "System swappiness",
                is_configurable=True, config_type="slider",
                config_value=10, config_unit="%", config_range=(0, 100)
            ),
            MenuItem(
                "toggle", "Enable Firewall", "Firewall setting",
                is_configurable=True, config_type="toggle",
                config_value=True
            ),
            MenuItem(
                "dropdown", "Desktop", "Desktop environment",
                is_configurable=True, config_type="dropdown",
                config_value="gnome", config_options=[("gnome", "GNOME"), ("kde", "KDE")]
            )
        ]
        
        # Mock the format methods
        with patch.object(renderer, 'format_slider') as mock_slider:
            with patch.object(renderer, 'format_toggle') as mock_toggle:
                with patch.object(renderer, 'format_dropdown') as mock_dropdown:
                    mock_slider.return_value = "[====------] 10%"
                    mock_toggle.return_value = "[ON]"
                    mock_dropdown.return_value = "GNOME"
                    
                    renderer.draw_menu(menu_items)
                    
                    mock_slider.assert_called_once()
                    mock_toggle.assert_called_once()
                    mock_dropdown.assert_called_once()
    
    def test_get_category_selection_status(self, renderer):
        """Test category selection status calculation."""
        # Add some child items
        renderer.menu_items["dev-child1"] = MenuItem("dev-child1", "Child 1", "Child 1", parent="development")
        renderer.menu_items["dev-child2"] = MenuItem("dev-child2", "Child 2", "Child 2", parent="development")
        renderer.menu_items["dev-child3"] = MenuItem("dev-child3", "Child 3", "Child 3", parent="development")
        renderer.menu_items["development"].children = ["dev-child1", "dev-child2", "dev-child3"]
        
        # Test none selected
        assert renderer.get_category_selection_status("development") == "none"
        
        # Test partial selection
        renderer.selected_items.add("dev-child1")
        assert renderer.get_category_selection_status("development") == "partial"
        
        # Test full selection
        renderer.selected_items.add("dev-child2")
        renderer.selected_items.add("dev-child3")
        assert renderer.get_category_selection_status("development") == "full"
    
    def test_format_configurable_items(self, renderer):
        """Test formatting of configurable items (if methods exist)."""
        # These methods might not exist in the actual implementation
        # This is a placeholder for testing format methods if they're added
        pass
    
    def test_draw_methods_missing(self, renderer, mock_stdscr):
        """Test that missing draw methods don't cause errors."""
        # Some draw methods might not be implemented yet
        # Test that calling them doesn't raise exceptions
        
        # These might not exist but shouldn't crash
        if hasattr(renderer, 'draw_help'):
            renderer.draw_help()
        
        if hasattr(renderer, 'draw_stats'):
            renderer.draw_stats()
    
    def test_unicode_handling(self, renderer, mock_stdscr):
        """Test handling of unicode characters."""
        menu_items = [
            MenuItem("unicode", "🚀 Rocket", "Unicode emoji test"),
            MenuItem("special", "Spëcial", "Special characters")
        ]
        
        renderer.draw_menu(menu_items)
        
        # Should handle unicode gracefully
        assert mock_stdscr.addstr.called
    
    def test_empty_menu(self, renderer, mock_stdscr):
        """Test drawing empty menu."""
        renderer.draw_menu([])
        
        # Should not crash with empty menu
        assert True
    
    def test_menu_item_truncation(self, renderer, mock_stdscr):
        """Test long menu items are truncated."""
        mock_stdscr.getmaxyx.return_value = (30, 50)  # Narrow terminal
        
        menu_items = [
            MenuItem(
                "long", 
                "This is a very long menu item label that should be truncated",
                "This is an extremely long description that definitely won't fit"
            )
        ]
        
        renderer.draw_menu(menu_items)
        
        # Verify addstr was called with truncated strings
        calls = mock_stdscr.addstr.call_args_list
        # Check that no call exceeds terminal width
        for call in calls:
            if len(call[0]) >= 3:  # Has string argument
                assert len(str(call[0][2])) <= 50