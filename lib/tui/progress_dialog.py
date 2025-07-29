#!/usr/bin/env python3
"""
Progress dialog for showing real-time command output in TUI
"""

import curses
import subprocess
import threading
import queue
from typing import Optional, List, Callable
import time

from .constants import DIALOG_WIDTH, DIALOG_HEIGHT
from .utils import draw_box, get_dialog_position, draw_centered_text


class ProgressDialog:
    """Show progress of long-running operations in TUI"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.output_lines: List[str] = []
        self.is_running = False
        self.exit_code: Optional[int] = None
        self.output_queue = queue.Queue()
        
    def run_command(self, command: List[str], title: str = "Processing...", 
                   show_output: bool = True, sudo_dialog=None) -> int:
        """Run a command and show progress in dialog"""
        self.is_running = True
        self.exit_code = None
        self.output_lines = []
        
        # Calculate dialog size (larger for output)
        dialog_height = min(self.height - 4, 20)
        dialog_width = min(self.width - 10, 80)
        y, x = get_dialog_position(self.height, self.width, dialog_height, dialog_width)
        
        # Start command in background thread
        cmd_thread = threading.Thread(
            target=self._run_command_thread,
            args=(command, sudo_dialog)
        )
        cmd_thread.daemon = True
        cmd_thread.start()
        
        # Show progress dialog
        while self.is_running or not self.output_queue.empty():
            # Clear and draw dialog
            self.stdscr.clear()
            draw_box(self.stdscr, y, x, dialog_height, dialog_width, title)
            
            # Process output queue
            while not self.output_queue.empty():
                try:
                    line = self.output_queue.get_nowait()
                    self.output_lines.append(line)
                    # Keep only last N lines that fit in dialog
                    max_lines = dialog_height - 6
                    if len(self.output_lines) > max_lines:
                        self.output_lines = self.output_lines[-max_lines:]
                except queue.Empty:
                    break
            
            # Draw output lines
            if show_output:
                output_y = y + 2
                for i, line in enumerate(self.output_lines):
                    if i >= dialog_height - 6:
                        break
                    # Truncate long lines
                    display_line = line[:dialog_width - 6]
                    try:
                        self.stdscr.addstr(output_y + i, x + 3, display_line)
                    except curses.error:
                        pass
            
            # Draw status
            status_y = y + dialog_height - 3
            if self.is_running:
                # Animated spinner
                spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'][int(time.time() * 10) % 8]
                status = f"{spinner} Running..."
                self.stdscr.addstr(status_y, x + 3, status, curses.A_BOLD)
            else:
                if self.exit_code == 0:
                    status = "✓ Completed successfully"
                    try:
                        self.stdscr.addstr(status_y, x + 3, status, curses.A_BOLD)
                    except:
                        self.stdscr.addstr(status_y, x + 3, status)
                else:
                    status = f"✗ Failed (exit code: {self.exit_code})"
                    try:
                        self.stdscr.addstr(status_y, x + 3, status, curses.A_BOLD)
                    except:
                        self.stdscr.addstr(status_y, x + 3, status)
            
            # Draw continue prompt if done
            if not self.is_running:
                prompt = "Press any key to continue..."
                prompt_y = y + dialog_height - 2
                draw_centered_text(self.stdscr, prompt_y, prompt, x, dialog_width)
            
            self.stdscr.refresh()
            
            # Check for user input
            self.stdscr.timeout(100)  # 100ms timeout
            key = self.stdscr.getch()
            if key != -1 and not self.is_running:
                break
        
        # Reset timeout
        self.stdscr.timeout(-1)
        
        # Wait for thread to complete
        cmd_thread.join(timeout=1.0)
        
        return self.exit_code or 1
    
    def _run_command_thread(self, command: List[str], sudo_dialog=None):
        """Run command in background thread"""
        try:
            # Handle sudo commands specially
            if command[0] == 'sudo' and sudo_dialog:
                # Use sudo dialog to get password
                result = sudo_dialog.execute_with_sudo(
                    command[1:],  # Remove 'sudo' from command
                    show_output=False  # We'll handle output ourselves
                )
                if result:
                    # Queue output lines
                    for line in result.stdout.splitlines():
                        self.output_queue.put(line)
                    for line in result.stderr.splitlines():
                        self.output_queue.put(f"ERROR: {line}")
                    self.exit_code = result.returncode
                else:
                    self.exit_code = 1
            else:
                # Run non-sudo command normally
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output line by line
                for line in process.stdout:
                    line = line.rstrip()
                    if line:
                        self.output_queue.put(line)
                
                # Wait for completion
                self.exit_code = process.wait()
                
        except Exception as e:
            self.output_queue.put(f"ERROR: {str(e)}")
            self.exit_code = 1
        finally:
            self.is_running = False
    
    def show_message(self, title: str, message: str, wait_for_key: bool = True):
        """Show a simple message dialog"""
        # Calculate dialog size
        lines = message.split('\n')
        dialog_height = min(len(lines) + 6, self.height - 4)
        dialog_width = min(max(len(line) for line in lines) + 6, self.width - 10, 60)
        dialog_width = max(dialog_width, len(title) + 10)
        
        y, x = get_dialog_position(self.height, self.width, dialog_height, dialog_width)
        
        # Draw dialog
        self.stdscr.clear()
        draw_box(self.stdscr, y, x, dialog_height, dialog_width, title)
        
        # Draw message lines
        msg_y = y + 2
        for i, line in enumerate(lines):
            if i >= dialog_height - 4:
                break
            try:
                self.stdscr.addstr(msg_y + i, x + 3, line[:dialog_width - 6])
            except curses.error:
                pass
        
        if wait_for_key:
            # Draw prompt
            prompt = "Press any key to continue..."
            prompt_y = y + dialog_height - 2
            draw_centered_text(self.stdscr, prompt_y, prompt, x, dialog_width)
            
            self.stdscr.refresh()
            self.stdscr.getch()
        else:
            self.stdscr.refresh()