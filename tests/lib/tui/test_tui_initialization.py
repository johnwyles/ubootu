#!/usr/bin/env python3
"""
Tests for TUI initialization and environment detection
Following TDD approach - write tests first
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, call
import subprocess
import tempfile

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))


class TestTUIInitialization(unittest.TestCase):
    """Test TUI initialization and environment handling"""
    
    def test_tty_detection_non_tty(self):
        """Test behavior when not in TTY"""
        # Run script in non-TTY environment and check error message
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py'],
            capture_output=True,
            text=True
        )
        
        # Should exit with error code
        self.assertNotEqual(result.returncode, 0)
        
        # Should provide helpful error message
        self.assertIn("terminal", result.stderr.lower())
        self.assertNotIn("nocbreak() returned ERR", result.stderr)
        
    @patch('sys.stdout.isatty')
    def test_tty_detection_message(self, mock_isatty):
        """Test that proper error message is shown when not in TTY"""
        mock_isatty.return_value = False
        
        # Import should work but execution should fail gracefully
        try:
            from configure_standard_tui import main
            # Should not use curses.wrapper when not in TTY
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.argv', ['configure_standard_tui.py']):
                    main()
            
            # Should exit with error code
            self.assertNotEqual(cm.exception.code, 0)
        except ImportError:
            self.fail("Failed to import configure_standard_tui")
    
    def test_help_works_without_tty(self):
        """Test that --help works even without TTY"""
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py', '--help'],
            capture_output=True,
            text=True
        )
        
        # Help should work without TTY
        self.assertEqual(result.returncode, 0)
        self.assertIn("Ubootu Configuration Tool", result.stdout)
        self.assertIn("--sections", result.stdout)
    
    def test_no_tui_flag(self):
        """Test --no-tui flag for non-interactive mode"""
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py', '--no-tui'],
            capture_output=True,
            text=True
        )
        
        # Should provide information about non-interactive mode
        self.assertIn("non-interactive", result.stdout.lower())
    
    @patch('curses.wrapper')
    @patch('sys.stdout.isatty')
    def test_tty_runs_curses(self, mock_isatty, mock_wrapper):
        """Test that curses.wrapper is called when in TTY"""
        mock_isatty.return_value = True
        mock_wrapper.return_value = 0
        
        from configure_standard_tui import main
        
        with patch('sys.argv', ['configure_standard_tui.py']):
            with self.assertRaises(SystemExit) as cm:
                main()
            
        # Should call curses.wrapper
        mock_wrapper.assert_called_once()
        # Should exit with success
        self.assertEqual(cm.exception.code, 0)
    
    def test_import_error_handling(self):
        """Test graceful handling of import errors"""
        # Create a test script that imports with missing dependency
        test_script = '''
import sys
import os
sys.path.insert(0, "lib")

# Simulate missing import
import builtins
real_import = builtins.__import__

def mock_import(name, *args, **kwargs):
    if name == "ansible":
        raise ImportError("No module named 'ansible'")
    return real_import(name, *args, **kwargs)

builtins.__import__ = mock_import

try:
    from tui.main_menu import MainMenu
    print("Import successful despite missing ansible")
except ImportError as e:
    print(f"Import failed: {e}")
'''
        
        result = subprocess.run(
            [sys.executable, '-c', test_script],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        )
        
        # Should handle missing ansible gracefully
        self.assertIn("Import successful", result.stdout)


class TestEnvironmentDetection(unittest.TestCase):
    """Test environment detection utilities"""
    
    def test_terminal_info_utility(self):
        """Test that we can get terminal information"""
        test_script = '''
import sys
import os

def get_terminal_info():
    """Get information about terminal environment"""
    info = {
        "is_tty": sys.stdout.isatty(),
        "term": os.environ.get("TERM", "not set"),
        "columns": os.get_terminal_size().columns if sys.stdout.isatty() else None,
        "lines": os.get_terminal_size().lines if sys.stdout.isatty() else None,
    }
    return info

info = get_terminal_info()
print(f"TTY: {info['is_tty']}, TERM: {info['term']}")
'''
        
        result = subprocess.run(
            [sys.executable, '-c', test_script],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("TTY:", result.stdout)
        self.assertIn("TERM:", result.stdout)


class TestFallbackBehavior(unittest.TestCase):
    """Test fallback behavior when TUI cannot run"""
    
    def test_suggest_alternative_commands(self):
        """Test that alternative commands are suggested when not in TTY"""
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py'],
            capture_output=True,
            text=True
        )
        
        # Should suggest using setup.sh or other alternatives
        output = result.stderr + result.stdout
        self.assertTrue(
            "setup.sh" in output or 
            "alternative" in output.lower() or
            "try" in output.lower()
        )
    
    def test_config_file_generation_without_tui(self):
        """Test that config can be generated without TUI"""
        # This would test a --generate-config flag or similar
        # For now, just verify the concept
        self.assertTrue(os.path.exists("config.example.yml"))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)