#!/usr/bin/env python3
"""
Curses-based help viewer for Ubootu
Shows comprehensive help documentation
"""

import curses
from typing import Dict, List, Optional

from .constants import *
from .utils import *


class HelpViewer:
    """Display help documentation"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_section = 0
        self.scroll_offset = 0

        # Define help sections
        self.sections = [
            {
                "title": "Getting Started",
                "content": [
                    "Welcome to Ubootu!",
                    "",
                    "Ubootu is a professional Ubuntu desktop and server configuration tool",
                    "that helps you set up your system with all the tools you need.",
                    "",
                    "Quick Start:",
                    "1. Choose 'Fresh Install' for a new Ubuntu system",
                    "2. Select the tools and applications you want",
                    "3. Configure any settings (like swappiness)",
                    "4. Apply the configuration",
                    "",
                    "Your selections are automatically saved to config.yml",
                ],
            },
            {
                "title": "Navigation",
                "content": [
                    "Keyboard Shortcuts:",
                    "",
                    "↑/↓ or j/k     - Navigate up/down",
                    "←/→ or h/l     - Go back / Enter submenu",
                    "Space          - Select/deselect item",
                    "Enter          - Select item or enter submenu",
                    "a              - Select all (in submenu)",
                    "d              - Deselect all (in submenu)",
                    "s              - Save configuration",
                    "A              - Apply configuration",
                    "ESC or ←       - Go back",
                    "M              - Return to main menu",
                    "q/Q            - Quit",
                    "F1 or ?        - Show help",
                ],
            },
            {
                "title": "Menu Options",
                "content": [
                    "Fresh Install:",
                    "  Complete configuration for a new Ubuntu installation",
                    "  Includes all categories and options",
                    "",
                    "Modify Setup:",
                    "  Modify your existing configuration",
                    "  Loads your previous selections",
                    "",
                    "Apply Profile:",
                    "  Restore from a saved configuration profile",
                    "  Useful for replicating setups across machines",
                    "",
                    "Backup Config:",
                    "  Save current configuration as a named profile",
                    "  Profiles are stored in the 'profiles' directory",
                    "",
                    "View History:",
                    "  View installation logs and history",
                    "  Check for errors in previous runs",
                    "",
                    "Quick Actions:",
                    "  Common system maintenance tasks",
                    "  Update system, clean packages, etc.",
                ],
            },
            {
                "title": "Selection Indicators",
                "content": [
                    "Understanding Selection Indicators:",
                    "",
                    "For Categories:",
                    "  ○ = No items selected",
                    "  ◐ = Some items selected",
                    "  ● = All items selected",
                    "",
                    "For Items:",
                    "  [ ] = Not selected",
                    "  [X] = Selected",
                    "",
                    "Configurable Items:",
                    "  Items with configurable values show current value",
                    "  Press Space or Enter to configure",
                    "",
                    "Note: Categories themselves cannot be selected,",
                    "only the items within them.",
                ],
            },
            {
                "title": "Configuration",
                "content": [
                    "Configuration Files:",
                    "",
                    "config.yml:",
                    "  Your current configuration",
                    "  Automatically saved when you make changes",
                    "  Contains selected items and configured values",
                    "",
                    "profiles/*.yml:",
                    "  Saved configuration profiles",
                    "  Created using 'Backup Config'",
                    "  Can be applied using 'Apply Profile'",
                    "",
                    "Ansible Integration:",
                    "  Ubootu uses Ansible for installation",
                    "  Playbooks are in the 'roles' directory",
                    "  Logs are saved in '.ansible/logs'",
                    "",
                    "Prerequisites:",
                    "  Python 3.8+, Ansible, and YAML support",
                    "  Automatically installed on first run",
                ],
            },
            {
                "title": "Troubleshooting",
                "content": [
                    "Common Issues:",
                    "",
                    "Terminal too small:",
                    "  Minimum size: 80x24",
                    "  Resize your terminal window",
                    "",
                    "Installation fails:",
                    "  Check logs in '.ansible/logs'",
                    "  Ensure you have sudo access",
                    "  Check internet connection",
                    "",
                    "Selections not saving:",
                    "  Check write permissions",
                    "  Ensure config.yml is writable",
                    "",
                    "Ansible not found:",
                    "  Prerequisites will be installed automatically",
                    "  Or run: sudo apt install ansible",
                    "",
                    "For more help:",
                    "  Check the README.md file",
                    "  View logs in '.ansible/logs'",
                    "  Report issues on GitHub",
                ],
            },
        ]

        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
        except:
            pass

    def render(self) -> None:
        """Render the help viewer"""
        self.stdscr.clear()

        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return

        # Draw header
        self.render_header()

        # Draw section tabs
        self.render_tabs()

        # Draw content
        self.render_content()

        # Draw help bar
        self.render_help_bar()

        self.stdscr.refresh()

    def render_size_error(self) -> None:
        """Render terminal size error"""
        msg = f"Terminal too small! Minimum {MIN_WIDTH}x{MIN_HEIGHT}"
        draw_centered_text(self.stdscr, self.height // 2, msg, bold=True)

    def render_header(self) -> None:
        """Render the header"""
        draw_box(self.stdscr, 0, 0, 3, self.width)
        draw_centered_text(self.stdscr, 1, "❓ Ubootu Help", bold=True)

    def render_tabs(self) -> None:
        """Render section tabs"""
        y = 3
        tab_width = self.width // len(self.sections)

        for i, section in enumerate(self.sections):
            x = i * tab_width
            title = truncate_text(section["title"], tab_width - 2)

            try:
                if i == self.current_section:
                    self.stdscr.attron(curses.A_REVERSE)

                self.stdscr.addstr(y, x, title.center(tab_width))

                if i == self.current_section:
                    self.stdscr.attroff(curses.A_REVERSE)
            except curses.error:
                pass

        # Draw line under tabs
        try:
            self.stdscr.addstr(y + 1, 0, "─" * self.width)
        except curses.error:
            pass

    def render_content(self) -> None:
        """Render the help content"""
        # Calculate content area
        start_y = 5
        content_height = self.height - start_y - 4

        # Get current section content
        content = self.sections[self.current_section]["content"]

        # Draw content box
        draw_box(self.stdscr, start_y - 1, 0, content_height + 2, self.width)

        # Calculate visible lines
        max_scroll = max(0, len(content) - content_height)
        self.scroll_offset = min(self.scroll_offset, max_scroll)

        visible_start = self.scroll_offset
        visible_end = min(len(content), visible_start + content_height)

        # Draw content lines
        for i, line in enumerate(content[visible_start:visible_end]):
            y = start_y + i
            # Center short lines, left-align longer ones
            if len(line) < 40 and not line.startswith(" "):
                draw_centered_text(self.stdscr, y, line)
            else:
                try:
                    self.stdscr.addstr(y, 4, truncate_text(line, self.width - 8))
                except curses.error:
                    pass

        # Draw scroll indicators
        if self.scroll_offset > 0:
            try:
                self.stdscr.addstr(start_y, self.width - 3, "▲")
            except curses.error:
                pass

        if self.scroll_offset < max_scroll:
            try:
                self.stdscr.addstr(start_y + content_height - 1, self.width - 3, "▼")
            except curses.error:
                pass

    def render_help_bar(self) -> None:
        """Render the help bar at bottom"""
        y = self.height - 2
        help_text = "←→ Switch Section  ↑↓ Scroll  ESC Back"

        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)

    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        # Section navigation
        if key == curses.KEY_LEFT or (key < 256 and chr(key) in ["h"]):
            self.current_section = (self.current_section - 1) % len(self.sections)
            self.scroll_offset = 0
            return "navigate"

        elif key == curses.KEY_RIGHT or (key < 256 and chr(key) in ["l"]):
            self.current_section = (self.current_section + 1) % len(self.sections)
            self.scroll_offset = 0
            return "navigate"

        # Content scrolling
        elif key_matches(key, KEY_BINDINGS["navigate_up"]):
            if self.scroll_offset > 0:
                self.scroll_offset -= 1
            return "scroll"

        elif key_matches(key, KEY_BINDINGS["navigate_down"]):
            content = self.sections[self.current_section]["content"]
            content_height = self.height - 9  # Adjust for header/footer
            max_scroll = max(0, len(content) - content_height)
            if self.scroll_offset < max_scroll:
                self.scroll_offset += 1
            return "scroll"

        # Page up/down
        elif key == curses.KEY_PPAGE:
            self.scroll_offset = max(0, self.scroll_offset - 10)
            return "scroll"

        elif key == curses.KEY_NPAGE:
            content = self.sections[self.current_section]["content"]
            content_height = self.height - 9
            max_scroll = max(0, len(content) - content_height)
            self.scroll_offset = min(max_scroll, self.scroll_offset + 10)
            return "scroll"

        # Back
        elif key_matches(key, KEY_BINDINGS["back"]) or key_matches(key, KEY_BINDINGS["quit"]):
            return "back"

        return None

    def run(self) -> None:
        """Run the help viewer"""
        while True:
            self.render()

            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return

            action = self.navigate(key)

            if action == "back":
                return

            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()
