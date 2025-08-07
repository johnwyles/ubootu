#!/usr/bin/env python3
"""
Tests for unified menu configurable item handling
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch

import yaml

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

# Mock curses before importing
sys.modules["curses"] = MagicMock()
import curses

# Set up minimal curses constants
curses.A_REVERSE = 262144
curses.error = Exception


class TestUnifiedMenuConfig(unittest.TestCase):
    """Test unified menu configuration handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch = MagicMock()

        # Import after mocking
        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

    def test_load_defaults(self):
        """Test loading default values for configurable items"""
        menu = self.UnifiedMenu(self.stdscr)

        # Create test items with defaults
        menu.items = [
            {"id": "test-slider", "is_configurable": True, "default_value": 50},
            {"id": "test-select", "is_configurable": True, "default_value": "Option A"},
            {"id": "test-checkbox", "default": True, "parent": None},
        ]

        menu.load_defaults()

        # Check configurable defaults loaded
        self.assertEqual(menu.configurable_values["test-slider"], 50)
        self.assertEqual(menu.configurable_values["test-select"], "Option A")

        # Check selection defaults loaded
        self.assertIn("test-checkbox", menu.selections)

    def test_configurable_item_display(self):
        """Test that configurable items show their values"""
        menu = self.UnifiedMenu(self.stdscr)

        # Set up a configurable item
        item = {"id": "font-size", "label": "Font Size", "is_configurable": True, "unit": "px", "default_value": 14}

        menu.configurable_values["font-size"] = 16

        # Test rendering
        menu.render_menu_item(10, item, False)

        # Check that value is displayed
        calls = [str(call) for call in self.stdscr.addstr.call_args_list]
        found_value = any("[16px]" in str(call) for call in calls)
        self.assertTrue(found_value, "Configurable value not displayed")

    @patch("lib.tui.dialogs.SpinnerDialog")
    def test_spinner_dialog_opened(self, mock_spinner_class):
        """Test spinner dialog opens for spinner config type"""
        mock_spinner = MagicMock()
        mock_spinner.show.return_value = 16
        mock_spinner_class.return_value = mock_spinner

        menu = self.UnifiedMenu(self.stdscr)

        item = {
            "id": "tab-size",
            "label": "Tab Size",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [2, 4, 8],
            "default_value": 4,
            "unit": "",
        }

        menu.configurable_values["tab-size"] = 4
        menu.show_config_dialog(item)

        # Verify spinner was shown with correct values
        mock_spinner.show.assert_called_once_with("Tab Size", 4, [2, 4, 8], "")

        # Verify value was updated
        self.assertEqual(menu.configurable_values["tab-size"], 16)

    @patch("lib.tui.dialogs.SelectDialog")
    def test_select_dialog_opened(self, mock_select_class):
        """Test select dialog opens for select config type"""
        mock_select = MagicMock()
        mock_select.show.return_value = "Fira Code"
        mock_select_class.return_value = mock_select

        menu = self.UnifiedMenu(self.stdscr)

        item = {
            "id": "font-family",
            "label": "Font Family",
            "is_configurable": True,
            "config_type": "select",
            "options": ["Monaco", "Fira Code", "JetBrains Mono"],
            "default_value": "Monaco",
        }

        menu.configurable_values["font-family"] = "Monaco"
        menu.show_config_dialog(item)

        # Verify select was shown
        mock_select.show.assert_called_once_with("Font Family", ["Monaco", "Fira Code", "JetBrains Mono"], "Monaco")

        # Verify value was updated
        self.assertEqual(menu.configurable_values["font-family"], "Fira Code")

    def test_toggle_selection_opens_dialog(self):
        """Test that toggle_selection opens dialog for configurable items"""
        menu = self.UnifiedMenu(self.stdscr)

        # Create a configurable item
        item = {"id": "test-config", "is_configurable": True, "config_type": "slider"}

        menu.items = [item]
        menu.current_index = 0

        # Mock the dialog method
        menu.show_config_dialog = MagicMock()

        # Call toggle_selection
        menu.toggle_selection()

        # Verify dialog was opened instead of toggling
        menu.show_config_dialog.assert_called_once_with(item)

    def test_regular_item_toggle(self):
        """Test that non-configurable items toggle normally"""
        menu = self.UnifiedMenu(self.stdscr)

        # Create a regular item
        item = {"id": "test-item", "label": "Test Item", "parent": None}

        menu.items = [item]
        menu.current_index = 0

        # Mock save_configuration to avoid file operations
        menu.save_configuration = MagicMock(return_value=True)

        # Toggle selection
        menu.toggle_selection()
        self.assertIn("test-item", menu.selections)

        # Verify auto-save was called
        menu.save_configuration.assert_called_with(silent=True)

        # Toggle again
        menu.toggle_selection()
        self.assertNotIn("test-item", menu.selections)


class TestConfigPersistence(unittest.TestCase):
    """Test configuration saving and loading"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

    def test_save_configuration(self):
        """Test saving configuration to YAML"""
        menu = self.UnifiedMenu(self.stdscr)

        # Set up some selections and values
        menu.selections = {"item1": True, "category1": {"subitem1", "subitem2"}}
        menu.configurable_values = {"font-size": 16, "theme": "Dark"}

        # Mock file operations
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            menu.save_configuration()

        # Get what was written
        handle = mock_file()
        written_calls = handle.write.call_args_list
        written_data = "".join(call[0][0] for call in written_calls)

        # Parse the YAML
        config = yaml.safe_load(written_data)

        # Verify structure
        self.assertIn("metadata", config)
        self.assertIn("selected_items", config)
        self.assertIn("configurable_items", config)

        # Verify selections saved
        self.assertIn("item1", config["selected_items"])
        self.assertIn("category1", config["selected_items"])
        self.assertIn("subitem1", config["selected_items"])

        # Verify configurable values saved
        self.assertEqual(config["configurable_items"]["font-size"]["value"], 16)
        self.assertEqual(config["configurable_items"]["theme"]["value"], "Dark")

    def test_load_configuration(self):
        """Test loading configuration from YAML"""
        menu = self.UnifiedMenu(self.stdscr)

        # Create test config
        test_config = {
            "metadata": {"version": "1.0"},
            "selected_items": ["item1", "category1", "subitem1"],
            "configurable_items": {
                "font-size": {"id": "font-size", "value": 18},
                "theme": {"id": "theme", "value": "Light"},
            },
        }

        # Mock file reading
        with patch("builtins.open", mock_open(read_data=yaml.dump(test_config))):
            with patch("pathlib.Path.exists", return_value=True):
                menu.category_items = {"category1": {"subitem1", "subitem2"}}
                menu.load_configuration()

        # Verify selections loaded
        self.assertIn("item1", menu.selections)
        self.assertIn("subitem1", menu.selections["category1"])

        # Verify configurable values loaded
        self.assertEqual(menu.configurable_values["font-size"], 18)
        self.assertEqual(menu.configurable_values["theme"], "Light")

    @patch("lib.tui.dialogs.ConfirmDialog")
    @patch("lib.tui.dialogs.MessageDialog")
    def test_load_corrupted_config(self, mock_msg_dialog, mock_confirm_dialog):
        """Test handling of corrupted config file"""
        # Mock dialogs to avoid hanging
        mock_confirm = MagicMock()
        mock_confirm.show.return_value = False  # Don't reset to defaults
        mock_confirm_dialog.return_value = mock_confirm

        menu = self.UnifiedMenu(self.stdscr)

        # Mock corrupted file
        with patch("builtins.open", mock_open(read_data="invalid: yaml: content:")):
            with patch("pathlib.Path.exists", return_value=True):
                # Should not raise exception
                menu.load_configuration()

        # Verify corruption dialog was shown
        mock_confirm.show.assert_called_once()

        # Should have empty selections (didn't reset)
        self.assertEqual(menu.selections, {})

    def test_load_config_overrides_defaults(self):
        """Test that loaded config overrides defaults"""
        menu = self.UnifiedMenu(self.stdscr)

        # Set up items with defaults
        menu.items = [
            {"id": "item1", "default": True},
            {"id": "item2", "default": True},
            {"id": "config1", "is_configurable": True, "default_value": 10},
        ]

        # Load defaults first
        menu.load_defaults()
        self.assertIn("item1", menu.selections)
        self.assertIn("item2", menu.selections)
        self.assertEqual(menu.configurable_values["config1"], 10)

        # Create config that only has item1 selected and different value
        test_config = {
            "selected_items": ["item1"],  # item2 not selected
            "configurable_items": {"config1": {"value": 20}},  # Different value
        }

        # Load configuration
        with patch("builtins.open", mock_open(read_data=yaml.dump(test_config))):
            with patch("pathlib.Path.exists", return_value=True):
                menu.load_configuration()

        # Verify only item1 selected (defaults overridden)
        self.assertIn("item1", menu.selections)
        self.assertNotIn("item2", menu.selections)

        # Verify configurable value overridden
        self.assertEqual(menu.configurable_values["config1"], 20)


if __name__ == "__main__":
    unittest.main()
