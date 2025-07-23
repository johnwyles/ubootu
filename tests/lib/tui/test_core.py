"""
Unit tests for tui/core.py - Core TUI orchestration.
"""

import curses
import sys
from unittest.mock import patch, Mock, MagicMock, mock_open, call
from typing import Dict

import pytest

from lib.tui.core import UbootuTUI, run_tui, main
from lib.tui.models import MenuItem


class TestUbootuTUI:
    """Test UbootuTUI class."""
    
    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock curses screen."""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 100)  # height, width
        stdscr.getch.return_value = -1  # No key pressed by default
        return stdscr
    
    @pytest.fixture
    def mock_components(self):
        """Mock all TUI components."""
        with patch('lib.tui.core.TUIRenderer') as mock_renderer:
            with patch('lib.tui.core.TUIDialogs') as mock_dialogs:
                with patch('lib.tui.core.TUIEventHandler') as mock_handler:
                    with patch('lib.tui.core.TUIConfigManager') as mock_config:
                        with patch('lib.tui.core.MenuRegistry') as mock_registry:
                            yield {
                                'renderer': mock_renderer,
                                'dialogs': mock_dialogs,
                                'handler': mock_handler,
                                'config': mock_config,
                                'registry': mock_registry
                            }
    
    def test_initialization(self, mock_stdscr, mock_components):
        """Test UbootuTUI initialization."""
        # Mock menu builders
        mock_dev_builder = Mock()
        mock_dev_builder.build.return_value = {
            "development": MenuItem("development", "Development", "Dev tools", is_category=True)
        }
        
        mock_components['registry'].return_value.builders = {
            'development': mock_dev_builder
        }
        
        tui = UbootuTUI(mock_stdscr)
        
        assert tui.stdscr == mock_stdscr
        assert tui.selected_sections is None
        assert tui.cancelled is False
        assert isinstance(tui.menu_items, dict)
        assert isinstance(tui.selected_items, set)
        
        # Verify components were initialized
        mock_components['config'].assert_called_once()
        mock_components['renderer'].assert_called_once()
        mock_components['dialogs'].assert_called_once()
        mock_components['handler'].assert_called_once()
    
    def test_initialization_with_selected_sections(self, mock_stdscr, mock_components):
        """Test UbootuTUI initialization with pre-selected sections."""
        selected_sections = ["development", "themes", "applications"]
        
        # Mock menu builders
        mock_registry = Mock()
        mock_registry.builders = {}
        mock_components['registry'].return_value = mock_registry
        
        tui = UbootuTUI(mock_stdscr, selected_sections)
        
        assert tui.selected_sections == selected_sections
        
        # Check that themes is mapped to desktop in root menu
        root_item = tui.menu_items.get("root")
        assert root_item is not None
        assert "desktop" in root_item.children  # themes mapped to desktop
        assert "development" in root_item.children
        assert "applications" in root_item.children
    
    def test_build_menu_structure(self, mock_stdscr, mock_components):
        """Test menu structure building."""
        # Mock menu builders
        mock_dev_builder = Mock()
        mock_dev_builder.build.return_value = {
            "development": MenuItem("development", "Development", "Dev tools", is_category=True, children=["python"]),
            "python": MenuItem("python", "Python", "Python development", parent="development")
        }
        
        mock_desktop_builder = Mock()
        mock_desktop_builder.build.return_value = {
            "desktop": MenuItem("desktop", "Desktop", "Desktop settings", is_category=True)
        }
        
        mock_registry = Mock()
        mock_registry.builders = {
            'development': mock_dev_builder,
            'desktop': mock_desktop_builder
        }
        mock_components['registry'].return_value = mock_registry
        
        tui = UbootuTUI(mock_stdscr)
        
        # Verify menu structure
        assert "root" in tui.menu_items
        assert "actions" in tui.menu_items
        assert "action-install" in tui.menu_items
        assert "action-save" in tui.menu_items
        assert "action-reset" in tui.menu_items
        assert "action-exit" in tui.menu_items
        assert "development" in tui.menu_items
        assert "python" in tui.menu_items
        assert "desktop" in tui.menu_items
        
        # Verify root menu
        root = tui.menu_items["root"]
        assert root.is_category
        assert "development" in root.children
        assert "desktop" in root.children
    
    @patch('curses.curs_set')
    def test_setup_screen(self, mock_curs_set, mock_stdscr, mock_components):
        """Test screen setup."""
        mock_components['registry'].return_value.builders = {}
        
        tui = UbootuTUI(mock_stdscr)
        
        # Verify screen setup
        mock_curs_set.assert_called_once_with(0)  # Hide cursor
        mock_stdscr.keypad.assert_called_once_with(True)
        mock_stdscr.timeout.assert_called_once_with(50)
    
    @patch('curses.curs_set', side_effect=Exception("Terminal doesn't support"))
    def test_setup_screen_error_handling(self, mock_curs_set, mock_stdscr, mock_components):
        """Test screen setup error handling."""
        mock_components['registry'].return_value.builders = {}
        
        # Should not raise exception
        tui = UbootuTUI(mock_stdscr)
        assert tui is not None
    
    def test_sync_component_state(self, mock_stdscr, mock_components):
        """Test component state synchronization."""
        mock_components['registry'].return_value.builders = {}
        
        # Set up mock config manager state
        mock_config_instance = mock_components['config'].return_value
        mock_config_instance.current_menu = "development"
        mock_config_instance.current_item = 2
        mock_config_instance.scroll_offset = 1
        
        tui = UbootuTUI(mock_stdscr)
        
        # Verify initial sync
        assert tui.renderer.current_menu == "development"
        assert tui.renderer.current_item == 2
        assert tui.renderer.scroll_offset == 1
        assert tui.event_handler.current_menu == "development"
        assert tui.event_handler.current_item == 2
        assert tui.event_handler.scroll_offset == 1
    
    def test_update_state_from_event_handler(self, mock_stdscr, mock_components):
        """Test state update from event handler."""
        mock_components['registry'].return_value.builders = {}
        
        tui = UbootuTUI(mock_stdscr)
        
        # Simulate event handler state change
        tui.event_handler.current_menu = "applications"
        tui.event_handler.current_item = 5
        tui.event_handler.scroll_offset = 3
        tui.event_handler.breadcrumb_stack = ["root", "applications"]
        tui.event_handler.cancelled = True
        
        tui._update_state_from_event_handler()
        
        # Verify state was updated
        assert tui.config_manager.current_menu == "applications"
        assert tui.config_manager.current_item == 5
        assert tui.config_manager.scroll_offset == 3
        assert tui.config_manager.breadcrumb_stack == ["root", "applications"]
        assert tui.cancelled is True
    
    def test_draw_interface(self, mock_stdscr, mock_components):
        """Test interface drawing."""
        mock_components['registry'].return_value.builders = {}
        
        # Set up mock config manager
        mock_config_instance = mock_components['config'].return_value
        mock_config_instance.get_current_menu_items.return_value = [
            MenuItem("item1", "Item 1", "First item"),
            MenuItem("item2", "Item 2", "Second item")
        ]
        
        tui = UbootuTUI(mock_stdscr)
        tui._draw_interface()
        
        # Verify all drawing methods were called
        tui.renderer.draw_header.assert_called_once()
        tui.renderer.draw_menu.assert_called_once()
        tui.renderer.draw_help.assert_called_once()
        tui.renderer.draw_stats.assert_called_once()
        mock_stdscr.refresh.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    def test_run_normal_exit(self, mock_file, mock_stdscr, mock_components):
        """Test normal TUI run and exit."""
        mock_components['registry'].return_value.builders = {}
        
        # Mock event handler to return False (exit)
        mock_handler_instance = mock_components['handler'].return_value
        mock_handler_instance.handle_key.return_value = False
        
        # Mock key press
        mock_stdscr.getch.side_effect = [ord('q'), -1]  # 'q' key then no key
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 0
        assert not tui.cancelled
        
        # Verify initial draw
        mock_stdscr.clear.assert_called_once()
        
        # Verify key handling
        mock_handler_instance.handle_key.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    def test_run_cancelled_exit(self, mock_file, mock_stdscr, mock_components):
        """Test TUI run with cancellation."""
        mock_components['registry'].return_value.builders = {}
        
        # Mock event handler to set cancelled
        mock_handler_instance = mock_components['handler'].return_value
        mock_handler_instance.handle_key.return_value = False
        mock_handler_instance.cancelled = True
        
        mock_stdscr.getch.side_effect = [27, -1]  # ESC key
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 1
        assert tui.cancelled
    
    @patch('builtins.open', new_callable=mock_open)
    def test_run_keyboard_interrupt(self, mock_file, mock_stdscr, mock_components):
        """Test TUI run with keyboard interrupt."""
        mock_components['registry'].return_value.builders = {}
        
        # Mock getch to raise KeyboardInterrupt
        mock_stdscr.getch.side_effect = KeyboardInterrupt()
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 1
        assert tui.cancelled
        
        # Verify debug log was written
        mock_file.assert_called()
        mock_file().write.assert_called()
    
    @patch('builtins.open', new_callable=mock_open)
    def test_run_exception_handling(self, mock_file, mock_stdscr, mock_components):
        """Test TUI run with general exception."""
        mock_components['registry'].return_value.builders = {}
        
        # Mock getch to raise exception
        mock_stdscr.getch.side_effect = Exception("Test error")
        
        tui = UbootuTUI(mock_stdscr)
        exit_code = tui.run()
        
        assert exit_code == 1
        assert tui.cancelled
        
        # Verify debug log was written
        mock_file.assert_called()
        write_calls = mock_file().write.call_args_list
        assert any("Test error" in str(call) for call in write_calls)
    
    def test_run_multiple_key_presses(self, mock_stdscr, mock_components):
        """Test TUI run with multiple key presses."""
        mock_components['registry'].return_value.builders = {}
        
        # Mock event handler
        mock_handler_instance = mock_components['handler'].return_value
        mock_handler_instance.handle_key.side_effect = [True, True, False]  # Continue, continue, exit
        
        # Mock key presses
        mock_stdscr.getch.side_effect = [ord('j'), ord('k'), ord('q'), -1]
        
        tui = UbootuTUI(mock_stdscr)
        with patch('builtins.open', mock_open()):
            exit_code = tui.run()
        
        assert exit_code == 0
        assert mock_handler_instance.handle_key.call_count == 3
        assert mock_stdscr.erase.call_count == 3  # Redrawn after each key


class TestRunTUI:
    """Test run_tui function."""
    
    @patch('curses.wrapper')
    def test_run_tui_no_sections(self, mock_wrapper):
        """Test run_tui without selected sections."""
        mock_wrapper.return_value = 0
        
        exit_code = run_tui()
        
        assert exit_code == 0
        mock_wrapper.assert_called_once()
        
        # Get the function passed to wrapper
        tui_main = mock_wrapper.call_args[0][0]
        assert callable(tui_main)
    
    @patch('curses.wrapper')
    def test_run_tui_with_sections(self, mock_wrapper):
        """Test run_tui with selected sections."""
        mock_wrapper.return_value = 0
        selected_sections = ["development", "security"]
        
        exit_code = run_tui(selected_sections)
        
        assert exit_code == 0
        mock_wrapper.assert_called_once()
    
    @patch('curses.wrapper')
    @patch('lib.tui.core.UbootuTUI')
    def test_run_tui_execution(self, mock_tui_class, mock_wrapper):
        """Test actual TUI execution through wrapper."""
        # Set up mock TUI instance
        mock_tui = Mock()
        mock_tui.run.return_value = 1
        mock_tui_class.return_value = mock_tui
        
        # Execute wrapper function directly
        def execute_wrapper(func):
            mock_stdscr = MagicMock()
            return func(mock_stdscr)
        
        mock_wrapper.side_effect = execute_wrapper
        
        exit_code = run_tui(["development"])
        
        assert exit_code == 1
        mock_tui_class.assert_called_once()
        mock_tui.run.assert_called_once()


class TestMain:
    """Test main function."""
    
    @patch('sys.argv', ['ubootu-tui'])
    @patch('sys.exit')
    @patch('lib.tui.core.run_tui')
    def test_main_no_args(self, mock_run_tui, mock_exit):
        """Test main with no command line arguments."""
        mock_run_tui.return_value = 0
        
        main()
        
        mock_run_tui.assert_called_once_with(None)
        mock_exit.assert_called_once_with(0)
    
    @patch('sys.argv', ['ubootu-tui', 'development', 'security', 'applications'])
    @patch('sys.exit')
    @patch('lib.tui.core.run_tui')
    def test_main_with_sections(self, mock_run_tui, mock_exit):
        """Test main with section arguments."""
        mock_run_tui.return_value = 0
        
        main()
        
        mock_run_tui.assert_called_once_with(['development', 'security', 'applications'])
        mock_exit.assert_called_once_with(0)
    
    @patch('sys.argv', ['ubootu-tui', 'invalid'])
    @patch('sys.exit')
    @patch('lib.tui.core.run_tui')
    def test_main_with_error(self, mock_run_tui, mock_exit):
        """Test main with TUI returning error."""
        mock_run_tui.return_value = 1
        
        main()
        
        mock_run_tui.assert_called_once_with(['invalid'])
        mock_exit.assert_called_once_with(1)