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
import os
import sys

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
        self.current_task = "Initializing..."
        self.task_count = 0
        self.completed_tasks = 0
        
    def run_command(self, command: List[str], title: str = "Processing...", 
                   show_output: bool = True, sudo_dialog=None, env=None) -> int:
        """Run a command and show progress in dialog"""
        self.is_running = True
        self.exit_code = None
        self.output_lines = []
        self.current_task = "Initializing Ansible..."
        self.completed_tasks = 0
        
        # Calculate dialog size (larger for output)
        dialog_height = min(self.height - 4, 20)
        dialog_width = min(self.width - 10, 80)
        y, x = get_dialog_position(self.height, self.width, dialog_height, dialog_width)
        
        # Start command in background thread
        cmd_thread = threading.Thread(
            target=self._run_command_thread,
            args=(command, sudo_dialog, env)
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
            
            # Draw current task info
            task_y = y + 2
            if self.is_running and self.current_task:
                # Show current task
                task_text = f"Current: {self.current_task}"
                # Truncate if too long
                max_len = dialog_width - 10
                if len(task_text) > max_len:
                    task_text = task_text[:max_len-3] + "..."
                try:
                    self.stdscr.addstr(task_y, x + 3, task_text, curses.A_BOLD)
                except curses.error:
                    pass
                
                # Show task count if available
                if self.completed_tasks > 0:
                    count_text = f"Tasks completed: {self.completed_tasks}"
                    try:
                        self.stdscr.addstr(task_y + 1, x + 3, count_text)
                    except curses.error:
                        pass
            
            # Adjust output area to make room for task info
            if show_output:
                output_y = y + 4 if self.is_running else y + 2
                max_output_lines = dialog_height - 8 if self.is_running else dialog_height - 6
                for i, line in enumerate(self.output_lines):
                    if i >= max_output_lines:
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
    
    def _run_command_thread(self, command: List[str], sudo_dialog=None, env=None):
        """Run command in background thread"""
        try:
            # Special handling for ansible-playbook
            if 'ansible-playbook' in command[0]:
                self._run_ansible_playbook(command, env)
            else:
                # Run non-ansible commands normally
                self._run_regular_command(command, env)
                
        except Exception as e:
            self.output_queue.put(f"ERROR: {str(e)}")
            self.exit_code = 1
        finally:
            self.is_running = False
    
    def _run_ansible_playbook(self, command: List[str], env=None):
        """Run ansible-playbook with proper output handling"""
        # Set up environment
        if env is None:
            env = os.environ.copy()
        else:
            new_env = os.environ.copy()
            new_env.update(env)
            env = new_env
        
        # Environment fixes to prevent hanging issues
        env['ANSIBLE_FORCE_COLOR'] = '0'
        env['PYTHONUNBUFFERED'] = '1'
        env['ANSIBLE_STDOUT_CALLBACK'] = 'default'
        env['ANSIBLE_HOST_KEY_CHECKING'] = 'False'  # Disable SSH key checking
        env['ANSIBLE_SSH_PIPELINING'] = 'False'     # Disable pipelining that can hang
        env['ANSIBLE_BECOME'] = 'False'             # Disable global become (we control per task)
        env['ANSIBLE_TIMEOUT'] = '30'               # Connection timeout
        
        # Show initial messages
        self.output_queue.put("Starting Ansible configuration...")
        self.output_queue.put(f"Running command: {' '.join(command[:3])}...")
        self.output_queue.put("Please wait, gathering system information...")
        self.output_queue.put("")
        
        # Set initial task
        self.current_task = "Initializing Ansible..."
        
        # Use simple subprocess.Popen with real-time line reading
        # This method works reliably as confirmed by testing
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True,
            env=env
        )
        
        # Read output line by line in real-time with improved timeout handling
        last_output_time = time.time()
        timeout_seconds = 180  # Reduced to 3 minutes for better UX
        warning_threshold = 60  # Warn after 1 minute of no output
        last_warning_time = 0
        
        try:
            for line in process.stdout:
                line = line.rstrip()
                if line:
                    last_output_time = time.time()
                    
                    # Skip ANSI escape sequences
                    import re
                    clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                    
                    # Parse and queue output
                    self._parse_ansible_output(clean_line)
                    self.output_queue.put(clean_line)
                
                # Check for warnings and timeouts
                current_time = time.time()
                time_since_output = current_time - last_output_time
                
                # Show warning for slow operations
                if (time_since_output > warning_threshold and 
                    current_time - last_warning_time > warning_threshold):
                    self.output_queue.put(f"INFO: Task running for {time_since_output:.0f}s - {self.current_task}")
                    last_warning_time = current_time
                
                # Hard timeout
                if time_since_output > timeout_seconds:
                    self.output_queue.put(f"ERROR: Task appears stuck after {timeout_seconds} seconds")
                    self.output_queue.put(f"Current task: {self.current_task}")
                    self.output_queue.put("Terminating process...")
                    
                    # Try graceful termination first
                    process.terminate()
                    time.sleep(5)
                    if process.poll() is None:
                        self.output_queue.put("Force killing stuck process...")
                        process.kill()
                    
                    self.exit_code = -1
                    return
                    
        except Exception as e:
            self.output_queue.put(f"ERROR reading output: {str(e)}")
            self.output_queue.put("This may indicate a configuration or permission issue")
            self.exit_code = 1
            return
        
        # Wait for process to complete and get exit code
        self.exit_code = process.wait()
    
    def _run_regular_command(self, command: List[str], env=None):
        """Run regular (non-ansible) commands"""
        # Set up environment
        if env is None:
            env = os.environ.copy()
        else:
            new_env = os.environ.copy()
            new_env.update(env)
            env = new_env
            
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=env
        )
        
        # Read output line by line
        for line in process.stdout:
            line = line.rstrip()
            if line:
                self.output_queue.put(line)
        
        # Wait for completion
        self.exit_code = process.wait()
    
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
    
    def _parse_ansible_output(self, line: str):
        """Parse Ansible output to extract progress information"""
        # Check for password prompt
        if "BECOME password:" in line or "sudo password" in line.lower():
            self.current_task = "Waiting for sudo authentication..."
            self.output_queue.put("ERROR: Password prompt detected - this should not happen!")
            self.output_queue.put("The sudo password should be provided via environment variable.")
        # Check for PLAY lines
        elif line.startswith("PLAY ["):
            self.current_task = "Starting configuration..."
        # Check for TASK lines
        elif line.startswith("TASK ["):
            # Extract task name
            import re
            match = re.match(r"TASK \[(.*?)\]", line)
            if match:
                task_name = match.group(1)
                # Make task names more user-friendly
                if "Gathering Facts" in task_name:
                    self.current_task = "Gathering system information..."
                elif "apt" in task_name.lower():
                    if "update" in task_name.lower():
                        self.current_task = "Updating package lists..."
                    elif "install" in task_name.lower():
                        # Try to extract package name
                        if ":" in task_name:
                            pkg_part = task_name.split(":")[-1].strip()
                            self.current_task = f"Installing {pkg_part}..."
                        else:
                            self.current_task = "Installing packages..."
                elif "git" in task_name.lower():
                    self.current_task = "Cloning repositories..."
                elif "file" in task_name.lower() or "directory" in task_name.lower():
                    self.current_task = "Creating directories..."
                elif "template" in task_name.lower():
                    self.current_task = "Configuring applications..."
                elif "service" in task_name.lower():
                    self.current_task = "Managing services..."
                elif "download" in task_name.lower() or "get_url" in task_name.lower():
                    self.current_task = "Downloading files..."
                else:
                    # Clean up the task name - keep it concise
                    clean_name = task_name
                    if ":" in clean_name:
                        clean_name = clean_name.split(":")[-1].strip()
                    # Truncate long task names
                    if len(clean_name) > 50:
                        clean_name = clean_name[:47] + "..."
                    self.current_task = clean_name + "..." if not clean_name.endswith("...") else clean_name
        # Check for ok/changed/failed
        elif "ok:" in line or "changed:" in line:
            self.completed_tasks += 1
        # Check for PLAY RECAP
        elif "PLAY RECAP" in line:
            self.current_task = "Finalizing configuration..."