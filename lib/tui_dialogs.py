#!/usr/bin/env python3
"""
TUI Dialog Components for Ubootu
Reusable curses-based dialogs for user interactions
"""

import curses
import textwrap
from typing import List, Tuple, Optional, Dict, Any
from tui_components import KeyHintBar, HelpOverlay


class TUIDialog:
    """Base class for TUI dialogs"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)  # Hide cursor
        self.key_hints = KeyHintBar(stdscr)
        self.help_overlay = HelpOverlay(stdscr)
        
    def draw_box(self, y, x, h, w, title=""):
        """Draw a box with optional title"""
        try:
            # Draw corners
            self.stdscr.addch(y, x, curses.ACS_ULCORNER)
            self.stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
            self.stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
            self.stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
            
            # Draw horizontal lines
            for i in range(1, w - 1):
                self.stdscr.addch(y, x + i, curses.ACS_HLINE)
                self.stdscr.addch(y + h - 1, x + i, curses.ACS_HLINE)
            
            # Draw vertical lines
            for i in range(1, h - 1):
                self.stdscr.addch(y + i, x, curses.ACS_VLINE)
                self.stdscr.addch(y + i, x + w - 1, curses.ACS_VLINE)
            
            # Draw title if provided
            if title:
                title = f" {title} "
                title_x = x + (w - len(title)) // 2
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(y, title_x, title)
                self.stdscr.attroff(curses.A_BOLD)
                
        except curses.error:
            pass
            
    def center_text(self, y, text, attrs=0):
        """Draw centered text at given y position"""
        try:
            x = (self.width - len(text)) // 2
            self.stdscr.addstr(y, x, text, attrs)
        except curses.error:
            pass


class ListDialog(TUIDialog):
    """Dialog for selecting from a list of options"""
    
    def show(self, title: str, items: List[Tuple[str, str]], 
             multi_select: bool = False, selected_items: List[str] = None) -> List[str]:
        """
        Show list selection dialog
        
        Args:
            title: Dialog title
            items: List of (id, display_name) tuples
            multi_select: Allow multiple selections
            selected_items: Pre-selected item IDs
            
        Returns:
            List of selected item IDs
        """
        if selected_items is None:
            selected_items = []
            
        selected = set(selected_items)
        current = 0
        scroll_offset = 0
        
        # Calculate dialog dimensions
        dialog_width = min(80, self.width - 4)
        dialog_height = min(20, self.height - 4)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2
        
        # Calculate list area
        list_start_y = dialog_y + 3
        list_height = dialog_height - 6
        
        while True:
            self.stdscr.clear()
            
            # Draw dialog box
            self.draw_box(dialog_y, dialog_x, dialog_height, dialog_width, title)
            
            # Draw key hints at bottom - Help first for visibility
            if multi_select:
                hints = [
                    ("H", "Help"),
                    ("↑↓", "Navigate"),
                    ("SPACE", "Toggle"),
                    ("ENTER", "Confirm"),
                    ("ESC", "Cancel")
                ]
            else:
                hints = [
                    ("H", "Help"),
                    ("↑↓", "Navigate"),
                    ("ENTER", "Select"),
                    ("ESC", "Cancel")
                ]
            self.key_hints.draw(hints, self.height - 1)
            
            # Draw list items
            visible_items = items[scroll_offset:scroll_offset + list_height]
            for i, (item_id, display_name) in enumerate(visible_items):
                y = list_start_y + i
                x = dialog_x + 3
                
                # Truncate display name if too long
                max_width = dialog_width - 8
                if len(display_name) > max_width:
                    display_name = display_name[:max_width-3] + "..."
                
                # Draw selection indicator
                if multi_select:
                    indicator = "[X]" if item_id in selected else "[ ]"
                    self.stdscr.addstr(y, x, indicator)
                    x += 4
                
                # Draw item text
                attrs = curses.A_REVERSE if i + scroll_offset == current else 0
                self.stdscr.addstr(y, x, display_name, attrs)
            
            # Draw scroll indicators
            if scroll_offset > 0:
                self.stdscr.addstr(list_start_y - 1, dialog_x + dialog_width - 3, "↑")
            if scroll_offset + list_height < len(items):
                self.stdscr.addstr(list_start_y + list_height, dialog_x + dialog_width - 3, "↓")
            
            self.stdscr.refresh()
            
            # Handle input
            key = self.stdscr.getch()
            
            if key == 27:  # ESC
                return []
            elif key in [ord('h'), ord('H')]:  # Help
                help_content = [
                    "List Selection Help",
                    "Use arrow keys to navigate through the list."
                ]
                if multi_select:
                    help_content.extend([
                        "Multi-select mode:",
                        "• Press SPACE to toggle selection",
                        "• Selected items show [X]",
                        "• Press ENTER to confirm all selections",
                        "• Press ESC to cancel without saving"
                    ])
                else:
                    help_content.extend([
                        "Single-select mode:",
                        "• Press ENTER to select highlighted item",
                        "• Press ESC to cancel without selecting"
                    ])
                help_content.extend([
                    "Tips:",
                    "• Items may have scroll indicators (↑↓)",
                    "• Long items are truncated with ..."
                ])
                self.help_overlay.show("List Selection Help", help_content)
            elif key == ord('\n'):  # Enter
                if multi_select:
                    return list(selected)
                else:
                    return [items[current][0]]
            elif key == ord(' ') and multi_select:  # Space
                item_id = items[current][0]
                if item_id in selected:
                    selected.remove(item_id)
                else:
                    selected.add(item_id)
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


class TextInputDialog(TUIDialog):
    """Dialog for text input"""
    
    def show(self, title: str, prompt: str, default: str = "") -> Optional[str]:
        """
        Show text input dialog
        
        Args:
            title: Dialog title
            prompt: Input prompt
            default: Default value
            
        Returns:
            User input or None if cancelled
        """
        # Calculate dialog dimensions
        dialog_width = min(60, self.width - 4)
        dialog_height = 8
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2
        
        # Input position
        input_y = dialog_y + 4
        input_x = dialog_x + 3
        input_width = dialog_width - 6
        
        # Initialize input
        text = default
        cursor_pos = len(text)
        
        # Enable cursor
        curses.curs_set(1)
        
        while True:
            self.stdscr.clear()
            
            # Draw dialog box
            self.draw_box(dialog_y, dialog_x, dialog_height, dialog_width, title)
            
            # Draw prompt
            wrapped_prompt = textwrap.wrap(prompt, dialog_width - 6)
            for i, line in enumerate(wrapped_prompt[:2]):  # Max 2 lines
                self.stdscr.addstr(dialog_y + 2 + i, dialog_x + 3, line)
            
            # Draw input field
            self.stdscr.addstr(input_y, input_x - 1, "[")
            self.stdscr.addstr(input_y, input_x + input_width, "]")
            
            # Draw text (with scrolling if needed)
            display_text = text
            if len(text) > input_width:
                if cursor_pos < input_width:
                    display_text = text[:input_width]
                else:
                    display_text = text[cursor_pos - input_width + 1:cursor_pos + 1]
            
            self.stdscr.addstr(input_y, input_x, display_text[:input_width])
            
            # Position cursor
            if len(text) <= input_width:
                cursor_x = input_x + cursor_pos
            else:
                cursor_x = input_x + min(cursor_pos, input_width - 1)
            self.stdscr.move(input_y, cursor_x)
            
            # Draw key hints - Help first for visibility
            hints = [
                ("H", "Help"),
                ("←→", "Move"),
                ("BACKSPACE", "Delete"),
                ("ENTER", "Confirm"),
                ("ESC", "Cancel")
            ]
            self.key_hints.draw(hints, self.height - 1)
            
            self.stdscr.refresh()
            
            # Handle input
            key = self.stdscr.getch()
            
            if key == 27:  # ESC
                curses.curs_set(0)
                return None
            elif key in [ord('h'), ord('H')]:  # Help
                help_content = [
                    "Text Input Help",
                    "Enter text using your keyboard.",
                    "Navigation:",
                    "• ← → - Move cursor left/right",
                    "• HOME - Jump to beginning",
                    "• END - Jump to end",
                    "Editing:",
                    "• BACKSPACE - Delete character before cursor",
                    "• DELETE - Delete character at cursor",
                    "• ENTER - Confirm input",
                    "• ESC - Cancel without saving"
                ]
                self.help_overlay.show("Text Input Help", help_content)
            elif key == ord('\n'):  # Enter
                curses.curs_set(0)
                return text
            elif key == curses.KEY_BACKSPACE or key == 127:
                if cursor_pos > 0:
                    text = text[:cursor_pos-1] + text[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:  # Delete
                if cursor_pos < len(text):
                    text = text[:cursor_pos] + text[cursor_pos+1:]
            elif key == curses.KEY_LEFT:
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif key == curses.KEY_RIGHT:
                if cursor_pos < len(text):
                    cursor_pos += 1
            elif key == curses.KEY_HOME:
                cursor_pos = 0
            elif key == curses.KEY_END:
                cursor_pos = len(text)
            elif 32 <= key <= 126:  # Printable characters
                text = text[:cursor_pos] + chr(key) + text[cursor_pos:]
                cursor_pos += 1


class ConfirmDialog(TUIDialog):
    """Dialog for yes/no confirmation"""
    
    def show(self, title: str, message: str, default: bool = True) -> bool:
        """
        Show confirmation dialog
        
        Args:
            title: Dialog title
            message: Confirmation message
            default: Default selection
            
        Returns:
            True if confirmed, False otherwise
        """
        # Calculate dialog dimensions
        dialog_width = min(60, self.width - 4)
        dialog_height = 10
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2
        
        selected = 0 if default else 1
        
        while True:
            self.stdscr.clear()
            
            # Draw dialog box
            self.draw_box(dialog_y, dialog_x, dialog_height, dialog_width, title)
            
            # Draw message
            wrapped_message = textwrap.wrap(message, dialog_width - 6)
            for i, line in enumerate(wrapped_message[:4]):  # Max 4 lines
                self.stdscr.addstr(dialog_y + 2 + i, dialog_x + 3, line)
            
            # Draw buttons
            button_y = dialog_y + dialog_height - 3
            buttons = ["Yes", "No"]
            button_spacing = 10
            total_width = len(buttons[0]) + len(buttons[1]) + button_spacing
            button_x = dialog_x + (dialog_width - total_width) // 2
            
            for i, button in enumerate(buttons):
                x = button_x + i * (len(buttons[0]) + button_spacing)
                attrs = curses.A_REVERSE if i == selected else 0
                self.stdscr.addstr(button_y, x, f"[ {button} ]", attrs)
            
            # Draw key hints - Help first for visibility
            hints = [
                ("H", "Help"),
                ("TAB/←→", "Switch"),
                ("ENTER", "Select"),
                ("ESC", "Cancel")
            ]
            self.key_hints.draw(hints, self.height - 1)
            
            self.stdscr.refresh()
            
            # Handle input
            key = self.stdscr.getch()
            
            if key == 27:  # ESC
                return False
            elif key in [ord('h'), ord('H')]:  # Help
                help_content = [
                    "Confirmation Dialog Help",
                    "Choose Yes or No for the confirmation.",
                    "Navigation:",
                    "• TAB or Arrow Keys - Switch between Yes/No",
                    "• ENTER - Select highlighted option",
                    "• ESC - Cancel (same as selecting No)",
                    "The highlighted button shows in reverse colors."
                ]
                self.help_overlay.show("Confirmation Help", help_content)
            elif key == ord('\n'):  # Enter
                return selected == 0
            elif key in [ord('\t'), curses.KEY_LEFT, curses.KEY_RIGHT]:
                selected = 1 - selected


class MessageDialog(TUIDialog):
    """Dialog for displaying messages"""
    
    def show(self, title: str, message: str, dialog_type: str = "info"):
        """
        Show message dialog
        
        Args:
            title: Dialog title
            message: Message to display
            dialog_type: Type of dialog (info, warning, error)
        """
        # Calculate dialog dimensions
        dialog_width = min(70, self.width - 4)
        wrapped_message = textwrap.wrap(message, dialog_width - 6)
        dialog_height = min(len(wrapped_message) + 6, self.height - 4)
        dialog_y = (self.height - dialog_height) // 2
        dialog_x = (self.width - dialog_width) // 2
        
        # Draw dialog
        self.stdscr.clear()
        self.draw_box(dialog_y, dialog_x, dialog_height, dialog_width, title)
        
        # Draw icon based on type
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌"
        }
        icon = icons.get(dialog_type, "ℹ️")
        
        # Draw message
        for i, line in enumerate(wrapped_message[:dialog_height - 6]):
            self.stdscr.addstr(dialog_y + 2 + i, dialog_x + 3, line)
        
        # Draw instruction
        self.center_text(dialog_y + dialog_height - 2, "Press any key to continue", curses.A_DIM)
        
        self.stdscr.refresh()
        self.stdscr.getch()


class ProgressDialog(TUIDialog):
    """Dialog for showing progress"""
    
    def __init__(self, stdscr, title: str, message: str = ""):
        super().__init__(stdscr)
        self.title = title
        self.message = message
        self.progress = 0
        self.status = ""
        
        # Calculate dialog dimensions
        self.dialog_width = min(60, self.width - 4)
        self.dialog_height = 8
        self.dialog_y = (self.height - self.dialog_height) // 2
        self.dialog_x = (self.width - self.dialog_width) // 2
        
    def update(self, progress: int, status: str = ""):
        """Update progress (0-100) and status message"""
        self.progress = max(0, min(100, progress))
        self.status = status
        self.draw()
        
    def draw(self):
        """Draw the progress dialog"""
        self.stdscr.clear()
        
        # Draw dialog box
        self.draw_box(self.dialog_y, self.dialog_x, self.dialog_height, self.dialog_width, self.title)
        
        # Draw message
        if self.message:
            self.center_text(self.dialog_y + 2, self.message)
        
        # Draw progress bar
        bar_width = self.dialog_width - 10
        bar_y = self.dialog_y + 4
        bar_x = self.dialog_x + 5
        
        filled = int(self.progress * bar_width / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        self.stdscr.addstr(bar_y, bar_x - 1, "[")
        self.stdscr.addstr(bar_y, bar_x, bar)
        self.stdscr.addstr(bar_y, bar_x + bar_width, "]")
        self.stdscr.addstr(bar_y, bar_x + bar_width + 2, f"{self.progress}%")
        
        # Draw status
        if self.status:
            truncated = self.status[:self.dialog_width - 6]
            self.center_text(bar_y + 1, truncated, curses.A_DIM)
        
        self.stdscr.refresh()