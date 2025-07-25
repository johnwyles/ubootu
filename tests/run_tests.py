#!/usr/bin/env python3
"""Simple test runner for CI without pytest dependency."""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_imports import (test_main_script_imports, test_splash_and_ui_imports,
                          test_tui_imports)
from test_tui_compilation import (test_other_lib_modules_compile,
                                  test_tui_modules_compile)


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("Running Ubootu Test Suite")
    print("=" * 70)

    test_results = []

    # Run compilation tests
    print("\n1. TUI Module Compilation Tests")
    print("-" * 40)
    try:
        test_tui_modules_compile()
        test_results.append(("TUI Module Compilation", True, None))
    except AssertionError as e:
        test_results.append(("TUI Module Compilation", False, str(e)))
        print(f"\nFAILED: {e}")

    print("\n2. Other Library Module Compilation Tests")
    print("-" * 40)
    try:
        test_other_lib_modules_compile()
        test_results.append(("Other Module Compilation", True, None))
    except AssertionError as e:
        test_results.append(("Other Module Compilation", False, str(e)))
        print(f"\nFAILED: {e}")

    # Run import tests
    print("\n3. TUI Import Tests")
    print("-" * 40)
    try:
        test_tui_imports()
        test_results.append(("TUI Imports", True, None))
    except AssertionError as e:
        test_results.append(("TUI Imports", False, str(e)))
        print(f"\nFAILED: {e}")

    print("\n4. Main Script Import Tests")
    print("-" * 40)
    try:
        test_main_script_imports()
        test_results.append(("Main Script Imports", True, None))
    except AssertionError as e:
        test_results.append(("Main Script Imports", False, str(e)))
        print(f"\nFAILED: {e}")

    print("\n5. UI Module Import Tests")
    print("-" * 40)
    try:
        test_splash_and_ui_imports()
        test_results.append(("UI Module Imports", True, None))
    except AssertionError as e:
        test_results.append(("UI Module Imports", False, str(e)))
        print(f"\nFAILED: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success, _ in test_results if success)
    failed = len(test_results) - passed

    for test_name, success, error in test_results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
        if error:
            print(f"  Error: {error}")

    print(f"\nTotal: {len(test_results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        print("\nTEST SUITE FAILED")
        return 1
    else:
        print("\nALL TESTS PASSED!")
        return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
