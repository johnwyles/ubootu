#!/usr/bin/env python3
"""
Dialog components for the unified TUI
"""

import curses
import textwrap
from typing import Any, List, Optional

from .constants import DIALOG_HEIGHT, DIALOG_WIDTH
from .utils import draw_box, draw_centered_text, get_dialog_position, truncate_text


class BaseDialog:
    """Base class for all dialogs"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def draw_dialog_box(self, dialog_height: int, dialog_width: int, title: str) -> tuple:
        """Draw dialog box and return content area position"""
        y, x = get_dialog_position(self.height, self.width, dialog_height, dialog_width)
        draw_box(self.stdscr, y, x, dialog_height, dialog_width, title)
        return y + 2, x + 2, dialog_height - 4, dialog_width - 4

    def wait_for_key(self, valid_keys: Optional[List[int]] = None) -> int:
        """Wait for user to press a key"""
        while True:
            key = self.stdscr.getch()
            if valid_keys is None or key in valid_keys:
                return key


class MessageDialog(BaseDialog):
    """Simple message dialog"""

    def show(self, title: str, message: str, dialog_type: str = "info") -> None:
        """Show a message dialog"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Calculate ideal dialog width (responsive to terminal size)
        # For small terminals (80x24), use most of the width
        if self.width <= 80:
            max_dialog_width = self.width - 4
            default_width = self.width - 8
        else:
            max_dialog_width = min(self.width - 10, 80)  # Cap at 80 for readability
            default_width = 60

        min_dialog_width = max(len(title) + 8, 30)  # Reduced minimum
        dialog_width = min(max_dialog_width, max(min_dialog_width, default_width))

        # Wrap text to fit dialog width
        wrapped_lines = []
        for paragraph in message.split("\n"):
            if paragraph.strip():
                # Wrap non-empty lines
                wrapped = textwrap.wrap(
                    paragraph, width=dialog_width - 6, break_long_words=False, break_on_hyphens=False
                )
                wrapped_lines.extend(wrapped)
            else:
                # Preserve empty lines
                wrapped_lines.append("")

        # Calculate required height
        content_height = len(wrapped_lines)
        dialog_height = min(content_height + 6, self.height - 4)

        # If content is too tall, we'll need scrolling
        needs_scrolling = content_height > (dialog_height - 6)

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Draw message (with potential scrolling)
        visible_lines = wrapped_lines[:h] if not needs_scrolling else wrapped_lines[: h - 1]
        for i, line in enumerate(visible_lines):
            try:
                self.stdscr.addstr(y + i, x, line[:w])
            except curses.error:
                pass

        # Add scroll indicator if needed
        if needs_scrolling:
            scroll_text = f"... ({content_height - h + 1} more lines)"
            try:
                self.stdscr.addstr(y + h - 1, x, scroll_text, curses.A_DIM)
            except curses.error:
                pass

        # Draw OK button
        ok_text = "[ OK ]"
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(y + h - 1, x + (w - len(ok_text)) // 2, ok_text)
        self.stdscr.attroff(curses.A_REVERSE)

        self.stdscr.refresh()

        # Wait for any key
        self.wait_for_key()


class ConfirmDialog(BaseDialog):
    """Confirmation dialog with Yes/No options"""

    def show(self, title: str, message: str, default: bool = False) -> bool:
        """Show confirmation dialog and return user's choice"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Calculate ideal dialog width (responsive)
        if self.width <= 80:
            max_dialog_width = self.width - 4
            default_width = self.width - 10
        else:
            max_dialog_width = min(self.width - 10, 70)
            default_width = 50

        min_dialog_width = max(len(title) + 8, 30)
        dialog_width = min(max_dialog_width, max(min_dialog_width, default_width))

        # Wrap text
        wrapped_lines = []
        for paragraph in message.split("\n"):
            if paragraph.strip():
                wrapped = textwrap.wrap(
                    paragraph, width=dialog_width - 6, break_long_words=False, break_on_hyphens=False
                )
                wrapped_lines.extend(wrapped)
            else:
                wrapped_lines.append("")

        # Calculate height
        content_height = len(wrapped_lines)
        dialog_height = min(content_height + 7, self.height - 4)

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Draw message
        max_message_lines = h - 2  # Leave room for buttons
        for i, line in enumerate(wrapped_lines[:max_message_lines]):
            try:
                self.stdscr.addstr(y + i, x, line[:w])
            except curses.error:
                pass

        # Draw buttons
        selected = 0 if default else 1
        buttons = ["Yes", "No"]
        button_y = y + h - 1

        while True:
            # Draw buttons
            button_x = x + (w - 15) // 2
            for i, button in enumerate(buttons):
                if i == selected:
                    self.stdscr.attron(curses.A_REVERSE)

                self.stdscr.addstr(button_y, button_x + i * 8, f"[ {button} ]")

                if i == selected:
                    self.stdscr.attroff(curses.A_REVERSE)

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key in [curses.KEY_LEFT, curses.KEY_RIGHT, ord("\t")]:
                selected = 1 - selected
            elif key == ord("\n"):
                return selected == 0
            elif key == 27:  # ESC
                return False
            elif key in [ord("y"), ord("Y")]:
                return True
            elif key in [ord("n"), ord("N")]:
                return False


class HelpDialog(BaseDialog):
    """Help dialog for showing detailed help text"""

    def show(self, help_text: str) -> None:
        """Show help dialog with scrollable text"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Dialog dimensions
        dialog_width = min(70, self.width - 4)
        dialog_height = min(20, self.height - 4)

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, "Help")

        # Wrap text to fit within dialog width
        wrapped_lines = []
        for paragraph in help_text.split("\n"):
            if paragraph:
                wrapped_lines.extend(textwrap.wrap(paragraph, width=w - 2))
            else:
                wrapped_lines.append("")  # Preserve blank lines
        lines = wrapped_lines

        # Scrolling state
        scroll_offset = 0
        max_scroll = max(0, len(lines) - h + 1)

        while True:
            # Clear content area
            for i in range(h - 1):
                self.stdscr.addstr(y + i, x, " " * w)

            # Draw visible lines
            visible_lines = lines[scroll_offset : scroll_offset + h - 1]
            for i, line in enumerate(visible_lines):
                text = truncate_text(line, w)
                self.stdscr.addstr(y + i, x, text)

            # Draw scroll indicators
            if scroll_offset > 0:
                self.stdscr.addstr(y - 1, x + w - 3, "▲")
            if scroll_offset < max_scroll:
                self.stdscr.addstr(y + h - 1, x + w - 3, "▼")

            # Draw navigation hints
            if max_scroll > 0:
                nav_text = "↑/↓ Scroll, PgUp/PgDn, Q to close"
            else:
                nav_text = "Press Q or ESC to close"
            self.stdscr.addstr(y + h - 1, x, nav_text[:w])

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key in [ord("q"), ord("Q"), 27]:  # Q or ESC
                break
            elif key == curses.KEY_UP and scroll_offset > 0:
                scroll_offset -= 1
            elif key == curses.KEY_DOWN and scroll_offset < max_scroll:
                scroll_offset += 1
            elif key == curses.KEY_PPAGE:  # Page Up
                scroll_offset = max(0, scroll_offset - (h - 2))
            elif key == curses.KEY_NPAGE:  # Page Down
                scroll_offset = min(max_scroll, scroll_offset + (h - 2))
            else:
                # Ignore other keys - don't exit
                continue


class InputDialog(BaseDialog):
    """Dialog for text input"""

    def show(self, title: str, prompt: str, default: str = "") -> Optional[str]:
        """Show input dialog and return entered text"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Dialog dimensions
        dialog_width = min(60, self.width - 4)
        dialog_height = 8

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Draw prompt
        self.stdscr.addstr(y, x, truncate_text(prompt, w))

        # Input field
        input_y = y + 2
        input_x = x
        input_width = w - 2

        # Draw input box
        draw_box(self.stdscr, input_y - 1, input_x - 1, 3, input_width + 2)

        # Enable cursor
        curses.curs_set(1)

        # Input handling
        text = default
        cursor_pos = len(text)

        while True:
            # Draw current text
            display_text = text[-input_width + 1 :] if len(text) > input_width - 1 else text
            self.stdscr.addstr(input_y, input_x, " " * input_width)
            self.stdscr.addstr(input_y, input_x, display_text)

            # Position cursor
            cursor_x = input_x + min(cursor_pos, input_width - 1)
            self.stdscr.move(input_y, cursor_x)

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == ord("\n"):
                curses.curs_set(0)
                return text
            elif key == 27:  # ESC
                curses.curs_set(0)
                return None
            elif key in [curses.KEY_BACKSPACE, 127]:
                if cursor_pos > 0:
                    text = text[: cursor_pos - 1] + text[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:  # Delete
                if cursor_pos < len(text):
                    text = text[:cursor_pos] + text[cursor_pos + 1 :]
            elif key == curses.KEY_LEFT:
                cursor_pos = max(0, cursor_pos - 1)
            elif key == curses.KEY_RIGHT:
                cursor_pos = min(len(text), cursor_pos + 1)
            elif key == curses.KEY_HOME:
                cursor_pos = 0
            elif key == curses.KEY_END:
                cursor_pos = len(text)
            elif 32 <= key <= 126:  # Printable characters
                text = text[:cursor_pos] + chr(key) + text[cursor_pos:]
                cursor_pos += 1


class SliderDialog(BaseDialog):
    """Dialog for adjusting numeric values with a slider"""

    def show(
        self, title: str, current_value: int, min_value: int = 0, max_value: int = 100, step: int = 1, unit: str = ""
    ) -> Optional[int]:
        """Show slider dialog and return selected value"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Dialog dimensions
        dialog_width = min(60, self.width - 4)
        dialog_height = 10

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Initialize value
        value = current_value

        while True:
            # Clear content area
            for i in range(h):
                self.stdscr.addstr(y + i, x, " " * w)

            # Draw current value
            value_text = f"Value: {value}{unit}"
            self.stdscr.addstr(y, x + (w - len(value_text)) // 2, value_text)

            # Draw slider
            slider_y = y + 2
            slider_width = w - 10
            slider_x = x + 5

            # Calculate slider position
            range_size = max_value - min_value
            normalized_value = (value - min_value) / range_size if range_size > 0 else 0
            slider_pos = int(normalized_value * (slider_width - 1))

            # Draw slider track
            self.stdscr.addstr(slider_y, slider_x - 1, "[")
            for i in range(slider_width):
                if i == slider_pos:
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(slider_y, slider_x + i, "●")
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(slider_y, slider_x + i, "─")
            self.stdscr.addstr(slider_y, slider_x + slider_width, "]")

            # Draw min/max values
            min_text = str(min_value)
            max_text = str(max_value)
            self.stdscr.addstr(slider_y + 1, slider_x, min_text)
            self.stdscr.addstr(slider_y + 1, slider_x + slider_width - len(max_text), max_text)

            # Draw instructions
            instructions = "← → or -/+ to adjust, Enter to confirm, ESC to cancel"
            self.stdscr.addstr(y + h - 2, x, truncate_text(instructions, w))

            # Draw quick jump hints
            quick_hints = "Home: Min, End: Max, PgUp/PgDn: ±10"
            self.stdscr.addstr(y + h - 1, x, truncate_text(quick_hints, w))

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == ord("\n"):
                return value
            elif key == 27:  # ESC
                return None
            elif key in [curses.KEY_LEFT, ord("-"), ord("_")]:
                value = max(min_value, value - step)
            elif key in [curses.KEY_RIGHT, ord("+"), ord("=")]:
                value = min(max_value, value + step)
            elif key == curses.KEY_HOME:
                value = min_value
            elif key == curses.KEY_END:
                value = max_value
            elif key == curses.KEY_PPAGE:  # Page Up
                value = min(max_value, value + 10 * step)
            elif key == curses.KEY_NPAGE:  # Page Down
                value = max(min_value, value - 10 * step)
            elif ord("0") <= key <= ord("9"):
                # Direct numeric input
                digit = key - ord("0")
                new_value = digit
                # Collect more digits
                self.stdscr.nodelay(True)
                try:
                    while True:
                        next_key = self.stdscr.getch()
                        if ord("0") <= next_key <= ord("9"):
                            new_value = new_value * 10 + (next_key - ord("0"))
                        else:
                            if next_key != -1:  # Put back non-digit key
                                curses.ungetch(next_key)
                            break
                finally:
                    self.stdscr.nodelay(False)

                # Clamp to valid range
                value = max(min_value, min(max_value, new_value))


class SpinnerDialog(BaseDialog):
    """Dialog for selecting discrete numeric values with up/down arrows"""

    def show(self, title: str, current_value: int, values: List[int], unit: str = "") -> Optional[int]:
        """Show spinner dialog and return selected value"""
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Dialog dimensions
        dialog_width = min(40, self.width - 4)
        dialog_height = 8

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Find current index
        try:
            current_index = values.index(current_value)
        except ValueError:
            current_index = 0

        while True:
            # Clear content area
            for i in range(h):
                self.stdscr.addstr(y + i, x, " " * w)

            # Draw spinner
            spinner_y = y + 2
            value = values[current_index]

            # Draw up arrow (if not at top)
            if current_index > 0:
                self.stdscr.addstr(spinner_y - 1, x + w // 2, "▲")

            # Draw current value in a box
            value_text = f" {value}{unit} "
            value_x = x + (w - len(value_text)) // 2
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr(spinner_y, value_x, value_text)
            self.stdscr.attroff(curses.A_REVERSE)

            # Draw down arrow (if not at bottom)
            if current_index < len(values) - 1:
                self.stdscr.addstr(spinner_y + 1, x + w // 2, "▼")

            # Draw instructions
            instructions = "↑↓ to change, Enter to confirm, ESC to cancel"
            self.stdscr.addstr(y + h - 1, x, truncate_text(instructions, w))

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == ord("\n"):
                return values[current_index]
            elif key == 27:  # ESC
                return None
            elif key in [curses.KEY_UP, ord("k")]:
                current_index = max(0, current_index - 1)
            elif key in [curses.KEY_DOWN, ord("j")]:
                current_index = min(len(values) - 1, current_index + 1)
            elif key == curses.KEY_HOME:
                current_index = 0
            elif key == curses.KEY_END:
                current_index = len(values) - 1


class SelectDialog(BaseDialog):
    """Dialog for selecting from a list of options"""

    def show(
        self, title: str, message: str = None, options: List[str] = None, current_value: str = None
    ) -> Optional[int]:
        """Show selection dialog and return selected option index

        Args:
            title: Dialog title
            message: Optional message to display above options (can be a string or None)
            options: List of options to choose from (can be a list or passed as message if message is actually the list)
            current_value: Currently selected value (optional)

        Returns:
            Index of selected option (0-based) or None if cancelled
        """
        # Handle the case where message is actually the options list (backward compatibility)
        if isinstance(message, list) and options is None:
            options = message
            message = None
        elif isinstance(options, str) and isinstance(message, str):
            # They passed (title, message, options) correctly but options is a string - swap them
            message, options = options, [message] if not isinstance(message, list) else message

        # Ensure options is a list
        if not isinstance(options, list):
            options = [str(options)] if options else []

        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()

        # Calculate dimensions
        max_option_len = max(len(opt) for opt in options) if options else 20
        message_lines = message.split("\n") if message else []
        max_message_len = max(len(line) for line in message_lines) if message_lines else 0

        dialog_width = min(max(50, max_option_len + 10, max_message_len + 10), self.width - 4)
        message_height = len(message_lines) + 1 if message else 0
        dialog_height = min(len(options) + message_height + 6, self.height - 4, 20)

        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)

        # Draw message if provided
        message_end_y = y
        if message:
            for i, line in enumerate(message_lines):
                if i < h - len(options) - 3:
                    self.stdscr.addstr(y + i, x + 2, truncate_text(line, w - 4))
                    message_end_y = y + i + 1

        # Find current selection
        current_index = 0
        if current_value and current_value in options:
            current_index = options.index(current_value)

        # Scrolling state - account for message space
        message_space = message_end_y - y if message else 0
        visible_items = h - 3 - message_space
        scroll_offset = 0

        while True:
            # Clear content area
            for i in range(h):
                self.stdscr.addstr(y + i, x, " " * w)

            # Calculate visible range
            if current_index < scroll_offset:
                scroll_offset = current_index
            elif current_index >= scroll_offset + visible_items:
                scroll_offset = current_index - visible_items + 1

            # Draw visible options (after the message if present)
            options_start_y = message_end_y if message else y
            for i in range(visible_items):
                option_index = scroll_offset + i
                if option_index >= len(options):
                    break

                option = options[option_index]
                display_y = options_start_y + i + 1

                if option_index == current_index:
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(display_y, x + 2, f"> {option}".ljust(w - 4))
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(display_y, x + 2, f"  {option}")

            # Draw scroll indicators
            if scroll_offset > 0:
                self.stdscr.addstr(y, x + w - 3, "▲")
            if scroll_offset + visible_items < len(options):
                self.stdscr.addstr(y + h - 2, x + w - 3, "▼")

            # Draw instructions
            instructions = "↑↓ to select, Enter to confirm, ESC to cancel"
            self.stdscr.addstr(y + h - 1, x, truncate_text(instructions, w))

            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()

            if key == ord("\n"):
                return current_index  # Return index instead of string
            elif key == 27:  # ESC
                return None
            elif key in [curses.KEY_UP, ord("k")]:
                current_index = max(0, current_index - 1)
            elif key in [curses.KEY_DOWN, ord("j")]:
                current_index = min(len(options) - 1, current_index + 1)
            elif key == curses.KEY_HOME:
                current_index = 0
            elif key == curses.KEY_END:
                current_index = len(options) - 1
            elif key == curses.KEY_PPAGE:  # Page Up
                current_index = max(0, current_index - visible_items)
            elif key == curses.KEY_NPAGE:  # Page Down
                current_index = min(len(options) - 1, current_index + visible_items)
