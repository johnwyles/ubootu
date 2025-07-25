#!/usr/bin/env python3
"""
Overlay Dialog System for Ubootu
Creates popup dialogs that overlay on existing screen content
"""

import curses
from typing import Any, List, Optional, Tuple


class OverlayDialog:
    """Base class for overlay dialogs that preserve background content"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.saved_screen = None
        curses.curs_set(0)  # Hide cursor

    def save_screen(self):
        """Save current screen content - simplified to avoid alignment issues"""
        # Don't actually save - just mark that we should refresh on exit
        self.saved_screen = True

    def restore_screen(self):
        """Restore screen by requesting refresh"""
        if self.saved_screen:
            # Just request a full refresh instead of trying to restore
            self.stdscr.touchwin()
            self.stdscr.refresh()

    def draw_shadow(self, y, x, h, w):
        """Draw drop shadow for 3D effect"""
        # Draw shadow to the right
        for i in range(1, h):
            try:
                self.stdscr.addch(y + i, x + w, " ", curses.A_REVERSE)
                if x + w + 1 < self.width:
                    self.stdscr.addch(y + i, x + w + 1, " ", curses.A_REVERSE)
            except:
                pass

        # Draw shadow below
        for i in range(1, w + 2):
            try:
                if y + h < self.height and x + i < self.width:
                    self.stdscr.addch(y + h, x + i, " ", curses.A_REVERSE)
            except:
                pass

    def draw_box_with_shadow(self, y, x, h, w, title=""):
        """Draw a box with drop shadow"""
        # Draw shadow first
        self.draw_shadow(y, x, h, w)

        # Draw box
        try:
            # Corners
            self.stdscr.addch(y, x, curses.ACS_ULCORNER)
            self.stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
            self.stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
            self.stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)

            # Horizontal lines
            for i in range(1, w - 1):
                self.stdscr.addch(y, x + i, curses.ACS_HLINE)
                self.stdscr.addch(y + h - 1, x + i, curses.ACS_HLINE)

            # Vertical lines
            for i in range(1, h - 1):
                self.stdscr.addch(y + i, x, curses.ACS_VLINE)
                self.stdscr.addch(y + i, x + w - 1, curses.ACS_VLINE)

            # Clear interior
            for i in range(1, h - 1):
                self.stdscr.addstr(y + i, x + 1, " " * (w - 2))

            # Draw title if provided
            if title:
                title = f" {title} "
                title_x = x + (w - len(title)) // 2
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(y, title_x, title)
                self.stdscr.attroff(curses.A_BOLD)

        except curses.error:
            pass


class SelectionOverlay(OverlayDialog):
    """Overlay dialog for selecting items with clear instructions"""

    def show(
        self,
        title: str,
        items: List[Tuple[str, str]],
        multi_select: bool = False,
        selected_items: List[str] = None,
        instructions: List[str] = None,
    ) -> List[str]:
        """
        Show selection overlay with instructions

        Args:
            title: Dialog title
            items: List of (id, display_name) tuples
            multi_select: Allow multiple selections
            selected_items: Pre-selected item IDs
            instructions: List of instruction lines to show at top

        Returns:
            List of selected item IDs
        """
        # Save current screen
        self.save_screen()

        if selected_items is None:
            selected_items = []

        selected = set(selected_items)
        current = 0
        scroll_offset = 0

        # Calculate dialog dimensions
        dialog_width = min(90, self.width - 10)
        dialog_height = min(24, self.height - 6)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2

        # Default instructions if none provided
        if instructions is None:
            if multi_select:
                instructions = [
                    "Select the sections you want to configure:",
                    "• Use ↑↓ arrow keys to navigate",
                    "• Press SPACE to select/deselect items",
                    "• Press ENTER when done selecting",
                    "• Press ESC to cancel",
                ]
            else:
                instructions = [
                    "Select an option:",
                    "• Use ↑↓ arrow keys to navigate",
                    "• Press ENTER to select",
                    "• Press ESC to cancel",
                ]

        # Calculate content area
        instruction_height = len(instructions) + 1  # +1 for separator
        list_start_y = dialog_y + instruction_height + 3
        list_height = dialog_height - instruction_height - 6

        while True:
            # Restore background
            self.restore_screen()

            # Draw dialog with shadow
            self.draw_box_with_shadow(
                dialog_y, dialog_x, dialog_height, dialog_width, title
            )

            # Draw instructions
            for i, instruction in enumerate(instructions):
                try:
                    if instruction:
                        # Center short lines, left-align bullet points
                        if instruction.startswith("•"):
                            self.stdscr.addstr(
                                dialog_y + 2 + i, dialog_x + 3, instruction
                            )
                        else:
                            x_pos = dialog_x + (dialog_width - len(instruction)) // 2
                            self.stdscr.addstr(dialog_y + 2 + i, x_pos, instruction)
                except:
                    pass

            # Draw separator line
            try:
                for i in range(dialog_x + 1, dialog_x + dialog_width - 1):
                    self.stdscr.addch(list_start_y - 1, i, curses.ACS_HLINE)
            except:
                pass

            # Draw list items
            visible_items = items[scroll_offset : scroll_offset + list_height]
            for i, (item_id, display_name) in enumerate(visible_items):
                y = list_start_y + i
                x = dialog_x + 3

                # Truncate display name if too long
                max_width = dialog_width - 10
                if len(display_name) > max_width:
                    display_name = display_name[: max_width - 3] + "..."

                try:
                    # Draw selection indicator
                    if multi_select:
                        if item_id in selected:
                            self.stdscr.addstr(y, x, "[✓]", curses.A_BOLD)
                        else:
                            self.stdscr.addstr(y, x, "[ ]")
                        x += 4

                    # Draw item text
                    if i + scroll_offset == current:
                        self.stdscr.attron(curses.A_REVERSE)

                    self.stdscr.addstr(y, x, display_name)

                    if i + scroll_offset == current:
                        # Fill the rest of the line for highlight
                        remaining = dialog_width - 10 - len(display_name)
                        if remaining > 0:
                            self.stdscr.addstr(
                                y, x + len(display_name), " " * remaining
                            )
                        self.stdscr.attroff(curses.A_REVERSE)
                except:
                    pass

            # Draw scroll indicators
            if scroll_offset > 0:
                try:
                    self.stdscr.addstr(
                        list_start_y - 1, dialog_x + dialog_width - 4, " ▲ "
                    )
                except:
                    pass
            if scroll_offset + list_height < len(items):
                try:
                    self.stdscr.addstr(
                        list_start_y + list_height, dialog_x + dialog_width - 4, " ▼ "
                    )
                except:
                    pass

            # Draw key hints at bottom of dialog - ALWAYS include help
            if multi_select:
                hint_text = "[H] Help  [↑↓] Navigate  [SPACE] Toggle  [A] All  [N] None  [ENTER] Confirm  [ESC] Cancel"
            else:
                hint_text = "[H] Help  [↑↓] Navigate  [ENTER] Select  [ESC] Cancel"

            try:
                hint_x = dialog_x + (dialog_width - len(hint_text)) // 2
                self.stdscr.addstr(
                    dialog_y + dialog_height - 2, hint_x, hint_text, curses.A_DIM
                )
            except:
                pass

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == 27:  # ESC
                self.restore_screen()
                return []
            elif key in [ord("h"), ord("H")]:  # Help
                # Show help overlay
                help_msg = MessageOverlay(self.stdscr)
                help_text = "Selection Dialog Help\n\n"
                if multi_select:
                    help_text += "• Use ↑↓ arrow keys to move between items\n"
                    help_text += "• Press SPACE to select/deselect an item\n"
                    help_text += "• Press A to select all items\n"
                    help_text += "• Press N to deselect all items\n"
                    help_text += "• Press ENTER to confirm your selections\n"
                    help_text += "• Press ESC to cancel without saving\n\n"
                    help_text += "Selected items are marked with [✓]"
                else:
                    help_text += "• Use ↑↓ arrow keys to move between items\n"
                    help_text += "• Press ENTER to select the highlighted item\n"
                    help_text += "• Press ESC to cancel without selecting"
                help_msg.show("Help", help_text, "info")
                # Continue showing the selection dialog
            elif key == ord("\n"):  # Enter
                self.restore_screen()
                if multi_select:
                    return list(selected)
                else:
                    return [items[current][0]] if items else []
            elif key == ord(" ") and multi_select:  # Space
                item_id = items[current][0]
                if item_id in selected:
                    selected.remove(item_id)
                else:
                    selected.add(item_id)
            elif key in [ord("a"), ord("A")] and multi_select:  # Select all
                selected = set(item[0] for item in items)
            elif key in [ord("n"), ord("N")] and multi_select:  # Select none
                selected = set()
            elif key == curses.KEY_UP:
                if current > 0:
                    current -= 1
                    if current < scroll_offset:
                        scroll_offset = current
            elif key == curses.KEY_DOWN:
                if current < len(items) - 1:
                    current += 1
                    if current >= scroll_offset + list_height:
                        scroll_offset = current - list_height + 1
            elif key == curses.KEY_HOME:
                current = 0
                scroll_offset = 0
            elif key == curses.KEY_END:
                current = len(items) - 1
                scroll_offset = max(0, len(items) - list_height)


class MessageOverlay(OverlayDialog):
    """Overlay dialog for showing messages"""

    def show(self, title: str, message: str, msg_type: str = "info"):
        """Show message overlay"""
        # Save current screen
        self.save_screen()

        # Split message into lines
        lines = message.split("\n")

        # Calculate dialog dimensions
        dialog_width = min(70, self.width - 10)
        dialog_height = min(len(lines) + 6, self.height - 6)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2

        # Restore background and draw dialog
        self.restore_screen()
        self.draw_box_with_shadow(
            dialog_y, dialog_x, dialog_height, dialog_width, title
        )

        # Draw icon based on type
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}
        icon = icons.get(msg_type, "ℹ️")

        # Draw message
        for i, line in enumerate(lines[: dialog_height - 6]):
            try:
                # Word wrap if needed
                if len(line) > dialog_width - 6:
                    line = line[: dialog_width - 9] + "..."
                x_pos = dialog_x + (dialog_width - len(line)) // 2
                self.stdscr.addstr(dialog_y + 2 + i, x_pos, line)
            except:
                pass

        # Draw instruction
        instruction = "Press any key to continue"
        try:
            inst_x = dialog_x + (dialog_width - len(instruction)) // 2
            self.stdscr.addstr(
                dialog_y + dialog_height - 2, inst_x, instruction, curses.A_DIM
            )
        except:
            pass

        self.stdscr.refresh()
        self.stdscr.getch()

        # Restore screen
        self.restore_screen()
        self.stdscr.refresh()


class ConfirmOverlay(OverlayDialog):
    """Overlay dialog for confirmations"""

    def show(self, title: str, message: str, default: bool = True) -> bool:
        """Show confirmation overlay"""
        # Save current screen
        self.save_screen()

        # Split message into lines
        lines = message.split("\n")

        # Calculate dialog dimensions
        dialog_width = min(60, self.width - 10)
        dialog_height = min(len(lines) + 8, self.height - 6)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2

        selected = 0 if default else 1

        while True:
            # Restore background and draw dialog
            self.restore_screen()
            self.draw_box_with_shadow(
                dialog_y, dialog_x, dialog_height, dialog_width, title
            )

            # Draw message
            for i, line in enumerate(lines[: dialog_height - 8]):
                try:
                    if len(line) > dialog_width - 6:
                        line = line[: dialog_width - 9] + "..."
                    x_pos = dialog_x + (dialog_width - len(line)) // 2
                    self.stdscr.addstr(dialog_y + 2 + i, x_pos, line)
                except:
                    pass

            # Draw buttons
            button_y = dialog_y + dialog_height - 4
            buttons = ["[  Yes  ]", "[  No   ]"]
            button_spacing = 4
            total_width = len(buttons[0]) + len(buttons[1]) + button_spacing
            button_x = dialog_x + (dialog_width - total_width) // 2

            for i, button in enumerate(buttons):
                x = button_x + i * (len(buttons[0]) + button_spacing)
                attrs = curses.A_REVERSE if i == selected else 0
                try:
                    self.stdscr.addstr(button_y, x, button, attrs)
                except:
                    pass

            # Draw key hints - ALWAYS include help
            hint_text = "[H] Help  [←→/TAB] Switch  [ENTER] Select  [ESC] Cancel"
            try:
                hint_x = dialog_x + (dialog_width - len(hint_text)) // 2
                self.stdscr.addstr(
                    dialog_y + dialog_height - 2, hint_x, hint_text, curses.A_DIM
                )
            except:
                pass

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == 27:  # ESC
                self.restore_screen()
                return False
            elif key in [ord("h"), ord("H")]:  # Help
                # Show help overlay
                help_msg = MessageOverlay(self.stdscr)
                help_text = "Confirmation Dialog Help\n\n"
                help_text += "• Use ←→ arrow keys or TAB to switch between Yes/No\n"
                help_text += "• Press ENTER to confirm your choice\n"
                help_text += "• Press ESC to cancel (same as choosing No)\n\n"
                help_text += "The highlighted button shows your current selection."
                help_msg.show("Help", help_text, "info")
                # Continue showing the confirmation dialog
            elif key == ord("\n"):  # Enter
                self.restore_screen()
                return selected == 0
            elif key in [ord("\t"), curses.KEY_LEFT, curses.KEY_RIGHT]:
                selected = 1 - selected
