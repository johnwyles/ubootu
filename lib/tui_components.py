#!/usr/bin/env python3
"""
Reusable TUI Components for Ubootu
Common UI elements used across all dialogs
"""

import curses
from typing import Dict, List, Optional, Tuple


class KeyHintBar:
    """Display key hints at the bottom of the screen"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def draw(self, hints: List[Tuple[str, str]], y: Optional[int] = None):
        """
        Draw key hints at the bottom of the screen

        Args:
            hints: List of (key, description) tuples
            y: Y position (defaults to bottom of screen)
        """
        if y is None:
            y = self.height - 1

        # Build hint string
        hint_parts = []
        for key, desc in hints:
            hint_parts.append(f"[{key}] {desc}")

        hint_str = "  ".join(hint_parts)

        # Truncate if too long
        if len(hint_str) > self.width - 2:
            hint_str = hint_str[: self.width - 5] + "..."

        # Clear the line first
        try:
            self.stdscr.addstr(y, 0, " " * self.width)

            # Center the hints
            x = max(0, (self.width - len(hint_str)) // 2)
            self.stdscr.addstr(y, x, hint_str, curses.A_DIM | curses.A_REVERSE)
        except curses.error:
            pass


class HelpOverlay:
    """Display help overlay without destroying current screen"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def show(self, title: str, content: List[str]):
        """
        Show help overlay

        Args:
            title: Help dialog title
            content: List of help text lines
        """
        # Calculate overlay dimensions
        overlay_width = min(70, self.width - 10)
        overlay_height = min(len(content) + 6, self.height - 4)
        overlay_y = (self.height - overlay_height) // 2
        overlay_x = (self.width - overlay_width) // 2

        # Create a new window for the overlay
        overlay_win = curses.newwin(overlay_height, overlay_width, overlay_y, overlay_x)

        # Draw help content
        overlay_win.box()

        # Draw title
        title_str = f" {title} "
        title_x = (overlay_width - len(title_str)) // 2
        overlay_win.attron(curses.A_BOLD | curses.A_REVERSE)
        overlay_win.addstr(0, title_x, title_str)
        overlay_win.attroff(curses.A_BOLD | curses.A_REVERSE)

        # Draw content
        content_start_y = 2
        visible_lines = overlay_height - 5  # Account for borders and padding

        for i, line in enumerate(content[:visible_lines]):
            if len(line) > overlay_width - 4:
                line = line[: overlay_width - 7] + "..."
            try:
                overlay_win.addstr(content_start_y + i, 2, line)
            except curses.error:
                pass

        # Draw instruction at bottom
        instruction = "Press any key to close"
        inst_x = (overlay_width - len(instruction)) // 2
        overlay_win.addstr(overlay_height - 2, inst_x, instruction, curses.A_DIM)

        # Show the overlay
        overlay_win.refresh()

        # Wait for keypress
        overlay_win.getch()

        # Clear the overlay
        del overlay_win

        # Refresh the main screen
        self.stdscr.touchwin()
        self.stdscr.refresh()


class CommandResult:
    """Enhanced command result with detailed information"""

    def __init__(
        self,
        command: str,
        exit_code: int,
        stdout: str,
        stderr: str,
        duration: float = 0.0,
    ):
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.duration = duration
        self.success = exit_code == 0

    def get_error_details(self) -> Dict[str, str]:
        """Parse error details and suggest fixes"""
        error_info = {
            "command": self.command,
            "exit_code": str(self.exit_code),
            "error": self.stderr or "No error message",
            "suggestion": self._get_suggestion(),
        }
        return error_info

    def _get_suggestion(self) -> str:
        """Get suggestion based on error patterns"""
        error_patterns = {
            "Could not get lock": "Another process is using apt. Wait or run: sudo killall apt apt-get",
            "Unable to lock": "Another process is using the package manager. Try again in a moment.",
            "dpkg was interrupted": "Run: sudo dpkg --configure -a",
            "Broken packages": "Run: sudo apt --fix-broken install",
            "No space left": "Free up disk space. Check with: df -h",
            "Permission denied": "Run with sudo or check file permissions",
            "command not found": "Install the required package or check PATH",
            "Connection refused": "Check if the service is running",
            "Network is unreachable": "Check your internet connection",
            "404 Not Found": "Repository may be outdated. Run: sudo apt update",
            "GPG error": "Repository key may be missing or expired",
            "Unmet dependencies": "Try: sudo apt -f install",
        }

        error_text = (self.stderr + self.stdout).lower()

        for pattern, suggestion in error_patterns.items():
            if pattern.lower() in error_text:
                return suggestion

        if self.exit_code == 1:
            return "General error. Check the command syntax and permissions."
        elif self.exit_code == 2:
            return "Misuse of shell command. Check the command syntax."
        elif self.exit_code == 126:
            return "Command cannot be executed. Check permissions."
        elif self.exit_code == 127:
            return "Command not found. Check if it's installed and in PATH."
        elif self.exit_code == 130:
            return "Process terminated by Ctrl+C."
        else:
            return "Check system logs for more details: journalctl -xe"


class ErrorDetailsDialog:
    """Show detailed error information"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def show(self, title: str, results: List[CommandResult]):
        """Show detailed error information for failed commands"""

        # Build error details
        content = []

        for i, result in enumerate(results):
            if not result.success:
                content.append(f"━━━ Command {i+1} Failed ━━━")
                details = result.get_error_details()
                content.append(f"Command: {details['command']}")
                content.append(f"Exit Code: {details['exit_code']}")
                content.append(f"Duration: {result.duration:.2f}s")
                content.append("")
                content.append("Error Message:")

                # Wrap error message
                error_lines = details["error"].split("\n")
                for line in error_lines[:5]:  # Show first 5 lines
                    if len(line) > 60:
                        line = line[:57] + "..."
                    content.append(f"  {line}")

                content.append("")
                content.append(f"Suggestion: {details['suggestion']}")
                content.append("")

        # Show in scrollable dialog
        self._show_scrollable_dialog(title, content)

    def _show_scrollable_dialog(self, title: str, content: List[str]):
        """Show content in a scrollable dialog"""

        # Calculate dialog dimensions
        dialog_width = min(80, self.width - 4)
        dialog_height = min(30, self.height - 4)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2

        # Create window
        dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

        scroll_offset = 0
        content_height = dialog_height - 4  # Account for borders and hints

        while True:
            dialog_win.clear()
            dialog_win.box()

            # Draw title
            title_str = f" {title} "
            title_x = (dialog_width - len(title_str)) // 2
            dialog_win.attron(curses.A_BOLD | curses.A_REVERSE)
            dialog_win.addstr(0, title_x, title_str)
            dialog_win.attroff(curses.A_BOLD | curses.A_REVERSE)

            # Draw content
            visible_lines = content[scroll_offset : scroll_offset + content_height]
            for i, line in enumerate(visible_lines):
                y = i + 2
                if len(line) > dialog_width - 4:
                    line = line[: dialog_width - 7] + "..."
                try:
                    # Highlight section headers
                    if line.startswith("━━━"):
                        dialog_win.attron(curses.A_BOLD)
                        dialog_win.addstr(y, 2, line)
                        dialog_win.attroff(curses.A_BOLD)
                    elif line.startswith("Suggestion:"):
                        dialog_win.attron(curses.A_BOLD)
                        dialog_win.addstr(y, 2, line)
                        dialog_win.attroff(curses.A_BOLD)
                    else:
                        dialog_win.addstr(y, 2, line)
                except curses.error:
                    pass

            # Draw scroll indicators
            if scroll_offset > 0:
                dialog_win.addstr(1, dialog_width - 2, "↑")
            if scroll_offset + content_height < len(content):
                dialog_win.addstr(dialog_height - 2, dialog_width - 2, "↓")

            # Draw key hints
            hints = "[↑↓] Scroll  [ESC/Q] Close"
            hint_x = (dialog_width - len(hints)) // 2
            dialog_win.addstr(dialog_height - 1, hint_x, hints, curses.A_DIM | curses.A_REVERSE)

            dialog_win.refresh()

            # Handle input
            key = dialog_win.getch()

            if key in [27, ord("q"), ord("Q")]:  # ESC or Q
                break
            elif key == curses.KEY_UP:
                if scroll_offset > 0:
                    scroll_offset -= 1
            elif key == curses.KEY_DOWN:
                if scroll_offset + content_height < len(content):
                    scroll_offset += 1
            elif key == curses.KEY_PPAGE:  # Page Up
                scroll_offset = max(0, scroll_offset - content_height)
            elif key == curses.KEY_NPAGE:  # Page Down
                max_scroll = max(0, len(content) - content_height)
                scroll_offset = min(max_scroll, scroll_offset + content_height)

        # Clean up
        del dialog_win
        self.stdscr.touchwin()
        self.stdscr.refresh()


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"


def wrap_text(text: str, width: int) -> List[str]:
    """Wrap text to specified width"""
    import textwrap

    return textwrap.wrap(text, width)
