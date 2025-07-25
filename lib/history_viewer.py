#!/usr/bin/env python3
"""
History Viewer TUI for Ubootu
Browse and manage configuration history
"""

import curses
import sys

from lib.profile_manager import ProfileManager
from lib.tui_dialogs import ConfirmDialog, ListDialog, MessageDialog, TextInputDialog


class HistoryViewer:
    """TUI for viewing configuration history"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.profile_mgr = ProfileManager()
        self.history = []

    def load_history(self):
        """Load configuration history"""
        try:
            self.history = self.profile_mgr.get_history(50)
        except Exception as e:
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Error", f"Failed to load history: {str(e)}", "error")
            self.history = []

    def show_history_list(self) -> str:
        """Show history list and return selected action"""

        # Build list items
        items = []
        for entry in self.history:
            date = entry["date"]
            hash_short = entry["hash"][:8]
            message = entry["message"]
            # Truncate message if too long
            if len(message) > 40:
                message = message[:37] + "..."

            display = f"{date} | {hash_short} | {message}"
            items.append((entry["hash"], display))

        if not items:
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("No History", "No configuration history found", "info")
            return None

        # Add action options at the end
        items.append(("__spacer__", ""))
        items.append(("__action_restore__", "→ Restore from a commit"))
        items.append(("__action_diff__", "→ View diff between commits"))
        items.append(("__action_back__", "← Back to main menu"))

        # Filter out spacers for selection
        selectable_items = [(id, name) for id, name in items if id != "__spacer__"]

        dialog = ListDialog(self.stdscr)
        selected = dialog.show(title="Configuration History", items=selectable_items, multi_select=False)

        if selected:
            return selected[0]
        return "__action_back__"

    def restore_commit(self):
        """Restore from a specific commit"""

        # Get commit hash
        input_dialog = TextInputDialog(self.stdscr)
        commit_hash = input_dialog.show(
            title="Restore Configuration",
            prompt="Enter commit hash (first 8 characters):",
            default="",
        )

        if not commit_hash:
            return

        # Confirm restoration
        confirm_dialog = ConfirmDialog(self.stdscr)
        if not confirm_dialog.show(
            title="Confirm Restore",
            message=f"Restore configuration from commit {commit_hash}? Current configuration will be overwritten.",
            default=False,
        ):
            return

        # Restore
        try:
            if self.profile_mgr.restore_from_commit(commit_hash):
                msg_dialog = MessageDialog(self.stdscr)
                msg_dialog.show("Success", f"Configuration restored from {commit_hash}", "info")
            else:
                msg_dialog = MessageDialog(self.stdscr)
                msg_dialog.show("Error", "Failed to restore configuration", "error")
        except Exception as e:
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Error", f"Restore failed: {str(e)}", "error")

    def view_diff(self):
        """View diff between two commits"""

        input_dialog = TextInputDialog(self.stdscr)

        # Get first commit
        commit1 = input_dialog.show(
            title="View Diff",
            prompt="Enter first commit hash (or 'current'):",
            default="current",
        )

        if not commit1:
            return

        # Get second commit
        commit2 = input_dialog.show(title="View Diff", prompt="Enter second commit hash:", default="")

        if not commit2:
            return

        # Get diff
        try:
            diff = self.profile_mgr.diff_profiles(commit1 if commit1 != "current" else None, commit2)

            # Show diff in a scrollable dialog
            # For now, just show a message with truncated diff
            if diff:
                lines = diff.split("\n")
                summary = f"Differences found ({len(lines)} lines)\n\n"
                summary += "\n".join(lines[:10])
                if len(lines) > 10:
                    summary += f"\n... and {len(lines) - 10} more lines"
            else:
                summary = "No differences found"

            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Diff Result", summary, "info")

        except Exception as e:
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Error", f"Failed to generate diff: {str(e)}", "error")

    def run(self):
        """Main loop for history viewer"""

        self.load_history()

        while True:
            action = self.show_history_list()

            if action == "__action_back__" or action is None:
                break
            elif action == "__action_restore__":
                self.restore_commit()
            elif action == "__action_diff__":
                self.view_diff()
            else:
                # User selected a specific commit - show options
                commit_dialog = ListDialog(self.stdscr)
                commit_actions = [
                    ("restore", "Restore this commit"),
                    ("diff", "Compare with current"),
                    ("back", "Back to history"),
                ]

                selected = commit_dialog.show(
                    title=f"Commit {action[:8]}",
                    items=commit_actions,
                    multi_select=False,
                )

                if selected and selected[0] == "restore":
                    # Set the commit hash for restoration
                    input_dialog = TextInputDialog(self.stdscr)
                    input_dialog.show("", "", action[:8])  # Pre-fill the hash
                    self.restore_commit()
                elif selected and selected[0] == "diff":
                    # Pre-fill the second commit
                    input_dialog = TextInputDialog(self.stdscr)
                    input_dialog.show("", "", action[:8])
                    self.view_diff()


def main():
    """Main entry point"""

    def run(stdscr):
        viewer = HistoryViewer(stdscr)
        viewer.run()

    try:
        curses.wrapper(run)
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
