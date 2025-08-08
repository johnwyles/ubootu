#!/usr/bin/env python3
"""Tests for lib/tui/constants.py"""

import pytest

from lib.tui.constants import (
    CHECKBOX_SELECTED,
    CHECKBOX_UNSELECTED,
    DIALOG_HEIGHT,
    DIALOG_WIDTH,
    HELP_BAR,
    HELP_BAR_SUBMENU,
    INDICATOR_FULL,
    INDICATOR_NONE,
    INDICATOR_PARTIAL,
    KEY_BINDINGS,
    MENU_CATEGORIES,
    MIN_HEIGHT,
    MIN_WIDTH,
    SUBTITLE,
    SUDO_DIALOG_HEIGHT,
    SUDO_DIALOG_WIDTH,
    TITLE,
)


class TestIndicators:
    """Test selection indicator constants"""

    def test_indicator_values(self):
        """Test that indicator constants have expected values"""
        assert INDICATOR_NONE == "○"
        assert INDICATOR_PARTIAL == "◐"
        assert INDICATOR_FULL == "●"

    def test_checkbox_values(self):
        """Test checkbox constants"""
        assert CHECKBOX_SELECTED == "[X]"
        assert CHECKBOX_UNSELECTED == "[ ]"

    def test_indicators_are_distinct(self):
        """Test that all indicators are unique"""
        indicators = [
            INDICATOR_NONE,
            INDICATOR_PARTIAL,
            INDICATOR_FULL,
            CHECKBOX_SELECTED,
            CHECKBOX_UNSELECTED,
        ]
        assert len(indicators) == len(set(indicators))


class TestKeyBindings:
    """Test key binding definitions"""

    def test_key_bindings_structure(self):
        """Test that KEY_BINDINGS is properly structured"""
        assert isinstance(KEY_BINDINGS, dict)
        assert len(KEY_BINDINGS) > 0

    def test_required_key_bindings_exist(self):
        """Test that all required key bindings are defined"""
        required_bindings = [
            "navigate_up",
            "navigate_down",
            "navigate_left",
            "navigate_right",
            "select",
            "enter",
            "back",
            "quit",
            "help",
            "save",
            "apply",
            "search",
            "select_all",
            "deselect_all",
            "main_menu",
        ]
        for binding in required_bindings:
            assert binding in KEY_BINDINGS
            assert isinstance(KEY_BINDINGS[binding], list)
            assert len(KEY_BINDINGS[binding]) > 0

    def test_key_bindings_values_are_lists(self):
        """Test that all key binding values are lists"""
        for key, value in KEY_BINDINGS.items():
            assert isinstance(value, list), f"KEY_BINDINGS['{key}'] should be a list"
            assert len(value) > 0, f"KEY_BINDINGS['{key}'] should not be empty"

    def test_navigation_keys(self):
        """Test navigation key bindings"""
        assert "KEY_UP" in KEY_BINDINGS["navigate_up"]
        assert "k" in KEY_BINDINGS["navigate_up"]
        assert "KEY_DOWN" in KEY_BINDINGS["navigate_down"]
        assert "j" in KEY_BINDINGS["navigate_down"]
        assert "KEY_LEFT" in KEY_BINDINGS["navigate_left"]
        assert "h" in KEY_BINDINGS["navigate_left"]
        assert "KEY_RIGHT" in KEY_BINDINGS["navigate_right"]
        assert "l" in KEY_BINDINGS["navigate_right"]

    def test_action_keys(self):
        """Test action key bindings"""
        assert " " in KEY_BINDINGS["select"]
        assert "\n" in KEY_BINDINGS["enter"]
        assert "q" in KEY_BINDINGS["quit"]
        assert "Q" in KEY_BINDINGS["quit"]
        assert "s" in KEY_BINDINGS["save"]
        assert "S" in KEY_BINDINGS["save"]


class TestUIText:
    """Test UI text constants"""

    def test_title_and_subtitle(self):
        """Test title and subtitle constants"""
        assert TITLE == "🚀 Ubootu Configuration"
        assert SUBTITLE == "Professional Ubuntu Desktop Configuration Tool"
        assert len(TITLE) > 0
        assert len(SUBTITLE) > 0

    def test_help_bar_text(self):
        """Test help bar text constants"""
        assert isinstance(HELP_BAR, str)
        assert isinstance(HELP_BAR_SUBMENU, str)
        assert len(HELP_BAR) > 0
        assert len(HELP_BAR_SUBMENU) > 0

    def test_help_bar_contains_key_hints(self):
        """Test that help bars contain key hints"""
        # Main help bar should have common keys
        assert "Nav" in HELP_BAR
        assert "Select" in HELP_BAR
        assert "Save" in HELP_BAR
        assert "Quit" in HELP_BAR

        # Submenu help bar should have All/None
        assert "All/None" in HELP_BAR_SUBMENU


class TestDimensions:
    """Test dimension constants"""

    def test_minimum_terminal_size(self):
        """Test minimum terminal size constants"""
        assert MIN_WIDTH == 80
        assert MIN_HEIGHT == 24
        assert MIN_WIDTH > 0
        assert MIN_HEIGHT > 0

    def test_dialog_dimensions(self):
        """Test dialog dimension constants"""
        assert DIALOG_WIDTH == 60
        assert DIALOG_HEIGHT == 10
        assert SUDO_DIALOG_WIDTH == 50
        assert SUDO_DIALOG_HEIGHT == 7

    def test_dialog_dimensions_reasonable(self):
        """Test that dialog dimensions are reasonable"""
        assert DIALOG_WIDTH < MIN_WIDTH
        assert DIALOG_HEIGHT < MIN_HEIGHT
        assert SUDO_DIALOG_WIDTH < MIN_WIDTH
        assert SUDO_DIALOG_HEIGHT < MIN_HEIGHT


class TestMenuCategories:
    """Test menu category definitions"""

    def test_menu_categories_structure(self):
        """Test that MENU_CATEGORIES is properly structured"""
        assert isinstance(MENU_CATEGORIES, list)
        assert len(MENU_CATEGORIES) == 6

    def test_menu_category_required_fields(self):
        """Test that each menu category has required fields"""
        for category in MENU_CATEGORIES:
            assert isinstance(category, dict)
            assert "id" in category
            assert "label" in category
            assert "description" in category
            assert "icon" in category

    def test_menu_category_ids(self):
        """Test specific menu category IDs"""
        category_ids = [cat["id"] for cat in MENU_CATEGORIES]
        expected_ids = [
            "development",
            "ai-ml",
            "desktop",
            "applications",
            "security",
            "system",
        ]
        assert category_ids == expected_ids

    def test_menu_category_unique_ids(self):
        """Test that all menu category IDs are unique"""
        category_ids = [cat["id"] for cat in MENU_CATEGORIES]
        assert len(category_ids) == len(set(category_ids))

    def test_menu_category_labels(self):
        """Test menu category labels"""
        labels = {cat["id"]: cat["label"] for cat in MENU_CATEGORIES}
        assert labels["development"] == "Development Tools"
        assert labels["ai-ml"] == "AI & Machine Learning"
        assert labels["desktop"] == "Desktop Environment"
        assert labels["applications"] == "Applications"
        assert labels["security"] == "Security & Privacy"
        assert labels["system"] == "System Configuration"

    def test_menu_category_icons(self):
        """Test that menu categories have emoji icons"""
        for category in MENU_CATEGORIES:
            assert len(category["icon"]) > 0
            # Basic check that it's likely an emoji (non-ASCII)
            assert ord(category["icon"][0]) > 127

    def test_menu_category_descriptions(self):
        """Test that menu categories have descriptions"""
        for category in MENU_CATEGORIES:
            assert len(category["description"]) > 0
            assert isinstance(category["description"], str)
