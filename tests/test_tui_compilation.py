#!/usr/bin/env python3
"""Test that all TUI modules compile successfully."""

import os
import py_compile
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_tui_modules_compile():
    """Test that all TUI Python modules compile without syntax errors."""
    project_root = Path(__file__).parent.parent

    # List of TUI modules to test (updated for enhanced_menu_ui)
    tui_modules = [
        "configure_standard_tui.py",
        "lib/enhanced_menu_ui.py",
        "lib/enhanced_menu_ui_old.py",
        "lib/ubootu_splash.py",
        "lib/show_profile_templates.py",
        "lib/menu_ui.py",
    ]

    errors = []
    for module in tui_modules:
        module_path = project_root / module
        if module_path.exists():
            try:
                py_compile.compile(str(module_path), doraise=True)
                print(f"✓ {module} compiled successfully")
            except py_compile.PyCompileError as e:
                errors.append(f"✗ {module}: {e}")
                print(f"✗ {module} failed to compile: {e}")
            except FileNotFoundError:
                # Skip if module doesn't exist (e.g., old lib/tui structure removed)
                print(f"- {module} not found (skipped)")

    # Assert no compilation errors
    assert not errors, f"Compilation errors found:\n" + "\n".join(errors)
    print(f"\nAll {len(tui_modules)} TUI modules compiled successfully!")


def test_other_lib_modules_compile():
    """Test that other lib modules compile without syntax errors."""
    project_root = Path(__file__).parent.parent
    lib_path = project_root / "lib"

    # List of other lib modules
    other_modules = [
        "lib/__init__.py",
        "lib/app_customization_templates.py",
        "lib/app_defaults.py",
        "lib/apt_fixer.py",
        "lib/backup_config_tui.py",
        "lib/config_models.py",
        "lib/config_validator.py",
        "lib/help_viewer.py",
        "lib/history_viewer.py",
        "lib/menu_dialog.py",
        "lib/overlay_dialog.py",
        "lib/profile_manager.py",
        "lib/profile_selector.py",
        "lib/quick_actions_tui.py",
        "lib/section_selector.py",
        "lib/terminal_check.py",
        "lib/terminal_customization.py",
        "lib/tui_components.py",
        "lib/tui_dialogs.py",
        "lib/tui_splash.py",
    ]

    errors = []
    for module in other_modules:
        module_path = project_root / module
        if module_path.exists():
            try:
                py_compile.compile(str(module_path), doraise=True)
                print(f"✓ {module} compiled successfully")
            except py_compile.PyCompileError as e:
                errors.append(f"✗ {module}: {e}")
                print(f"✗ {module} failed to compile: {e}")

    # Assert no compilation errors
    assert not errors, f"Compilation errors found:\n" + "\n".join(errors)
    print(f"\nAll lib modules compiled successfully!")


if __name__ == "__main__":
    print("Testing TUI module compilation...\n")
    test_tui_modules_compile()
    print("\nTesting other lib module compilation...\n")
    test_other_lib_modules_compile()
