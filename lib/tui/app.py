"""
Main Ubootu TUI Application
Coordinates all modules to provide the terminal user interface
"""

import curses
from typing import Dict, List, Set

from lib.tui.colors import init_colors
from lib.tui.menu_structure import MenuItem, build_menu_structure


class UbootuTUI:
    """Main TUI application class"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu_items = build_menu_structure()
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.selected_items: Set[str] = set()
        self.breadcrumb_stack = []
        self.cancelled = False

        # Initialize curses
        self._init_curses()

        # Apply defaults
        self._apply_defaults()

    def _init_curses(self):
        """Initialize curses settings"""
        # Get terminal dimensions
        height, width = self.stdscr.getmaxyx()
        if height < 24 or width < 80:
            # Terminal too small, but continue anyway
            pass

        # Initialize colors
        init_colors()

        # Setup screen
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
            self.stdscr.timeout(50)  # Reduced timeout for better responsiveness
        except:
            # Some terminals don't support all features
            pass

    def _apply_defaults(self):
        """Apply default selections"""
        for item in self.menu_items.values():
            if item.default:
                item.selected = True
                self.selected_items.add(item.id)

    def get_current_menu_items(self) -> List[MenuItem]:
        """Get items for current menu level"""
        current = self.menu_items[self.current_menu]
        if current.children:
            return [self.menu_items[child_id] for child_id in current.children]
        return []

    def get_category_selection_status(self, category_id: str) -> str:
        """Get selection status for a category: 'full', 'partial', 'empty'"""
        if category_id not in self.menu_items:
            return "empty"

        # Get all selectable items in this category (recursively)
        selectable_items = self._get_all_selectable_items(category_id)

        if not selectable_items:
            return "empty"

        selected_count = sum(
            1 for item_id in selectable_items if item_id in self.selected_items
        )

        if selected_count == 0:
            return "empty"
        elif selected_count == len(selectable_items):
            return "full"
        else:
            return "partial"

    def _get_all_selectable_items(self, category_id: str) -> List[str]:
        """Get all selectable items in a category (recursively)"""
        items = []
        category = self.menu_items.get(category_id)

        if not category or not category.children:
            return items

        for child_id in category.children:
            child = self.menu_items.get(child_id)
            if not child:
                continue

            if child.is_category:
                # Recursively get items from subcategories
                items.extend(self._get_all_selectable_items(child_id))
            else:
                # This is a selectable item
                items.append(child_id)

        return items

    def run(self) -> int:
        """Main TUI loop - simplified for now"""
        try:
            # For now, just display a message
            # The full implementation would use the renderer, input handler, etc.
            self.stdscr.clear()
            self.stdscr.addstr(10, 20, "Ubootu TUI - Modular Version")
            self.stdscr.addstr(12, 15, "Press any key to exit...")
            self.stdscr.refresh()
            self.stdscr.getch()

            return 0
        except KeyboardInterrupt:
            self.cancelled = True
            return 1
        except Exception:
            self.cancelled = True
            return 1
