#!/usr/bin/env python3
"""
Functional tests for progress_dialog module
Tests progress dialog functionality
"""

import curses
import subprocess
from unittest.mock import MagicMock, Mock, patch, call

import pytest

# Mock curses constants that aren't available without initscr
if not hasattr(curses, 'ACS_ULCORNER'):
    curses.ACS_ULCORNER = ord('+')
    curses.ACS_URCORNER = ord('+')
    curses.ACS_LLCORNER = ord('+')
    curses.ACS_LRCORNER = ord('+')
    curses.ACS_HLINE = ord('-')
    curses.ACS_VLINE = ord('|')
    curses.A_BOLD = 1
    curses.A_DIM = 2
    curses.A_REVERSE = 4
    curses.COLOR_RED = 1
    curses.COLOR_GREEN = 2
    curses.COLOR_YELLOW = 3
    curses.COLOR_BLACK = 0

from lib.tui.progress_dialog import ProgressDialog, run_ansible_with_progress


class TestProgressDialogFunctional:
    """Test ProgressDialog functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch.return_value = -1  # Non-blocking

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_init(self, mock_curs_set):
        """Test ProgressDialog initialization"""
        dialog = ProgressDialog(self.stdscr)
        
        assert dialog.stdscr == self.stdscr
        assert dialog.height == 24
        assert dialog.width == 80
        assert dialog.messages == []
        assert dialog.progress == 0
        assert dialog.task_count == 0
        assert dialog.current_task == 0

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_update_progress(self, mock_curs_set):
        """Test updating progress"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog.update_progress(50, "Half way there!")
        
        assert dialog.progress == 50
        assert dialog.status == "Half way there!"

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_add_message(self, mock_curs_set):
        """Test adding messages"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog.add_message("Starting process...")
        dialog.add_message("Processing item 1")
        
        assert len(dialog.messages) == 2
        assert "Starting process..." in dialog.messages
        assert "Processing item 1" in dialog.messages

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_add_message_max_limit(self, mock_curs_set):
        """Test message limit"""
        dialog = ProgressDialog(self.stdscr)
        
        # Add many messages
        for i in range(1000):
            dialog.add_message(f"Message {i}")
        
        # Should be limited to max_messages (default 100)
        assert len(dialog.messages) <= 100

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_draw(self, mock_curs_set):
        """Test drawing the progress dialog"""
        dialog = ProgressDialog(self.stdscr)
        dialog.title = "Installing Packages"
        dialog.progress = 25
        dialog.status = "Installing package 1 of 4"
        dialog.add_message("Started installation")
        
        dialog.draw()
        
        # Check that drawing methods were called
        self.stdscr.clear.assert_called()
        self.stdscr.refresh.assert_called()
        
        # Check that title was drawn
        addstr_calls = self.stdscr.addstr.call_args_list
        assert any("Installing Packages" in str(call) for call in addstr_calls)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    @patch('lib.tui.progress_dialog.curses.has_colors')
    @patch('lib.tui.progress_dialog.curses.start_color')
    @patch('lib.tui.progress_dialog.curses.init_pair')
    def test_draw_with_colors(self, mock_init_pair, mock_start_color, mock_has_colors, mock_curs_set):
        """Test drawing with colors enabled"""
        mock_has_colors.return_value = True
        
        dialog = ProgressDialog(self.stdscr)
        dialog.draw()
        
        # Check that colors were initialized
        mock_start_color.assert_called()
        assert mock_init_pair.called

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_draw_progress_bar(self, mock_curs_set):
        """Test drawing progress bar"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog._draw_progress_bar(10, 5, 50, 50)
        
        # Check that progress bar was drawn
        assert self.stdscr.addstr.called

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_parse_ansible_output_task(self, mock_curs_set):
        """Test parsing Ansible task output"""
        dialog = ProgressDialog(self.stdscr)
        
        line = "TASK [common : Install base packages] *******"
        dialog.parse_ansible_output(line)
        
        assert dialog.current_task == 1
        assert dialog.status == "Install base packages"
        assert any("Install base packages" in msg for msg in dialog.messages)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_parse_ansible_output_ok(self, mock_curs_set):
        """Test parsing Ansible OK output"""
        dialog = ProgressDialog(self.stdscr)
        
        line = "ok: [localhost]"
        dialog.parse_ansible_output(line)
        
        assert any("OK" in msg for msg in dialog.messages)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_parse_ansible_output_changed(self, mock_curs_set):
        """Test parsing Ansible changed output"""
        dialog = ProgressDialog(self.stdscr)
        
        line = "changed: [localhost]"
        dialog.parse_ansible_output(line)
        
        assert any("CHANGED" in msg for msg in dialog.messages)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_parse_ansible_output_failed(self, mock_curs_set):
        """Test parsing Ansible failed output"""
        dialog = ProgressDialog(self.stdscr)
        
        line = "failed: [localhost] => {\"msg\": \"Package not found\"}"
        dialog.parse_ansible_output(line)
        
        assert dialog.has_errors
        assert any("FAILED" in msg for msg in dialog.messages)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_parse_ansible_output_skipping(self, mock_curs_set):
        """Test parsing Ansible skipping output"""
        dialog = ProgressDialog(self.stdscr)
        
        line = "skipping: [localhost]"
        dialog.parse_ansible_output(line)
        
        assert any("SKIPPED" in msg for msg in dialog.messages)

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_set_task_count(self, mock_curs_set):
        """Test setting task count"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog.set_task_count(10)
        
        assert dialog.task_count == 10

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_calculate_progress_with_tasks(self, mock_curs_set):
        """Test progress calculation with tasks"""
        dialog = ProgressDialog(self.stdscr)
        dialog.set_task_count(10)
        dialog.current_task = 5
        
        progress = dialog._calculate_progress()
        
        assert progress == 50

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_is_complete(self, mock_curs_set):
        """Test completion check"""
        dialog = ProgressDialog(self.stdscr)
        
        assert not dialog.is_complete()
        
        dialog.progress = 100
        assert dialog.is_complete()

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_show_completion_message(self, mock_curs_set):
        """Test showing completion message"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog.show_completion_message("Installation complete!")
        
        assert dialog.status == "Installation complete!"
        assert dialog.progress == 100

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_show_error_message(self, mock_curs_set):
        """Test showing error message"""
        dialog = ProgressDialog(self.stdscr)
        
        dialog.show_error_message("Installation failed!")
        
        assert dialog.status == "Installation failed!"
        assert dialog.has_errors

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_clear_messages(self, mock_curs_set):
        """Test clearing messages"""
        dialog = ProgressDialog(self.stdscr)
        dialog.add_message("Test 1")
        dialog.add_message("Test 2")
        
        dialog.clear_messages()
        
        assert dialog.messages == []

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_reset(self, mock_curs_set):
        """Test resetting dialog"""
        dialog = ProgressDialog(self.stdscr)
        dialog.progress = 50
        dialog.status = "In progress"
        dialog.add_message("Test")
        dialog.has_errors = True
        
        dialog.reset()
        
        assert dialog.progress == 0
        assert dialog.status == ""
        assert dialog.messages == []
        assert not dialog.has_errors

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_format_message(self, mock_curs_set):
        """Test message formatting"""
        dialog = ProgressDialog(self.stdscr)
        
        formatted = dialog._format_message("Test message", "INFO")
        assert "[INFO]" in formatted
        assert "Test message" in formatted

    @patch('lib.tui.progress_dialog.curses.curs_set')
    def test_handle_curses_error(self, mock_curs_set):
        """Test handling curses errors"""
        dialog = ProgressDialog(self.stdscr)
        self.stdscr.addstr.side_effect = curses.error
        
        # Should not raise exception
        dialog.draw()

    @patch('lib.tui.progress_dialog.subprocess.Popen')
    @patch('lib.tui.progress_dialog.curses.wrapper')
    def test_run_ansible_with_progress(self, mock_wrapper, mock_popen):
        """Test running Ansible with progress"""
        # Mock the process
        mock_process = MagicMock()
        mock_process.poll.side_effect = [None, None, 0]  # Still running, then done
        mock_process.stdout.readline.side_effect = [
            b"TASK [test task] ***\n",
            b"ok: [localhost]\n",
            b""
        ]
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = run_ansible_with_progress(
            ["ansible-playbook", "test.yml"],
            "Testing"
        )
        
        assert result == 0
        mock_wrapper.assert_called_once()