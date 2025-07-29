#!/usr/bin/env python3
"""
Dialog components for the unified TUI
"""

import curses
import textwrap
from typing import Optional, List

from .constants import DIALOG_WIDTH, DIALOG_HEIGHT
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
        
        # Calculate dialog size based on message
        lines = message.split('\n')
        dialog_width = min(max(len(title) + 4, max(len(line) for line in lines) + 4, 40), self.width - 4)
        dialog_height = min(len(lines) + 6, self.height - 4)
        
        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)
        
        # Draw message
        for i, line in enumerate(lines[:h]):
            text = truncate_text(line, w)
            self.stdscr.addstr(y + i, x, text)
            
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
        
        # Calculate dialog size
        lines = message.split('\n')
        dialog_width = min(max(len(title) + 4, max(len(line) for line in lines) + 4, 50), self.width - 4)
        dialog_height = min(len(lines) + 7, self.height - 4)
        
        # Draw dialog
        y, x, h, w = self.draw_dialog_box(dialog_height, dialog_width, title)
        
        # Draw message
        for i, line in enumerate(lines[:h-2]):
            text = truncate_text(line, w)
            self.stdscr.addstr(y + i, x, text)
            
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
            
            if key in [curses.KEY_LEFT, curses.KEY_RIGHT, ord('\t')]:
                selected = 1 - selected
            elif key == ord('\n'):
                return selected == 0
            elif key == 27:  # ESC
                return False
            elif key in [ord('y'), ord('Y')]:
                return True
            elif key in [ord('n'), ord('N')]:
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
        for paragraph in help_text.split('\n'):
            if paragraph:
                wrapped_lines.extend(textwrap.wrap(paragraph, width=w-2))
            else:
                wrapped_lines.append('')  # Preserve blank lines
        lines = wrapped_lines
        
        # Scrolling state
        scroll_offset = 0
        max_scroll = max(0, len(lines) - h + 1)
        
        while True:
            # Clear content area
            for i in range(h - 1):
                self.stdscr.addstr(y + i, x, " " * w)
                
            # Draw visible lines
            visible_lines = lines[scroll_offset:scroll_offset + h - 1]
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
            
            if key in [ord('q'), ord('Q'), 27]:  # Q or ESC
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
            display_text = text[-input_width+1:] if len(text) > input_width - 1 else text
            self.stdscr.addstr(input_y, input_x, " " * input_width)
            self.stdscr.addstr(input_y, input_x, display_text)
            
            # Position cursor
            cursor_x = input_x + min(cursor_pos, input_width - 1)
            self.stdscr.move(input_y, cursor_x)
            
            self.stdscr.refresh()
            
            # Handle input
            key = self.stdscr.getch()
            
            if key == ord('\n'):
                curses.curs_set(0)
                return text
            elif key == 27:  # ESC
                curses.curs_set(0)
                return None
            elif key in [curses.KEY_BACKSPACE, 127]:
                if cursor_pos > 0:
                    text = text[:cursor_pos-1] + text[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:  # Delete
                if cursor_pos < len(text):
                    text = text[:cursor_pos] + text[cursor_pos+1:]
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