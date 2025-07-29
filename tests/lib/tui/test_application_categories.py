#!/usr/bin/env python3
"""
Tests for application categories to ensure proper organization
"""

import unittest
from unittest.mock import MagicMock, Mock, patch
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Mock curses before importing
sys.modules['curses'] = MagicMock()
import curses

# Set up minimal curses constants
curses.A_REVERSE = 262144
curses.error = Exception


class TestApplicationCategories(unittest.TestCase):
    """Test application categorization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        
        # Import after mocking
        from lib.tui.unified_menu import UnifiedMenu
        from lib.tui.menu_items import load_menu_structure
        self.UnifiedMenu = UnifiedMenu
        self.load_menu_structure = load_menu_structure
        
    def test_has_required_application_categories(self):
        """Test that all required application categories exist"""
        required_categories = [
            'graphics-media',
            'productivity-office', 
            'communication',
            'audio-music',
            'video-streaming',
            'security-tools',
            'text-editors-ides',
            'web-browsers',
            'file-management',
            'system-tools'
        ]
        
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        root_categories = [item['id'] for item in menu.items if item.get('parent') is None]
        
        for cat in required_categories:
            self.assertIn(cat, root_categories, f"Missing category: {cat}")
    
    def test_old_applications_category_renamed(self):
        """Test that old 'applications' category is renamed to general-apps"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Old applications category should be renamed
        old_apps = next((item for item in menu.items if item['id'] == 'applications'), None)
        if old_apps:
            # If it exists, it should be renamed to indicate it's for general/misc apps
            self.assertEqual(old_apps['label'], 'General Applications')
            self.assertIn('miscellaneous', old_apps['description'].lower())
    
    def test_applications_properly_categorized(self):
        """Test that applications are in appropriate categories"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Check GIMP is under graphics-media
        gimp = next((item for item in menu.items if item['id'] == 'gimp'), None)
        self.assertIsNotNone(gimp, "GIMP not found in menu")
        self.assertEqual(gimp['parent'], 'graphics-media')
        
        # Check VS Code is under text-editors-ides
        vscode = next((item for item in menu.items if item['id'] == 'vscode'), None)
        self.assertIsNotNone(vscode, "VS Code not found in menu")
        self.assertEqual(vscode['parent'], 'text-editors-ides')
        
        # Check Firefox is under web-browsers
        firefox = next((item for item in menu.items if item['id'] == 'firefox'), None)
        self.assertIsNotNone(firefox, "Firefox not found in menu")
        self.assertEqual(firefox['parent'], 'web-browsers')
        
        # Check Slack is under communication
        slack = next((item for item in menu.items if item['id'] == 'slack'), None)
        self.assertIsNotNone(slack, "Slack not found in menu")
        self.assertEqual(slack['parent'], 'communication')
        
    def test_category_descriptions(self):
        """Test that categories have appropriate descriptions"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Check graphics-media category
        graphics = next((item for item in menu.items if item['id'] == 'graphics-media'), None)
        self.assertIsNotNone(graphics)
        self.assertIn('graphics', graphics['description'].lower())
        self.assertIn('media', graphics['description'].lower())
        
    def test_category_icons(self):
        """Test that categories have appropriate icons"""
        expected_icons = {
            'graphics-media': '🖼️',
            'productivity-office': '💼',
            'communication': '💬',
            'audio-music': '🎵',
            'video-streaming': '🎥',
            'security-tools': '🛡️',
            'text-editors-ides': '📝',
            'web-browsers': '🌐',
            'file-management': '📁',
            'system-tools': '🔧'
        }
        
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        for cat_id, expected_icon in expected_icons.items():
            cat = next((item for item in menu.items if item['id'] == cat_id), None)
            if cat:  # Only check if category exists
                self.assertEqual(cat.get('icon'), expected_icon, 
                    f"Category {cat_id} has wrong icon")
    
    def test_minimum_applications_per_category(self):
        """Test that each category has at least some applications"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Categories that should have applications
        app_categories = [
            'graphics-media',
            'productivity-office',
            'communication',
            'audio-music',
            'video-streaming',
            'text-editors-ides',
            'web-browsers',
            'system-tools'
        ]
        
        for cat_id in app_categories:
            # Count items with this category as parent
            items = [item for item in menu.items if item.get('parent') == cat_id]
            self.assertGreater(len(items), 0, 
                f"Category {cat_id} has no applications")
    
    def test_no_duplicate_applications(self):
        """Test that applications aren't duplicated across categories"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()
        
        # Get all non-category items
        apps = [item for item in menu.items if not item.get('is_category')]
        
        # Check for duplicates
        app_ids = [app['id'] for app in apps]
        self.assertEqual(len(app_ids), len(set(app_ids)), 
            "Duplicate application IDs found")


if __name__ == '__main__':
    unittest.main()