#!/usr/bin/env python3
"""
Help Viewer TUI for Ubootu
Display help documentation in a scrollable TUI interface
"""

import curses
import sys


class HelpViewer:
    """TUI for viewing help documentation"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)  # Hide cursor

        # Help content
        self.sections = [
            (
                "Overview",
                [
                    "🚀 Ubootu - Professional Ubuntu Desktop Configuration Tool",
                    "=" * 60,
                    "Ubootu is an advanced Ansible-based configuration tool that helps you",
                    "set up and customize your Ubuntu desktop with 400+ tools and options.",
                    "Features:",
                    "• Intuitive TUI interface with hierarchical menus",
                    "• Support for Ubuntu 20.04, 22.04, and 24.04",
                    "• 15+ categories of software and configurations",
                    "• Profile management for saving/restoring setups",
                    "• Comprehensive system customization options",
                    "• Security hardening and privacy tools",
                    "• Development environment setup",
                    "• Theme and appearance customization",
                ],
            ),
            (
                "Keyboard Shortcuts",
                [
                    "Navigation:",
                    "• Arrow Keys     - Navigate menus",
                    "• Enter         - Select/Confirm",
                    "• Space         - Toggle selection (multi-select)",
                    "• Tab           - Switch between buttons",
                    "• Backspace/ESC - Go back/Cancel",
                    "• Q             - Quit to main menu",
                    "• H             - Show help (in configuration)",
                    "In Lists:",
                    "• Page Up/Down  - Scroll quickly",
                    "• Home/End      - Jump to start/end",
                    "In Text Input:",
                    "• Ctrl+A        - Move to start",
                    "• Ctrl+E        - Move to end",
                    "• Ctrl+K        - Delete to end of line",
                ],
            ),
            (
                "Configuration Files",
                [
                    "Main Files:",
                    "• config.yml    - Current configuration (auto-generated)",
                    "• site.yml      - Master Ansible playbook",
                    "• CLAUDE.md     - AI context and project documentation",
                    "Directories:",
                    "• roles/        - Ansible roles for each component",
                    "• lib/          - Python TUI and utility modules",
                    "• group_vars/   - Default variables",
                    "• inventories/  - Target machine configurations",
                    "Profile Storage:",
                    "• ~/.config/ubootu/profiles/     - Saved configurations",
                    "• ~/.config/ubootu/.git/         - Version history",
                ],
            ),
            (
                "Command Line Usage",
                [
                    "Interactive Mode (default):",
                    "  ./setup.sh",
                    "Direct Options:",
                    "  ./setup.sh --fresh           Start fresh installation",
                    "  ./setup.sh --tui            Force TUI interface",
                    "  ./setup.sh --restore FILE   Restore from config file",
                    "  ./setup.sh --backup         Backup current config",
                    "  ./setup.sh --help           Show command help",
                    "Environment Variables:",
                    "  FORCE_TUI=1                 Force TUI compatibility",
                    "  BOOTSTRAP_DEBUG=1           Enable debug output",
                    "Running Ansible Directly:",
                    "  ansible-playbook site.yml --ask-become-pass",
                    "  ansible-playbook site.yml --tags 'applications'",
                    "  ansible-playbook site.yml --check  # Dry run",
                ],
            ),
            (
                "Tips & Tricks",
                [
                    "Performance Tips:",
                    "• Use profiles to save your favorite configurations",
                    "• Run with specific tags to update only what changed",
                    "• Enable zram for better memory usage on low-RAM systems",
                    "Customization Tips:",
                    "• Press 'h' on any item to see detailed information",
                    "• Use sliders to fine-tune system settings",
                    "• Global themes apply across all compatible applications",
                    "Troubleshooting:",
                    "• If TUI fails, try: FORCE_TUI=1 ./setup.sh",
                    "• Check ansible.log for detailed error messages",
                    "• Use Quick Actions to fix common issues",
                    "• Run './setup.sh --check' to verify without changes",
                ],
            ),
        ]

        self.current_section = 0
        self.scroll_offset = 0

    def draw_border(self):
        """Draw window border"""
        try:
            # Draw corners
            self.stdscr.addch(0, 0, curses.ACS_ULCORNER)
            self.stdscr.addch(0, self.width - 1, curses.ACS_URCORNER)
            self.stdscr.addch(self.height - 1, 0, curses.ACS_LLCORNER)
            self.stdscr.addch(self.height - 1, self.width - 1, curses.ACS_LRCORNER)

            # Draw lines
            for x in range(1, self.width - 1):
                self.stdscr.addch(0, x, curses.ACS_HLINE)
                self.stdscr.addch(self.height - 1, x, curses.ACS_HLINE)

            for y in range(1, self.height - 1):
                self.stdscr.addch(y, 0, curses.ACS_VLINE)
                self.stdscr.addch(y, self.width - 1, curses.ACS_VLINE)

            # Draw title
            title = " Ubootu Help "
            title_x = (self.width - len(title)) // 2
            self.stdscr.attron(curses.A_BOLD)
            self.stdscr.addstr(0, title_x, title)
            self.stdscr.attroff(curses.A_BOLD)

        except curses.error:
            pass

    def draw_tabs(self):
        """Draw section tabs"""
        tab_y = 2
        tab_x = 2

        for i, (section_name, _) in enumerate(self.sections):
            if tab_x + len(section_name) + 4 > self.width - 2:
                # Move to next line if no space
                tab_y += 1
                tab_x = 2

            if i == self.current_section:
                # Active tab
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(tab_y, tab_x, f" {section_name} ")
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                # Inactive tab
                self.stdscr.addstr(tab_y, tab_x, f" {section_name} ")

            tab_x += len(section_name) + 3

    def draw_content(self):
        """Draw current section content"""
        _, content = self.sections[self.current_section]

        # Content area
        content_start_y = 4
        content_height = self.height - 6  # Leave room for border and instructions
        content_width = self.width - 4

        # Draw visible content lines
        visible_lines = content[self.scroll_offset : self.scroll_offset + content_height]

        for i, line in enumerate(visible_lines):
            y = content_start_y + i
            if y < self.height - 2:
                # Truncate long lines
                if len(line) > content_width:
                    line = line[: content_width - 3] + "..."

                try:
                    # Highlight headers
                    if line.endswith(":") and not line.startswith("•"):
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(y, 2, line)
                        self.stdscr.attroff(curses.A_BOLD)
                    else:
                        self.stdscr.addstr(y, 2, line)
                except curses.error:
                    pass

        # Draw scroll indicators
        if self.scroll_offset > 0:
            try:
                self.stdscr.addstr(content_start_y - 1, self.width - 3, "↑")
            except Exception:
                pass

        if self.scroll_offset + content_height < len(content):
            try:
                self.stdscr.addstr(self.height - 3, self.width - 3, "↓")
            except Exception:
                pass

    def draw_instructions(self):
        """Draw bottom instructions"""
        instructions = "←→/Tab: Switch Section  ↑↓: Scroll  Q/ESC: Exit"
        try:
            y = self.height - 2
            x = (self.width - len(instructions)) // 2
            self.stdscr.addstr(y, x, instructions, curses.A_DIM)
        except curses.error:
            pass

    def run(self):
        """Main help viewer loop"""

        while True:
            self.stdscr.clear()

            self.draw_border()
            self.draw_tabs()
            self.draw_content()
            self.draw_instructions()

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key in [ord("q"), ord("Q"), 27]:  # Q or ESC
                break
            elif key == curses.KEY_LEFT or key == ord("\t"):
                # Previous section
                self.current_section = (self.current_section - 1) % len(self.sections)
                self.scroll_offset = 0
            elif key == curses.KEY_RIGHT:
                # Next section
                self.current_section = (self.current_section + 1) % len(self.sections)
                self.scroll_offset = 0
            elif key == curses.KEY_UP:
                # Scroll up
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1
            elif key == curses.KEY_DOWN:
                # Scroll down
                _, content = self.sections[self.current_section]
                max_scroll = max(0, len(content) - (self.height - 6))
                if self.scroll_offset < max_scroll:
                    self.scroll_offset += 1
            elif key == curses.KEY_PPAGE:  # Page Up
                self.scroll_offset = max(0, self.scroll_offset - (self.height - 6))
            elif key == curses.KEY_NPAGE:  # Page Down
                _, content = self.sections[self.current_section]
                max_scroll = max(0, len(content) - (self.height - 6))
                self.scroll_offset = min(max_scroll, self.scroll_offset + (self.height - 6))
            elif key == curses.KEY_HOME:
                self.scroll_offset = 0
            elif key == curses.KEY_END:
                _, content = self.sections[self.current_section]
                self.scroll_offset = max(0, len(content) - (self.height - 6))


def main():
    """Main entry point"""

    def run(stdscr):
        viewer = HelpViewer(stdscr)
        viewer.run()

    try:
        curses.wrapper(run)
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
