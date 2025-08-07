#!/usr/bin/env python3
"""
Integration tests for complete TUI flow
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))


class TestCompleteTUIFlow(unittest.TestCase):
    """Test the complete TUI flow from start to finish"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    def test_help_message(self):
        """Test that help message works"""
        result = subprocess.run(
            [sys.executable, "configure_standard_tui.py", "--help"], capture_output=True, text=True, cwd=self.test_dir
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Ubootu Configuration Tool", result.stdout)
        self.assertIn("--no-tui", result.stdout)

    def test_no_tui_mode(self):
        """Test non-interactive mode"""
        result = subprocess.run(
            [sys.executable, "configure_standard_tui.py", "--no-tui"], capture_output=True, text=True, cwd=self.test_dir
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("non-interactive", result.stdout)
        self.assertIn("setup.sh", result.stdout)

    def test_non_tty_error_message(self):
        """Test error message when not in TTY"""
        result = subprocess.run(
            [sys.executable, "configure_standard_tui.py"], capture_output=True, text=True, cwd=self.test_dir
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("terminal", result.stderr.lower())
        self.assertIn("setup.sh", result.stderr)
        # Should NOT show raw curses error
        self.assertNotIn("nocbreak()", result.stderr)

    def test_environment_diagnostic(self):
        """Test environment diagnostic utility"""
        result = subprocess.run(
            [sys.executable, "-m", "lib.tui.environment"], capture_output=True, text=True, cwd=self.test_dir
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Terminal Environment Diagnostics", result.stdout)
        self.assertIn("TTY:", result.stdout)
        self.assertIn("Prerequisites:", result.stdout)

    def test_import_chain(self):
        """Test that all imports work correctly"""
        test_script = """
import sys
sys.path.insert(0, 'lib')

# Test main imports
try:
    from tui.unified_menu import UnifiedMenu
    print("✓ UnifiedMenu imported")
except ImportError as e:
    print(f"✗ UnifiedMenu import failed: {e}")

try:
    from tui.main_menu import MainMenu
    print("✓ MainMenu imported")
except ImportError as e:
    print(f"✗ MainMenu import failed: {e}")

try:
    from tui.prerequisite_installer import PrerequisiteInstaller
    print("✓ PrerequisiteInstaller imported")
except ImportError as e:
    print(f"✗ PrerequisiteInstaller import failed: {e}")

try:
    from tui.progress_dialog import ProgressDialog
    print("✓ ProgressDialog imported")
except ImportError as e:
    print(f"✗ ProgressDialog import failed: {e}")

try:
    from tui.sudo_dialog import SudoDialog
    print("✓ SudoDialog imported")
except ImportError as e:
    print(f"✗ SudoDialog import failed: {e}")

try:
    from tui.environment import get_terminal_info
    print("✓ Environment utilities imported")
except ImportError as e:
    print(f"✗ Environment import failed: {e}")
"""

        result = subprocess.run([sys.executable, "-c", test_script], capture_output=True, text=True, cwd=self.test_dir)

        self.assertEqual(result.returncode, 0)
        # All imports should succeed
        self.assertNotIn("✗", result.stdout)
        self.assertEqual(result.stdout.count("✓"), 6)

    def test_sections_argument(self):
        """Test --sections argument parsing"""
        # This should fail gracefully since we're not in TTY
        result = subprocess.run(
            [sys.executable, "configure_standard_tui.py", "--sections", "development,applications"],
            capture_output=True,
            text=True,
            cwd=self.test_dir,
        )

        # Should still show terminal error
        self.assertEqual(result.returncode, 1)
        self.assertIn("terminal", result.stderr.lower())


class TestSetupShIntegration(unittest.TestCase):
    """Test integration with setup.sh"""

    def test_tui_mode_environment(self):
        """Test that TUI_MODE is properly set"""
        test_script = """
#!/bin/bash
export TUI_MODE="1"
echo "TUI_MODE=$TUI_MODE"

# Test that print_info is suppressed
print_info() {
    [[ "$TUI_MODE" != "1" ]] && echo "[INFO] $1"
}

print_info "This should not appear"
echo "Done"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False) as f:
            f.write(test_script)
            f.flush()
            os.chmod(f.name, 0o755)

            result = subprocess.run(["bash", f.name], capture_output=True, text=True)

            os.unlink(f.name)

        self.assertEqual(result.returncode, 0)
        self.assertIn("TUI_MODE=1", result.stdout)
        self.assertNotIn("[INFO]", result.stdout)
        self.assertIn("Done", result.stdout)


class TestErrorRecovery(unittest.TestCase):
    """Test error recovery and edge cases"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    def test_missing_lib_directory(self):
        """Test behavior when lib directory is missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal script without lib directory
            script_path = Path(tmpdir) / "test_tui.py"
            script_path.write_text(
                """#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

try:
    from tui.unified_menu import UnifiedMenu
except ImportError as e:
    print(f"Expected import error: {e}")
    sys.exit(1)
"""
            )

            result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)

            self.assertEqual(result.returncode, 1)
            self.assertIn("Expected import error", result.stdout)

    def test_partial_imports(self):
        """Test that system handles missing optional imports gracefully"""
        test_script = """
import sys
sys.path.insert(0, 'lib')

# Test that missing ansible doesn't break main menu
import builtins
real_import = builtins.__import__

def mock_import(name, *args, **kwargs):
    if name == "ansible":
        raise ImportError("No module named 'ansible'")
    return real_import(name, *args, **kwargs)

builtins.__import__ = mock_import

try:
    from tui.main_menu import MainMenu
    print("MainMenu imported successfully without ansible")
except ImportError as e:
    print(f"Unexpected failure: {e}")
"""

        result = subprocess.run([sys.executable, "-c", test_script], capture_output=True, text=True, cwd=self.test_dir)

        self.assertEqual(result.returncode, 0)
        self.assertIn("successfully", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
