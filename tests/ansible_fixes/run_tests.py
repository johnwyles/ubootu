#!/usr/bin/env python3
"""
Test runner for Ansible fixes
"""

import os
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests in the correct order"""
    test_files = [
        "test_variable_passing.py",
        "test_ubuntu_repos.py",
        "test_prerequisites.py",
        "test_packages.py",
        "test_full_run.py",
    ]

    test_dir = Path(__file__).parent
    os.chdir("/home/jwyles/code/ubootu")

    # Add project to Python path
    env = os.environ.copy()
    env["PYTHONPATH"] = f"/home/jwyles/code/ubootu:{env.get('PYTHONPATH', '')}"

    print("Running Ansible Fix Tests")
    print("=" * 50)

    total_passed = 0
    total_failed = 0

    for test_file in test_files:
        print(f"\nRunning {test_file}...")
        print("-" * 30)

        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_dir / test_file), "-v", "--tb=short"],
            env=env,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        # Count results
        if result.returncode == 0:
            print(f"✓ {test_file} PASSED")
            total_passed += 1
        else:
            print(f"✗ {test_file} FAILED")
            total_failed += 1

    print("\n" + "=" * 50)
    print(f"Summary: {total_passed} passed, {total_failed} failed")

    if total_failed > 0:
        print("\nExpected failures - now implement fixes to make tests pass!")
        return 1
    else:
        print("\nAll tests passing!")
        return 0


if __name__ == "__main__":
    exit(run_tests())
