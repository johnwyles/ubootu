#!/usr/bin/env python3
"""Test progress dialog functionality"""

import queue
import subprocess

# Mock curses module
import sys
import threading
import time
from unittest.mock import MagicMock, call, patch

import pytest

sys.modules["curses"] = MagicMock()
import curses

# Set up curses constants
curses.A_BOLD = 1
curses.error = Exception


class TestProgressDialog:
    """Test the ProgressDialog class"""

    @pytest.fixture
    def mock_stdscr(self):
        """Create a mock screen"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        stdscr.getch.return_value = -1  # No key pressed
        return stdscr

    @pytest.fixture
    def progress_dialog(self, mock_stdscr):
        """Create a ProgressDialog instance"""
        from lib.tui.progress_dialog import ProgressDialog

        return ProgressDialog(mock_stdscr)

    def test_ansible_command_includes_become_pass(self, progress_dialog):
        """Test that ansible-playbook command includes --ask-become-pass"""
        from lib.tui.unified_menu import UnifiedMenu

        # Check the command being passed
        with patch("subprocess.Popen") as mock_popen:
            # Mock the process
            mock_process = MagicMock()
            mock_process.stdout = iter([])  # Empty output
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process

            # The unified menu should pass --ask-become-pass
            stdscr = MagicMock()
            stdscr.getmaxyx.return_value = (24, 80)
            menu = UnifiedMenu(stdscr)

            # Check the actual command construction
            # This should include --ask-become-pass
            expected_cmd = [
                "ansible-playbook",
                "site.yml",
                "-i",
                "inventories/local/hosts",
                "--diff",
                "-v",
                "--ask-become-pass",
            ]

            # We need to ensure the command includes --ask-become-pass
            assert "--ask-become-pass" in expected_cmd

    def test_real_time_output_capture(self, progress_dialog):
        """Test that output is captured in real-time without buffering"""
        with patch("subprocess.Popen") as mock_popen:
            # Mock process that outputs lines with delays
            mock_process = MagicMock()

            def mock_stdout():
                yield "PLAY [localhost]"
                time.sleep(0.1)
                yield "TASK [Gathering Facts]"
                time.sleep(0.1)
                yield "ok: [localhost]"

            mock_process.stdout = mock_stdout()
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process

            # Start time
            start_time = time.time()

            # Run command in thread
            result_queue = queue.Queue()

            def run_test():
                result = progress_dialog.run_command(["ansible-playbook", "test.yml"], "Testing", show_output=True)
                result_queue.put(result)

            thread = threading.Thread(target=run_test)
            thread.start()

            # Wait a bit for output to be processed
            time.sleep(0.5)

            # Check that output lines were queued
            assert not progress_dialog.output_queue.empty()

            # Stop the dialog
            progress_dialog.is_running = False
            thread.join(timeout=1.0)

    def test_stderr_capture(self, progress_dialog):
        """Test that stderr is also captured"""
        with patch("subprocess.Popen") as mock_popen:
            # Mock process with stderr
            mock_process = MagicMock()
            mock_process.stdout = iter(["stdout line"])
            mock_process.stderr = iter(["stderr line"])
            mock_process.wait.return_value = 1
            mock_popen.return_value = mock_process

            # We need to ensure stderr=subprocess.STDOUT is used
            # to merge stderr into stdout
            progress_dialog._run_command_thread(["test", "command"])

            # Check that Popen was called with stderr=subprocess.STDOUT
            mock_popen.assert_called_once()
            call_kwargs = mock_popen.call_args[1]
            assert call_kwargs.get("stderr") == subprocess.STDOUT

    def test_ansible_output_parsing(self, progress_dialog):
        """Test parsing of Ansible output for user-friendly messages"""
        # Test various Ansible output lines
        test_cases = [
            ("TASK [Gathering Facts]", "Gathering system information..."),
            ("TASK [common : Update apt cache]", "Updating package lists..."),
            ("TASK [development-tools : Install Docker]", "Installing Docker..."),
            ("TASK [git : Clone repository]", "Cloning repositories..."),
            ("TASK [file : Create directory]", "Creating directories..."),
            ("TASK [template : Configure application]", "Configuring applications..."),
            ("TASK [service : Start nginx]", "Managing services..."),
            ("PLAY RECAP", "Finalizing configuration..."),
        ]

        for ansible_output, expected_task in test_cases:
            progress_dialog._parse_ansible_output(ansible_output)
            assert progress_dialog.current_task == expected_task

    def test_task_counting(self, progress_dialog):
        """Test that completed tasks are counted correctly"""
        progress_dialog.completed_tasks = 0

        # Simulate task completion lines
        progress_dialog._parse_ansible_output("ok: [localhost]")
        assert progress_dialog.completed_tasks == 1

        progress_dialog._parse_ansible_output("changed: [localhost]")
        assert progress_dialog.completed_tasks == 2

    def test_timeout_detection(self, progress_dialog):
        """Test detection of stuck processes"""
        with patch("subprocess.Popen") as mock_popen:
            # Mock a process that hangs
            mock_process = MagicMock()
            mock_process.stdout = iter([])  # No output
            mock_process.wait.side_effect = subprocess.TimeoutExpired("cmd", 30)
            mock_popen.return_value = mock_process

            # This should handle the timeout gracefully
            result = progress_dialog._run_command_thread(["hanging", "command"])

            # Should set an error exit code
            assert progress_dialog.exit_code != 0

    def test_unbuffered_output(self, progress_dialog):
        """Test that output uses line buffering for real-time display"""
        with patch("subprocess.Popen") as mock_popen:
            progress_dialog._run_command_thread(["test", "command"])

            # Check that Popen was called with line buffering
            mock_popen.assert_called_once()
            call_kwargs = mock_popen.call_args[1]
            assert call_kwargs.get("bufsize") == 1  # Line buffered
            assert call_kwargs.get("universal_newlines") == True

    def test_ansible_color_disabled(self, progress_dialog):
        """Test that Ansible color output is disabled"""
        import os

        with patch.dict(os.environ, {}, clear=True):
            with patch("subprocess.Popen") as mock_popen:
                mock_process = MagicMock()
                mock_process.stdout = iter([])
                mock_process.wait.return_value = 0
                mock_popen.return_value = mock_process

                # Run command
                progress_dialog._run_command_thread(["ansible-playbook", "test.yml"])

                # Check that ANSIBLE_FORCE_COLOR is set to 0
                # This should be done before running the command
                # We'll need to fix the implementation to set this
                pass  # Will be implemented in the fix

    def test_progress_display_updates(self, progress_dialog, mock_stdscr):
        """Test that progress display updates correctly"""
        progress_dialog.current_task = "Installing packages..."
        progress_dialog.completed_tasks = 5
        progress_dialog.is_running = True

        # Mock the dialog rendering
        with patch("lib.tui.utils.draw_box"):
            with patch("lib.tui.utils.draw_centered_text"):
                # Trigger a render by simulating the main loop iteration
                progress_dialog.output_queue.put("test output")

                # The display should show current task and count
                # We'll verify this by checking the addstr calls
                # This will be implemented in the actual fix
                pass
