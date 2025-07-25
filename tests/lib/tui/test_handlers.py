"""
Unit tests for tui/handlers.py - Event handling system.
"""

from __future__ import annotations

import curses
from datetime import datetime
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import pytest
import yaml

from lib.tui.handlers import TUIEventHandler
from lib.tui.models import MenuItem


class TestTUIEventHandler:
    """Test TUIEventHandler class."""

    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock curses screen."""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 100)  # height, width
        stdscr.getch.return_value = -1  # No key by default
        return stdscr

    @pytest.fixture
    def sample_menu_items(self):
        """Create sample menu items."""
        return {
            "root": MenuItem(
                "root", "Root", "Root menu", is_category=True, children=["dev", "apps"]
            ),
            "dev": MenuItem(
                "dev",
                "Development",
                "Dev tools",
                parent="root",
                is_category=True,
                children=["python", "nodejs"],
            ),
            "apps": MenuItem(
                "apps",
                "Applications",
                "Apps",
                parent="root",
                is_category=True,
                children=["firefox"],
            ),
            "python": MenuItem("python", "Python", "Python dev", parent="dev"),
            "nodejs": MenuItem("nodejs", "Node.js", "Node dev", parent="dev"),
            "firefox": MenuItem("firefox", "Firefox", "Browser", parent="apps"),
            "actions": MenuItem(
                "actions",
                "Actions",
                "Actions menu",
                parent="root",
                is_category=True,
                children=[
                    "action-install",
                    "action-save",
                    "action-reset",
                    "action-exit",
                ],
            ),
            "action-install": MenuItem(
                "action-install", "Install", "Start installation", parent="actions"
            ),
            "action-save": MenuItem(
                "action-save", "Save", "Save config", parent="actions"
            ),
            "action-reset": MenuItem(
                "action-reset", "Reset", "Reset config", parent="actions"
            ),
            "action-exit": MenuItem(
                "action-exit", "Exit", "Exit without saving", parent="actions"
            ),
            "configurable": MenuItem(
                "configurable",
                "Config Item",
                "Configurable",
                is_configurable=True,
                config_type="slider",
                config_value=50,
            ),
        }

    @pytest.fixture
    def handler(self, mock_stdscr, sample_menu_items):
        """Create TUIEventHandler instance."""
        selected_items = set()
        return TUIEventHandler(mock_stdscr, sample_menu_items, selected_items)

    def test_initialization(self, handler, mock_stdscr, sample_menu_items):
        """Test TUIEventHandler initialization."""
        assert handler.stdscr == mock_stdscr
        assert handler.menu_items == sample_menu_items
        assert isinstance(handler.selected_items, set)
        assert handler.current_menu == "root"
        assert handler.current_item == 0
        assert handler.scroll_offset == 0
        assert handler.breadcrumb_stack == []
        assert handler.cancelled is False
        assert handler.dialog_handler is None

    def test_set_dialog_handler(self, handler):
        """Test setting dialog handler."""
        mock_dialog = Mock()
        handler.set_dialog_handler(mock_dialog)
        assert handler.dialog_handler == mock_dialog

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_navigation_up(self, mock_file, handler):
        """Test UP key navigation."""
        menu_items = [handler.menu_items["dev"], handler.menu_items["apps"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 1

        # Test UP arrow
        result = handler.handle_key(curses.KEY_UP, menu_getter, help_callback)
        assert result is True
        assert handler.current_item == 0

        # Test 'k' key
        handler.current_item = 1
        result = handler.handle_key(ord("k"), menu_getter, help_callback)
        assert handler.current_item == 0

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_navigation_down(self, mock_file, handler):
        """Test DOWN key navigation."""
        menu_items = [handler.menu_items["dev"], handler.menu_items["apps"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0

        # Test DOWN arrow
        result = handler.handle_key(curses.KEY_DOWN, menu_getter, help_callback)
        assert result is True
        assert handler.current_item == 1

        # Test 'j' key
        handler.current_item = 0
        result = handler.handle_key(ord("j"), menu_getter, help_callback)
        assert handler.current_item == 1

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_page_navigation(self, mock_file, handler):
        """Test page up/down navigation."""
        # Create many items
        menu_items = [MenuItem(f"item{i}", f"Item {i}", f"Desc {i}") for i in range(20)]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 10

        # Page down
        handler.handle_key(curses.KEY_NPAGE, menu_getter, help_callback)
        assert handler.current_item == 19  # Last item (10 + 10 capped at 19)

        # Page up
        handler.current_item = 15
        handler.handle_key(curses.KEY_PPAGE, menu_getter, help_callback)
        assert handler.current_item == 5  # 15 - 10

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_home_end(self, mock_file, handler):
        """Test HOME/END keys."""
        menu_items = [MenuItem(f"item{i}", f"Item {i}", f"Desc {i}") for i in range(10)]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 5

        # HOME key
        handler.handle_key(curses.KEY_HOME, menu_getter, help_callback)
        assert handler.current_item == 0

        # END key
        handler.handle_key(curses.KEY_END, menu_getter, help_callback)
        assert handler.current_item == 9

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_space_toggle_item(self, mock_file, handler):
        """Test SPACE key for item selection."""
        menu_items = [handler.menu_items["python"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0

        # Toggle on
        handler.handle_key(ord(" "), menu_getter, help_callback)
        assert "python" in handler.selected_items
        assert handler.menu_items["python"].selected is True

        # Toggle off
        handler.handle_key(ord(" "), menu_getter, help_callback)
        assert "python" not in handler.selected_items
        assert handler.menu_items["python"].selected is False

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_space_toggle_category(self, mock_file, handler):
        """Test SPACE key for category selection."""
        menu_items = [handler.menu_items["dev"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0

        # Toggle category (should select all children)
        with patch.object(handler, "_select_all_in_category_toggle") as mock_toggle:
            handler.handle_key(ord(" "), menu_getter, help_callback)
            mock_toggle.assert_called_once_with("dev")

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_enter_category(self, mock_file, handler):
        """Test ENTER key on category."""
        menu_items = [handler.menu_items["dev"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0
        handler.current_menu = "root"

        # Enter category
        result = handler.handle_key(ord("\n"), menu_getter, help_callback)

        assert result is True
        assert handler.current_menu == "dev"
        assert handler.current_item == 0
        assert handler.scroll_offset == 0
        assert len(handler.breadcrumb_stack) == 1
        assert handler.breadcrumb_stack[0] == ("root", 0, 0)

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_enter_action(self, mock_file, handler):
        """Test ENTER key on action items."""
        menu_getter = Mock()
        help_callback = Mock()

        # Test install action
        menu_items = [handler.menu_items["action-install"]]
        menu_getter.return_value = menu_items
        handler.current_item = 0

        with patch.object(
            handler, "_handle_install", return_value=False
        ) as mock_install:
            result = handler.handle_key(ord("\n"), menu_getter, help_callback)
            assert result is False
            mock_install.assert_called_once()

        # Test save action
        menu_items = [handler.menu_items["action-save"]]
        menu_getter.return_value = menu_items

        with patch.object(handler, "_handle_save", return_value=True) as mock_save:
            result = handler.handle_key(ord("\n"), menu_getter, help_callback)
            assert result is True
            mock_save.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_enter_configurable(self, mock_file, handler):
        """Test ENTER key on configurable item."""
        menu_items = [handler.menu_items["configurable"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0
        mock_dialog = Mock()
        handler.set_dialog_handler(mock_dialog)

        result = handler.handle_key(ord("\n"), menu_getter, help_callback)

        assert result is True
        mock_dialog.show_configuration_dialog.assert_called_once_with(
            handler.menu_items["configurable"]
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_right_arrow(self, mock_file, handler):
        """Test RIGHT arrow key."""
        # On category - should enter it
        menu_items = [handler.menu_items["dev"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0
        handler.current_menu = "root"

        result = handler.handle_key(curses.KEY_RIGHT, menu_getter, help_callback)

        assert result is True
        assert handler.current_menu == "dev"

        # On regular item - should toggle
        handler.current_menu = "dev"
        menu_items = [handler.menu_items["python"]]
        menu_getter.return_value = menu_items
        handler.current_item = 0

        result = handler.handle_key(curses.KEY_RIGHT, menu_getter, help_callback)
        assert "python" in handler.selected_items

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_back_navigation(self, mock_file, handler, sample_menu_items):
        """Test back navigation keys."""

        # Menu getter should return the current menu items
        def get_menu_items():
            current = handler.menu_items.get(handler.current_menu)
            if current and current.children:
                return [handler.menu_items[child_id] for child_id in current.children]
            return []

        menu_getter = Mock(side_effect=get_menu_items)
        help_callback = Mock()

        # Setup: we're in a submenu
        handler.breadcrumb_stack = [("root", 1, 0)]
        handler.current_menu = "dev"

        # Test BACKSPACE
        result = handler.handle_key(curses.KEY_BACKSPACE, menu_getter, help_callback)
        assert result is True
        assert handler.current_menu == "root"
        assert handler.current_item == 1
        assert len(handler.breadcrumb_stack) == 0

        # Test LEFT arrow
        handler.breadcrumb_stack = [("root", 2, 0)]
        handler.current_menu = "apps"
        result = handler.handle_key(curses.KEY_LEFT, menu_getter, help_callback)
        assert handler.current_menu == "root"

        # Test 'b' key
        handler.breadcrumb_stack = [("root", 0, 0)]
        handler.current_menu = "dev"
        result = handler.handle_key(ord("b"), menu_getter, help_callback)
        assert handler.current_menu == "root"

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_select_all(self, mock_file, handler, sample_menu_items):
        """Test select all keys."""
        # Return some menu items to prevent early return
        menu_getter = Mock(
            return_value=[sample_menu_items["python"], sample_menu_items["nodejs"]]
        )
        help_callback = Mock()

        with patch.object(handler, "_select_all_in_category") as mock_select:
            # Test 'a' - select all
            handler.handle_key(ord("a"), menu_getter, help_callback)
            mock_select.assert_called_with(True)

            # Test 'n' - deselect all
            handler.handle_key(ord("n"), menu_getter, help_callback)
            mock_select.assert_called_with(False)

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_function_keys(self, mock_file, handler, sample_menu_items):
        """Test function keys."""
        # Return some menu items to prevent early return
        menu_getter = Mock(return_value=[sample_menu_items["python"]])
        help_callback = Mock()

        with patch.object(
            handler, "_show_actions_popup", return_value=True
        ) as mock_popup:
            # Test F1
            result = handler.handle_key(curses.KEY_F1, menu_getter, help_callback)
            assert result is True
            mock_popup.assert_called_once()

            # Test F10
            mock_popup.reset_mock()
            result = handler.handle_key(curses.KEY_F10, menu_getter, help_callback)
            assert result is True
            mock_popup.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_help(self, mock_file, handler):
        """Test help keys."""
        menu_items = [handler.menu_items["python"]]
        menu_getter = Mock(return_value=menu_items)
        help_callback = Mock()

        handler.current_item = 0

        # Test 'h'
        handler.handle_key(ord("h"), menu_getter, help_callback)
        help_callback.assert_called_once_with(handler.menu_items["python"])

        # Test '?'
        help_callback.reset_mock()
        handler.handle_key(ord("?"), menu_getter, help_callback)
        help_callback.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_quit(self, mock_file, handler, sample_menu_items):
        """Test quit keys."""
        menu_getter = Mock(return_value=[sample_menu_items["python"]])
        help_callback = Mock()

        with patch.object(handler, "_handle_exit", return_value=False) as mock_exit:
            # Test 'q'
            result = handler.handle_key(ord("q"), menu_getter, help_callback)
            assert result is False
            mock_exit.assert_called_once()

            # Test 'Q'
            mock_exit.reset_mock()
            result = handler.handle_key(ord("Q"), menu_getter, help_callback)
            assert result is False
            mock_exit.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_key_escape(self, mock_file, handler, sample_menu_items):
        """Test ESC key behavior."""
        menu_getter = Mock(return_value=[sample_menu_items["python"]])
        help_callback = Mock()

        # ESC with breadcrumb - go back
        handler.breadcrumb_stack = [("root", 0, 0)]
        handler.current_menu = "dev"

        result = handler.handle_key(27, menu_getter, help_callback)
        assert result is True
        assert handler.current_menu == "root"

        # ESC at root - exit
        handler.breadcrumb_stack = []
        with patch.object(handler, "_handle_exit", return_value=False) as mock_exit:
            result = handler.handle_key(27, menu_getter, help_callback)
            assert result is False
            mock_exit.assert_called_once()

    def test_select_all_in_category_toggle(self, handler):
        """Test category toggle selection."""
        # Initially no items selected
        handler._select_all_in_category_toggle("dev")

        # Should select all items in dev
        assert "python" in handler.selected_items
        assert "nodejs" in handler.selected_items
        assert handler.menu_items["python"].selected is True
        assert handler.menu_items["nodejs"].selected is True

        # Toggle again - should deselect all
        handler._select_all_in_category_toggle("dev")

        assert "python" not in handler.selected_items
        assert "nodejs" not in handler.selected_items
        assert handler.menu_items["python"].selected is False
        assert handler.menu_items["nodejs"].selected is False

    def test_get_all_selectable_items(self, handler):
        """Test getting all selectable items."""
        # Get items from dev category
        items = handler._get_all_selectable_items("dev")
        assert len(items) == 2
        assert "python" in items
        assert "nodejs" in items

        # Get items from apps category
        items = handler._get_all_selectable_items("apps")
        assert len(items) == 1
        assert "firefox" in items

        # Get items from non-category
        items = handler._get_all_selectable_items("python")
        assert len(items) == 0

    @patch("curses.napms")
    def test_handle_install_no_items(self, mock_napms, handler):
        """Test install with no items selected."""
        handler.selected_items.clear()

        result = handler._handle_install()

        assert result is True  # Continue running
        mock_napms.assert_called_once_with(2000)

        # Check error message was displayed
        handler.stdscr.addstr.assert_called()
        handler.stdscr.attron.assert_called()
        handler.stdscr.attroff.assert_called()

    def test_handle_install_with_items(self, handler):
        """Test install with items selected."""
        handler.selected_items.add("python")

        with patch.object(handler, "_save_configuration") as mock_save:
            result = handler._handle_install()

            assert result is False  # Exit TUI
            mock_save.assert_called_once()

    @patch("curses.napms")
    def test_handle_save(self, mock_napms, handler):
        """Test save configuration."""
        with patch.object(handler, "_save_configuration") as mock_save:
            result = handler._handle_save()

            assert result is True  # Continue running
            mock_save.assert_called_once()
            mock_napms.assert_called_once_with(2000)

            # Check that we returned to root menu
            assert handler.current_menu == "root"
            assert handler.current_item == 0
            assert handler.breadcrumb_stack == []

    @patch("curses.napms")
    def test_handle_reset_confirm(self, mock_napms, handler):
        """Test reset with confirmation."""
        # Add some selections
        handler.selected_items.add("python")
        handler.menu_items["python"].selected = True
        handler.menu_items["nodejs"].default = True

        # Mock user confirming
        handler.stdscr.getch.return_value = ord("y")
        handler.stdscr.timeout = Mock()

        result = handler._handle_reset()

        assert result is True
        assert "python" not in handler.selected_items
        assert "nodejs" in handler.selected_items  # Has default=True
        assert handler.menu_items["python"].selected is False
        assert handler.menu_items["nodejs"].selected is True

    def test_handle_reset_cancel(self, handler):
        """Test reset with cancellation."""
        # Add selections
        handler.selected_items.add("python")

        # Mock user cancelling
        handler.stdscr.getch.return_value = ord("n")
        handler.stdscr.timeout = Mock()

        result = handler._handle_reset()

        assert result is True
        assert "python" in handler.selected_items  # Unchanged

    def test_show_exit_confirmation(self, handler):
        """Test exit confirmation dialog."""
        # Mock selecting YES - need to move UP from default NO position
        handler.stdscr.getch.side_effect = [
            curses.KEY_UP,
            ord("\n"),
        ]  # Move to YES, then enter

        result = handler._show_exit_confirmation()

        assert result is False  # Exit
        assert handler.cancelled is True

        # Mock selecting NO (default position)
        handler.cancelled = False
        handler.stdscr.getch.side_effect = [ord("\n")]  # Just enter on default NO

        result = handler._show_exit_confirmation()

        assert result is True  # Continue
        assert handler.cancelled is False

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_save_configuration(self, mock_yaml_dump, mock_file, handler):
        """Test configuration saving."""
        # Setup selections
        handler.selected_items = {"python", "firefox"}
        handler.menu_items["python"].ansible_var = "install_python"
        handler.menu_items["firefox"].ansible_var = "install_firefox"

        # Add configurable item
        config_item = MenuItem(
            "swappiness",
            "Swappiness",
            "System swappiness",
            is_configurable=True,
            config_type="slider",
            config_value=10,
            config_unit="%",
            ansible_var="system_swappiness",
        )
        handler.menu_items["swappiness"] = config_item
        handler.selected_items.add("swappiness")
        config_item.selected = True

        handler._save_configuration()

        # Verify file was opened
        mock_file.assert_called_once_with("config.yml", "w")

        # Verify yaml dump was called
        mock_yaml_dump.assert_called_once()
        config = mock_yaml_dump.call_args[0][0]

        assert "selected_items" in config
        assert "python" in config["selected_items"]
        assert "firefox" in config["selected_items"]
        assert "configurable_values" in config
        assert "swappiness" in config["configurable_values"]
        assert config["configurable_values"]["swappiness"]["value"] == 10
        assert "ansible_variables" in config

    @patch("builtins.open", side_effect=Exception("Write error"))
    @patch("curses.napms")
    def test_save_configuration_error(self, mock_napms, mock_file, handler):
        """Test configuration save error handling."""
        handler._save_configuration()

        # Should show error message
        handler.stdscr.addstr.assert_called()
        mock_napms.assert_called_once_with(3000)

    def test_show_actions_popup(self, handler):
        """Test actions popup display."""
        # Mock selecting install action
        handler.stdscr.getch.side_effect = [ord("\n")]  # Enter on first option

        with patch.object(
            handler, "_handle_install", return_value=False
        ) as mock_install:
            result = handler._show_actions_popup()

            assert result is False
            mock_install.assert_called_once()

        # Mock ESC to close
        handler.stdscr.getch.side_effect = [27]  # ESC
        result = handler._show_actions_popup()
        assert result is True
