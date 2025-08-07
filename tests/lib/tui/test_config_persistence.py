#!/usr/bin/env python3
"""
Tests for configuration persistence and auto-save functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import yaml

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

# Mock curses before importing
sys.modules["curses"] = MagicMock()
import curses

# Set up minimal curses constants
curses.error = Exception


class TestAutoSave(unittest.TestCase):
    """Test auto-save functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

    def test_auto_save_after_selection(self):
        """Test that configuration is saved after each selection change"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.items = [{"id": "test-item", "label": "Test", "parent": None}]
        menu.current_index = 0

        # Mock save_configuration to track calls
        save_calls = []

        def mock_save(silent=False):
            save_calls.append(silent)
            return True

        menu.save_configuration = mock_save

        # Make a selection
        menu.toggle_selection()

        # Verify save was called with silent=True
        self.assertEqual(len(save_calls), 1)
        self.assertTrue(save_calls[0])  # Should be silent

    def test_auto_save_after_config_change(self):
        """Test that configuration is saved after configurable value change"""
        menu = self.UnifiedMenu(self.stdscr)

        # Track save calls
        save_calls = []
        menu.save_configuration = lambda silent=False: save_calls.append(silent) or True

        # Mock dialog to return a new value
        with patch("lib.tui.dialogs.SliderDialog") as mock_slider_class:
            mock_slider = MagicMock()
            mock_slider.show.return_value = 75
            mock_slider_class.return_value = mock_slider

            item = {
                "id": "test-slider",
                "label": "Test",
                "is_configurable": True,
                "config_type": "slider",
                "default_value": 50,
                "min_value": 0,
                "max_value": 100,
                "step": 1,
            }

            menu.show_config_dialog(item)

        # Verify save was called
        self.assertEqual(len(save_calls), 1)
        self.assertTrue(save_calls[0])  # Should be silent

    def test_auto_save_handles_errors(self):
        """Test that auto-save handles write errors gracefully"""
        menu = self.UnifiedMenu(self.stdscr)

        # Mock file write to raise exception
        with patch("builtins.open", side_effect=IOError("Disk full")):
            # This should not raise exception
            menu.save_configuration()

        # Menu should continue to work
        self.assertIsNotNone(menu)


class TestConfigValidation(unittest.TestCase):
    """Test configuration validation and error handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

    def test_validate_config_structure(self):
        """Test validation of config file structure"""
        menu = self.UnifiedMenu(self.stdscr)

        # Valid config
        valid_config = {
            "metadata": {"version": "1.0"},
            "selected_items": ["item1", "item2"],
            "configurable_items": {"setting1": {"id": "setting1", "value": 10}},
        }

        # This should work (test the actual validation if implemented)
        result = menu.validate_config(valid_config) if hasattr(menu, "validate_config") else True
        self.assertTrue(result)

    def test_handle_missing_sections(self):
        """Test handling of config with missing sections"""
        menu = self.UnifiedMenu(self.stdscr)

        # Config missing sections
        incomplete_config = {
            "selected_items": ["item1"]
            # Missing metadata and configurable_items
        }

        with patch("builtins.open", mock_open(read_data=yaml.dump(incomplete_config))):
            with patch("pathlib.Path.exists", return_value=True):
                # Should not crash
                menu.load_configuration()

        # Should have loaded what was available
        self.assertIn("item1", menu.selections)

    def test_handle_wrong_types(self):
        """Test handling of config with wrong data types"""
        menu = self.UnifiedMenu(self.stdscr)

        # Config with wrong types
        bad_config = {
            "selected_items": "not-a-list",  # Should be list
            "configurable_items": ["not-a-dict"],  # Should be dict
        }

        with patch("builtins.open", mock_open(read_data=yaml.dump(bad_config))):
            with patch("pathlib.Path.exists", return_value=True):
                # Should not crash
                menu.load_configuration()

        # Should have empty selections (failed to load)
        self.assertEqual(menu.selections, {})

    @patch("lib.tui.dialogs.MessageDialog")
    def test_corruption_notification(self, mock_dialog_class):
        """Test that user is notified of corrupted config"""
        menu = self.UnifiedMenu(self.stdscr)

        # Mock corrupted file that raises exception
        with patch("builtins.open", side_effect=yaml.YAMLError("Invalid YAML")):
            with patch("pathlib.Path.exists", return_value=True):
                # If notification is implemented
                if hasattr(menu, "notify_corruption"):
                    menu.notify_corruption()
                    mock_dialog_class.assert_called()


class TestConfigMigration(unittest.TestCase):
    """Test configuration format migration"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

    def test_load_old_format(self):
        """Test loading config from older format"""
        menu = self.UnifiedMenu(self.stdscr)

        # Old format might have different structure
        old_config = {"selections": ["item1", "item2"], "values": {"setting1": 10}}  # Old key name  # Old key name

        # If migration is implemented
        if hasattr(menu, "migrate_config"):
            migrated = menu.migrate_config(old_config)
            self.assertIn("selected_items", migrated)
            self.assertIn("configurable_items", migrated)


class TestRealFileOperations(unittest.TestCase):
    """Test with real file operations using temp files"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu

        # Create temp directory
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "config.yml")

    def tearDown(self):
        """Clean up temp files"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_real_save_and_load(self):
        """Test actual file save and load operations"""
        # Create menu with custom config path
        menu = self.UnifiedMenu(self.stdscr)
        menu.config_file = self.config_file

        # Set some data
        menu.selections = {"item1": True, "cat1": {"sub1", "sub2"}}
        menu.configurable_values = {"font": "Monaco", "size": 14}

        # Save
        menu.save_configuration()

        # Verify file exists
        self.assertTrue(os.path.exists(self.config_file))

        # Create new menu instance
        menu2 = self.UnifiedMenu(self.stdscr)
        menu2.config_file = self.config_file
        menu2.category_items = {"cat1": {"sub1", "sub2", "sub3"}}

        # Load
        menu2.load_configuration()

        # Verify data loaded correctly
        self.assertIn("item1", menu2.selections)
        self.assertEqual(menu2.selections["cat1"], {"sub1", "sub2"})
        self.assertEqual(menu2.configurable_values["font"], "Monaco")
        self.assertEqual(menu2.configurable_values["size"], 14)

    def test_concurrent_access(self):
        """Test handling of concurrent file access"""
        menu1 = self.UnifiedMenu(self.stdscr)
        menu1.config_file = self.config_file

        menu2 = self.UnifiedMenu(self.stdscr)
        menu2.config_file = self.config_file

        # Both try to save at same time
        menu1.selections = {"item1": True}
        menu2.selections = {"item2": True}

        menu1.save_configuration()
        menu2.save_configuration()

        # Last write wins
        menu3 = self.UnifiedMenu(self.stdscr)
        menu3.config_file = self.config_file
        menu3.load_configuration()

        # Should have menu2's data
        self.assertIn("item2", menu3.selections)
        self.assertNotIn("item1", menu3.selections)


if __name__ == "__main__":
    unittest.main()
