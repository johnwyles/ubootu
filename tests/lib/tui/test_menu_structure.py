"""
Unit tests for menu_structure module
"""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, call, patch

import pytest

from lib.tui.menu_structure import MenuItem, build_menu_structure


class TestMenuItem:
    """Test the MenuItem dataclass."""

    def test_menu_item_creation(self):
        """Test creating a MenuItem."""
        item = MenuItem(id="test", label="Test Item", description="Test description")

        assert item.id == "test"
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

    def test_menu_item_with_all_fields(self):
        """Test creating a MenuItem with all fields."""
        item = MenuItem(
            id="test",
            label="Test Item",
            description="Test description",
            parent="root",
            children=["child1", "child2"],
            selected=True,
            default=True,
            is_category=True,
            is_configurable=True,
            config_type="slider",
            config_range=(0, 100),
            config_value=50,
            config_unit="%",
        )

        assert item.id == "test"
        assert item.label == "Test Item"
        assert item.description == "Test description"
        assert item.parent == "root"
        assert item.children == ["child1", "child2"]
        assert item.selected is True
        assert item.default is True
        assert item.is_category is True
        assert item.is_configurable is True
        assert item.config_type == "slider"
        assert item.config_range == (0, 100)
        assert item.config_value == 50
        assert item.config_unit == "%"

    def test_menu_item_mutability(self):
        """Test that MenuItem fields can be modified."""
        item = MenuItem("test", "Test", "Description")

        # Modify fields
        item.selected = True
        item.config_value = 10
        item.children = ["new_child"]

        assert item.selected is True
        assert item.config_value == 10
        assert item.children == ["new_child"]


class TestBuildMenuStructure:
    """Test the build_menu_structure function."""

    def test_build_menu_structure_returns_dict(self):
        """Test that build_menu_structure returns a dictionary."""
        result = build_menu_structure()
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_root_menu_exists(self):
        """Test that root menu is created."""
        items = build_menu_structure()
        assert "root" in items

        root = items["root"]
        assert root.id == "root"
        assert root.label == "🚀 Ubootu - Ubuntu System Setup"
        assert root.is_category is True
        assert root.parent is None
        assert root.children == [
            "development",
            "desktop",
            "applications",
            "security",
            "system",
        ]

    def test_main_categories_exist(self):
        """Test that all main categories exist."""
        items = build_menu_structure()

        main_categories = [
            "development",
            "desktop",
            "applications",
            "security",
            "system",
            "actions",
        ]
        for cat_id in main_categories:
            assert cat_id in items
            assert items[cat_id].is_category is True
            assert items[cat_id].parent == "root"

    def test_development_category_structure(self):
        """Test development category and its subcategories."""
        items = build_menu_structure()

        # Check development category
        dev = items["development"]
        assert dev.label == "Development Tools"
        assert dev.description == "Programming languages, IDEs, debugging tools"
        assert dev.children == [
            "dev-ides",
            "dev-languages",
            "dev-tools",
            "dev-containers",
        ]

        # Check subcategories exist
        assert "dev-ides" in items
        assert "dev-languages" in items
        assert "dev-tools" in items
        assert "dev-containers" in items

        # Check IDEs subcategory
        ides = items["dev-ides"]
        assert ides.parent == "development"
        assert ides.is_category is True
        assert "vscode" in ides.children
        assert "intellij" in ides.children
        assert "vim" in ides.children

    def test_desktop_category_structure(self):
        """Test desktop category and its subcategories."""
        items = build_menu_structure()

        desktop = items["desktop"]
        assert desktop.label == "Desktop Environment"
        assert desktop.children == ["desktop-env", "desktop-themes", "desktop-settings"]

        # Check desktop environments
        assert "desktop-env" in items
        env = items["desktop-env"]
        assert env.parent == "desktop"
        assert "gnome" in env.children
        assert "kde" in env.children

    def test_actions_menu(self):
        """Test actions menu structure."""
        items = build_menu_structure()

        assert "actions" in items
        actions = items["actions"]
        assert actions.label == "Actions"
        assert actions.children == [
            "action-install",
            "action-save",
            "action-reset",
            "action-exit",
        ]

        # Check individual actions
        assert "action-install" in items
        install = items["action-install"]
        assert install.parent == "actions"
        assert install.label == "🚀 Start Installation"
        assert not install.is_category

    def test_configurable_items(self):
        """Test items with configuration options."""
        items = build_menu_structure()

        # Check swappiness configuration
        assert "swappiness" in items
        swap = items["swappiness"]
        assert swap.is_configurable is True
        assert swap.config_type == "slider"
        assert swap.config_range == (1, 100)
        assert swap.config_unit == ""

        # Check CPU governor
        assert "cpu-governor" in items
        cpu = items["cpu-governor"]
        assert cpu.is_configurable is True
        assert cpu.config_type == "slider"

    def test_default_items(self):
        """Test items marked as default."""
        items = build_menu_structure()

        # Find items marked as default
        default_items = [item for item in items.values() if item.default]
        assert len(default_items) > 0

        # Common defaults should be marked
        if "curl" in items:
            assert items["curl"].default is True
        if "git" in items:
            assert items["git"].default is True

    def test_all_children_have_parents(self):
        """Test that all children referenced in parents actually exist."""
        items = build_menu_structure()

        for item_id, item in items.items():
            if item.children:
                for child_id in item.children:
                    assert (
                        child_id in items
                    ), f"Child {child_id} of {item_id} does not exist"
                    assert (
                        items[child_id].parent == item_id
                    ), f"Child {child_id} parent mismatch"

    def test_no_circular_references(self):
        """Test that there are no circular parent-child references."""
        items = build_menu_structure()

        def check_circular(item_id, visited=None):
            if visited is None:
                visited = set()

            if item_id in visited:
                return True

            visited.add(item_id)
            item = items.get(item_id)

            if item and item.parent:
                return check_circular(item.parent, visited.copy())

            return False

        for item_id in items:
            assert not check_circular(
                item_id
            ), f"Circular reference detected for {item_id}"

    def test_menu_item_ids_are_unique(self):
        """Test that all menu item IDs are unique."""
        items = build_menu_structure()
        ids = list(items.keys())
        assert len(ids) == len(set(ids)), "Duplicate menu item IDs found"

    def test_categories_have_children(self):
        """Test that all categories have children."""
        items = build_menu_structure()

        for item_id, item in items.items():
            if item.is_category and item_id != "actions":
                assert item.children, f"Category {item_id} has no children"
                assert (
                    len(item.children) > 0
                ), f"Category {item_id} has empty children list"

    def test_non_categories_have_no_children(self):
        """Test that non-category items don't have children."""
        items = build_menu_structure()

        for item_id, item in items.items():
            if not item.is_category:
                assert not item.children, f"Non-category {item_id} has children"

    def test_menu_depth(self):
        """Test that menu structure has reasonable depth."""
        items = build_menu_structure()

        def get_depth(item_id, current_depth=0):
            item = items.get(item_id)
            if not item or not item.children:
                return current_depth

            max_child_depth = 0
            for child_id in item.children:
                child_depth = get_depth(child_id, current_depth + 1)
                max_child_depth = max(max_child_depth, child_depth)

            return max_child_depth

        depth = get_depth("root")
        assert 2 <= depth <= 4, f"Menu depth {depth} is outside expected range"

    def test_all_items_have_descriptions(self):
        """Test that all items have non-empty descriptions."""
        items = build_menu_structure()

        for item_id, item in items.items():
            assert item.description, f"Item {item_id} has no description"
            assert (
                len(item.description) > 5
            ), f"Item {item_id} has too short description"

    def test_specific_menu_items_exist(self):
        """Test that specific expected menu items exist."""
        items = build_menu_structure()

        # Development tools
        expected_dev = ["python", "nodejs", "docker", "git", "vscode"]
        for item_id in expected_dev:
            assert item_id in items, f"Expected development item {item_id} not found"

        # Desktop environments
        expected_desktop = ["gnome", "kde", "xfce"]
        for item_id in expected_desktop:
            assert item_id in items, f"Expected desktop item {item_id} not found"

        # Applications
        expected_apps = ["firefox", "chrome", "vlc"]
        for item_id in expected_apps:
            assert item_id in items, f"Expected application {item_id} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
