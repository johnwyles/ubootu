#!/usr/bin/env python3
"""
Profile Selector TUI for Ubootu
Allows users to select and apply saved profiles
"""

import curses
import os
import sys
from typing import List, Optional, Tuple

import yaml

from lib.profile_manager import ProfileManager
from lib.tui_dialogs import ListDialog, MessageDialog


def show_profile_selector(stdscr) -> Optional[str]:
    """Show profile selection dialog and return selected profile"""

    try:
        profile_mgr = ProfileManager()
        profiles = profile_mgr.list_profiles()

        # Build list of all profiles
        items = []

        # Add saved profiles
        if profiles.get("saved"):
            items.append(("__header_saved__", "── Saved Profiles ──"))
            for profile in profiles["saved"]:
                items.append((f"saved:{profile}", f"   {profile}"))

        # Add template profiles
        if profiles.get("templates"):
            if items:
                items.append(("__spacer__", ""))
            items.append(("__header_templates__", "── Template Profiles ──"))
            for profile in profiles["templates"]:
                items.append((f"templates:{profile}", f"   {profile}"))

        if not items:
            msg_dialog = MessageDialog(stdscr)
            msg_dialog.show("No Profiles", "No profiles found", "warning")
            return None

        # Filter out headers and spacers for selection
        selectable_items = [(id, name) for id, name in items if not id.startswith("__")]

        dialog = ListDialog(stdscr)
        selected = dialog.show(
            title="Select Profile to Apply", items=selectable_items, multi_select=False
        )

        if selected:
            return selected[0]
        return None

    except Exception as e:
        msg_dialog = MessageDialog(stdscr)
        msg_dialog.show("Error", f"Failed to load profiles: {str(e)}", "error")
        return None


def apply_profile(stdscr, profile_id: str) -> bool:
    """Apply the selected profile"""

    try:
        profile_mgr = ProfileManager()

        # Parse profile type and name
        if ":" in profile_id:
            profile_type, profile_name = profile_id.split(":", 1)
        else:
            profile_name = profile_id

        # Load profile
        config = profile_mgr.load_profile(profile_name)

        # Save as current config
        with open("config.yml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        msg_dialog = MessageDialog(stdscr)
        msg_dialog.show(
            "Success", f"Profile '{profile_name}' loaded successfully", "info"
        )
        return True

    except Exception as e:
        msg_dialog = MessageDialog(stdscr)
        msg_dialog.show("Error", f"Failed to apply profile: {str(e)}", "error")
        return False


def main():
    """Main entry point for profile selector"""

    def run(stdscr):
        # Select profile
        profile_id = show_profile_selector(stdscr)

        if profile_id:
            # Apply profile
            success = apply_profile(stdscr, profile_id)

            # Write result for bash to read
            with open("/tmp/profile_loaded.txt", "w") as f:
                f.write("yes" if success else "no")
        else:
            with open("/tmp/profile_loaded.txt", "w") as f:
                f.write("no")

    try:
        curses.wrapper(run)
        return 0
    except Exception:
        with open("/tmp/profile_loaded.txt", "w") as f:
            f.write("no")
        return 1


if __name__ == "__main__":
    sys.exit(main())
