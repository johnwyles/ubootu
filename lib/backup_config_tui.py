#!/usr/bin/env python3
"""
Backup Configuration TUI for Ubootu
Allows users to backup their current configuration
"""

import curses
import sys
from datetime import datetime

from lib.profile_manager import ProfileManager
from lib.tui_dialogs import ConfirmDialog, MessageDialog, ProgressDialog, TextInputDialog


def backup_configuration(stdscr) -> bool:
    """Show backup configuration dialog"""

    try:
        # Get backup name
        input_dialog = TextInputDialog(stdscr)
        default_name = datetime.now().strftime("backup_%Y%m%d_%H%M%S")

        backup_name = input_dialog.show(
            title="Backup Configuration",
            prompt="Enter backup name:",
            default=default_name,
        )

        if not backup_name:
            return False

        # Initialize progress dialog
        progress = ProgressDialog(stdscr, "Creating Backup", "Saving configuration...")
        progress.update(0, "Initializing...")

        # Create profile manager
        profile_mgr = ProfileManager()

        # Create backup
        progress.update(50, "Saving profile...")
        profile_mgr.save_profile(
            profile_mgr.load_profile(),
            name=backup_name,
            commit_message=f"Backup: {backup_name}",
        )

        progress.update(100, "Backup complete!")

        # Ask about remote sync
        confirm_dialog = ConfirmDialog(stdscr)
        sync_remote = confirm_dialog.show(
            title="Remote Sync",
            message="Push backup to remote repository?",
            default=False,
        )

        if sync_remote:
            progress = ProgressDialog(stdscr, "Syncing", "Pushing to remote...")
            progress.update(50, "Pushing changes...")

            if profile_mgr.push_to_remote():
                progress.update(100, "Push complete!")
                msg_dialog = MessageDialog(stdscr)
                msg_dialog.show(
                    "Success",
                    f"Backup '{backup_name}' created and pushed to remote",
                    "info",
                )
            else:
                msg_dialog = MessageDialog(stdscr)
                msg_dialog.show(
                    "Warning",
                    f"Backup '{backup_name}' created locally but failed to push to remote",
                    "warning",
                )
        else:
            msg_dialog = MessageDialog(stdscr)
            msg_dialog.show("Success", f"Backup '{backup_name}' created successfully", "info")

        return True

    except Exception as e:
        msg_dialog = MessageDialog(stdscr)
        msg_dialog.show("Error", f"Failed to create backup: {str(e)}", "error")
        return False


def main():
    """Main entry point"""
    try:
        success = curses.wrapper(backup_configuration)
        return 0 if success else 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
