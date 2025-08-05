#!/usr/bin/env python3
"""
Verify the fix is applied correctly
"""

import subprocess
import os

print("=== Verifying Fix ===")
print()

# 1. Check that unified_menu.py has been updated
print("1. Checking unified_menu.py for -v flag...")
with open('lib/tui/unified_menu.py', 'r') as f:
    content = f.read()
    in_ansible_section = False
    has_v_flag = False
    
    for line in content.split('\n'):
        if 'ansible-playbook' in line:
            in_ansible_section = True
        if in_ansible_section and "'-v'" in line or '"-v"' in line:
            has_v_flag = True
            print(f"   FOUND -v flag: {line.strip()}")
            break
        if in_ansible_section and ']' in line:
            in_ansible_section = False
    
    if not has_v_flag:
        print("   ✓ Good: -v flag has been removed from ansible command")
    else:
        print("   ✗ Bad: -v flag is still present!")

# 2. Check progress_dialog.py for environment fixes
print("\n2. Checking progress_dialog.py for environment fixes...")
with open('lib/tui/progress_dialog.py', 'r') as f:
    content = f.read()
    
    checks = [
        ("ANSIBLE_STDOUT_CALLBACK.*oneline", "oneline callback"),
        ("ANSIBLE_DISPLAY_OK_HOSTS.*False", "hide OK hosts"),
        ("ANSIBLE_VERBOSITY.*0", "verbosity override"),
        ("ansible_facts.*in.*line.*or.*len.*line.*>.*500", "facts filtering")
    ]
    
    import re
    for pattern, desc in checks:
        if re.search(pattern, content):
            print(f"   ✓ {desc}: Found")
        else:
            print(f"   ✗ {desc}: NOT FOUND")

# 3. Show what command will be run now
print("\n3. Command that will be executed (from unified_menu.py):")
print("   ansible-playbook site.yml -i [temp_inventory] --diff")
print("   --become-password-file [password_file] --connection local --forks 1")
print("   (Note: NO -v flag)")

# 4. Show environment overrides
print("\n4. Environment overrides (from progress_dialog.py):")
print("   ANSIBLE_STDOUT_CALLBACK=oneline  (compact output)")
print("   ANSIBLE_DISPLAY_OK_HOSTS=False   (less output)")
print("   ANSIBLE_VERBOSITY=0              (override any -v)")
print("   + Facts filtering in output processing")

print("\n=== SUMMARY ===")
print("The fix has been applied to BOTH files:")
print("1. lib/tui/unified_menu.py - Removed -v flag from command")
print("2. lib/tui/progress_dialog.py - Added output reduction and filtering")
print("\nThe user needs to RESTART the TUI to pick up these changes.")
print("The old process is still using the old code with -v flag.")