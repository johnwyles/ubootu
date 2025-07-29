#!/usr/bin/env python3
"""
Test that the script actually runs in a real terminal
This test exposes what happens when user runs ./configure_standard_tui.py
"""

import unittest
import subprocess
import sys
import os
import pty
import select


class TestScriptRuns(unittest.TestCase):
    """Test the script in realistic conditions"""
    
    def test_script_with_pty(self):
        """Test script with a pseudo-terminal to simulate real usage"""
        # Create a pseudo-terminal
        master, slave = pty.openpty()
        
        # Start the script
        proc = subprocess.Popen(
            [sys.executable, 'configure_standard_tui.py'],
            stdin=slave,
            stdout=slave,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            env={**os.environ, 'TERM': 'xterm'}
        )
        
        # Close slave end in parent
        os.close(slave)
        
        # Try to read some output
        import time
        time.sleep(0.5)  # Give it time to start
        
        # Check if process is still running
        poll = proc.poll()
        
        if poll is not None:
            # Process died immediately
            stderr = proc.stderr.read().decode('utf-8', errors='replace')
            os.close(master)
            self.fail(f"Script died immediately with exit code {poll}. stderr: {stderr}")
        
        # Send quit command
        os.write(master, b'q')
        time.sleep(0.1)
        os.write(master, b'n')  # Don't save
        
        # Wait for process to exit
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            self.fail("Script didn't exit after sending quit command")
        
        os.close(master)
        
        # Check exit code
        self.assertIn(proc.returncode, [0, 1], f"Unexpected exit code: {proc.returncode}")
    
    def test_script_shows_error_without_tty(self):
        """Test that script shows proper error when not in TTY"""
        result = subprocess.run(
            [sys.executable, 'configure_standard_tui.py'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        )
        
        self.assertEqual(result.returncode, 1)
        self.assertIn("terminal", result.stderr.lower())
        self.assertIn("setup.sh", result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)