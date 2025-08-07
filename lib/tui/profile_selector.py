#!/usr/bin/env python3
"""
Curses-based profile selector for Ubootu
Replaces the Rich-based version with unified TUI style
"""

import curses
import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from .constants import *
from .dialogs import ConfirmDialog, MessageDialog
from .utils import *


class ProfileSelector:
    """Select and apply saved configuration profiles"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_index = 0
        self.profiles = []
        self.profile_dir = Path("profiles")

        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
        except:
            pass

    def load_profiles(self) -> None:
        """Load available profiles from the profiles directory"""
        self.profiles = []

        if not self.profile_dir.exists():
            return

        # Load all YAML files from profiles directory
        for profile_file in self.profile_dir.glob("*.yml"):
            try:
                with open(profile_file, "r") as f:
                    profile_data = yaml.safe_load(f) or {}

                # Extract metadata
                metadata = profile_data.get("metadata", {})
                profile_info = {
                    "filename": profile_file.name,
                    "path": profile_file,
                    "name": metadata.get("name", profile_file.stem),
                    "description": metadata.get("description", "No description"),
                    "created_at": metadata.get("created_at", "Unknown"),
                    "system_info": metadata.get("system_info", {}),
                    "items_count": len(profile_data.get("selected_items", [])),
                }
                self.profiles.append(profile_info)
            except Exception as e:
                # Skip invalid profiles
                continue

        # Sort by name
        self.profiles.sort(key=lambda p: p["name"])

    def render(self) -> None:
        """Render the profile selector"""
        self.stdscr.clear()

        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return

        # Draw header
        self.render_header()

        # Draw profile list
        self.render_profiles()

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
        draw_centered_text(self.stdscr, 1, "📦 Select Profile to Apply", bold=True)

    def render_profiles(self) -> None:
        """Render the profile list"""
        # Calculate list area
        start_y = 4
        list_height = self.height - start_y - 4

        if not self.profiles:
            draw_centered_text(self.stdscr, self.height // 2, "No profiles found!")
            draw_centered_text(self.stdscr, self.height // 2 + 2, "Create profiles by saving configurations")
            return

        # Draw profile box
        draw_box(self.stdscr, start_y - 1, 0, list_height + 2, self.width)

        # Calculate visible range
        visible_start = max(0, self.current_index - list_height // 2)
        visible_end = min(len(self.profiles), visible_start + list_height)

        # Adjust if at the end
        if visible_end - visible_start < list_height:
            visible_start = max(0, visible_end - list_height)

        # Draw profiles
        for i, profile in enumerate(self.profiles[visible_start:visible_end]):
            y = start_y + i
            selected = (visible_start + i) == self.current_index
            self.render_profile_item(y, 2, profile, selected, self.width - 4)

    def render_profile_item(self, y: int, x: int, profile: dict, selected: bool, max_width: int) -> None:
        """Render a single profile item"""
        # Build profile text
        name = profile["name"]
        desc = profile["description"]
        items = profile["items_count"]
        date = profile["created_at"]

        # Format text
        text = f"{name} - {desc} ({items} items, created {date})"
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
        help_text = "↑↓ Navigate  Enter Apply  V View  D Delete  ESC Back"

        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)

    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        if not self.profiles:
            # Only handle back/quit when no profiles
            if key_matches(key, KEY_BINDINGS["back"]) or key_matches(key, KEY_BINDINGS["quit"]):
                return "back"
            return None

        # Navigation
        if key_matches(key, KEY_BINDINGS["navigate_up"]):
            self.current_index = (self.current_index - 1) % len(self.profiles)
            return "navigate"

        elif key_matches(key, KEY_BINDINGS["navigate_down"]):
            self.current_index = (self.current_index + 1) % len(self.profiles)
            return "navigate"

        # Select/Apply
        elif key_matches(key, KEY_BINDINGS["select"]):
            return "apply"

        # View profile
        elif key == ord("v") or key == ord("V"):
            return "view"

        # Delete profile
        elif key == ord("d") or key == ord("D"):
            return "delete"

        # Back
        elif key_matches(key, KEY_BINDINGS["back"]):
            return "back"

        # Quit
        elif key_matches(key, KEY_BINDINGS["quit"]):
            return "quit"

        return None

    def view_profile(self) -> None:
        """View the selected profile details"""
        if not self.profiles or self.current_index >= len(self.profiles):
            return

        profile = self.profiles[self.current_index]

        # Load full profile data
        try:
            with open(profile["path"], "r") as f:
                data = yaml.safe_load(f) or {}

            # Format profile information
            lines = [
                f"Name: {profile['name']}",
                f"Description: {profile['description']}",
                f"Created: {profile['created_at']}",
                f"Items: {profile['items_count']}",
                "",
                "System Info:",
                f"  Hostname: {data.get('metadata', {}).get('system_info', {}).get('hostname', 'Unknown')}",
                f"  Ubuntu: {data.get('metadata', {}).get('system_info', {}).get('version', 'Unknown')}",
                "",
                "Selected Items:",
            ]

            # Add selected items (first 10)
            items = data.get("selected_items", [])[:10]
            for item in items:
                lines.append(f"  - {item}")
            if len(data.get("selected_items", [])) > 10:
                lines.append(f"  ... and {len(data.get('selected_items', [])) - 10} more")

            # Show in dialog
            dialog = MessageDialog(self.stdscr)
            dialog.show("Profile Details", "\n".join(lines))

        except Exception as e:
            dialog = MessageDialog(self.stdscr)
            dialog.show("Error", f"Failed to load profile: {str(e)}", "error")

    def delete_profile(self) -> bool:
        """Delete the selected profile"""
        if not self.profiles or self.current_index >= len(self.profiles):
            return False

        profile = self.profiles[self.current_index]

        # Confirm deletion
        dialog = ConfirmDialog(self.stdscr)
        if dialog.show(f"Delete profile '{profile['name']}'?", "This action cannot be undone."):
            try:
                # Delete the file
                profile["path"].unlink()

                # Remove from list
                self.profiles.pop(self.current_index)

                # Adjust index
                if self.current_index >= len(self.profiles) and self.current_index > 0:
                    self.current_index -= 1

                # Show success
                msg_dialog = MessageDialog(self.stdscr)
                msg_dialog.show("Success", f"Profile '{profile['name']}' deleted")
                return True

            except Exception as e:
                msg_dialog = MessageDialog(self.stdscr)
                msg_dialog.show("Error", f"Failed to delete profile: {str(e)}", "error")

        return False

    def apply_profile(self) -> Optional[str]:
        """Apply the selected profile and return its path"""
        if not self.profiles or self.current_index >= len(self.profiles):
            return None

        profile = self.profiles[self.current_index]

        # Confirm application
        dialog = ConfirmDialog(self.stdscr)
        if dialog.show(
            f"Apply profile '{profile['name']}'?", f"This will use the configuration from {profile['created_at']}"
        ):
            return str(profile["path"])

        return None

    def run(self) -> Optional[str]:
        """Run the profile selector and return selected profile path"""
        # Load profiles
        self.load_profiles()

        while True:
            self.render()

            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return None

            action = self.navigate(key)

            if action == "apply":
                profile_path = self.apply_profile()
                if profile_path:
                    return profile_path

            elif action == "view":
                self.view_profile()

            elif action == "delete":
                self.delete_profile()

            elif action in ["back", "quit"]:
                return None

            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()
