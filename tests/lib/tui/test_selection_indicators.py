#!/usr/bin/env python3
"""Test subcategory selection indicators"""

from unittest.mock import MagicMock, patch

import pytest

from lib.tui.constants import INDICATOR_FULL, INDICATOR_NONE, INDICATOR_PARTIAL
from lib.tui.menu_items import load_menu_structure
from lib.tui.unified_menu import UnifiedMenu


class TestSelectionIndicators:
    """Test selection indicators for nested categories"""

    def test_subcategory_selection_indicators(self):
        """Test that parent categories show correct indicators when subcategories have selections"""
        # Load menu structure
        items = load_menu_structure()

        # Create a mock unified menu
        class MockUnifiedMenu(UnifiedMenu):
            def __init__(self):
                self.items = items
                self.selections = {}
                self.category_items = {}

                # Build category mappings
                for item in self.items:
                    if item.get("is_category"):
                        children = item.get("children", [])
                        if children:
                            self.category_items[item["id"]] = set(children)

        # Create menu instance
        menu = MockUnifiedMenu()

        # Test 1: Verify hierarchy is preserved
        print("Test 1: Checking hierarchy preservation...")

        # Check that Programming Languages has subcategories as children
        assert "dev-languages" in menu.category_items, "Programming Languages not in category_items"
        children = menu.category_items["dev-languages"]
        assert "dev-go" in children, "Go subcategory not found in Programming Languages children"
        assert "dev-python" in children, "Python subcategory not found in Programming Languages children"
        print("✓ Programming Languages has subcategory children")

        # Check that Go subcategory has items as children
        assert "dev-go" in menu.category_items, "Go not in category_items"
        go_children = menu.category_items["dev-go"]
        assert "go" in go_children, "go item not found in Go subcategory"
        assert "gofmt" in go_children, "gofmt item not found in Go subcategory"
        print("✓ Go subcategory has item children")

        # Test 2: Test selection indicators with partial selection
        print("\nTest 2: Testing partial selection indicators...")

        # Select some items in Go subcategory
        menu.selections["dev-go"] = {"go", "gofmt"}  # 2 out of 3 items

        # Check Go indicator (should be partial since not all items selected)
        go_indicator = menu.get_selection_indicator("dev-go", menu.selections.get("dev-go", set()))
        assert go_indicator == INDICATOR_PARTIAL, f"Expected {INDICATOR_PARTIAL} for Go, got {go_indicator}"
        print(f"✓ Go shows partial indicator with 2/3 items selected: {go_indicator}")

        # Check Programming Languages indicator (should be partial due to Go selections)
        prog_lang_indicator = menu.get_selection_indicator("dev-languages", menu.selections.get("dev-languages", set()))
        assert (
            prog_lang_indicator == INDICATOR_PARTIAL
        ), f"Expected {INDICATOR_PARTIAL} for Programming Languages, got {prog_lang_indicator}"
        print(f"✓ Programming Languages shows partial indicator when Go has selections: {prog_lang_indicator}")

        # Test 3: Test full selection indicators
        print("\nTest 3: Testing full selection indicators...")

        # Select all items in Go
        menu.selections["dev-go"] = {"go", "goland", "gofmt"}

        # Check Go indicator (should be full)
        go_indicator = menu.get_selection_indicator("dev-go", menu.selections.get("dev-go", set()))
        assert go_indicator == INDICATOR_FULL, f"Expected {INDICATOR_FULL} for Go, got {go_indicator}"
        print(f"✓ Go shows full indicator with all items selected: {go_indicator}")

        # Programming Languages should still be partial (other subcategories have no selections)
        prog_lang_indicator = menu.get_selection_indicator("dev-languages", menu.selections.get("dev-languages", set()))
        assert (
            prog_lang_indicator == INDICATOR_PARTIAL
        ), f"Expected {INDICATOR_PARTIAL} for Programming Languages, got {prog_lang_indicator}"
        print(f"✓ Programming Languages still shows partial (only Go fully selected): {prog_lang_indicator}")

        # Test 4: Test empty selection indicators
        print("\nTest 4: Testing empty selection indicators...")

        # Clear all selections
        menu.selections = {}

        # All indicators should be empty
        go_indicator = menu.get_selection_indicator("dev-go", set())
        assert go_indicator == INDICATOR_NONE, f"Expected {INDICATOR_NONE} for Go, got {go_indicator}"

        prog_lang_indicator = menu.get_selection_indicator("dev-languages", set())
        assert (
            prog_lang_indicator == INDICATOR_NONE
        ), f"Expected {INDICATOR_NONE} for Programming Languages, got {prog_lang_indicator}"
        print(f"✓ All indicators show empty with no selections")

        print("\n✅ All tests passed!")


if __name__ == "__main__":
    test = TestSelectionIndicators()
    test.test_subcategory_selection_indicators()
