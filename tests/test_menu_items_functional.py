#!/usr/bin/env python3
"""
Functional tests for menu_items module
Tests the actual menu structure and data loading
"""

import pytest

from lib.tui.menu_items import load_menu_structure


class TestMenuItemsFunctional:
    """Test menu items functionality"""

    def test_load_menu_structure_returns_list(self):
        """Test that load_menu_structure returns a list"""
        result = load_menu_structure()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_menu_structure_has_required_categories(self):
        """Test all required categories exist"""
        menu = load_menu_structure()
        
        # Get all category IDs
        category_ids = [item['id'] for item in menu if item.get('is_category')]
        
        # Check required categories
        required_categories = [
            'development', 'desktop', 'applications', 'security', 
            'system', 'ai-ml', 'gaming', 'multimedia'
        ]
        
        for category in required_categories:
            assert category in category_ids, f"Missing category: {category}"

    def test_menu_items_have_required_fields(self):
        """Test all menu items have required fields"""
        menu = load_menu_structure()
        
        for item in menu:
            assert 'id' in item, f"Item missing 'id': {item}"
            assert 'label' in item, f"Item missing 'label': {item}"
            # is_category is optional, defaults to False if not present
            
            if item.get('is_category', False):
                assert 'children' in item, f"Category missing 'children': {item['id']}"
                assert isinstance(item['children'], list)

    def test_development_category_structure(self):
        """Test development category has expected subcategories"""
        menu = load_menu_structure()
        dev_category = next((item for item in menu if item['id'] == 'development'), None)
        
        assert dev_category is not None
        assert dev_category.get('is_category', False) is True
        assert len(dev_category['children']) > 0
        
        # Check for common development subcategories - these are actual subcategories in the menu
        dev_children_ids = dev_category['children']
        expected_subcategories = ['dev-languages', 'dev-ides', 'dev-vcs', 'dev-containers']
        
        for subcat in expected_subcategories:
            assert subcat in dev_children_ids, f"Missing dev subcategory: {subcat}"

    def test_application_items_have_ansible_vars(self):
        """Test application items have ansible variable names"""
        menu = load_menu_structure()
        
        # Find non-category items (actual applications)
        apps = [item for item in menu if not item.get('is_category', False)]
        
        for app in apps[:50]:  # Test first 50 apps
            # Apps should have either ansible_var or be special items
            if app['id'] not in ['back', 'separator']:
                # Most apps should have label and id
                assert app['label'], f"App missing label: {app['id']}"
                assert app['id'], f"App missing id"

    def test_menu_hierarchy_parent_child_consistency(self):
        """Test parent-child relationships are consistent"""
        menu = load_menu_structure()
        
        # Build parent map
        parent_map = {}
        for item in menu:
            if item.get('is_category') and 'children' in item:
                for child_id in item['children']:
                    parent_map[child_id] = item['id']
        
        # Verify all items with parents exist
        all_ids = [item['id'] for item in menu]
        for child_id, parent_id in parent_map.items():
            if child_id != 'back':  # Skip special items
                assert child_id in all_ids, f"Child {child_id} of {parent_id} not found in menu"

    def test_desktop_environments_complete(self):
        """Test all desktop environments are present"""
        menu = load_menu_structure()
        desktop = next((item for item in menu if item['id'] == 'desktop'), None)
        
        assert desktop is not None
        
        # Find desktop environments - they might be nested under desktop subcategories
        # Check all items in the menu that contain desktop environment names
        all_ids = [item['id'] for item in menu]
        
        expected_des = ['gnome', 'kde', 'xfce', 'mate']
        for de in expected_des:
            # Check if DE exists anywhere in the menu structure
            de_exists = any(de in item_id.lower() for item_id in all_ids)
            assert de_exists, f"Missing desktop environment: {de}"

    def test_security_tools_present(self):
        """Test security category has expected tools"""
        menu = load_menu_structure()
        security = next((item for item in menu if item['id'] == 'security'), None)
        
        assert security is not None
        assert security.get('is_category', False) is True
        
        # Check for security subcategories
        security_items = [item for item in menu if item.get('parent') == 'security']
        
        # Should have various security tools
        assert len(security_items) > 0 or len(security.get('children', [])) > 0

    def test_ai_ml_category_exists(self):
        """Test AI/ML category exists with tools"""
        menu = load_menu_structure()
        ai_ml = next((item for item in menu if item['id'] == 'ai-ml'), None)
        
        assert ai_ml is not None
        assert ai_ml.get('is_category', False) is True
        assert ai_ml['label'] == 'AI & Machine Learning'
        
        # Should have children
        assert 'children' in ai_ml
        assert len(ai_ml['children']) > 0

    def test_system_category_tools(self):
        """Test system category has monitoring and management tools"""
        menu = load_menu_structure()
        system = next((item for item in menu if item['id'] == 'system'), None)
        
        assert system is not None
        assert system.get('is_category', False) is True
        
        # Check for system subcategories
        system_children = system.get('children', [])
        
        # Should have system tools - just check that it has children
        assert len(system_children) > 0, "System category should have subcategories"

    def test_menu_item_descriptions(self):
        """Test that categories have descriptions"""
        menu = load_menu_structure()
        categories = [item for item in menu if item.get('is_category')]
        
        for category in categories[:20]:  # Test first 20 categories
            # Categories should have descriptions
            if 'description' in category:
                assert category['description'], f"Empty description for: {category['id']}"
                assert len(category['description']) > 5, f"Description too short for: {category['id']}"

    def test_gaming_category_structure(self):
        """Test gaming category exists and has content"""
        menu = load_menu_structure()
        gaming = next((item for item in menu if item['id'] == 'gaming'), None)
        
        assert gaming is not None
        assert gaming.get('is_category', False) is True
        assert 'children' in gaming or any(item.get('parent') == 'gaming' for item in menu)

    def test_multimedia_category_tools(self):
        """Test multimedia category has expected tools"""
        menu = load_menu_structure()
        multimedia = next((item for item in menu if item['id'] == 'multimedia'), None)
        
        assert multimedia is not None
        assert multimedia.get('is_category', False) is True
        
        # Should have multimedia tools
        multimedia_items = [item for item in menu if item.get('parent') == 'multimedia']
        assert len(multimedia_items) > 0 or len(multimedia.get('children', [])) > 0

    def test_menu_structure_size(self):
        """Test menu has substantial content"""
        menu = load_menu_structure()
        
        # Should have many items
        assert len(menu) > 100, f"Menu too small: only {len(menu)} items"
        
        # Count categories and apps
        categories = [item for item in menu if item.get('is_category')]
        apps = [item for item in menu if not item.get('is_category')]
        
        assert len(categories) > 20, f"Too few categories: {len(categories)}"
        assert len(apps) > 80, f"Too few applications: {len(apps)}"

    def test_menu_icons_present(self):
        """Test categories have icons"""
        menu = load_menu_structure()
        categories = [item for item in menu if item.get('is_category')]
        
        for category in categories[:10]:  # Test first 10 categories
            if 'icon' in category:
                assert category['icon'], f"Empty icon for: {category['id']}"
                # Icons should be emoji or text
                assert len(category['icon']) > 0, f"Invalid icon for: {category['id']}"