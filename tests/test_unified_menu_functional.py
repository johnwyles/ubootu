#!/usr/bin/env python3
"""
Functional tests for unified_menu module
Tests the main menu system and configuration management
"""

import hashlib
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import pytest
import yaml

from lib.tui.unified_menu import UnifiedMenu


class TestUnifiedMenuFunctional:
    """Test UnifiedMenu functionality"""

    def setup_method(self):
        """Setup mock stdscr and menu instance"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch.return_value = ord("q")  # Default to quit

        with patch("lib.tui.unified_menu.curses.curs_set"):
            self.menu = UnifiedMenu(self.stdscr)

    def test_init(self):
        """Test UnifiedMenu initialization"""
        assert self.menu.stdscr == self.stdscr
        assert self.menu.height == 24
        assert self.menu.width == 80
        assert self.menu.current_menu == "root"
        assert self.menu.current_index == 0
        assert self.menu.selections == {}
        assert self.menu.config_file == "config.yml"
        assert self.menu.config_applied is False
        assert self.menu.operation_mode == "additive"

    @patch("lib.tui.unified_menu.load_menu_structure")
    def test_load_menu_structure(self, mock_load):
        """Test loading menu structure"""
        mock_items = [
            {"id": "dev", "is_category": True, "children": ["python", "rust"]},
            {"id": "python", "parent": "dev", "is_category": False},
            {"id": "rust", "parent": "dev", "is_category": False},
        ]
        mock_load.return_value = mock_items

        self.menu.load_menu_structure()

        assert self.menu.items == mock_items
        assert "dev" in self.menu.category_items
        assert self.menu.category_items["dev"] == {"python", "rust"}

    def test_load_defaults(self):
        """Test loading default selections"""
        self.menu.items = [
            {"id": "cat1", "is_category": True, "children": ["item1", "item2"]},
            {"id": "item1", "parent": "cat1", "default": True, "is_category": False},
            {"id": "item2", "parent": "cat1", "default": False, "is_category": False},
            {"id": "item3", "default": True, "is_category": False},
            {"id": "conf1", "is_configurable": True, "default_value": "test_value"},
        ]
        self.menu.category_items = {"cat1": {"item1", "item2"}}

        self.menu.load_defaults()

        assert "cat1" in self.menu.selections
        assert "item1" in self.menu.selections["cat1"]
        assert "item2" not in self.menu.selections.get("cat1", set())
        assert self.menu.selections.get("item3") is True
        assert self.menu.configurable_values["conf1"] == "test_value"

    def test_refresh_system_state(self):
        """Test refreshing system state"""
        self.menu.items = [
            {"id": "firefox", "is_category": False},
            {"id": "chrome", "is_category": False},
            {"id": "dev", "is_category": True},
        ]

        # Mock the discovery instance
        self.menu.discovery = MagicMock()
        self.menu.discovery.map_to_menu_items.return_value = {"firefox": "installed", "chrome": "not_installed"}

        self.menu.refresh_system_state()

        assert self.menu.system_state["firefox"] == "installed"
        assert self.menu.system_state["chrome"] == "not_installed"

    def test_get_item_sync_status(self):
        """Test getting item sync status"""
        self.menu.selections = {"firefox": True}
        self.menu.system_state = {"firefox": "installed", "chrome": "not_installed"}

        # Selected and installed
        assert self.menu.get_item_sync_status("firefox") == "synced_selected"

        # Not selected and not installed
        assert self.menu.get_item_sync_status("chrome") == "synced_unselected"

        # Selected but not installed
        self.menu.selections["chrome"] = True
        assert self.menu.get_item_sync_status("chrome") == "needs_install"

        # Installed but not selected
        self.menu.system_state["opera"] = "installed"
        assert self.menu.get_item_sync_status("opera") == "orphaned"

    def test_get_status_indicator(self):
        """Test getting visual status indicators"""
        self.menu.selections = {"firefox": True}
        self.menu.system_state = {"firefox": "installed"}

        assert self.menu.get_status_indicator("firefox") == "[✓]"

        self.menu.system_state["firefox"] = "not_installed"
        assert self.menu.get_status_indicator("firefox") == "[⚠]"

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_initialize_state_tracking(self, mock_file, mock_exists):
        """Test initializing state tracking"""
        mock_exists.side_effect = [True, True]  # Both files exist

        # Mock file content for hashing
        mock_file.return_value.read.return_value = b"test content"

        with patch.object(self.menu, "_get_file_hash") as mock_hash:
            mock_hash.side_effect = ["hash1", "hash2"]

            self.menu.initialize_state_tracking()

            assert self.menu.changes_since_apply is True  # Different hashes
            assert self.menu.applied_config_hash == "hash2"

    def test_get_file_hash(self):
        """Test calculating file hash"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            f.flush()

            hash_result = self.menu._get_file_hash(f.name)

            # Calculate expected hash
            expected_hash = hashlib.sha256(b"test content").hexdigest()

            assert hash_result == expected_hash

            Path(f.name).unlink()

    def test_get_file_hash_nonexistent(self):
        """Test hash of non-existent file"""
        result = self.menu._get_file_hash("/nonexistent/file.txt")
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data="selections:\n  firefox: true\n")
    @patch("pathlib.Path.exists")
    def test_load_configuration(self, mock_exists, mock_file):
        """Test loading configuration from file"""
        mock_exists.return_value = True

        self.menu.load_configuration()

        assert self.menu.selections.get("firefox") is True

    @patch("builtins.open", new_callable=mock_open)
    def test_save_configuration(self, mock_file):
        """Test saving configuration to file"""
        self.menu.selections = {"firefox": True, "chrome": False}
        self.menu.configurable_values = {"timeout": 30}

        result = self.menu.save_configuration(silent=True)

        assert result is True
        mock_file.assert_called_with("config.yml", "w")

    def test_get_current_items(self):
        """Test getting current menu items"""
        self.menu.items = [
            {"id": "item1", "parent": None},
            {"id": "item2", "parent": None},
            {"id": "item3", "parent": "submenu"},
            {"id": "submenu", "is_category": True},
        ]
        self.menu.current_menu = "root"

        items = self.menu.get_current_items()

        # Should only get root items
        assert len(items) == 3  # item1, item2, submenu
        assert any(item["id"] == "item1" for item in items)
        assert any(item["id"] == "submenu" for item in items)
        assert not any(item["id"] == "item3" for item in items)

    def test_get_all_descendant_items(self):
        """Test getting all descendant items of a category"""
        self.menu.items = [
            {"id": "cat1", "is_category": True, "children": ["cat2", "item1"]},
            {"id": "cat2", "is_category": True, "parent": "cat1", "children": ["item2", "item3"]},
            {"id": "item1", "parent": "cat1"},
            {"id": "item2", "parent": "cat2"},
            {"id": "item3", "parent": "cat2"},
        ]
        self.menu.category_items = {"cat1": {"cat2", "item1"}, "cat2": {"item2", "item3"}}

        descendants = self.menu.get_all_descendant_items("cat1")

        assert "item1" in descendants
        assert "item2" in descendants
        assert "item3" in descendants
        assert len(descendants) == 3

    def test_is_item_selected(self):
        """Test checking if item is selected"""
        self.menu.selections = {"firefox": True, "chrome": False, "dev": {"python", "rust"}}

        assert self.menu.is_item_selected("firefox") is True
        assert self.menu.is_item_selected("chrome") is False
        assert self.menu.is_item_selected("python") is True
        assert self.menu.is_item_selected("rust") is True
        assert self.menu.is_item_selected("golang") is False

    def test_get_selection_indicator(self):
        """Test getting selection indicator for items"""
        selections = {"python", "rust"}

        # Regular selection
        indicator = self.menu.get_selection_indicator("python", selections)
        assert indicator == "[✓]"

        # Not selected
        indicator = self.menu.get_selection_indicator("golang", selections)
        assert indicator == "[ ]"

        # Configurable item
        self.menu.items = [{"id": "timeout", "is_configurable": True}]
        self.menu.configurable_values = {"timeout": 30}
        indicator = self.menu.get_selection_indicator("timeout", selections)
        assert "30" in indicator

    def test_toggle_selection(self):
        """Test toggling item selection"""
        self.menu.items = [
            {"id": "firefox", "parent": None, "is_category": False},
            {"id": "dev", "is_category": True, "children": ["python"]},
            {"id": "python", "parent": "dev", "is_category": False},
        ]
        self.menu.current_menu = "root"
        self.menu.current_index = 0

        # Toggle firefox (top-level item)
        self.menu.toggle_selection()
        assert self.menu.selections.get("firefox") is True

        # Toggle again to deselect
        self.menu.toggle_selection()
        assert self.menu.selections.get("firefox") is False

    def test_select_all(self):
        """Test selecting all items in current menu"""
        self.menu.items = [
            {"id": "item1", "parent": None, "is_category": False},
            {"id": "item2", "parent": None, "is_category": False},
            {"id": "cat1", "is_category": True},
        ]
        self.menu.current_menu = "root"

        self.menu.select_all()

        assert self.menu.selections.get("item1") is True
        assert self.menu.selections.get("item2") is True
        assert self.menu.selections.get("cat1") is not True  # Categories aren't selected

    def test_deselect_all(self):
        """Test deselecting all items in current menu"""
        self.menu.selections = {"item1": True, "item2": True, "item3": True}
        self.menu.items = [
            {"id": "item1", "parent": None, "is_category": False},
            {"id": "item2", "parent": None, "is_category": False},
            {"id": "item3", "parent": "other", "is_category": False},
        ]
        self.menu.current_menu = "root"

        self.menu.deselect_all()

        assert self.menu.selections.get("item1") is False
        assert self.menu.selections.get("item2") is False
        assert self.menu.selections.get("item3") is True  # Not in current menu

    def test_enter_submenu(self):
        """Test entering a submenu"""
        self.menu.items = [{"id": "dev", "label": "Development", "is_category": True}]

        self.menu.enter_submenu("dev")

        assert self.menu.current_menu == "dev"
        assert self.menu.menu_stack == ["root"]
        assert "Development" in self.menu.breadcrumb

    def test_go_back(self):
        """Test going back from submenu"""
        self.menu.menu_stack = ["root", "dev"]
        self.menu.current_menu = "tools"
        self.menu.breadcrumb = ["Root", "Development", "Tools"]

        self.menu.go_back()

        assert self.menu.current_menu == "dev"
        assert self.menu.menu_stack == ["root"]
        assert len(self.menu.breadcrumb) == 2

    def test_toggle_operation_mode(self):
        """Test toggling between operation modes"""
        assert self.menu.operation_mode == "additive"

        self.menu.toggle_operation_mode()
        assert self.menu.operation_mode == "strict"

        self.menu.toggle_operation_mode()
        assert self.menu.operation_mode == "additive"

    def test_validate_config(self):
        """Test configuration validation"""
        # Valid config
        config = {"selections": {"firefox": True}, "configurable_values": {"timeout": 30}}
        assert self.menu.validate_config(config) is True

        # Invalid config - wrong types
        config = {"selections": "not a dict", "configurable_values": {"timeout": 30}}
        assert self.menu.validate_config(config) is False

        # Invalid config - missing required keys
        config = {"other_key": "value"}
        assert self.menu.validate_config(config) is False

    def test_get_config_data(self):
        """Test getting configuration data"""
        self.menu.selections = {"firefox": True, "chrome": False}
        self.menu.configurable_values = {"timeout": 30}

        config_data = self.menu._get_config_data()

        assert config_data["selections"] == {"firefox": True, "chrome": False}
        assert config_data["configurable_values"] == {"timeout": 30}
        assert "metadata" in config_data
        assert config_data["metadata"]["version"] == "2.0"

    def test_get_config_hash(self):
        """Test getting configuration hash"""
        self.menu.selections = {"firefox": True}
        self.menu.configurable_values = {"timeout": 30}

        hash1 = self.menu._get_config_hash()

        # Change config
        self.menu.selections["chrome"] = True
        hash2 = self.menu._get_config_hash()

        assert hash1 != hash2

        # Revert change
        del self.menu.selections["chrome"]
        hash3 = self.menu._get_config_hash()

        assert hash1 == hash3

    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    @patch("pathlib.Path.exists")
    def test_get_saved_config_hash(self, mock_exists, mock_file):
        """Test getting saved configuration hash"""
        mock_exists.return_value = True

        hash_result = self.menu._get_saved_config_hash()

        expected_hash = hashlib.sha256(b"test content").hexdigest()
        assert hash_result == expected_hash

    def test_prepare_ansible_variables(self):
        """Test preparing Ansible variables"""
        self.menu.selections = {"docker": True, "firefox": True, "dev": {"python", "rust"}}
        self.menu.configurable_values = {"git_user_name": "Test User"}

        # Mock items with ansible_var mappings
        self.menu.items = [
            {"id": "docker", "ansible_var": "install_docker"},
            {"id": "firefox", "ansible_var": "install_firefox"},
            {"id": "python", "ansible_var": "install_python"},
            {"id": "rust", "ansible_var": "install_rust"},
        ]

        vars_dict = self.menu._prepare_ansible_variables()

        assert vars_dict["install_docker"] is True
        assert vars_dict["install_firefox"] is True
        assert vars_dict["install_python"] is True
        assert vars_dict["install_rust"] is True
        assert vars_dict["git_user_name"] == "Test User"

    def test_get_ansible_var_name(self):
        """Test getting Ansible variable name from config name"""
        # Test various transformations
        assert self.menu._get_ansible_var_name("docker-ce") == "docker_ce"
        assert self.menu._get_ansible_var_name("install_docker") == "install_docker"
        assert self.menu._get_ansible_var_name("my-app-name") == "my_app_name"

    @patch("lib.tui.unified_menu.MessageDialog")
    def test_show_corruption_message(self, mock_dialog):
        """Test showing corruption message"""
        mock_dialog_instance = MagicMock()
        mock_dialog.return_value = mock_dialog_instance

        self.menu.show_corruption_message("Invalid YAML format")

        mock_dialog.assert_called_once()
        mock_dialog_instance.show.assert_called_once()
        call_args = mock_dialog_instance.show.call_args[0]
        assert "Configuration Error" in call_args[0]

    def test_get_packages_to_remove(self):
        """Test getting packages that need removal"""
        self.menu.operation_mode = "strict"
        self.menu.discovery = MagicMock()

        # Mock orphaned packages
        self.menu.discovery.get_orphaned_packages.return_value = {
            "opera-stable": {"menu_id": "opera", "safe_to_remove": True, "reason": "Safe to remove"},
            "vim": {"menu_id": "vim", "safe_to_remove": False, "reason": "System package"},
        }

        packages = self.menu.get_packages_to_remove()

        assert "opera-stable" in packages["safe"]
        assert "vim" in packages["unsafe"]
        assert len(packages["safe"]) == 1
        assert len(packages["unsafe"]) == 1

    def test_navigate_up_down(self):
        """Test navigation with arrow keys"""
        self.menu.items = [
            {"id": "item1", "parent": None},
            {"id": "item2", "parent": None},
            {"id": "item3", "parent": None},
        ]
        self.menu.current_menu = "root"
        self.menu.current_index = 0

        # Test down navigation
        result = self.menu.navigate(258)  # KEY_DOWN
        assert result is None
        assert self.menu.current_index == 1

        # Test up navigation
        result = self.menu.navigate(259)  # KEY_UP
        assert result is None
        assert self.menu.current_index == 0

    def test_navigate_quit(self):
        """Test quit navigation"""
        # Test with 'q' key
        result = self.menu.navigate(ord("q"))
        assert result == "quit"

        # Test with ESC key
        result = self.menu.navigate(27)
        assert result == "quit"
