"""
Unit tests for menu_ui.py - Professional menu UI system.
"""

import os
import sys
import time
from unittest.mock import patch, Mock, MagicMock, call
from io import StringIO

import pytest

# Mock rich library components before importing
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.layout'] = MagicMock()
sys.modules['rich.progress'] = MagicMock()
sys.modules['rich.prompt'] = MagicMock()
sys.modules['rich.text'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.box'] = MagicMock()
sys.modules['rich.live'] = MagicMock()

# Mock keyboard module
sys.modules['keyboard'] = MagicMock()

from lib.menu_ui import MenuOption, MenuUI, create_menu_ui


class TestMenuOption:
    """Test MenuOption dataclass."""
    
    def test_default_values(self):
        """Test default values for MenuOption."""
        option = MenuOption(
            key="1",
            icon="🚀",
            title="Test Option",
            description="Test description"
        )
        assert option.key == "1"
        assert option.icon == "🚀"
        assert option.title == "Test Option"
        assert option.description == "Test description"
        assert option.action is None
        assert option.visible is True
    
    def test_custom_values(self):
        """Test custom values for MenuOption."""
        option = MenuOption(
            key="2",
            icon="🔧",
            title="Custom",
            description="Custom desc",
            action="custom_action",
            visible=False
        )
        assert option.key == "2"
        assert option.icon == "🔧"
        assert option.title == "Custom"
        assert option.description == "Custom desc"
        assert option.action == "custom_action"
        assert option.visible is False


class TestMenuUI:
    """Test MenuUI class."""
    
    @pytest.fixture
    def menu_ui(self):
        """Create a MenuUI instance with mocked console."""
        with patch('lib.menu_ui.Console') as mock_console:
            ui = MenuUI()
            ui.console = mock_console.return_value
            return ui
    
    def test_initialization(self, menu_ui):
        """Test MenuUI initialization."""
        assert menu_ui.current_selection == 0
        assert menu_ui.console is not None
    
    @patch('os.system')
    def test_clear_screen_posix(self, mock_system, menu_ui):
        """Test clear_screen on POSIX systems."""
        with patch('os.name', 'posix'):
            menu_ui.clear_screen()
            mock_system.assert_called_once_with('clear')
    
    @patch('os.system')
    def test_clear_screen_windows(self, mock_system, menu_ui):
        """Test clear_screen on Windows systems."""
        with patch('os.name', 'nt'):
            menu_ui.clear_screen()
            mock_system.assert_called_once_with('cls')
    
    @patch('time.sleep')
    def test_show_splash_screen(self, mock_sleep, menu_ui):
        """Test splash screen display."""
        # Mock Progress context manager
        mock_progress = MagicMock()
        mock_progress.__enter__ = MagicMock(return_value=mock_progress)
        mock_progress.__exit__ = MagicMock(return_value=None)
        mock_progress.add_task.return_value = 1
        
        with patch('lib.menu_ui.Progress', return_value=mock_progress):
            with patch.object(menu_ui, 'clear_screen'):
                menu_ui.show_splash_screen()
                
                # Verify clear_screen was called
                menu_ui.clear_screen.assert_called_once()
                
                # Verify console print was called (for splash art)
                assert menu_ui.console.print.called
                
                # Verify progress bar was used
                mock_progress.add_task.assert_called_once()
                assert mock_progress.update.call_count == 4  # 4 loading messages
    
    @patch('lib.menu_ui.Prompt')
    def test_show_main_menu_without_config(self, mock_prompt, menu_ui):
        """Test main menu display without existing config."""
        mock_prompt.ask.return_value = "1"
        
        with patch.object(menu_ui, 'clear_screen'):
            choice = menu_ui.show_main_menu(has_config=False)
            
            # Verify clear_screen was called
            menu_ui.clear_screen.assert_called_once()
            
            # Verify choice returned
            assert choice == "1"
            
            # Verify prompt was called with correct choices
            mock_prompt.ask.assert_called_once()
            call_args = mock_prompt.ask.call_args[1]
            assert "1" in call_args["choices"]
            assert "8" in call_args["choices"]  # Exit option
            assert "2" not in call_args["choices"]  # Modify Setup (hidden when no config)
    
    @patch('lib.menu_ui.Prompt')
    def test_show_main_menu_with_config(self, mock_prompt, menu_ui):
        """Test main menu display with existing config."""
        mock_prompt.ask.return_value = "2"
        
        with patch.object(menu_ui, 'clear_screen'):
            choice = menu_ui.show_main_menu(has_config=True)
            
            # Verify choice returned
            assert choice == "2"
            
            # Verify prompt includes config-specific options
            call_args = mock_prompt.ask.call_args[1]
            assert "2" in call_args["choices"]  # Modify Setup
            assert "4" in call_args["choices"]  # Backup Config
            assert "5" in call_args["choices"]  # View History
    
    @patch('lib.menu_ui.Prompt')
    @patch('builtins.input')
    def test_show_main_menu_fallback(self, mock_input, mock_prompt, menu_ui):
        """Test main menu fallback to simple input."""
        mock_prompt.ask.side_effect = EOFError()
        mock_input.return_value = "3"
        
        with patch.object(menu_ui, 'clear_screen'):
            choice = menu_ui.show_main_menu(has_config=False)
            
            assert choice == "3"
            mock_input.assert_called_once()
    
    @patch('lib.menu_ui.Prompt')
    def test_show_profile_templates(self, mock_prompt, menu_ui):
        """Test profile template selection."""
        mock_prompt.ask.return_value = "1"
        
        with patch.object(menu_ui, 'clear_screen'):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('sys.stdout.isatty', return_value=True):
                    choice = menu_ui.show_profile_templates()
                    
                    assert choice == "1"
                    menu_ui.clear_screen.assert_called_once()
                    
                    # Verify prompt was called with correct choices
                    call_args = mock_prompt.ask.call_args[1]
                    assert "1" in call_args["choices"]
                    assert "5" in call_args["choices"]
                    assert "c" in call_args["choices"]
                    assert "C" in call_args["choices"]
    
    @patch('builtins.input')
    def test_show_profile_templates_fallback(self, mock_input, menu_ui):
        """Test profile template selection fallback."""
        mock_input.return_value = "c"
        
        with patch.object(menu_ui, 'clear_screen'):
            with patch('sys.stdin.isatty', return_value=False):
                choice = menu_ui.show_profile_templates()
                
                assert choice == "c"
                mock_input.assert_called_once()
    
    @patch('lib.menu_ui.Confirm')
    def test_show_section_selection(self, mock_confirm, menu_ui):
        """Test section selection."""
        # Mock user selecting first 3 sections
        mock_confirm.ask.side_effect = [True, True, True, False, False, False, False, False]
        
        with patch.object(menu_ui, 'clear_screen'):
            selected = menu_ui.show_section_selection()
            
            assert len(selected) == 3
            assert "desktop" in selected
            assert "themes" in selected
            assert "development" in selected
            assert "security" not in selected
    
    @patch('lib.menu_ui.Prompt')
    def test_show_app_customization_accept(self, mock_prompt, menu_ui):
        """Test app customization with accept all."""
        mock_prompt.ask.return_value = "a"
        
        customizations = {
            "description": "Test app customization",
            "features": ["Feature 1", "Feature 2"],
            "settings": {"setting1": "value1"},
            "extensions": ["ext1", "ext2"]
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            choice = menu_ui.show_app_customization("TestApp", customizations)
            
            assert choice == "a"
            menu_ui.clear_screen.assert_called_once()
    
    @patch('lib.menu_ui.Prompt')
    def test_show_app_customization_help(self, mock_prompt, menu_ui):
        """Test app customization with help request."""
        mock_prompt.ask.side_effect = ["?", "a"]  # First ask for help, then accept
        
        customizations = {
            "description": "Test app",
            "help": "This is help text"
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            with patch.object(menu_ui, 'show_customization_help'):
                choice = menu_ui.show_app_customization("TestApp", customizations)
                
                assert choice == "a"
                menu_ui.show_customization_help.assert_called_once_with("TestApp", customizations)
    
    def test_show_app_customization_system_preferences(self, menu_ui):
        """Test system preferences customization display."""
        customizations = {
            "description": "System settings",
            "mouse_touchpad": {"speed": "fast"},
            "keyboard": {"repeat": "fast"},
            "shortcuts": {
                "Ctrl+C": "Copy",
                "Ctrl+V": "Paste",
                "Ctrl+X": "Cut",
                "Ctrl+Z": "Undo",
                "Ctrl+Y": "Redo",
                "Ctrl+A": "Select All",
                "Ctrl+S": "Save",
                "Ctrl+O": "Open",
                "Ctrl+N": "New"
            }
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            with patch.object(menu_ui, '_show_system_preferences_overview'):
                with patch('lib.menu_ui.Prompt') as mock_prompt:
                    mock_prompt.ask.return_value = "a"
                    
                    choice = menu_ui.show_app_customization("System Preferences", customizations)
                    
                    assert choice == "a"
                    menu_ui._show_system_preferences_overview.assert_called_once_with(customizations)
    
    def test_show_system_preferences_overview(self, menu_ui):
        """Test system preferences overview display."""
        customizations = {
            "mouse_touchpad": {"speed": "fast", "scroll": "natural"},
            "keyboard": {"repeat": "fast", "delay": "short"},
            "shortcuts": {"Ctrl+C": "Copy", "Ctrl+V": "Paste"}
        }
        
        menu_ui._show_system_preferences_overview(customizations)
        
        # Verify console print was called
        assert menu_ui.console.print.called
        
        # Check that categories were printed
        print_calls = [call[0][0] for call in menu_ui.console.print.call_args_list]
        assert any("Mouse & Touchpad" in str(call) for call in print_calls)
        assert any("Keyboard" in str(call) for call in print_calls)
    
    @patch('builtins.input')
    def test_show_customization_help(self, mock_input, menu_ui):
        """Test customization help display."""
        mock_input.return_value = ""
        
        customizations = {
            "help": "This is detailed help text"
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            menu_ui.show_customization_help("TestApp", customizations)
            
            menu_ui.clear_screen.assert_called_once()
            assert menu_ui.console.print.called
    
    @patch('lib.menu_ui.Confirm')
    def test_show_detailed_customization(self, mock_confirm, menu_ui):
        """Test detailed customization selection."""
        # User selects first feature, first setting, first extension
        mock_confirm.ask.side_effect = [True, False, True, False, True, False]
        
        customizations = {
            "features": ["Feature 1", "Feature 2"],
            "settings": {"setting1": "value1", "setting2": "value2"},
            "extensions": ["ext1", "ext2"]
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            result = menu_ui.show_detailed_customization("TestApp", customizations)
            
            assert "features" in result
            assert len(result["features"]) == 1
            assert "Feature 1" in result["features"]
            
            assert "settings" in result
            assert "setting1" in result["settings"]
            assert "setting2" not in result["settings"]
            
            assert "extensions" in result
            assert len(result["extensions"]) == 1
            assert "ext1" in result["extensions"]
    
    @patch('lib.menu_ui.Confirm')
    def test_show_system_detailed_customization(self, mock_confirm, menu_ui):
        """Test system detailed customization."""
        # User selects mouse_touchpad and keyboard categories
        mock_confirm.ask.side_effect = [True, True, False, False, False, False, False, False, False, False, False, False]
        
        customizations = {
            "mouse_touchpad": {"speed": "fast"},
            "keyboard": {"repeat": "fast"},
            "clipboard": {"history": "enabled"},
            "features": ["feature1"],
            "help": "System help"
        }
        
        result = menu_ui._show_system_detailed_customization(customizations)
        
        assert "mouse_touchpad" in result
        assert "keyboard" in result
        assert "clipboard" not in result
        assert "features" in result  # Always included
        assert "help" in result  # Always included
    
    @patch('time.sleep')
    def test_show_progress(self, mock_sleep, menu_ui):
        """Test progress display."""
        steps = ["Step 1", "Step 2", "Step 3"]
        
        mock_progress = MagicMock()
        mock_progress.__enter__ = MagicMock(return_value=mock_progress)
        mock_progress.__exit__ = MagicMock(return_value=None)
        mock_progress.add_task.return_value = 1
        
        with patch('lib.menu_ui.Progress', return_value=mock_progress):
            menu_ui.show_progress("Test Task", steps)
            
            mock_progress.add_task.assert_called_once()
            assert mock_progress.update.call_count == len(steps)
            assert mock_sleep.call_count == len(steps)
    
    @patch('lib.menu_ui.Prompt')
    def test_show_success_screen(self, mock_prompt, menu_ui):
        """Test success screen display."""
        mock_prompt.ask.return_value = "r"
        
        stats = {
            "configured": ["Desktop Environment", "Development Tools"],
            "packages": 42,
            "boot_improvement": "3.5",
            "security_score": "A+"
        }
        
        with patch.object(menu_ui, 'clear_screen'):
            choice = menu_ui.show_success_screen(stats)
            
            assert choice == "r"
            menu_ui.clear_screen.assert_called_once()
            
            # Verify stats were displayed
            print_calls = [call[0][0] for call in menu_ui.console.print.call_args_list]
            assert any("42" in str(call) for call in print_calls)
            assert any("3.5" in str(call) for call in print_calls)
            assert any("A+" in str(call) for call in print_calls)
    
    @patch('builtins.input')
    def test_show_success_screen_fallback(self, mock_input, menu_ui):
        """Test success screen with fallback input."""
        mock_input.return_value = "l"
        
        stats = {"configured": [], "packages": 0}
        
        with patch.object(menu_ui, 'clear_screen'):
            with patch('lib.menu_ui.Prompt') as mock_prompt:
                mock_prompt.ask.side_effect = EOFError()
                
                choice = menu_ui.show_success_screen(stats)
                
                assert choice == "l"
                mock_input.assert_called_once()


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_create_menu_ui(self):
        """Test create_menu_ui factory function."""
        with patch('lib.menu_ui.Console'):
            ui = create_menu_ui()
            assert isinstance(ui, MenuUI)
            assert ui.current_selection == 0


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('lib.menu_ui.Prompt')
    @patch('builtins.input')
    def test_keyboard_interrupt_handling(self, mock_input, mock_prompt, menu_ui):
        """Test handling of keyboard interrupts."""
        mock_prompt.ask.side_effect = KeyboardInterrupt()
        mock_input.side_effect = KeyboardInterrupt()
        
        with patch.object(menu_ui, 'clear_screen'):
            # Main menu should default to exit
            choice = menu_ui.show_main_menu()
            assert choice == "8"
            
            # Profile templates should default to custom
            choice = menu_ui.show_profile_templates()
            assert choice == "c"
    
    def test_invalid_input_handling(self, menu_ui):
        """Test handling of invalid inputs."""
        with patch.object(menu_ui, 'clear_screen'):
            with patch('builtins.input') as mock_input:
                # Invalid profile choice
                mock_input.return_value = "x"
                with patch('sys.stdin.isatty', return_value=False):
                    choice = menu_ui.show_profile_templates()
                    assert choice == "c"  # Should default to custom
                    
                    # Verify warning was printed
                    print_calls = [call[0][0] for call in menu_ui.console.print.call_args_list]
                    assert any("Invalid choice" in str(call) for call in print_calls)


class TestIntegration:
    """Integration tests for menu flow."""
    
    def test_full_menu_flow(self, menu_ui):
        """Test a complete menu interaction flow."""
        with patch.object(menu_ui, 'clear_screen'):
            # Show splash
            with patch('time.sleep'):
                with patch('lib.menu_ui.Progress'):
                    menu_ui.show_splash_screen()
            
            # Show main menu and select fresh install
            with patch('lib.menu_ui.Prompt') as mock_prompt:
                mock_prompt.ask.return_value = "1"
                choice = menu_ui.show_main_menu()
                assert choice == "1"
            
            # Show profile templates and select developer
            with patch('lib.menu_ui.Prompt') as mock_prompt:
                mock_prompt.ask.return_value = "1"
                with patch('sys.stdin.isatty', return_value=True):
                    with patch('sys.stdout.isatty', return_value=True):
                        profile = menu_ui.show_profile_templates()
                        assert profile == "1"
            
            # Show app customization
            with patch('lib.menu_ui.Prompt') as mock_prompt:
                mock_prompt.ask.return_value = "a"
                customizations = {"description": "Test", "features": ["F1"]}
                choice = menu_ui.show_app_customization("VS Code", customizations)
                assert choice == "a"
            
            # Show success
            with patch('lib.menu_ui.Prompt') as mock_prompt:
                mock_prompt.ask.return_value = "r"
                stats = {"configured": ["VS Code"], "packages": 10}
                choice = menu_ui.show_success_screen(stats)
                assert choice == "r"