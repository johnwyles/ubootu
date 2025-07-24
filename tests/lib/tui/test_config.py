"""
Unit tests for tui/config.py - Configuration management for TUI interface
"""


from __future__ import annotations
import pytest
from typing import Dict, Set
from lib.tui.config import TUIConfigManager
from lib.tui.models import MenuItem


class TestTUIConfigManager:
    """Test TUIConfigManager class"""
    
    @pytest.fixture
    def sample_menu_items(self) -> Dict[str, MenuItem]:
        """Create sample menu items for testing"""
        items = {
            "root": MenuItem(
                id="root",
                label="Root Menu",
                description="Main menu",
                is_category=True,
                children=["cat1", "cat2", "item1"]
            ),
            "cat1": MenuItem(
                id="cat1",
                label="Category 1",
                description="First category",
                parent="root",
                is_category=True,
                children=["item2", "item3", "subcat1"]
            ),
            "cat2": MenuItem(
                id="cat2",
                label="Category 2",
                description="Second category",
                parent="root",
                is_category=True,
                children=["item4", "item5"]
            ),
            "subcat1": MenuItem(
                id="subcat1",
                label="Subcategory 1",
                description="Nested category",
                parent="cat1",
                is_category=True,
                children=["item6", "item7"]
            ),
            "item1": MenuItem(
                id="item1",
                label="Item 1",
                description="Direct root item",
                parent="root",
                selected=False
            ),
            "item2": MenuItem(
                id="item2",
                label="Item 2",
                description="Item in cat1",
                parent="cat1",
                selected=False,
                default=True
            ),
            "item3": MenuItem(
                id="item3",
                label="Item 3",
                description="Item in cat1",
                parent="cat1",
                selected=False
            ),
            "item4": MenuItem(
                id="item4",
                label="Item 4",
                description="Item in cat2",
                parent="cat2",
                selected=True,
                default=True
            ),
            "item5": MenuItem(
                id="item5",
                label="Item 5",
                description="Item in cat2",
                parent="cat2",
                selected=False
            ),
            "item6": MenuItem(
                id="item6",
                label="Item 6",
                description="Item in subcat1",
                parent="subcat1",
                selected=False
            ),
            "item7": MenuItem(
                id="item7",
                label="Item 7",
                description="Item in subcat1",
                parent="subcat1",
                selected=True
            ),
        }
        return items
    
    @pytest.fixture
    def selected_items(self) -> Set[str]:
        """Create initial selected items set"""
        return {"item4", "item7"}
    
    @pytest.fixture
    def config_manager(self, sample_menu_items, selected_items):
        """Create TUIConfigManager instance"""
        return TUIConfigManager(sample_menu_items, selected_items)
    
    def test_init(self, sample_menu_items, selected_items):
        """Test TUIConfigManager initialization"""
        manager = TUIConfigManager(sample_menu_items, selected_items)
        assert manager.menu_items == sample_menu_items
        assert manager.selected_items == selected_items
        assert manager.current_menu == "root"
        assert manager.current_item == 0
        assert manager.scroll_offset == 0
        assert manager.breadcrumb_stack == []
    
    def test_get_current_menu_items(self, config_manager):
        """Test getting items for current menu"""
        # Root menu
        items = config_manager.get_current_menu_items()
        assert len(items) == 3
        assert items[0].id == "cat1"
        assert items[1].id == "cat2"
        assert items[2].id == "item1"
        
        # Navigate to cat1
        config_manager.current_menu = "cat1"
        items = config_manager.get_current_menu_items()
        assert len(items) == 3
        assert items[0].id == "item2"
        assert items[1].id == "item3"
        assert items[2].id == "subcat1"
        
        # Navigate to item (no children)
        config_manager.current_menu = "item1"
        items = config_manager.get_current_menu_items()
        assert len(items) == 0
    
    def test_navigate_to_menu(self, config_manager):
        """Test menu navigation"""
        # Navigate to cat1
        config_manager.navigate_to_menu("cat1")
        assert config_manager.current_menu == "cat1"
        assert config_manager.current_item == 0
        assert config_manager.scroll_offset == 0
        assert len(config_manager.breadcrumb_stack) == 1
        assert config_manager.breadcrumb_stack[0] == ("root", 0, 0)
        
        # Navigate to subcat1
        config_manager.current_item = 2
        config_manager.navigate_to_menu("subcat1")
        assert config_manager.current_menu == "subcat1"
        assert len(config_manager.breadcrumb_stack) == 2
        
        # Navigate without saving breadcrumb
        config_manager.navigate_to_menu("cat2", save_breadcrumb=False)
        assert config_manager.current_menu == "cat2"
        assert len(config_manager.breadcrumb_stack) == 2  # No change
    
    def test_navigate_back(self, config_manager):
        """Test navigating back through breadcrumb stack"""
        # Navigate forward
        config_manager.navigate_to_menu("cat1")
        config_manager.current_item = 2
        config_manager.navigate_to_menu("subcat1")
        
        # Navigate back once
        result = config_manager.navigate_back()
        assert result is True
        assert config_manager.current_menu == "cat1"
        assert config_manager.current_item == 2
        
        # Navigate back again
        result = config_manager.navigate_back()
        assert result is True
        assert config_manager.current_menu == "root"
        assert config_manager.current_item == 0
        
        # Try to navigate back from root
        result = config_manager.navigate_back()
        assert result is False
        assert config_manager.current_menu == "root"
    
    def test_reset_to_root(self, config_manager):
        """Test resetting navigation to root"""
        # Navigate deep
        config_manager.navigate_to_menu("cat1")
        config_manager.navigate_to_menu("subcat1")
        config_manager.current_item = 5
        config_manager.scroll_offset = 10
        
        # Reset
        config_manager.reset_to_root()
        assert config_manager.current_menu == "root"
        assert config_manager.current_item == 0
        assert config_manager.scroll_offset == 0
        assert config_manager.breadcrumb_stack == []
    
    def test_get_breadcrumb(self, config_manager):
        """Test breadcrumb generation"""
        # At root
        breadcrumb = config_manager.get_breadcrumb()
        assert breadcrumb == "Root Menu"
        
        # Navigate to cat1
        config_manager.current_menu = "cat1"
        breadcrumb = config_manager.get_breadcrumb()
        assert breadcrumb == "Category 1"
        
        # Navigate to subcat1
        config_manager.current_menu = "subcat1"
        breadcrumb = config_manager.get_breadcrumb()
        assert breadcrumb == "Category 1 > Subcategory 1"
        
        # Navigate to item
        config_manager.current_menu = "item6"
        breadcrumb = config_manager.get_breadcrumb()
        assert breadcrumb == "Category 1 > Subcategory 1 > Item 6"
    
    def test_get_category_selection_status(self, config_manager):
        """Test getting category selection status"""
        # cat1: has item2, item3, item6, item7
        # Selected: item7
        status = config_manager.get_category_selection_status("cat1")
        assert status == "partial"
        
        # cat2: has item4, item5
        # Selected: item4
        status = config_manager.get_category_selection_status("cat2")
        assert status == "partial"
        
        # Select all in cat2
        config_manager.selected_items.add("item5")
        status = config_manager.get_category_selection_status("cat2")
        assert status == "full"
        
        # Deselect all in cat2
        config_manager.selected_items.discard("item4")
        config_manager.selected_items.discard("item5")
        status = config_manager.get_category_selection_status("cat2")
        assert status == "empty"
        
        # Non-existent category
        status = config_manager.get_category_selection_status("nonexistent")
        assert status == "empty"
    
    def test_get_all_selectable_items(self, config_manager):
        """Test getting all selectable items in a category"""
        # cat1 contains item2, item3, and subcat1 (which has item6, item7)
        items = config_manager.get_all_selectable_items("cat1")
        assert set(items) == {"item2", "item3", "item6", "item7"}
        
        # cat2 contains item4, item5
        items = config_manager.get_all_selectable_items("cat2")
        assert set(items) == {"item4", "item5"}
        
        # subcat1 contains item6, item7
        items = config_manager.get_all_selectable_items("subcat1")
        assert set(items) == {"item6", "item7"}
        
        # root contains all items
        items = config_manager.get_all_selectable_items("root")
        assert set(items) == {"item1", "item2", "item3", "item4", "item5", "item6", "item7"}
        
        # Non-category item
        items = config_manager.get_all_selectable_items("item1")
        assert items == []
    
    def test_select_all_in_category(self, config_manager):
        """Test selecting/deselecting all items in a category"""
        # Select all in cat1
        config_manager.select_all_in_category("cat1", True)
        assert "item2" in config_manager.selected_items
        assert "item3" in config_manager.selected_items
        assert "item6" in config_manager.selected_items
        assert "item7" in config_manager.selected_items
        assert config_manager.menu_items["item2"].selected is True
        assert config_manager.menu_items["item3"].selected is True
        
        # Deselect all in cat1
        config_manager.select_all_in_category("cat1", False)
        assert "item2" not in config_manager.selected_items
        assert "item3" not in config_manager.selected_items
        assert "item6" not in config_manager.selected_items
        assert "item7" not in config_manager.selected_items
        assert config_manager.menu_items["item2"].selected is False
        assert config_manager.menu_items["item3"].selected is False
    
    def test_select_all_in_current_menu(self, config_manager):
        """Test selecting/deselecting all items in current menu"""
        # Navigate to cat1
        config_manager.current_menu = "cat1"
        
        # Select all
        config_manager.select_all_in_current_menu(True)
        assert "item2" in config_manager.selected_items
        assert "item3" in config_manager.selected_items
        # subcat1 is a category, shouldn't be selected
        assert "subcat1" not in config_manager.selected_items
        
        # Deselect all
        config_manager.select_all_in_current_menu(False)
        assert "item2" not in config_manager.selected_items
        assert "item3" not in config_manager.selected_items
    
    def test_toggle_item_selection(self, config_manager):
        """Test toggling individual item selection"""
        item = config_manager.menu_items["item1"]
        initial_state = item.selected
        initial_in_set = "item1" in config_manager.selected_items
        
        # Toggle once
        config_manager.toggle_item_selection(item)
        assert item.selected is not initial_state
        assert ("item1" in config_manager.selected_items) is not initial_in_set
        
        # Toggle again
        config_manager.toggle_item_selection(item)
        assert item.selected is initial_state
        assert ("item1" in config_manager.selected_items) is initial_in_set
    
    def test_apply_defaults(self, config_manager):
        """Test applying default selections"""
        # Clear all selections first
        config_manager.selected_items.clear()
        for item in config_manager.menu_items.values():
            item.selected = False
        
        # Apply defaults
        config_manager.apply_defaults()
        
        # Check that default items are selected
        assert "item2" in config_manager.selected_items  # default=True
        assert "item4" in config_manager.selected_items  # default=True
        assert config_manager.menu_items["item2"].selected is True
        assert config_manager.menu_items["item4"].selected is True
        
        # Non-default items should not be selected
        assert "item1" not in config_manager.selected_items
        assert "item3" not in config_manager.selected_items
    
    def test_reset_all_selections(self, config_manager):
        """Test resetting all selections to defaults"""
        # Make some changes
        config_manager.selected_items.add("item1")
        config_manager.selected_items.add("item3")
        config_manager.selected_items.discard("item4")  # Remove default
        
        # Reset
        config_manager.reset_all_selections()
        
        # Should only have default items selected
        assert config_manager.selected_items == {"item2", "item4"}
        assert config_manager.menu_items["item2"].selected is True
        assert config_manager.menu_items["item4"].selected is True
        assert config_manager.menu_items["item1"].selected is False
        assert config_manager.menu_items["item3"].selected is False
    
    def test_get_selection_counts(self, config_manager):
        """Test getting selection counts"""
        selected, total = config_manager.get_selection_counts()
        assert selected == 2  # item4, item7
        assert total == 7  # All non-category items
        
        # Add selections
        config_manager.selected_items.add("item1")
        config_manager.selected_items.add("item2")
        selected, total = config_manager.get_selection_counts()
        assert selected == 4
        assert total == 7
    
    def test_get_category_selection_counts(self, config_manager):
        """Test getting category-specific selection counts"""
        # cat1 has 4 items (item2, item3, item6, item7), 1 selected (item7)
        selected, total = config_manager.get_category_selection_counts("cat1")
        assert selected == 1
        assert total == 4
        
        # cat2 has 2 items (item4, item5), 1 selected (item4)
        selected, total = config_manager.get_category_selection_counts("cat2")
        assert selected == 1
        assert total == 2
    
    def test_has_selections(self, config_manager):
        """Test checking if any selections exist"""
        assert config_manager.has_selections() is True
        
        # Clear selections
        config_manager.selected_items.clear()
        assert config_manager.has_selections() is False
        
        # Add one selection
        config_manager.selected_items.add("item1")
        assert config_manager.has_selections() is True
    
    def test_validate_menu_structure(self, config_manager):
        """Test menu structure validation"""
        # Valid structure should have no issues
        issues = config_manager.validate_menu_structure()
        assert len(issues) == 0
        
        # Add orphaned item
        config_manager.menu_items["orphan"] = MenuItem(
            id="orphan",
            label="Orphaned Item",
            description="Has invalid parent",
            parent="nonexistent"
        )
        issues = config_manager.validate_menu_structure()
        assert len(issues) == 1
        assert "invalid parent" in issues[0]
        
        # Clean up
        del config_manager.menu_items["orphan"]
    
    def test_circular_reference_detection(self, config_manager):
        """Test detection of circular references"""
        # Create circular reference: cat1 -> circ1 -> circ2 -> cat1
        config_manager.menu_items["circ1"] = MenuItem(
            id="circ1",
            label="Circular 1",
            description="Part of circle",
            parent="cat1",
            is_category=True,
            children=["circ2"]
        )
        config_manager.menu_items["circ2"] = MenuItem(
            id="circ2",
            label="Circular 2",
            description="Part of circle",
            parent="circ1",
            is_category=True,
            children=["cat1"]
        )
        config_manager.menu_items["cat1"].children.append("circ1")
        
        issues = config_manager.validate_menu_structure()
        assert any("Circular reference" in issue for issue in issues)
        
        # Clean up
        del config_manager.menu_items["circ1"]
        del config_manager.menu_items["circ2"]
        config_manager.menu_items["cat1"].children.remove("circ1")
    
    def test_empty_menu_items(self):
        """Test TUIConfigManager with empty menu items"""
        # Create a minimal root menu for empty case
        from lib.tui.models import MenuItem
        root = MenuItem(id="root", label="Root", description="Root menu", is_category=True)
        manager = TUIConfigManager({"root": root}, set())
        assert manager.get_current_menu_items() == []  # root has no children
        assert manager.get_breadcrumb() == "Root"
        assert manager.get_selection_counts() == (0, 0)
        assert manager.has_selections() is False
    
    def test_navigation_with_invalid_menu_id(self, config_manager):
        """Test navigation to invalid menu ID"""
        config_manager.navigate_to_menu("nonexistent")
        assert config_manager.current_menu == "nonexistent"
        # Should handle gracefully
        items = config_manager.get_current_menu_items()
        assert items == []


@pytest.mark.parametrize("category_id,expected_status", [
    ("cat1", "partial"),  # Has 4 items, 1 selected
    ("cat2", "partial"),  # Has 2 items, 1 selected
    ("subcat1", "partial"),  # Has 2 items, 1 selected
    ("nonexistent", "empty"),  # Invalid category
])
def test_category_selection_status_parametrized(category_id, expected_status):
    """Parametrized test for category selection status"""
    menu_items = {
        "cat1": MenuItem(id="cat1", label="Cat 1", description="", is_category=True, children=["item1", "item2"]),
        "cat2": MenuItem(id="cat2", label="Cat 2", description="", is_category=True, children=["item3", "item4"]),
        "subcat1": MenuItem(id="subcat1", label="Subcat 1", description="", is_category=True, children=["item5", "item6"]),
        "item1": MenuItem(id="item1", label="Item 1", description="", parent="cat1"),
        "item2": MenuItem(id="item2", label="Item 2", description="", parent="cat1"),
        "item3": MenuItem(id="item3", label="Item 3", description="", parent="cat2"),
        "item4": MenuItem(id="item4", label="Item 4", description="", parent="cat2"),
        "item5": MenuItem(id="item5", label="Item 5", description="", parent="subcat1"),
        "item6": MenuItem(id="item6", label="Item 6", description="", parent="subcat1"),
    }
    selected_items = {"item1", "item3", "item5"}
    
    manager = TUIConfigManager(menu_items, selected_items)
    assert manager.get_category_selection_status(category_id) == expected_status