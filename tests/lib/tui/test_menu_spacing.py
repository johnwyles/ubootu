#!/usr/bin/env python3
"""
Tests for menu item spacing to ensure no double spaces between emojis and text
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

# Mock curses before importing
sys.modules["curses"] = MagicMock()
import curses

# Set up minimal curses constants
curses.A_REVERSE = 262144
curses.error = Exception


class TestMenuSpacing(unittest.TestCase):
    """Test menu item spacing and formatting"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        # Import after mocking
        from lib.tui.menu_items import load_menu_structure
        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu
        self.load_menu_structure = load_menu_structure

    def test_no_double_spaces_in_menu_items(self):
        """Test that menu items don't have double spaces between emoji and text"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        # Mock rendering to check for double spaces
        rendered_items = []

        def mock_addstr(y, x, text, *args):
            rendered_items.append(text)

        self.stdscr.addstr = mock_addstr

        # Render each category
        for item in menu.items:
            if item.get("is_category") and item.get("parent") is None:
                menu.render_menu_item(5, item, False)

        # Check for double spaces in rendered text
        for text in rendered_items:
            # Remove leading/trailing spaces for this check
            text = text.strip()
            self.assertNotIn("  ", text, f"Double space found in rendered text: '{text}'")

    def test_icon_fields_have_no_trailing_spaces(self):
        """Test that icon fields don't have trailing spaces"""
        items = self.load_menu_structure()

        for item in items:
            if "icon" in item:
                self.assertFalse(
                    item["icon"].endswith(" "), f"Icon for {item['id']} has trailing space: '{item['icon']}'"
                )

    def test_consistent_spacing_after_emoji(self):
        """Test that all emojis have consistent spacing"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        # Check the actual rendering format
        for item in menu.items:
            if item.get("is_category"):
                icon = item.get("icon", "")
                label = item["label"]

                # Simulate how it's rendered in unified_menu.py
                indicator = "○"  # Default empty indicator
                rendered = f"{indicator} {icon} {label}"  # Note the space after icon

                # Should not have double spaces
                self.assertNotIn("  ", rendered, f"Double space found in: '{rendered}'")

    def test_menu_item_rendering_format(self):
        """Test the actual menu item rendering format"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.items = [
            {
                "id": "test-cat",
                "label": "Test Category",
                "icon": "🔧",  # No trailing space
                "is_category": True,
                "parent": None,
                "children": [],
            }
        ]

        # Mock addstr to capture output
        captured = []
        self.stdscr.addstr = lambda y, x, text, *args: captured.append(text)

        # Render the item
        menu.render_menu_item(5, menu.items[0], False)

        # Check the rendered text
        self.assertEqual(len(captured), 1)
        text = captured[0].strip()

        # Should be: "○ 🔧 Test Category" (single space after emoji)
        self.assertEqual(text, "○ 🔧 Test Category")
        self.assertNotIn("  ", text)  # No double spaces

    def test_all_category_icons_consistent(self):
        """Test that all category icons follow the same format"""
        items = self.load_menu_structure()

        categories = [item for item in items if item.get("is_category")]

        for cat in categories:
            if "icon" in cat:
                icon = cat["icon"]
                # Icon should be just the emoji, no spaces
                self.assertFalse(icon.startswith(" "), f"Icon for {cat['id']} starts with space")
                self.assertFalse(icon.endswith(" "), f"Icon for {cat['id']} ends with space")

                # Icon should be 1-2 characters (emoji can be multi-byte)
                self.assertLessEqual(len(icon), 4, f"Icon for {cat['id']} seems too long: '{icon}'")


if __name__ == "__main__":
    unittest.main()
