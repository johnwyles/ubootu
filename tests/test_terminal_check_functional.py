#!/usr/bin/env python3
"""
Functional tests for terminal_check module
Tests terminal compatibility checking
"""

import curses
import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

from lib import terminal_check


class TestTerminalCheckFunctional:
    """Test terminal_check functionality"""

    def test_check_terminal_capabilities_good(self):
        """Test terminal capabilities check with good terminal"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert issues == []
                    assert warnings == []

    def test_check_terminal_capabilities_no_tty(self):
        """Test terminal capabilities check without TTY"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=False):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert issues == []
                    assert len(warnings) > 0
                    assert any("terminal" in w.lower() for w in warnings)

    def test_check_terminal_capabilities_dumb_term(self):
        """Test terminal capabilities check with dumb terminal"""
        with patch.dict(os.environ, {'TERM': 'dumb'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert len(issues) > 0
                    assert any("dumb" in i.lower() for i in issues)

    def test_check_terminal_capabilities_no_term(self):
        """Test terminal capabilities check without TERM env"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert len(warnings) > 0
                    assert any("TERM" in w for w in warnings)

    def test_check_terminal_capabilities_small_size(self):
        """Test terminal capabilities check with small terminal"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 40
                    mock_size.return_value.lines = 10
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert len(warnings) >= 2
                    assert any("width" in w.lower() or "columns" in w.lower() for w in warnings)
                    assert any("height" in w.lower() or "lines" in w.lower() for w in warnings)

    def test_check_terminal_capabilities_size_error(self):
        """Test terminal capabilities check when size cannot be determined"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size', side_effect=OSError("Cannot get size")):
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert len(warnings) > 0
                    assert any("size" in w.lower() for w in warnings)

    @patch('lib.terminal_check.curses.wrapper')
    def test_test_curses_basic_interactive(self, mock_wrapper):
        """Test curses basic test in interactive mode"""
        mock_wrapper.return_value = None
        
        result, error = terminal_check.test_curses_basic(interactive=True)
        
        assert result is True
        assert error is None
        mock_wrapper.assert_called_once()

    @patch('lib.terminal_check.curses.wrapper')
    def test_test_curses_basic_non_interactive(self, mock_wrapper):
        """Test curses basic test in non-interactive mode"""
        mock_wrapper.return_value = None
        
        result, error = terminal_check.test_curses_basic(interactive=False)
        
        assert result is True
        assert error is None
        mock_wrapper.assert_called_once()

    @patch('lib.terminal_check.curses.wrapper')
    def test_test_curses_basic_fails(self, mock_wrapper):
        """Test curses basic test failure"""
        mock_wrapper.side_effect = Exception("Curses error")
        
        result, error = terminal_check.test_curses_basic(interactive=False)
        
        assert result is False
        assert "Curses error" in str(error)

    def test_can_run_tui_success(self):
        """Test can_run_tui with all checks passing"""
        with patch('lib.terminal_check.check_terminal_capabilities', return_value=([], [])):
            with patch('lib.terminal_check.test_curses_basic', return_value=(True, None)):
                
                can_run, issues, warnings = terminal_check.can_run_tui()
                
                assert can_run is True
                assert issues == []
                assert warnings == []

    def test_can_run_tui_with_issues(self):
        """Test can_run_tui with terminal issues"""
        with patch('lib.terminal_check.check_terminal_capabilities', return_value=(["Major issue"], [])):
            with patch('lib.terminal_check.test_curses_basic', return_value=(True, None)):
                
                can_run, issues, warnings = terminal_check.can_run_tui()
                
                assert can_run is False
                assert "Major issue" in issues

    def test_can_run_tui_curses_fails(self):
        """Test can_run_tui with curses failure"""
        with patch('lib.terminal_check.check_terminal_capabilities', return_value=([], [])):
            with patch('lib.terminal_check.test_curses_basic', return_value=(False, "Curses failed")):
                
                can_run, issues, warnings = terminal_check.can_run_tui()
                
                assert can_run is False
                assert any("Curses" in issue for issue in issues)

    def test_can_run_tui_with_warnings_only(self):
        """Test can_run_tui with warnings only"""
        with patch('lib.terminal_check.check_terminal_capabilities', return_value=([], ["Minor warning"])):
            with patch('lib.terminal_check.test_curses_basic', return_value=(True, None)):
                
                can_run, issues, warnings = terminal_check.can_run_tui()
                
                assert can_run is True
                assert "Minor warning" in warnings

    @patch('builtins.print')
    def test_print_compatibility_report(self, mock_print):
        """Test printing compatibility report"""
        with patch('lib.terminal_check.can_run_tui', return_value=(False, ["Issue 1"], ["Warning 1"])):
            with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 80
                    mock_size.return_value.lines = 24
                    
                    terminal_check.print_compatibility_report()
                    
                    # Check that report was printed
                    assert mock_print.called
                    printed_content = ' '.join(str(call) for call in mock_print.call_args_list)
                    assert "Terminal Compatibility Report" in printed_content
                    assert "Issue 1" in printed_content
                    assert "Warning 1" in printed_content

    def test_check_terminal_capabilities_uncommon_term(self):
        """Test terminal capabilities with uncommon terminal type"""
        with patch.dict(os.environ, {'TERM': 'vt100'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    assert len(warnings) > 0
                    assert any("uncommon" in w.lower() or "vt100" in w.lower() for w in warnings)

    def test_check_terminal_capabilities_force_tui(self):
        """Test terminal capabilities with FORCE_TUI set"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color', 'FORCE_TUI': '1'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=False):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    
                    issues, warnings = terminal_check.check_terminal_capabilities()
                    
                    # With FORCE_TUI, no tty should not add warnings
                    assert issues == []
                    assert warnings == []

    def test_check_terminal_capabilities_locale_issue(self):
        """Test terminal capabilities with locale issues"""
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            with patch('lib.terminal_check.sys.stdout.isatty', return_value=True):
                with patch('lib.terminal_check.os.get_terminal_size') as mock_size:
                    mock_size.return_value.columns = 100
                    mock_size.return_value.lines = 30
                    with patch('lib.terminal_check.locale.getpreferredencoding', return_value='ascii'):
                        
                        issues, warnings = terminal_check.check_terminal_capabilities()
                        
                        # Check for locale-related warnings
                        assert len(warnings) > 0
                        assert any("UTF-8" in w or "encoding" in w.lower() for w in warnings)