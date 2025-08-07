#!/usr/bin/env python3
"""
Unified Menu Dialog Component for Ubootu
Provides consistent arrow-key navigation across all menus
"""

import curses
from typing import Callable, List, Optional, Tuple


class KeyHintBar:
    """Simple key hint bar for displaying keyboard shortcuts"""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
    
    def draw(self, hints, y):
        """Draw key hints at specified y position"""
        try:
            hint_str = "  ".join([f"{key}:{desc}" for key, desc in hints])
            if len(hint_str) > self.width - 2:
                hint_str = hint_str[:self.width - 5] + "..."
            x = max(0, (self.width - len(hint_str)) // 2)
            self.stdscr.addstr(y, x, hint_str, curses.A_DIM)
        except curses.error:
            pass


class HelpOverlay:
    """Simple help overlay for displaying help text"""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
    
    def show(self, title, content):
        """Show help overlay with title and content lines"""
        self.stdscr.clear()
        
        # Draw title
        try:
            self.stdscr.addstr(1, (self.width - len(title)) // 2, title, curses.A_BOLD)
        except curses.error:
            pass
        
        # Draw content
        y = 3
        for line in content:
            if y >= self.height - 2:
                break
            try:
                self.stdscr.addstr(y, 2, line[:self.width - 4])
            except curses.error:
                pass
            y += 1
        
        # Draw "Press any key to continue"
        try:
            msg = "Press any key to continue"
            self.stdscr.addstr(self.height - 2, (self.width - len(msg)) // 2, msg, curses.A_DIM)
        except curses.error:
            pass
        
        self.stdscr.refresh()
        self.stdscr.getch()


class MenuDialog:
    """Unified menu dialog with arrow key navigation"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.key_hints = KeyHintBar(stdscr)
        self.help_overlay = HelpOverlay(stdscr)
        curses.curs_set(0)  # Hide cursor

    def draw_box(self, y, x, h, w, title=""):
        """Draw a box with optional title"""
        try:
            # Draw corners
            self.stdscr.addch(y, x, curses.ACS_ULCORNER)
            self.stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
            self.stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
            self.stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)

            # Draw horizontal lines
            for i in range(1, w - 1):
                self.stdscr.addch(y, x + i, curses.ACS_HLINE)
                self.stdscr.addch(y + h - 1, x + i, curses.ACS_HLINE)

            # Draw vertical lines
            for i in range(1, h - 1):
                self.stdscr.addch(y + i, x, curses.ACS_VLINE)
                self.stdscr.addch(y + i, x + w - 1, curses.ACS_VLINE)

            # Draw title if provided
            if title:
                title = f" {title} "
                title_x = x + (w - len(title)) // 2
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(y, title_x, title)
                self.stdscr.attroff(curses.A_BOLD)

        except curses.error:
            pass

    def draw_centered_text(self, y, text, attrs=0):
        """Draw centered text at given y position"""
        try:
            x = max(0, (self.width - len(text)) // 2)
            if y >= 0 and y < self.height and x < self.width:
                self.stdscr.addstr(y, x, text[: self.width - x], attrs)
        except curses.error:
            pass

    def draw_left_aligned_block(self, y, text, center_x, attrs=0):
        """Draw left-aligned text within a centered block"""
        try:
            if y >= 0 and y < self.height and center_x < self.width:
                self.stdscr.addstr(y, center_x, text[: self.width - center_x], attrs)
        except curses.error:
            pass

    def show(
        self,
        title: str,
        items: List[Tuple[str, str, str]],  # (id, icon+name, description)
        header_lines: List[str] = None,
        footer_lines: List[str] = None,
        box_mode: bool = True,
        allow_help: bool = True,
        on_select: Callable = None,
    ) -> Optional[str]:
        """
        Show menu with arrow key navigation

        Args:
            title: Menu title
            items: List of (id, display_name_with_icon, description) tuples
            header_lines: Optional header lines to display above menu
            footer_lines: Optional footer lines to display below menu
            box_mode: Whether to draw a box around the menu
            allow_help: Whether to show help option
            on_select: Optional callback for instant selection feedback

        Returns:
            Selected item ID or None if cancelled
        """
        current = 0
        scroll_offset = 0

        # Calculate dimensions
        if box_mode:
            menu_width = min(80, self.width - 4)
            menu_height = min(24, self.height - 4)
            menu_y = (self.height - menu_height) // 2
            menu_x = (self.width - menu_width) // 2

            # Calculate content area
            content_start_y = menu_y + 2
            if header_lines:
                content_start_y += len(header_lines) + 1

            footer_space = 2  # For key hints
            if footer_lines:
                footer_space += len(footer_lines) + 1

            list_height = menu_height - (content_start_y - menu_y) - footer_space
        else:
            # Full screen mode
            menu_width = self.width
            menu_height = self.height
            menu_y = 0
            menu_x = 0

            content_start_y = 1
            if header_lines:
                content_start_y += len(header_lines) + 1

            list_height = self.height - content_start_y - 3  # Leave room for key hints

        # Find longest item for proper alignment
        max_item_width = max(len(item[1]) for item in items) if items else 0

        while True:
            self.stdscr.clear()

            # Draw box if in box mode
            if box_mode:
                self.draw_box(menu_y, menu_x, menu_height, menu_width, title)
            else:
                # Just draw title at top
                self.draw_centered_text(0, title, curses.A_BOLD)

            # Draw header lines
            if header_lines:
                y = menu_y + 1 if box_mode else 1
                for line in header_lines:
                    self.draw_centered_text(y, line)
                    y += 1

            # Draw menu items
            visible_items = items[scroll_offset : scroll_offset + list_height]

            # Calculate x position for centered block of left-aligned items
            if box_mode:
                item_x = menu_x + (menu_width - max_item_width) // 2
            else:
                item_x = (self.width - max_item_width) // 2

            for i, (item_id, display_name, description) in enumerate(visible_items):
                y = content_start_y + i

                # Highlight current selection
                attrs = curses.A_REVERSE if i + scroll_offset == current else 0

                # Draw the menu item
                self.draw_left_aligned_block(y, display_name, item_x, attrs)

            # Draw scroll indicators
            if scroll_offset > 0:
                indicator_x = item_x + max_item_width + 2
                self.stdscr.addstr(content_start_y - 1, indicator_x, "↑", curses.A_BOLD)
            if scroll_offset + list_height < len(items):
                indicator_x = item_x + max_item_width + 2
                self.stdscr.addstr(content_start_y + list_height, indicator_x, "↓", curses.A_BOLD)

            # Draw footer lines
            if footer_lines:
                y = content_start_y + list_height + 1
                for line in footer_lines:
                    self.draw_centered_text(y, line)
                    y += 1

            # Draw key hints at bottom - H=Help first for visibility
            hints = [("H", "Help")] if allow_help else []
            hints.extend([("↑↓", "Navigate"), ("ENTER", "Select"), ("ESC", "Exit")])
            self.key_hints.draw(hints, self.height - 1)

            # Draw current selection description at bottom if available
            if items and items[current][2]:
                desc_y = self.height - 2
                desc_text = items[current][2]
                max_desc_width = self.width - 4
                if len(desc_text) > max_desc_width:
                    desc_text = desc_text[: max_desc_width - 3] + "..."
                self.draw_centered_text(desc_y, desc_text, curses.A_DIM)

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == 27:  # ESC
                return None
            elif key in [ord("q"), ord("Q")]:  # Q also exits
                return None
            elif key in [ord("h"), ord("H")] and allow_help:  # Help
                help_content = [
                    "Menu Navigation Help",
                    "Use arrow keys to navigate through menu options.",
                    "Controls:",
                    "• ↑ UP ARROW - Move to previous option",
                    "• ↓ DOWN ARROW - Move to next option",
                    "• ENTER - Select highlighted option",
                    "• ESC or Q - Exit menu",
                    "• H - Show this help",
                    "The highlighted option is shown in reverse colors.",
                    "If there are more items than can fit on screen,",
                    "scroll indicators (↑↓) will appear.",
                ]
                self.help_overlay.show("Menu Help", help_content)
            elif key == ord("\n"):  # Enter
                if items:
                    return items[current][0]
            elif key == curses.KEY_UP:
                if current > 0:
                    current -= 1
                    if current < scroll_offset:
                        scroll_offset = current
                    if on_select:
                        on_select(items[current][0])
            elif key == curses.KEY_DOWN:
                if current < len(items) - 1:
                    current += 1
                    if current >= scroll_offset + list_height:
                        scroll_offset = current - list_height + 1
                    if on_select:
                        on_select(items[current][0])
            elif key >= ord("1") and key <= ord("9"):
                # Still support number keys for compatibility
                num = key - ord("0")
                if num <= len(items):
                    return items[num - 1][0]


class QuickMenu:
    """Quick menu for simple selections without box"""

    def __init__(self, stdscr):
        self.menu = MenuDialog(stdscr)

    def show(self, title: str, options: List[Tuple[str, str]]) -> Optional[str]:
        """
        Show a quick menu with minimal UI

        Args:
            title: Menu title
            options: List of (id, display_text) tuples

        Returns:
            Selected option ID or None
        """
        # Convert to full format with empty descriptions
        items = [(opt[0], opt[1], "") for opt in options]

        return self.menu.show(title=title, items=items, box_mode=False, allow_help=False)
