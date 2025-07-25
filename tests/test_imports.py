#!/usr/bin/env python3
"""Test that all TUI modules can be imported successfully."""

import importlib
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_tui_imports():
    """Test that all TUI modules can be imported without errors."""
    # List of modules to import (now using enhanced_menu_ui)
    modules_to_import = [
        "lib.enhanced_menu_ui",
        "lib.enhanced_menu_ui_old",
    ]

    errors = []
    for module_name in modules_to_import:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ {module_name} imported successfully")
        except ImportError as e:
            errors.append(f"✗ {module_name}: {e}")
            print(f"✗ {module_name} failed to import: {e}")
        except Exception as e:
            errors.append(f"✗ {module_name}: {type(e).__name__}: {e}")
            print(f"✗ {module_name} failed with error: {type(e).__name__}: {e}")

    # Assert no import errors
    assert not errors, f"Import errors found:\n" + "\n".join(errors)
    print(f"\nAll {len(modules_to_import)} TUI modules imported successfully!")


def test_main_script_imports():
    """Test that the main configure script can import TUI modules."""
    try:
        # Test importing from the main script's perspective
        from lib.enhanced_menu_ui import main, run_tui

        print("✓ Main TUI functions imported successfully from configure_standard_tui.py perspective")
    except ImportError as e:
        raise AssertionError(f"Failed to import main TUI functions: {e}")


def test_splash_and_ui_imports():
    """Test that splash and UI utility modules can be imported."""
    ui_modules = [
        "lib.ubootu_splash",
        "lib.show_profile_templates",
        "lib.menu_ui",
    ]

    errors = []
    for module_name in ui_modules:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ {module_name} imported successfully")
        except ImportError as e:
            errors.append(f"✗ {module_name}: {e}")
            print(f"✗ {module_name} failed to import: {e}")

    assert not errors, f"UI module import errors found:\n" + "\n".join(errors)
    print("\nAll UI modules imported successfully!")


if __name__ == "__main__":
    print("Testing TUI module imports...\n")
    test_tui_imports()
    print("\nTesting main script imports...\n")
    test_main_script_imports()
    print("\nTesting splash and UI imports...\n")
    test_splash_and_ui_imports()
