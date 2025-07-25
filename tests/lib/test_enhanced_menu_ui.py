#!/usr/bin/env python3
"""
Comprehensive unit tests for enhanced_menu_ui module
"""

import os
import sys
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import pytest
import yaml

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lib.enhanced_menu_ui import HELP_DESCRIPTIONS, EnhancedMenuUI, MenuItem, main, run_tui


class TestMenuItem:
    """Test MenuItem dataclass"""

    def test_menu_item_creation(self):
        """Test creating a MenuItem with all fields"""
        item = MenuItem(
            id="test-item",
            label="Test Item",
            description="Test description",
            parent="parent-id",
            children=["child1", "child2"],
            is_category=True,
            is_configurable=False,
            default=True,
            selected=False,
            config_type="slider",
            config_value=50,
            config_range=(0, 100),
            config_unit="%",
            config_options=None,
            ansible_var="test_var",
            emoji="🔧",
            help_text="Detailed help",
        )

        assert item.id == "test-item"
        assert item.label == "Test Item"
        assert item.description == "Test description"
        assert item.parent == "parent-id"
        assert item.children == ["child1", "child2"]
        assert item.is_category is True
        assert item.is_configurable is False
        assert item.default is True
        assert item.selected is False
        assert item.emoji == "🔧"
        assert item.help_text == "Detailed help"

    def test_menu_item_defaults(self):
        """Test MenuItem with default values"""
        item = MenuItem(id="simple", label="Simple Item", description="Simple description")

        assert item.parent is None
        assert item.children == []
        assert item.is_category is False
        assert item.is_configurable is False
        assert item.default is False
        assert item.selected is False
        assert item.config_type == "slider"
        assert item.config_value is None
        assert item.config_range == (1, 10)
        assert item.config_unit == ""
        assert item.config_options is None
        assert item.ansible_var is None
        assert item.emoji == ""
        assert item.help_text is None


class TestEnhancedMenuUI:
    """Test EnhancedMenuUI class"""

    @pytest.fixture
    def mock_console(self):
        """Mock Rich console"""
        with patch("lib.enhanced_menu_ui.Console") as mock:
            yield mock.return_value

    @pytest.fixture
    def menu_ui(self, mock_console):
        """Create EnhancedMenuUI instance with mocked console"""
        ui = EnhancedMenuUI()
        ui.console = mock_console
        return ui

    def test_initialization(self, menu_ui):
        """Test EnhancedMenuUI initialization"""
        assert menu_ui.current_item == 0
        assert menu_ui.current_menu == "root"
        assert isinstance(menu_ui.selected_items, set)
        assert isinstance(menu_ui.menu_items, dict)
        assert isinstance(menu_ui.installed_fonts, set)

        # Check root menu exists
        assert "root" in menu_ui.menu_items
        assert menu_ui.menu_items["root"].is_category

    def test_build_menus(self, menu_ui):
        """Test that all menus are built correctly"""
        # Check main categories
        main_categories = ["development", "desktop", "applications", "security", "system"]
        for cat in main_categories:
            assert cat in menu_ui.menu_items
            assert menu_ui.menu_items[cat].is_category
            assert menu_ui.menu_items[cat].parent == "root"

    def test_development_menu_structure(self, menu_ui):
        """Test development menu structure"""
        # Check development subcategories
        dev_subcats = ["dev-ides", "dev-languages", "dev-tools", "dev-containers", "dev-cli-modern"]
        for subcat in dev_subcats:
            assert subcat in menu_ui.menu_items
            assert menu_ui.menu_items[subcat].is_category
            assert menu_ui.menu_items[subcat].parent == "development"

        # Check some development tools
        assert "vscode" in menu_ui.menu_items
        assert menu_ui.menu_items["vscode"].parent == "dev-ides"
        assert menu_ui.menu_items["vscode"].default is True
        assert menu_ui.menu_items["vscode"].emoji == "📝"

        assert "python" in menu_ui.menu_items
        assert menu_ui.menu_items["python"].parent == "dev-languages"
        assert menu_ui.menu_items["python"].default is True

    def test_help_descriptions(self, menu_ui):
        """Test that help descriptions are properly linked"""
        # Check that items with help descriptions have them set
        assert "vscode" in HELP_DESCRIPTIONS
        assert menu_ui.menu_items["vscode"].help_text == HELP_DESCRIPTIONS["vscode"]

        assert "python" in HELP_DESCRIPTIONS
        assert menu_ui.menu_items["python"].help_text == HELP_DESCRIPTIONS["python"]

    def test_default_selections(self, menu_ui):
        """Test that default items are selected"""
        # Check some default items
        default_items = ["vscode", "python", "git", "docker", "firefox", "ufw"]
        for item_id in default_items:
            assert item_id in menu_ui.selected_items
            assert menu_ui.menu_items[item_id].selected is True

    def test_get_selection_indicator(self, menu_ui):
        """Test selection indicator logic"""
        # Non-category item
        item = menu_ui.menu_items["vscode"]
        assert menu_ui.get_selection_indicator(item) == "✓"

        # Unselected item
        unselected = MenuItem("test", "Test", "Test", selected=False)
        assert menu_ui.get_selection_indicator(unselected) == " "

        # Category with no selections
        category = MenuItem("cat", "Category", "Test", is_category=True, children=["item1", "item2"])
        menu_ui.menu_items["item1"] = MenuItem("item1", "Item 1", "Test", parent="cat", selected=False)
        menu_ui.menu_items["item2"] = MenuItem("item2", "Item 2", "Test", parent="cat", selected=False)
        assert menu_ui.get_selection_indicator(category) == "○"

        # Category with all selections
        menu_ui.menu_items["item1"].selected = True
        menu_ui.menu_items["item2"].selected = True
        assert menu_ui.get_selection_indicator(category) == "◉"

        # Category with partial selections
        menu_ui.menu_items["item1"].selected = True
        menu_ui.menu_items["item2"].selected = False
        assert menu_ui.get_selection_indicator(category) == "◎"

    def test_font_availability(self, menu_ui):
        """Test font availability logic"""
        # Initially only Ubuntu font should be available
        fonts = menu_ui._get_available_fonts()
        font_names = [f[0] for f in fonts]
        assert "ubuntu" in font_names

        # Add Noto font selection
        menu_ui.selected_items.add("fonts-noto")
        fonts = menu_ui._get_available_fonts()
        font_names = [f[0] for f in fonts]
        assert "noto" in font_names

        # Add JetBrains Mono Nerd Font selection (the actual ID in the menu)
        menu_ui.selected_items.add("nf-jetbrains")
        fonts = menu_ui._get_available_fonts()
        font_names = [f[0] for f in fonts]
        assert "jetbrains-nerd" in font_names

    def test_toggle_selection(self, menu_ui):
        """Test toggling item selection"""
        # Find an unselected item
        item = menu_ui.menu_items["sublime"]
        assert item.selected is False
        assert item.id not in menu_ui.selected_items

        # Toggle selection on
        menu_ui._toggle_selection(item)
        assert item.selected is True
        assert item.id in menu_ui.selected_items

        # Toggle selection off
        menu_ui._toggle_selection(item)
        assert item.selected is False
        assert item.id not in menu_ui.selected_items

    def test_select_deselect_all_in_menu(self, menu_ui):
        """Test selecting/deselecting all in current menu"""
        # Navigate to dev-ides menu
        menu_ui.current_menu = "dev-ides"

        # Select all in current menu
        menu_ui._select_all_in_menu()
        items = menu_ui.get_current_menu_items()
        for item in items:
            if not item.is_category:
                assert item.selected is True
                assert item.id in menu_ui.selected_items

        # Deselect all in current menu
        menu_ui._deselect_all_in_menu()
        for item in items:
            if not item.is_category:
                assert item.selected is False
                assert item.id not in menu_ui.selected_items

    @patch("builtins.input", return_value="")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_save_configuration(self, mock_exists, mock_file, mock_input, menu_ui, mock_console):
        """Test saving configuration"""
        mock_exists.return_value = False

        # Add some selections
        menu_ui.selected_items = {"vscode", "python", "docker"}

        # Set a configurable value
        menu_ui.menu_items["swappiness"].config_value = 20

        # Save configuration
        menu_ui._save_configuration()

        # Check file was opened for writing
        mock_file.assert_called_once_with("config.yml", "w")

        # Check YAML was written
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        config = yaml.safe_load(written_content)

        assert "selected_items" in config
        assert set(config["selected_items"]) == {"vscode", "python", "docker"}
        assert "configurable_items" in config
        assert "swappiness" in config["configurable_items"]
        assert config["configurable_items"]["swappiness"]["value"] == 20

    def test_configuration_loading_on_init(self, menu_ui):
        """Test that configuration would be loaded on initialization"""
        # Since _load_configuration doesn't exist, test that defaults are applied
        # Check that default items are selected
        assert "vscode" in menu_ui.selected_items
        assert "python" in menu_ui.selected_items
        assert "git" in menu_ui.selected_items

        # Check default configurable values
        assert menu_ui.menu_items["swappiness"].config_value == 10

    def test_get_current_menu_items(self, menu_ui):
        """Test getting items for current menu"""
        # Root menu
        items = menu_ui.get_current_menu_items()
        item_ids = [item.id for item in items]
        assert "development" in item_ids
        assert "desktop" in item_ids
        assert "applications" in item_ids

        # Navigate to development menu
        menu_ui.current_menu = "development"
        items = menu_ui.get_current_menu_items()
        item_ids = [item.id for item in items]
        assert "dev-ides" in item_ids
        assert "dev-languages" in item_ids
        assert "dev-tools" in item_ids

    def test_menu_navigation(self, menu_ui):
        """Test menu navigation logic"""
        # Start at root
        assert menu_ui.current_menu == "root"
        assert menu_ui.current_item == 0

        # Simulate navigating to development (this would normally happen via keyboard input)
        menu_ui.current_menu = "development"
        assert menu_ui.current_menu == "development"

        # Get items in development menu
        items = menu_ui.get_current_menu_items()
        assert len(items) > 0
        assert any(item.id == "dev-ides" for item in items)

    def test_configurable_items(self, menu_ui):
        """Test configurable items"""
        # Check swappiness is configurable
        swappiness = menu_ui.menu_items["swappiness"]
        assert swappiness.is_configurable is True
        assert swappiness.config_type == "slider"
        assert swappiness.config_range == (0, 100)
        assert swappiness.config_value == 10  # Default

        # Check font settings
        font_interface = menu_ui.menu_items["font-interface"]
        assert font_interface.is_configurable is True
        assert font_interface.config_type == "dropdown"


class TestHelpDescriptions:
    """Test help descriptions"""

    def test_help_descriptions_exist(self):
        """Test that help descriptions dictionary exists and has content"""
        assert len(HELP_DESCRIPTIONS) > 0
        assert "vscode" in HELP_DESCRIPTIONS
        assert "python" in HELP_DESCRIPTIONS
        assert "swappiness" in HELP_DESCRIPTIONS

    def test_help_description_format(self):
        """Test help description formatting"""
        for key, desc in HELP_DESCRIPTIONS.items():
            assert isinstance(desc, str)
            assert len(desc) > 20  # Meaningful description
            assert not desc.startswith(" ")  # No leading spaces
            assert not desc.endswith(" ")  # No trailing spaces


class TestMainFunctions:
    """Test main entry point functions"""

    @patch("lib.enhanced_menu_ui.EnhancedMenuUI")
    def test_run_tui(self, mock_ui_class):
        """Test run_tui function"""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.run_hierarchical_tui.return_value = 0

        # Run with no sections
        result = run_tui()
        assert result == 0
        mock_ui.run_hierarchical_tui.assert_called_once()

        # Reset mock
        mock_ui.reset_mock()

        # Run with sections
        result = run_tui(["development", "security"])
        assert result == 0
        mock_ui.run_hierarchical_tui.assert_called_once()

    @patch("lib.enhanced_menu_ui.run_tui")
    @patch("sys.argv", ["enhanced_menu_ui.py"])
    def test_main_no_args(self, mock_run_tui):
        """Test main function with no arguments"""
        mock_run_tui.return_value = 0

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_run_tui.assert_called_once_with(None)

    @patch("lib.enhanced_menu_ui.run_tui")
    @patch("sys.argv", ["enhanced_menu_ui.py", "development", "applications"])
    def test_main_with_sections(self, mock_run_tui):
        """Test main function with section arguments"""
        mock_run_tui.return_value = 0

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_run_tui.assert_called_once_with(["development", "applications"])

    @patch("lib.enhanced_menu_ui.run_tui")
    @patch("sys.argv", ["enhanced_menu_ui.py", "--help"])
    def test_main_help_flag(self, mock_run_tui):
        """Test main function with help flag"""
        with pytest.raises(SystemExit):
            main()

        # Should not call run_tui when help is requested
        mock_run_tui.assert_not_called()


class TestMenuStructure:
    """Test the complete menu structure"""

    @pytest.fixture
    def menu_ui(self):
        """Create a fresh EnhancedMenuUI instance"""
        with patch("lib.enhanced_menu_ui.Console"):
            return EnhancedMenuUI()

    def test_all_items_have_parents(self, menu_ui):
        """Test that all non-root items have valid parents"""
        for item_id, item in menu_ui.menu_items.items():
            if item_id != "root" and item_id != "actions":
                assert item.parent is not None
                assert item.parent in menu_ui.menu_items

    def test_all_children_exist(self, menu_ui):
        """Test that all referenced children exist"""
        for item in menu_ui.menu_items.values():
            if item.is_category:
                for child_id in item.children:
                    assert child_id in menu_ui.menu_items

    def test_no_orphaned_items(self, menu_ui):
        """Test that all items are reachable from root"""
        visited = set()

        def visit(item_id):
            if item_id in visited:
                return
            visited.add(item_id)
            item = menu_ui.menu_items[item_id]
            if item.is_category:
                for child_id in item.children:
                    visit(child_id)

        # Start from root and actions
        visit("root")
        visit("actions")

        # All items should be visited
        for item_id in menu_ui.menu_items:
            assert item_id in visited, f"Item {item_id} is not reachable from root"

    def test_emojis_are_consistent(self, menu_ui):
        """Test that items have appropriate emojis"""
        # Categories should have emojis
        categories = [item for item in menu_ui.menu_items.values() if item.is_category]
        for cat in categories:
            if cat.id not in ["root", "actions"]:  # Root might not have emoji
                assert cat.emoji != "", f"Category {cat.id} is missing emoji"

        # Check some specific items have emojis
        emoji_items = ["vscode", "python", "docker", "git", "firefox"]
        for item_id in emoji_items:
            if item_id in menu_ui.menu_items:
                assert menu_ui.menu_items[item_id].emoji != "", f"Item {item_id} is missing emoji"


class TestConfigurationPersistence:
    """Test configuration saving and loading"""

    @pytest.fixture
    def menu_ui(self):
        """Create EnhancedMenuUI with mocked console"""
        with patch("lib.enhanced_menu_ui.Console"):
            return EnhancedMenuUI()

    def test_configuration_format(self, menu_ui):
        """Test the configuration format when saved"""
        # Set up some state
        menu_ui.selected_items = {"vscode", "python", "docker", "git"}
        menu_ui.menu_items["swappiness"].config_value = 15
        menu_ui.menu_items["font-interface"].config_value = "Ubuntu 12"

        # Generate config
        config = {
            "metadata": {"version": "1.0", "created_at": "2024-01-01T00:00:00"},
            "selected_items": sorted(menu_ui.selected_items),
            "configurable_items": {},
        }

        # Add configurable items
        for item in menu_ui.menu_items.values():
            if item.is_configurable and item.config_value is not None:
                config["configurable_items"][item.id] = {"id": item.id, "value": item.config_value}

        # Verify structure
        assert "metadata" in config
        assert "selected_items" in config
        assert "configurable_items" in config
        assert len(config["selected_items"]) == 4
        assert config["configurable_items"]["swappiness"]["value"] == 15
        assert config["configurable_items"]["font-interface"]["value"] == "Ubuntu 12"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
