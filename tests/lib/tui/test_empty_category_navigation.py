#!/usr/bin/env python3
"""Test navigation in empty categories"""

import pytest
from unittest.mock import MagicMock, patch
import curses

# Mock curses module
import sys
sys.modules['curses'] = MagicMock()

# Set up curses constants
curses.KEY_LEFT = 260
curses.KEY_RIGHT = 261
curses.KEY_UP = 259
curses.KEY_DOWN = 258


@pytest.fixture
def mock_menu():
    """Create a mock menu instance with empty categories"""
    from lib.tui.unified_menu import UnifiedMenu
    
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)
    
    menu = UnifiedMenu(stdscr)
    
    # Mock menu items with some empty categories
    menu.items = [
        {'id': 'empty-cat', 'label': 'Empty Category', 'is_category': True, 'parent': None},
        {'id': 'normal-cat', 'label': 'Normal Category', 'is_category': True, 'parent': None},
        {'id': 'item1', 'label': 'Item 1', 'parent': 'normal-cat', 'is_category': False},
    ]
    
    menu.category_items = {
        'normal-cat': {'item1'},
        # empty-cat has no items
    }
    
    return menu


def test_navigation_in_empty_category(mock_menu):
    """Test that back navigation works even in empty categories"""
    # Enter empty category
    mock_menu.enter_submenu('empty-cat')
    assert mock_menu.current_menu == 'empty-cat'
    assert mock_menu.menu_stack == ['root']
    
    # Try to navigate back with left arrow
    action = mock_menu.navigate(260)  # curses.KEY_LEFT
    assert action == 'back'
    assert mock_menu.current_menu == 'root'
    assert mock_menu.menu_stack == []


def test_navigation_in_normal_category(mock_menu):
    """Test that back navigation works in categories with items"""
    # Enter normal category
    mock_menu.enter_submenu('normal-cat')
    assert mock_menu.current_menu == 'normal-cat'
    assert mock_menu.menu_stack == ['root']
    
    # Try to navigate back with left arrow
    action = mock_menu.navigate(260)  # curses.KEY_LEFT
    assert action == 'back'
    assert mock_menu.current_menu == 'root'
    assert mock_menu.menu_stack == []


def test_all_back_keys_in_empty_category(mock_menu):
    """Test all back navigation keys work in empty categories"""
    back_keys = [
        260,       # curses.KEY_LEFT
        27,        # ESC
        ord('h'),  # h key
    ]
    
    for key in back_keys:
        # Reset state
        mock_menu.current_menu = 'root'
        mock_menu.menu_stack = []
        
        # Enter empty category
        mock_menu.enter_submenu('empty-cat')
        
        # Try to navigate back
        action = mock_menu.navigate(key)
        assert action == 'back', f"Key {key} should trigger back action in empty category"
        assert mock_menu.current_menu == 'root', f"Key {key} should return to root menu"


def test_main_menu_key_in_empty_category(mock_menu):
    """Test main menu key works in empty categories"""
    # Enter empty category
    mock_menu.enter_submenu('empty-cat')
    
    # Press M for main menu
    action = mock_menu.navigate(ord('m'))
    assert action == 'main_menu'
    
    # Also test uppercase M
    mock_menu.enter_submenu('empty-cat')
    action = mock_menu.navigate(ord('M'))
    assert action == 'main_menu'


def test_navigation_keys_in_empty_category(mock_menu):
    """Test that up/down navigation doesn't crash in empty categories"""
    # Enter empty category
    mock_menu.enter_submenu('empty-cat')
    
    # Try up/down navigation (should do nothing but not crash)
    action = mock_menu.navigate(259)  # curses.KEY_UP
    # Should return None or 'navigate' but not crash
    assert action in [None, 'navigate']
    
    action = mock_menu.navigate(258)  # curses.KEY_DOWN
    assert action in [None, 'navigate']