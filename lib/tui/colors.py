"""
Color Management Module for Ubootu TUI
Defines and initializes the vibrant color scheme
"""

import curses

# NO COLORS - All color pairs return 0 (no color)
COLOR_HEADER = 0
COLOR_SELECTED = 0
COLOR_ITEM_SELECTED = 0
COLOR_CATEGORY_FULL = 0
COLOR_F_KEY_BAR = 0
COLOR_INFO = 0
COLOR_BREADCRUMB = 0
COLOR_CATEGORY_PARTIAL = 0
COLOR_CATEGORY_EMPTY = 0
COLOR_HELP_BAR = 0
COLOR_SAVE_BUTTON = 0
COLOR_ACTION_POPUP = 0
COLOR_ACTION_SELECTED = 0


def init_colors():
    """NO COLORS - Monochrome interface only"""
    # All text will be default terminal colors
    # Selected items will use reverse video
    return False


def get_category_color(status: str) -> int:
    """Get color pair for category based on selection status"""
    # NO COLORS - return 0 for all categories
    return 0
