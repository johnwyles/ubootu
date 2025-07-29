#!/usr/bin/env python3
"""
Curses-based sudo password dialog
Never drops to console for password input
"""

import curses
import subprocess
from typing import Optional

from .constants import SUDO_DIALOG_WIDTH, SUDO_DIALOG_HEIGHT
from .utils import draw_box, get_dialog_position


class SudoDialog:
    """Curses-based sudo password dialog"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.enable_caching = False
        self._cached_password: Optional[str] = None
        
    def get_password(self, message: str = "Enter sudo password:") -> Optional[str]:
        """Show password dialog and return password"""
        # Return cached password if available
        if self.enable_caching and self._cached_password is not None:
            return self._cached_password
            
        # Clear and redraw
        self.stdscr.clear()
        self.stdscr.refresh()
        
        # Dialog position
        dialog_height = SUDO_DIALOG_HEIGHT
        dialog_width = SUDO_DIALOG_WIDTH
        y, x = get_dialog_position(self.height, self.width, dialog_height, dialog_width)
        
        # Draw dialog box
        draw_box(self.stdscr, y, x, dialog_height, dialog_width, "Authentication Required")
        
        # Draw message
        msg_y = y + 2
        msg_x = x + 2
        self.stdscr.addstr(msg_y, msg_x, message[:dialog_width-4])
        
        # Password input field
        input_y = msg_y + 2
        input_x = msg_x
        input_width = dialog_width - 6
        
        # Draw input field border
        draw_box(self.stdscr, input_y - 1, input_x - 1, 3, input_width + 2)
        
        # Enable cursor (temporarily)
        curses.curs_set(1)
        curses.echo(0)  # Disable echo
        
        # Collect password
        password = ""
        cursor_pos = 0
        
        while True:
            # Display asterisks for password
            display = '*' * len(password)
            self.stdscr.addstr(input_y, input_x, " " * input_width)
            self.stdscr.addstr(input_y, input_x, display[:input_width-1])
            
            # Position cursor
            self.stdscr.move(input_y, input_x + min(cursor_pos, input_width - 1))
            self.stdscr.refresh()
            
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                curses.curs_set(0)
                return None
                
            if key == ord('\n'):  # Enter
                break
            elif key == 27:  # ESC
                curses.curs_set(0)
                return None
            elif key in [curses.KEY_BACKSPACE, 127]:  # Backspace
                if cursor_pos > 0:
                    password = password[:cursor_pos-1] + password[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:  # Delete
                if cursor_pos < len(password):
                    password = password[:cursor_pos] + password[cursor_pos+1:]
            elif key == curses.KEY_LEFT:
                cursor_pos = max(0, cursor_pos - 1)
            elif key == curses.KEY_RIGHT:
                cursor_pos = min(len(password), cursor_pos + 1)
            elif key == curses.KEY_HOME:
                cursor_pos = 0
            elif key == curses.KEY_END:
                cursor_pos = len(password)
            elif 32 <= key <= 126:  # Printable characters
                password = password[:cursor_pos] + chr(key) + password[cursor_pos:]
                cursor_pos += 1
                
        # Hide cursor again
        curses.curs_set(0)
        
        # Cache if enabled
        if self.enable_caching:
            self._cached_password = password
            
        return password
        
    def clear_cache(self) -> None:
        """Clear cached password"""
        self._cached_password = None
        
    def execute_with_sudo(self, command: str, show_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Execute a command with sudo using the password dialog"""
        password = self.get_password()
        if password is None:
            return None
            
        # Prepare sudo command
        sudo_cmd = ['sudo', '-S']  # -S reads password from stdin
        
        # Add the actual command
        if isinstance(command, str):
            sudo_cmd.extend(command.split())
        else:
            sudo_cmd.extend(command)
            
        try:
            # Execute with password on stdin
            result = subprocess.run(
                sudo_cmd,
                input=password + '\n',
                text=True,
                capture_output=True
            )
            
            if show_output and result.returncode != 0:
                # Show error in a dialog
                from .dialogs import MessageDialog
                dialog = MessageDialog(self.stdscr)
                error_msg = f"Command failed:\n{result.stderr[:200]}"
                dialog.show("Error", error_msg, "error")
                
            return result
            
        except Exception as e:
            # Show error in a dialog
            from .dialogs import MessageDialog
            dialog = MessageDialog(self.stdscr)
            dialog.show("Error", f"Failed to execute command:\n{str(e)}", "error")
            return None
            
    def test_sudo_password(self, password: str) -> bool:
        """Test if a password is valid for sudo"""
        try:
            result = subprocess.run(
                ['sudo', '-S', 'true'],
                input=password + '\n',
                text=True,
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False