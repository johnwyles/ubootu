#!/usr/bin/env python3
"""
Main menu for the unified TUI
Shows splash screen and main menu options
"""

import curses
import os
import time
from pathlib import Path
from typing import Optional

from .constants import *
from .dialogs import HelpDialog
from .prerequisite_installer import PrerequisiteInstaller
from .splash_screen import show_splash
from .utils import *


class MainMenu:
    """Main menu with splash screen using unified TUI style"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_index = 0
        self.prerequisites_checked = False

        # Menu options
        self.menu_items = [
            {
                "id": "1",
                "label": "Fresh Install",
                "description": "Configure a brand new Ubuntu installation",
                "icon": "🚀",
            },
            {"id": "2", "label": "Modify Setup", "description": "Tweak your existing configuration", "icon": "🔧"},
            {"id": "3", "label": "Apply Profile", "description": "Restore from a saved configuration", "icon": "📦"},
            {"id": "4", "label": "Backup Config", "description": "Save your current setup", "icon": "💾"},
            {"id": "5", "label": "View History", "description": "Browse configuration timeline", "icon": "📜"},
            {"id": "6", "label": "Quick Actions", "description": "Common tasks and fixes", "icon": "🎯"},
            {"id": "7", "label": "Help", "description": "Get help and documentation", "icon": "❓"},
            {"id": "8", "label": "Exit", "description": "See you later!", "icon": "🚪"},
        ]

        # Initialize curses
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
        except:
            pass

    def get_logo_lines(self):
        """Get ASCII logo lines for UBOOTU"""
        return [
            "██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗",
            "██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║",
            "██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║",
            "██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║",
            "╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝",
            " ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ",
        ]

    def show_splash_with_loading(self):
        """Show splash screen with loading animation"""
        show_splash(self.stdscr, animated=True)

    def render(self) -> None:
        """Render the main menu"""
        self.stdscr.clear()

        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return

        # Draw header with logo
        self.render_header()

        # Draw menu items
        self.render_menu_items()

        # Draw help bar
        self.render_help_bar()

        self.stdscr.refresh()

    def render_size_error(self) -> None:
        """Render terminal size error"""
        msg = f"Terminal too small! Minimum {MIN_WIDTH}x{MIN_HEIGHT}"
        draw_centered_text(self.stdscr, self.height // 2, msg, bold=True)

    def render_header(self) -> None:
        """Render the header section with logo"""
        # Get logo
        logo_lines = self.get_logo_lines()

        # Draw logo
        start_y = 1
        for i, line in enumerate(logo_lines):
            if start_y + i < self.height - 15:
                draw_centered_text(self.stdscr, start_y + i, line, bold=True)

        # Draw title below logo
        title_y = start_y + len(logo_lines) + 1
        draw_centered_text(self.stdscr, title_y, "🚀 UBOOTU 🚀", bold=True)
        draw_centered_text(self.stdscr, title_y + 1, "Ubuntu Desktop Configuration Tool")
        draw_centered_text(self.stdscr, title_y + 3, "What would you like to do?")

    def render_menu_items(self) -> None:
        """Render the menu items"""
        # Calculate menu area
        start_y = 12
        menu_height = min(len(self.menu_items) + 2, self.height - start_y - 3)

        # Draw menu box
        menu_width = min(70, self.width - 4)
        menu_x = (self.width - menu_width) // 2
        draw_box(self.stdscr, start_y - 1, menu_x, menu_height, menu_width)

        # Draw items
        for i, item in enumerate(self.menu_items):
            if i >= menu_height - 2:
                break

            y = start_y + i
            self.render_menu_item(y, menu_x + 2, item, i == self.current_index, menu_width - 4)

    def render_menu_item(self, y: int, x: int, item: dict, selected: bool, max_width: int) -> None:
        """Render a single menu item"""
        # Build item text
        text = f"{item['id']}. {item['icon']} {item['label']} - {item['description']}"

        # Truncate if needed
        text = truncate_text(text, max_width)

        # Draw with selection highlight
        try:
            if selected:
                self.stdscr.attron(curses.A_REVERSE)

            self.stdscr.addstr(y, x, text.ljust(max_width))

            if selected:
                self.stdscr.attroff(curses.A_REVERSE)
        except curses.error:
            pass

    def render_help_bar(self) -> None:
        """Render the help bar at bottom"""
        y = self.height - 2
        help_text = "↑↓ Navigate  Enter Select  Q Quit"

        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)

    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        # Navigation
        if key_matches(key, KEY_BINDINGS["navigate_up"]):
            self.current_index = (self.current_index - 1) % len(self.menu_items)
            return "navigate"

        elif key_matches(key, KEY_BINDINGS["navigate_down"]):
            self.current_index = (self.current_index + 1) % len(self.menu_items)
            return "navigate"

        # Selection with Enter
        elif key_matches(key, KEY_BINDINGS["enter"]):
            return "select"

        # Number keys for direct selection
        elif 49 <= key <= 56:  # '1' to '8'
            index = key - 49
            if index < len(self.menu_items):
                self.current_index = index
                return "select"

        # Quit
        elif key_matches(key, KEY_BINDINGS["quit"]) or key == 27:  # Q or ESC
            self.current_index = 7  # Exit option
            return "select"

        return None

    def check_prerequisites(self) -> bool:
        """Check and install prerequisites if needed"""
        # Check if prerequisites marker exists
        marker_file = Path(".prerequisites_installed")
        if marker_file.exists() or os.environ.get("PREREQUISITES_INSTALLED"):
            return True

        # Check if we actually need to install
        # Quick check for Python and Ansible
        try:
            import yaml

            # If we can import yaml, basic prerequisites are likely installed
            # Don't check for ansible here as it might not be needed for basic menu
            return True
        except ImportError:
            pass

        # Install prerequisites using TUI installer
        installer = PrerequisiteInstaller(self.stdscr)
        if installer.check_and_install():
            # Create marker file
            marker_file.touch()
            os.environ["PREREQUISITES_INSTALLED"] = "1"
            return True
        return False

    def run(self) -> str:
        """Run the main menu and return selected option"""
        # Show splash screen first
        self.show_splash_with_loading()

        # Check prerequisites before showing menu
        if not self.prerequisites_checked:
            if not self.check_prerequisites():
                return "8"  # Exit if prerequisites failed
            self.prerequisites_checked = True

        # Then show main menu
        while True:
            self.render()

            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return "8"  # Exit

            action = self.navigate(key)

            if action == "select":
                selected_id = self.menu_items[self.current_index]["id"]

                # For options that need configuration, ensure prerequisites
                if selected_id in ["1", "2", "3"] and not self.prerequisites_checked:
                    if not self.check_prerequisites():
                        continue
                    self.prerequisites_checked = True

                return selected_id

            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()


def show_main_menu(stdscr) -> str:
    """Show main menu and return selected option"""
    menu = MainMenu(stdscr)
    return menu.run()
