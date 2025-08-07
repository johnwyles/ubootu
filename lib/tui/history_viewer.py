#!/usr/bin/env python3
"""
Curses-based history viewer for Ubootu
Shows installation history and logs
"""

import curses
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .constants import *
from .dialogs import MessageDialog
from .utils import *


class HistoryViewer:
    """View installation history and logs"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_index = 0
        self.history_items = []
        self.log_dir = Path(".ansible/logs")
        self.history_file = Path(".ansible/history.yml")

        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
        except:
            pass

    def load_history(self) -> None:
        """Load installation history"""
        self.history_items = []

        # Check for Ansible log directory
        if self.log_dir.exists():
            # Load log files
            for log_file in sorted(self.log_dir.glob("*.log"), reverse=True):
                try:
                    # Extract date from filename (assumed format: ansible_YYYYMMDD_HHMMSS.log)
                    filename = log_file.stem
                    if filename.startswith("ansible_"):
                        date_str = filename.replace("ansible_", "")
                        # Parse date
                        try:
                            date_parts = date_str.split("_")
                            if len(date_parts) >= 2:
                                date = datetime.strptime(f"{date_parts[0]}_{date_parts[1]}", "%Y%m%d_%H%M%S")
                                date_formatted = date.strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                date_formatted = date_str
                        except:
                            date_formatted = date_str
                    else:
                        date_formatted = filename

                    # Get file size
                    size = log_file.stat().st_size
                    size_str = self.format_size(size)

                    # Check if log contains errors
                    has_errors = False
                    try:
                        with open(log_file, "r") as f:
                            content = f.read(10000)  # Read first 10KB
                            if "failed:" in content or "ERROR" in content:
                                has_errors = True
                    except:
                        pass

                    self.history_items.append(
                        {
                            "type": "log",
                            "path": log_file,
                            "date": date_formatted,
                            "size": size_str,
                            "has_errors": has_errors,
                            "description": f"Installation log - {size_str}",
                        }
                    )
                except:
                    continue

        # Also check for any backup configs in profiles directory
        profile_dir = Path("profiles")
        if profile_dir.exists():
            for profile in sorted(profile_dir.glob("*.yml"), reverse=True):
                try:
                    stat = profile.stat()
                    date = datetime.fromtimestamp(stat.st_mtime)
                    date_formatted = date.strftime("%Y-%m-%d %H:%M:%S")

                    self.history_items.append(
                        {
                            "type": "profile",
                            "path": profile,
                            "date": date_formatted,
                            "size": self.format_size(stat.st_size),
                            "has_errors": False,
                            "description": f"Configuration profile: {profile.stem}",
                        }
                    )
                except:
                    continue

    def format_size(self, size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def render(self) -> None:
        """Render the history viewer"""
        self.stdscr.clear()

        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return

        # Draw header
        self.render_header()

        # Draw history list
        self.render_history()

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
        draw_centered_text(self.stdscr, 1, "📜 Installation History", bold=True)

    def render_history(self) -> None:
        """Render the history list"""
        # Calculate list area
        start_y = 4
        list_height = self.height - start_y - 4

        if not self.history_items:
            draw_centered_text(self.stdscr, self.height // 2, "No history found!")
            draw_centered_text(self.stdscr, self.height // 2 + 2, "Run an installation to generate history")
            return

        # Draw history box
        draw_box(self.stdscr, start_y - 1, 0, list_height + 2, self.width)

        # Calculate visible range
        visible_start = max(0, self.current_index - list_height // 2)
        visible_end = min(len(self.history_items), visible_start + list_height)

        # Adjust if at the end
        if visible_end - visible_start < list_height:
            visible_start = max(0, visible_end - list_height)

        # Draw items
        for i, item in enumerate(self.history_items[visible_start:visible_end]):
            y = start_y + i
            selected = (visible_start + i) == self.current_index
            self.render_history_item(y, 2, item, selected, self.width - 4)

    def render_history_item(self, y: int, x: int, item: dict, selected: bool, max_width: int) -> None:
        """Render a single history item"""
        # Build item text
        icon = "📄" if item["type"] == "log" else "📦"
        if item["has_errors"]:
            icon = "❌"

        text = f"{icon} {item['date']} - {item['description']}"
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
        help_text = "↑↓ Navigate  Enter View  D Delete  ESC Back"

        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)

    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        if not self.history_items:
            # Only handle back/quit when no history
            if key_matches(key, KEY_BINDINGS["back"]) or key_matches(key, KEY_BINDINGS["quit"]):
                return "back"
            return None

        # Navigation
        if key_matches(key, KEY_BINDINGS["navigate_up"]):
            self.current_index = (self.current_index - 1) % len(self.history_items)
            return "navigate"

        elif key_matches(key, KEY_BINDINGS["navigate_down"]):
            self.current_index = (self.current_index + 1) % len(self.history_items)
            return "navigate"

        # View
        elif key_matches(key, KEY_BINDINGS["select"]):
            return "view"

        # Delete
        elif key == ord("d") or key == ord("D"):
            return "delete"

        # Back
        elif key_matches(key, KEY_BINDINGS["back"]):
            return "back"

        # Quit
        elif key_matches(key, KEY_BINDINGS["quit"]):
            return "quit"

        return None

    def view_item(self) -> None:
        """View the selected history item"""
        if not self.history_items or self.current_index >= len(self.history_items):
            return

        item = self.history_items[self.current_index]

        if item["type"] == "log":
            # View log file
            self.view_log_file(item["path"])
        else:
            # View profile
            self.view_profile(item["path"])

    def view_log_file(self, log_path: Path) -> None:
        """View a log file in a pager-like interface"""
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()

            # Show in a simple pager
            # TODO: Implement a proper pager dialog
            # For now, show first/last parts
            preview_lines = []
            if len(lines) > 40:
                preview_lines.extend(lines[:20])
                preview_lines.append("\n... [Middle section omitted] ...\n\n")
                preview_lines.extend(lines[-20:])
            else:
                preview_lines = lines

            content = "".join(preview_lines)
            dialog = MessageDialog(self.stdscr)
            dialog.show(f"Log: {log_path.name}", content[:2000])  # Limit to 2000 chars

        except Exception as e:
            dialog = MessageDialog(self.stdscr)
            dialog.show("Error", f"Failed to read log: {str(e)}", "error")

    def view_profile(self, profile_path: Path) -> None:
        """View a profile file"""
        try:
            import yaml

            with open(profile_path, "r") as f:
                data = yaml.safe_load(f) or {}

            # Format profile information
            metadata = data.get("metadata", {})
            lines = [
                f"Name: {metadata.get('name', profile_path.stem)}",
                f"Description: {metadata.get('description', 'No description')}",
                f"Created: {metadata.get('created_at', 'Unknown')}",
                f"Items: {len(data.get('selected_items', []))}",
                "",
                "First 10 items:",
            ]

            # Add selected items
            for item in data.get("selected_items", [])[:10]:
                lines.append(f"  - {item}")

            dialog = MessageDialog(self.stdscr)
            dialog.show(f"Profile: {profile_path.name}", "\n".join(lines))

        except Exception as e:
            dialog = MessageDialog(self.stdscr)
            dialog.show("Error", f"Failed to read profile: {str(e)}", "error")

    def delete_item(self) -> bool:
        """Delete the selected history item"""
        # For now, we don't allow deleting logs
        # Could be implemented later with confirmation
        dialog = MessageDialog(self.stdscr)
        dialog.show(
            "Not Implemented",
            "Deleting history items is not yet implemented.\n" "Log files are kept for troubleshooting.",
        )
        return False

    def run(self) -> None:
        """Run the history viewer"""
        # Load history
        self.load_history()

        while True:
            self.render()

            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return

            action = self.navigate(key)

            if action == "view":
                self.view_item()

            elif action == "delete":
                self.delete_item()

            elif action in ["back", "quit"]:
                return

            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()
