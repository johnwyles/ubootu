"""
Unit tests for tui.menus.development - Development tools menu builder
"""


from __future__ import annotations
import pytest
from unittest.mock import Mock, MagicMock
from lib.tui.menus.development import DevelopmentMenuBuilder


class TestDevelopmentMenuBuilder:
    """Test DevelopmentMenuBuilder menu builder"""
    
    @pytest.fixture
    def menu_builder(self):
        """Create menu builder instance"""
        return DevelopmentMenuBuilder()
    
    def test_build_creates_menu_structure(self, menu_builder):
        """Test that build() creates proper menu structure"""
        items = menu_builder.build()
        
        # Should return a dictionary
        assert isinstance(items, dict)
        assert len(items) > 0
        
        # Check root category exists
        assert any(item.is_category for item in items.values())
    
    def test_menu_items_have_required_fields(self, menu_builder):
        """Test all menu items have required fields"""
        items = menu_builder.build()
        
        for item_id, item in items.items():
            assert hasattr(item, 'id')
            assert hasattr(item, 'label')
            assert hasattr(item, 'description')
            assert item.id == item_id
            assert item.label  # Not empty
            assert item.description  # Not empty
    
    def test_parent_child_relationships(self, menu_builder):
        """Test parent-child relationships are valid"""
        items = menu_builder.build()
        
        for item in items.values():
            if item.parent and item.parent != 'root':
                assert item.parent in items, f"Parent {item.parent} not found for {item.id}"
            
            if item.children:
                for child_id in item.children:
                    assert child_id in items, f"Child {child_id} not found for {item.id}"
                    assert items[child_id].parent == item.id
    
    def test_no_circular_references(self, menu_builder):
        """Test menu structure has no circular references"""
        items = menu_builder.build()
        
        def has_circular_ref(item_id, visited=None):
            if visited is None:
                visited = set()
            
            if item_id in visited:
                return True
            
            visited.add(item_id)
            item = items.get(item_id)
            
            if item and item.children:
                for child_id in item.children:
                    if has_circular_ref(child_id, visited.copy()):
                        return True
            
            return False
        
        for item_id in items:
            assert not has_circular_ref(item_id)
    
    def test_categories_have_children(self, menu_builder):
        """Test that categories have children"""
        items = menu_builder.build()
        
        for item in items.values():
            if item.is_category:
                assert item.children, f"Category {item.id} has no children"
    
    def test_configurable_items_have_valid_config(self, menu_builder):
        """Test configurable items have valid configuration"""
        items = menu_builder.build()
        
        for item in items.values():
            if item.is_configurable:
                assert item.config_type in ['slider', 'dropdown', 'toggle', 'text']
                
                if item.config_type == 'slider':
                    assert hasattr(item, 'config_range')
                    assert len(item.config_range) == 2
                    assert item.config_range[0] < item.config_range[1]
                
                elif item.config_type == 'dropdown':
                    assert hasattr(item, 'config_options')
                    assert isinstance(item.config_options, list)
                    assert len(item.config_options) > 0
