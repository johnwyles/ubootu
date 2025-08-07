#!/usr/bin/env python3
"""
Progress dialog for showing real-time command output in TUI
"""

import curses
import errno
import os
import queue
import signal
import subprocess
import sys
import threading
import time
from typing import Callable, List, Optional

from .constants import DIALOG_HEIGHT, DIALOG_WIDTH
from .utils import draw_box, draw_centered_text, get_dialog_position


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
        self.skipped_tasks = 0
        self.failed_tasks = 0
        self.skip_reasons = {}  # Track skip reasons by category
        self.success_details = {}  # Track what succeeded
        self.failure_details = {}  # Track what failed
        self.current_task_name = ""  # Store full task name for categorization

        # Smart refresh tracking
        self.last_output_count = 0
        self.last_task = ""
        self.last_completed_tasks = 0
        self.last_skipped_tasks = 0
        self.needs_redraw = True

    def run_command(
        self, command: List[str], title: str = "Processing...", show_output: bool = True, sudo_dialog=None, env=None
    ) -> int:
        """Run a command and show progress in dialog"""
        sys.stderr.write(f"\n[DEBUG] ProgressDialog.run_command called at {time.strftime('%H:%M:%S')}\n")
        sys.stderr.write(f"[DEBUG] Command: {' '.join(command[:3])}...\n")
        sys.stderr.flush()

        self.is_running = True
        self.exit_code = None
        self.output_lines = []
        self.current_task = "Initializing Ansible..."
        self.completed_tasks = 0

        # Use fullscreen mode with small margins
        dialog_height = self.height - 2
        dialog_width = self.width - 2
        y = 1
        x = 1

        # Start command in background thread
        cmd_thread = threading.Thread(target=self._run_command_thread, args=(command, sudo_dialog, env))
        cmd_thread.daemon = True
        cmd_thread.start()

        # Show progress dialog
        while self.is_running or not self.output_queue.empty():
            # Process output queue first to check for changes
            new_lines_added = False
            while not self.output_queue.empty():
                try:
                    line = self.output_queue.get_nowait()
                    self.output_lines.append(line)
                    new_lines_added = True
                    # Keep only last N lines that fit in dialog
                    max_lines = dialog_height - 6
                    if len(self.output_lines) > max_lines:
                        self.output_lines = self.output_lines[-max_lines:]
                except queue.Empty:
                    break

            # Check if we need to redraw
            if (
                new_lines_added
                or self.last_task != self.current_task
                or self.last_completed_tasks != self.completed_tasks
                or self.last_skipped_tasks != self.skipped_tasks
                or self.needs_redraw
            ):

                # Clear and draw dialog
                self.stdscr.clear()
                draw_box(self.stdscr, y, x, dialog_height, dialog_width, title)
                self.needs_redraw = False
            else:
                # Skip the rest if nothing changed
                self.stdscr.timeout(100)
                key = self.stdscr.getch()
                if key != -1 and not self.is_running:
                    break
                continue

            # Update tracking variables
            self.last_output_count = len(self.output_lines)
            self.last_task = self.current_task
            self.last_completed_tasks = self.completed_tasks

            # Draw current task info
            task_y = y + 2
            if self.is_running and self.current_task:
                # Show current task
                task_text = f"Current: {self.current_task}"
                # Truncate if too long
                max_len = dialog_width - 10
                if len(task_text) > max_len:
                    task_text = task_text[: max_len - 3] + "..."
                try:
                    self.stdscr.addstr(task_y, x + 3, task_text, curses.A_BOLD)
                except curses.error:
                    pass

                # Show task count and progress bar if available
                if self.completed_tasks > 0:
                    # Estimate total tasks (can be refined based on playbook analysis)
                    estimated_total = max(self.completed_tasks + 10, 50)  # Rough estimate
                    percentage = min(100, int((self.completed_tasks / estimated_total) * 100))

                    # Draw progress bar
                    bar_width = min(50, dialog_width - 20)
                    filled = int(bar_width * percentage / 100)
                    empty = bar_width - filled

                    progress_bar = f"[{'█' * filled}{'░' * empty}] {percentage}%"
                    count_text = f"Tasks: {self.completed_tasks} completed"
                    if self.skipped_tasks > 0:
                        count_text += f", {self.skipped_tasks} skipped"
                    if self.failed_tasks > 0:
                        count_text += f", {self.failed_tasks} failed"
                    count_text += f" | {progress_bar}"

                    try:
                        self.stdscr.addstr(task_y + 1, x + 3, count_text)
                    except curses.error:
                        pass

            # Adjust output area to make room for task info
            if show_output:
                output_y = y + 5 if self.is_running else y + 2
                max_output_lines = dialog_height - 7 if self.is_running else dialog_height - 4

                # Keep only last N lines that fit
                if len(self.output_lines) > max_output_lines:
                    self.output_lines = self.output_lines[-max_output_lines:]

                for i, line in enumerate(self.output_lines):
                    if i >= max_output_lines:
                        break
                    # Truncate long lines to fit
                    display_line = line[: dialog_width - 6]
                    try:
                        self.stdscr.addstr(output_y + i, x + 3, display_line)
                    except curses.error:
                        pass

            # Draw status
            status_y = y + dialog_height - 3
            if self.is_running:
                # Animated spinner
                spinner = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"][int(time.time() * 10) % 8]
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

        return self.exit_code if self.exit_code is not None else 1

    def _run_command_thread(self, command: List[str], sudo_dialog=None, env=None):
        """Run command in background thread"""
        try:
            # Emergency debug to file
            with open("/tmp/thread_debug.log", "a") as f:
                f.write(f"\n[{time.strftime('%H:%M:%S')}] _run_command_thread started\n")
                f.write(f"Command: {' '.join(command)}\n")

            # Special handling for ansible-playbook
            if "ansible-playbook" in command[0]:
                self._run_ansible_playbook(command, env)
            else:
                # Run non-ansible commands normally
                self._run_regular_command(command, env)

        except Exception as e:
            import traceback

            with open("/tmp/thread_debug.log", "a") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] EXCEPTION in thread: {e}\n")
                f.write(traceback.format_exc())

            self.output_queue.put(f"ERROR: {str(e)}")
            self.exit_code = 1
        finally:
            with open("/tmp/thread_debug.log", "a") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] Thread ending, exit_code={self.exit_code}\n")
            self.is_running = False

    def _run_ansible_playbook(self, command: List[str], env=None):
        """Run ansible-playbook with proper output handling"""
        # DEBUG: Write to stderr so we can see it
        sys.stderr.write(f"\n[DEBUG] _run_ansible_playbook called at {time.strftime('%H:%M:%S')}\n")
        sys.stderr.write(f"[DEBUG] Command: {' '.join(command)}\n")
        sys.stderr.flush()

        # NOTE: We cannot set signal handlers in a thread!
        # signal.signal() only works in the main thread
        # This was causing the "signal only works in main thread" error

        # Debug logging - use timestamped file
        debug_log = f"/tmp/ubootu_debug_{int(time.time())}.log"
        emergency_log = "/tmp/ubootu_emergency.log"

        try:
            with open(debug_log, "w") as f:
                f.write(f"=== Ansible Debug Log ===\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Command: {' '.join(command)}\n")
                f.write(f"Environment (without passwords):\n")
                for k, v in sorted((env or os.environ).items()):
                    if "PASS" not in k and "PASSWORD" not in k:
                        f.write(f"  {k}={v}\n")
                f.write("\n")

            # Also write to emergency log
            with open(emergency_log, "a") as f:
                f.write(f"\n[{time.strftime('%H:%M:%S')}] Starting ansible\n")
                f.write(f"Command: {' '.join(command)}\n")

            sys.stderr.write(f"[DEBUG] Debug logs created: {debug_log}, {emergency_log}\n")
            sys.stderr.flush()
        except Exception as e:
            sys.stderr.write(f"[DEBUG] Failed to create debug log: {e}\n")
            sys.stderr.flush()

        # Set up environment
        if env is None:
            env = os.environ.copy()
        else:
            new_env = os.environ.copy()
            new_env.update(env)
            env = new_env

        # Environment fixes to prevent hanging issues
        env["ANSIBLE_FORCE_COLOR"] = "0"
        env["PYTHONUNBUFFERED"] = "1"
        env["ANSIBLE_HOST_KEY_CHECKING"] = "False"  # Disable SSH key checking
        env["ANSIBLE_SSH_PIPELINING"] = "False"  # Disable pipelining that can hang
        env["ANSIBLE_BECOME"] = "False"  # Disable global become (we control per task)
        env["ANSIBLE_TIMEOUT"] = "30"  # Connection timeout
        env["ANSIBLE_TASK_TIMEOUT"] = "600"  # Task-level timeout (10 minutes for large installs)
        env["ANSIBLE_GATHER_TIMEOUT"] = "30"  # Facts gathering timeout
        env["ANSIBLE_DISPLAY_ARGS_TO_STDOUT"] = "False"  # Don't display module args

        # Critical environment variables to prevent interactive prompts
        env["DEBIAN_FRONTEND"] = "noninteractive"  # Prevent interactive prompts
        env["APT_LISTCHANGES_FRONTEND"] = "none"  # No package change listings
        env["NEEDRESTART_MODE"] = "a"  # Auto-restart services without asking
        env["NEEDRESTART_SUSPEND"] = "1"  # Suspend needrestart during install
        env["UCF_FORCE_CONFFNEW"] = "1"  # Always use new config files
        env["DEBIAN_PRIORITY"] = "critical"  # Only show critical prompts

        # Fix broken pipe errors
        env["PYTHONUNBUFFERED"] = "1"  # Unbuffered Python output
        env["ANSIBLE_UNBUFFERED"] = "1"  # Unbuffered Ansible output
        env["ANSIBLE_PIPE_FAILURES"] = "False"  # Don't treat pipe failures as fatal

        # Display task information with cleaner output
        env["ANSIBLE_STDOUT_CALLBACK"] = "oneline"  # Single line output per task
        env["ANSIBLE_DISPLAY_SKIPPED_HOSTS"] = "True"  # Show skipped tasks (oneline keeps it compact)
        env["ANSIBLE_DISPLAY_OK_HOSTS"] = "True"  # Show OK tasks (oneline keeps it compact)
        # Don't set result format - let oneline handle it
        env["PYTHONIOENCODING"] = "utf-8"  # Ensure proper encoding
        # Don't override verbosity - let command line -v work
        # env['ANSIBLE_VERBOSITY'] = '0'

        # Additional robustness settings
        env["ANSIBLE_LOAD_CALLBACK_PLUGINS"] = "True"
        env["ANSIBLE_RETRY_FILES_ENABLED"] = "False"  # Don't create retry files
        env["ANSIBLE_LOG_PATH"] = "/tmp/ubootu_ansible.log"  # Secondary log
        env["ANSIBLE_PYTHON_INTERPRETER"] = "/usr/bin/python3"  # Explicit python
        env["LANG"] = "C.UTF-8"  # Consistent locale
        env["LC_ALL"] = "C.UTF-8"

        # Show initial messages
        self.output_queue.put("Starting Ansible configuration...")
        self.output_queue.put(f"Running command: {' '.join(command[:3])}...")
        self.output_queue.put("")
        self.output_queue.put("This may take a moment as Ansible:")
        self.output_queue.put("  1. Gathers system facts")
        self.output_queue.put("  2. Checks sudo permissions")
        self.output_queue.put("  3. Begins installation tasks")
        self.output_queue.put("")
        self.output_queue.put(f"DEBUG: Process will start at {time.strftime('%H:%M:%S')}")

        # Set initial task
        self.current_task = "Initializing Ansible..."

        # Use subprocess.Popen with proper pipe handling to prevent broken pipe errors
        # Set up process with explicit error handling
        try:
            sys.stderr.write(f"[DEBUG] About to start subprocess.Popen at {time.strftime('%H:%M:%S')}\n")
            sys.stderr.flush()

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,  # Prevent stdin issues
                text=True,
                bufsize=0,  # Unbuffered to prevent pipe blocking
                universal_newlines=True,
                env=env,
                preexec_fn=os.setsid,  # Create new process group to prevent signal issues
            )

            sys.stderr.write(f"[DEBUG] Process started with PID: {process.pid}\n")
            sys.stderr.flush()

            with open("/tmp/ubootu_emergency.log", "a") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] Process started, PID: {process.pid}\n")

        except Exception as e:
            sys.stderr.write(f"[DEBUG] FAILED to start process: {e}\n")
            sys.stderr.flush()

            with open("/tmp/ubootu_emergency.log", "a") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] FAILED to start: {e}\n")
                import traceback

                f.write(traceback.format_exc())

            self.output_queue.put(f"ERROR: Failed to start Ansible process: {str(e)}")
            self.exit_code = 1
            return

        # Read output line by line in real-time with improved timeout handling
        last_output_time = time.time()
        timeout_seconds = 300  # 5 minutes maximum (increased for large package updates)
        warning_threshold = 90  # Warn after 90 seconds of no output
        last_warning_time = 0
        task_start_time = time.time()
        max_total_time = 1800  # 30 minutes absolute maximum
        lines_read = 0

        sys.stderr.write(f"[DEBUG] Starting output read loop at {time.strftime('%H:%M:%S')}\n")
        sys.stderr.flush()

        try:
            while True:
                try:
                    # Read line with timeout protection
                    line = process.stdout.readline()
                    if not line:
                        # Check if process is still running
                        poll_result = process.poll()
                        if poll_result is not None:
                            # Process has terminated
                            sys.stderr.write(f"[DEBUG] Process terminated with code: {poll_result}\n")
                            sys.stderr.flush()

                            # If no lines were read, this is suspicious
                            if lines_read == 0:
                                self.output_queue.put("ERROR: Process exited without producing any output")
                                self.output_queue.put(f"Exit code was: {poll_result}")
                                self.exit_code = poll_result

                            # Process has terminated, drain any remaining output
                            remaining = process.stdout.read()
                            if remaining:
                                for remaining_line in remaining.splitlines():
                                    if remaining_line.strip():
                                        self.output_queue.put(remaining_line.strip())
                            break
                        # Empty line but process still running
                        time.sleep(0.1)
                        continue

                    # Check if this is a hung process waiting for password
                    current_time = time.time()
                    if current_time - last_output_time > 5 and current_time - last_output_time < 10:
                        # Check if ansible is waiting for password
                        try:
                            # Non-blocking check of process state
                            import select

                            if process.stdout and select.select([process.stdout], [], [], 0)[0]:
                                # There's data available, continue normally
                                pass
                            else:
                                # No data available, might be waiting
                                if process.poll() is None:
                                    # Process still running but no output
                                    self.output_queue.put("INFO: Process appears to be waiting...")
                                    self.output_queue.put("If stuck at password prompt, check sudo configuration")
                        except:
                            pass
                        continue

                    if line:
                        line = line.rstrip()
                        if line:
                            lines_read += 1
                            last_output_time = time.time()

                            # Skip ANSI escape sequences
                            import re

                            clean_line = re.sub(r"\x1b\[[0-9;]*m", "", line)

                            # DEBUG: Log first few lines and any errors
                            if lines_read <= 5 or "error" in clean_line.lower() or "fail" in clean_line.lower():
                                sys.stderr.write(f"[DEBUG] Line {lines_read}: {clean_line[:100]}\n")
                                sys.stderr.flush()

                            # Skip massive facts output to prevent overflow
                            if '"ansible_facts"' in clean_line or len(clean_line) > 500:
                                # For very long lines (facts), just show a summary
                                if '"ansible_facts"' in clean_line:
                                    sys.stderr.write(f"[DEBUG] Skipping facts line, length: {len(clean_line)}\n")
                                    sys.stderr.flush()
                                    self.output_queue.put("✓ Gathered system facts")
                                    self.current_task = "System facts gathered"
                                elif "SUCCESS" in clean_line and len(clean_line) > 500:
                                    # This is likely a facts SUCCESS line with JSON
                                    self.output_queue.put("✓ Facts gathering completed")
                                # Skip the actual facts data
                                continue

                            # Parse ansible output and decide what to show
                            formatted_line = self._parse_ansible_output(clean_line)
                            if formatted_line:
                                self.output_queue.put(formatted_line)
                            elif not self._should_suppress_line(clean_line):
                                # Only show the line if it's not suppressed
                                self.output_queue.put(clean_line)

                            # Debug log output
                            try:
                                with open("/tmp/ubootu_emergency.log", "a") as f:
                                    f.write(f"[{time.strftime('%H:%M:%S')}] {clean_line}\n")
                            except:
                                pass

                except (IOError, BrokenPipeError) as e:
                    # Handle broken pipe errors gracefully
                    if isinstance(e, BrokenPipeError) or (hasattr(e, "errno") and e.errno == errno.EPIPE):
                        self.output_queue.put("WARNING: Output pipe closed by Ansible")
                        # Try to get exit code anyway
                        exit_code = process.poll()
                        if exit_code is not None:
                            self.exit_code = exit_code
                            return
                        break
                    else:
                        raise

                # Check for warnings and timeouts
                current_time = time.time()
                time_since_output = current_time - last_output_time
                total_time = current_time - task_start_time

                # Show warning for slow operations
                if time_since_output > warning_threshold and current_time - last_warning_time > warning_threshold:
                    self.output_queue.put(f"INFO: Task running for {time_since_output:.0f}s - {self.current_task}")
                    self.output_queue.put(f"INFO: Total time elapsed: {total_time:.0f}s")
                    last_warning_time = current_time

                # Absolute maximum time check (30 minutes)
                if total_time > max_total_time:
                    self.output_queue.put(
                        f"ERROR: Process exceeded maximum time limit ({max_total_time/60:.0f} minutes)"
                    )
                    self.output_queue.put("This may indicate a system issue. Terminating...")
                    process.kill()
                    self.exit_code = -2
                    return

                # No output timeout (5 minutes)
                if time_since_output > timeout_seconds:
                    self.output_queue.put(f"ERROR: No output for {timeout_seconds} seconds")
                    self.output_queue.put(f"Current task: {self.current_task}")
                    self.output_queue.put("This usually indicates the process is stuck waiting for input.")
                    self.output_queue.put("Terminating process...")

                    # Try graceful termination first
                    process.terminate()
                    time.sleep(3)
                    if process.poll() is None:
                        self.output_queue.put("Force killing stuck process...")
                        process.kill()
                        time.sleep(2)

                    self.exit_code = -1
                    return

        except Exception as e:
            self.output_queue.put(f"ERROR reading output: {str(e)}")
            self.output_queue.put("This may indicate a configuration or permission issue")
            self.exit_code = 1
            return

        # Wait for process to complete and get exit code
        try:
            # Close stdout to signal we're done reading (prevents broken pipe)
            if process.stdout:
                process.stdout.close()
        except:
            pass

        # Now wait for process to fully terminate
        self.exit_code = process.wait()

        sys.stderr.write(f"[DEBUG] Process exited with code: {self.exit_code}\n")
        sys.stderr.write(f"[DEBUG] Total lines read: {lines_read}\n")
        sys.stderr.flush()

        # Log final exit code
        try:
            with open("/tmp/ubootu_emergency.log", "a") as f:
                f.write(f"\n[{time.strftime('%H:%M:%S')}] === Process completed ===\n")
                f.write(f"Exit code: {self.exit_code}\n")
                f.write(f"Lines read: {lines_read}\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except:
            pass

        # IMPORTANT: Log the exit code to queue
        if self.exit_code != 0:
            self.output_queue.put(f"\nDEBUG: Ansible exited with code {self.exit_code}")

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
            env=env,
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
        lines = message.split("\n")
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
                self.stdscr.addstr(msg_y + i, x + 3, line[: dialog_width - 6])
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

    def _parse_ansible_output(self, line: str) -> Optional[str]:
        """Parse Ansible output to extract progress information and return formatted line"""
        # Track if we should return a custom formatted line
        formatted_output = None

        # Check for password prompt
        if "BECOME password:" in line or "sudo password" in line.lower():
            self.current_task = "Waiting for sudo authentication..."
            return "ERROR: Password prompt detected - this should not happen!"
        # Check for PLAY lines
        elif line.startswith("PLAY ["):
            self.current_task = "Starting configuration..."
            return None  # Let original line through
        # Check for TASK lines
        elif line.startswith("TASK ["):
            # Extract task name
            import re

            match = re.match(r"TASK \[(.*?)\]", line)
            if match:
                task_name = match.group(1)
                self.current_task_name = task_name  # Store for categorization
                # Make task names more user-friendly
                if "Gathering Facts" in task_name:
                    self.current_task = "Gathering system information..."
                elif "apt" in task_name.lower():
                    if "update" in task_name.lower():
                        if "retry" in task_name.lower():
                            self.current_task = "Retrying package list update..."
                        else:
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
        # Check for ok/changed/failed - handle lines with timestamps like "[16:11:58] ok: [localhost]"
        elif " ok: " in line or line.startswith("ok: "):
            self.completed_tasks += 1
            self._categorize_success(self.current_task_name)
            if self.current_task_name:
                task_display = self.current_task_name
                if ":" in task_display:
                    task_display = task_display.split(":")[-1].strip()
                # Extract item if present
                if "(item=" in line:
                    item_match = re.search(r"\(item=([^)]+)\)", line)
                    if item_match:
                        item_name = item_match.group(1)
                        return f"OK [{task_display}: {item_name}]"
                return f"OK [{task_display}]"
        elif " changed: " in line or line.startswith("changed: "):
            self.completed_tasks += 1
            self._categorize_success(self.current_task_name)
            if self.current_task_name:
                task_display = self.current_task_name
                if ":" in task_display:
                    task_display = task_display.split(":")[-1].strip()
                # Extract item if present
                if "(item=" in line:
                    item_match = re.search(r"\(item=([^)]+)\)", line)
                    if item_match:
                        item_name = item_match.group(1)
                        return f"CHANGED [{task_display}: {item_name}]"
                return f"CHANGED [{task_display}]"
        elif " failed: " in line or line.startswith("failed: "):
            self.failed_tasks += 1
            self._categorize_failure(self.current_task_name)
            # Format failed output
            if self.current_task_name:
                task_display = self.current_task_name
                if ":" in task_display:
                    task_display = task_display.split(":")[-1].strip()
                # Try to extract error message
                error_detail = ""
                if "msg:" in line:
                    msg_start = line.find("msg:")
                    error_msg = line[msg_start + 4 :].strip()
                    if len(error_msg) > 50:
                        error_msg = error_msg[:47] + "..."
                    error_detail = f" - {error_msg}"
                return f"FAILED [{task_display}]{error_detail}"
        # Check for skipped tasks - handle lines like "[16:11:58] skipping: [localhost]"
        elif " skipping: " in line or line.startswith("skipping: "):
            self.skipped_tasks += 1
            skip_reason = "Condition not met"

            # Try to extract skip reason from verbose output
            if "=>" in line:
                # Extract reason after =>
                parts = line.split("=>", 1)
                if len(parts) > 1:
                    reason = parts[1].strip()
                    # Parse common skip reasons
                    if "'selected_items'" in reason or "not in selected_items" in reason:
                        skip_reason = "Not selected"
                        self._categorize_skip("Not selected in menu")
                    elif "when:" in reason:
                        if "desktop_environment" in reason:
                            skip_reason = "Wrong desktop environment"
                            self._categorize_skip("Desktop environment mismatch")
                        elif "enable_" in reason or "install_" in reason:
                            skip_reason = "Feature disabled"
                            self._categorize_skip("Feature not enabled")
                        else:
                            skip_reason = "Condition failed"
                            self._categorize_skip("Conditional check failed")
                    else:
                        self._categorize_skip("Other conditions")

            # Format clean single-line output
            if self.current_task_name:
                # Extract just the important part of the task name
                task_display = self.current_task_name
                if ":" in task_display:
                    task_display = task_display.split(":")[-1].strip()
                # Extract item if present
                if "(item=" in line:
                    item_match = re.search(r"\(item=([^)]+)\)", line)
                    if item_match:
                        item_name = item_match.group(1)
                        return f"SKIPPED [{task_display}: {item_name}] - {skip_reason}"
                return f"SKIPPED [{task_display}] - {skip_reason}"
        # Check for PLAY RECAP
        elif "PLAY RECAP" in line:
            self.current_task = "Finalizing configuration..."

        # Return None to indicate no custom formatting needed
        return None

    def _should_suppress_line(self, line: str) -> bool:
        """Determine if a line should be suppressed from output"""
        # Don't suppress our formatted lines
        if any(line.startswith(prefix) for prefix in ["SKIPPED [", "OK [", "CHANGED [", "FAILED [", "TASK ["]):
            return False

        # Since we're using oneline callback, we want to suppress multi-line YAML output
        # but not the actual status lines
        if "] ok: " in line or "] changed: " in line or "] skipping: " in line or "] failed: " in line:
            # These are the main output lines from oneline callback - don't suppress
            return False

        # Suppress verbose details that come after the main status line
        if any(
            phrase in line
            for phrase in [
                "=>",  # YAML output indicator
                "ansible_loop_var",
                "false_condition",
                "skip_reason",
                "cache_update",
                "_raw_params",
                "item:",
                "    ",  # Indented YAML lines
                "localhost                  :",
                "ESTABLISH LOCAL CONNECTION",
                "EXEC /bin/sh",
                "<localhost>",
                "included:",
                "redirecting",
                "deprecation",
            ]
        ):
            return True

        # Suppress empty lines and continuation lines
        if line.strip().startswith("...") or line.strip() == "" or line.strip() == "---":
            return True

        return False

    def _categorize_skip(self, category: str):
        """Categorize skip reasons for summary"""
        if category not in self.skip_reasons:
            self.skip_reasons[category] = 0
        self.skip_reasons[category] += 1

    def _categorize_success(self, task_name: str):
        """Categorize successful tasks"""
        if not task_name:
            return

        # Extract category from task name
        category = self._extract_category(task_name)
        if category not in self.success_details:
            self.success_details[category] = []

        # Extract specific action
        action = self._extract_action(task_name)
        if action and action not in self.success_details[category]:
            self.success_details[category].append(action)

    def _categorize_failure(self, task_name: str):
        """Categorize failed tasks"""
        if not task_name:
            return

        # Extract category from task name
        category = self._extract_category(task_name)
        if category not in self.failure_details:
            self.failure_details[category] = []

        # Extract specific action
        action = self._extract_action(task_name)
        if action and action not in self.failure_details[category]:
            self.failure_details[category].append(action)

    def _extract_category(self, task_name: str) -> str:
        """Extract category from task name"""
        # Format is usually "role : task description"
        if " : " in task_name:
            parts = task_name.split(" : ", 1)
            role = parts[0].strip()
            # Map roles to user-friendly categories
            category_map = {
                "common": "System Setup",
                "security": "Security Configuration",
                "desktop-environment": "Desktop Environment",
                "development-tools": "Development Tools",
                "applications": "Applications",
                "themes": "Themes & Customization",
                "dotfiles": "Dotfile Configuration",
                "security-tools": "Security Tools",
            }
            return category_map.get(role, role.title())
        return "General"

    def _extract_action(self, task_name: str) -> str:
        """Extract specific action from task name"""
        # Get the part after role separator
        if " : " in task_name:
            action = task_name.split(" : ", 1)[1].strip()
            # Simplify common patterns
            if action.startswith("Install "):
                # Extract package/tool name
                if "(" in action:
                    action = action.split("(")[0].strip()
            return action
        return task_name
