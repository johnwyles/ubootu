"""
Unit tests for tui/models.py - TUI data models.
"""

from __future__ import annotations

import pytest

from lib.tui.models import MenuItem


class TestMenuItem:
    """Test MenuItem dataclass."""

    def test_minimal_initialization(self):
        """Test MenuItem with minimal required fields."""
        item = MenuItem(
            id="test-item", label="Test Item", description="Test description"
        )

        assert item.id == "test-item"
        assert item.label == "Test Item"
        assert item.description == "Test description"
        assert item.parent is None
        assert item.children is None
        assert item.selected is False
        assert item.default is False
        assert item.is_category is False
        assert item.is_configurable is False
        assert item.config_type == ""
        assert item.config_range == (1, 10)
        assert item.config_value == 5
        assert item.config_unit == ""
        assert item.config_options is None
        assert item.ansible_var is None

    def test_full_initialization(self):
        """Test MenuItem with all fields specified."""
        item = MenuItem(
            id="test-config",
            label="Test Config Item",
            description="Configurable test item",
            parent="parent-menu",
            children=["child1", "child2"],
            selected=True,
            default=True,
            is_category=True,
            is_configurable=True,
            config_type="slider",
            config_range=(0, 100),
            config_value=75,
            config_unit="%",
            config_options=[("opt1", "Option 1"), ("opt2", "Option 2")],
            ansible_var="test_config_value",
        )

        assert item.id == "test-config"
        assert item.label == "Test Config Item"
        assert item.description == "Configurable test item"
        assert item.parent == "parent-menu"
        assert item.children == ["child1", "child2"]
        assert item.selected is True
        assert item.default is True
        assert item.is_category is True
        assert item.is_configurable is True
        assert item.config_type == "slider"
        assert item.config_range == (0, 100)
        assert item.config_value == 75
        assert item.config_unit == "%"
        assert item.config_options == [("opt1", "Option 1"), ("opt2", "Option 2")]
        assert item.ansible_var == "test_config_value"

    def test_category_item(self):
        """Test MenuItem configured as a category."""
        item = MenuItem(
            id="dev-tools",
            label="Development Tools",
            description="Programming and development tools",
            is_category=True,
            children=["python", "nodejs", "docker"],
        )

        assert item.is_category is True
        assert item.children == ["python", "nodejs", "docker"]
        assert item.is_configurable is False
        assert item.selected is False

    def test_configurable_slider_item(self):
        """Test MenuItem configured as a slider."""
        item = MenuItem(
            id="swappiness",
            label="Swappiness",
            description="System swappiness value",
            is_configurable=True,
            config_type="slider",
            config_range=(0, 100),
            config_value=10,
            config_unit="%",
            ansible_var="system_swappiness",
        )

        assert item.is_configurable is True
        assert item.config_type == "slider"
        assert item.config_range == (0, 100)
        assert item.config_value == 10
        assert item.config_unit == "%"
        assert item.ansible_var == "system_swappiness"

    def test_configurable_dropdown_item(self):
        """Test MenuItem configured as a dropdown."""
        item = MenuItem(
            id="desktop-env",
            label="Desktop Environment",
            description="Choose your desktop environment",
            is_configurable=True,
            config_type="dropdown",
            config_options=[
                ("gnome", "GNOME"),
                ("kde", "KDE Plasma"),
                ("xfce", "XFCE"),
            ],
            config_value="gnome",
            ansible_var="desktop_environment",
        )

        assert item.is_configurable is True
        assert item.config_type == "dropdown"
        assert item.config_options == [
            ("gnome", "GNOME"),
            ("kde", "KDE Plasma"),
            ("xfce", "XFCE"),
        ]
        assert item.config_value == "gnome"
        assert item.ansible_var == "desktop_environment"

    def test_configurable_toggle_item(self):
        """Test MenuItem configured as a toggle."""
        item = MenuItem(
            id="enable-firewall",
            label="Enable Firewall",
            description="Enable UFW firewall",
            is_configurable=True,
            config_type="toggle",
            config_value=True,
            ansible_var="enable_firewall",
        )

        assert item.is_configurable is True
        assert item.config_type == "toggle"
        assert item.config_value is True
        assert item.ansible_var == "enable_firewall"

    def test_item_with_parent(self):
        """Test MenuItem with parent relationship."""
        item = MenuItem(
            id="python-tools",
            label="Python Development",
            description="Python tools and libraries",
            parent="development",
            default=True,
        )

        assert item.parent == "development"
        assert item.default is True
        assert item.children is None

    def test_item_selection_state(self):
        """Test MenuItem selection state changes."""
        item = MenuItem(id="test-item", label="Test", description="Test item")

        # Initially not selected
        assert item.selected is False

        # Select the item
        item.selected = True
        assert item.selected is True

        # Deselect the item
        item.selected = False
        assert item.selected is False

    def test_item_equality(self):
        """Test MenuItem equality based on ID."""
        item1 = MenuItem(id="same-id", label="Item 1", description="First item")

        item2 = MenuItem(id="same-id", label="Item 2", description="Second item")

        item3 = MenuItem(id="different-id", label="Item 3", description="Third item")

        # Items with same ID should be considered equal
        assert item1.id == item2.id
        assert item1.id != item3.id

    def test_config_value_types(self):
        """Test different config value types."""
        # String value
        item_str = MenuItem(
            id="test-str",
            label="String Config",
            description="String configuration",
            config_value="test value",
        )
        assert isinstance(item_str.config_value, str)
        assert item_str.config_value == "test value"

        # Integer value
        item_int = MenuItem(
            id="test-int",
            label="Int Config",
            description="Integer configuration",
            config_value=42,
        )
        assert isinstance(item_int.config_value, int)
        assert item_int.config_value == 42

        # Boolean value
        item_bool = MenuItem(
            id="test-bool",
            label="Bool Config",
            description="Boolean configuration",
            config_value=True,
        )
        assert isinstance(item_bool.config_value, bool)
        assert item_bool.config_value is True

        # List value
        item_list = MenuItem(
            id="test-list",
            label="List Config",
            description="List configuration",
            config_value=["opt1", "opt2", "opt3"],
        )
        assert isinstance(item_list.config_value, list)
        assert item_list.config_value == ["opt1", "opt2", "opt3"]
