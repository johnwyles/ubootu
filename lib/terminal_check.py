#!/usr/bin/env python3
"""
Terminal compatibility checker for TUI
"""

import curses
import locale
import os
import sys


def check_terminal_capabilities():
    """Check if terminal supports required features for TUI"""
    issues = []
    warnings = []

    # Check if we're in a real terminal (more lenient)
    if not sys.stdout.isatty() and not os.environ.get("FORCE_TUI"):
        warnings.append("Output may not be connected to terminal")
        # Don't make this a hard failure - let curses decide

    # Check TERM environment variable
    term = os.environ.get("TERM", "unknown")
    if term == "unknown":
        warnings.append("TERM environment variable not set")
    elif term == "dumb":
        issues.append("Terminal type is 'dumb' - no advanced features supported")
    elif term not in [
        "xterm",
        "xterm-256color",
        "screen",
        "screen-256color",
        "tmux",
        "tmux-256color",
        "linux",
        "rxvt",
        "rxvt-unicode",
    ]:
        warnings.append(f"Uncommon terminal type: {term}")

    # Check terminal size (more lenient)
    try:
        columns = os.get_terminal_size().columns
        lines = os.get_terminal_size().lines
        if columns < 80:
            warnings.append(f"Terminal width may be too small ({columns} columns)")
        if lines < 24:
            warnings.append(f"Terminal height may be too small ({lines} lines)")
    except:
        warnings.append("Cannot determine terminal size - will try anyway")

    # Check locale
    try:
        current_locale = locale.getlocale()
        if current_locale[1] is None:
            warnings.append("No character encoding set in locale")
        elif "UTF" not in current_locale[1].upper():
            warnings.append(f"Non-UTF locale detected: {current_locale[1]}")
    except:
        warnings.append("Cannot determine locale settings")

    # Check for SSH/remote session
    if os.environ.get("SSH_CLIENT") or os.environ.get("SSH_TTY"):
        warnings.append("Running over SSH - some features may not work correctly")

    # Check if running in screen/tmux
    if os.environ.get("STY"):
        warnings.append("Running inside GNU Screen")
    if os.environ.get("TMUX"):
        warnings.append("Running inside tmux")

    return issues, warnings


def test_curses_basic(interactive=True):
    """Test basic curses functionality"""
    try:

        def test_screen(stdscr):
            # Basic setup
            try:
                curses.curs_set(0)
            except curses.error:
                # Some terminals don't support cursor visibility changes
                pass
            stdscr.keypad(True)

            # Test colors
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            # Test basic drawing
            height, width = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.box()

            # Test addstr
            test_string = "Terminal Test"
            stdscr.addstr(1, 1, test_string)

            # Test special characters (ASCII only)
            stdscr.addstr(2, 1, "[OK] Basic functionality working")

            stdscr.refresh()

            if interactive:
                stdscr.getch()

            return None

        curses.wrapper(test_screen)
        return True, None
    except Exception as e:
        return False, str(e)


def can_run_tui():
    """Determine if TUI can run successfully"""
    issues, warnings = check_terminal_capabilities()

    # Critical issues prevent TUI from running
    if issues:
        return False, issues, warnings

    # Test curses (non-interactive)
    curses_ok, curses_error = test_curses_basic(interactive=False)
    if not curses_ok:
        issues.append(f"Curses test failed: {curses_error}")
        return False, issues, warnings

    return True, [], warnings


def print_compatibility_report():
    """Print detailed compatibility report"""
    can_run, issues, warnings = can_run_tui()

    print("Terminal Compatibility Check")
    print("=" * 40)
    print(f"Terminal: {os.environ.get('TERM', 'unknown')}")

    try:
        size = os.get_terminal_size()
        print(f"Size: {size.columns}x{size.lines}")
    except:
        print("Size: unknown")

    print(f"Locale: {locale.getlocale()}")
    print()

    if issues:
        print("[CRITICAL ISSUES]")
        for issue in issues:
            print(f"  ✗ {issue}")
        print()

    if warnings:
        print("[WARNINGS]")
        for warning in warnings:
            print(f"  ! {warning}")
        print()

    if can_run:
        print("[OK] Terminal appears compatible with TUI")
        return 0
    else:
        print("[FAIL] Terminal is not compatible with TUI")
        print("\nSuggestions:")
        print("  - Use a modern terminal emulator (gnome-terminal, konsole, xterm)")
        print("  - Ensure terminal size is at least 80x24")
        print("  - Set TERM environment variable (export TERM=xterm-256color)")
        print("  - Use the classic wizard interface instead")
        return 1


if __name__ == "__main__":
    sys.exit(print_compatibility_report())
