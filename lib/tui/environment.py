#!/usr/bin/env python3
"""
Environment detection utilities for TUI
"""

import sys
import os
from typing import Dict, Any


def get_terminal_info() -> Dict[str, Any]:
    """Get information about the terminal environment"""
    info = {
        "is_tty": sys.stdout.isatty(),
        "term": os.environ.get("TERM", "not set"),
        "columns": None,
        "lines": None,
        "color_support": False,
        "unicode_support": True,  # Assume UTF-8 by default
    }
    
    # Get terminal size if in TTY
    if info["is_tty"]:
        try:
            size = os.get_terminal_size()
            info["columns"] = size.columns
            info["lines"] = size.lines
        except:
            pass
    
    # Check color support
    if info["term"] and "color" in info["term"]:
        info["color_support"] = True
    elif info["term"] in ["xterm", "screen", "tmux"]:
        info["color_support"] = True
    
    # Check Unicode support
    try:
        sys.stdout.write("✓")
        sys.stdout.flush()
    except:
        info["unicode_support"] = False
    
    return info


def check_prerequisites() -> Dict[str, bool]:
    """Check which prerequisites are installed"""
    prereqs = {
        "python3": True,  # We're running Python
        "pip": False,
        "ansible": False,
        "yaml": False,
        "curses": False,
    }
    
    # Check pip
    try:
        import pip
        prereqs["pip"] = True
    except ImportError:
        # Try subprocess
        import subprocess
        try:
            subprocess.run(["pip3", "--version"], capture_output=True, check=True)
            prereqs["pip"] = True
        except:
            pass
    
    # Check ansible
    try:
        import ansible
        prereqs["ansible"] = True
    except ImportError:
        pass
    
    # Check yaml
    try:
        import yaml
        prereqs["yaml"] = True
    except ImportError:
        pass
    
    # Check curses
    try:
        import curses
        prereqs["curses"] = True
    except ImportError:
        pass
    
    return prereqs


def is_suitable_for_tui() -> bool:
    """Check if environment is suitable for running TUI"""
    info = get_terminal_info()
    
    # Must be in TTY
    if not info["is_tty"]:
        return False
    
    # Should have reasonable terminal size
    if info["columns"] and info["lines"]:
        if info["columns"] < 80 or info["lines"] < 24:
            return False
    
    # Should have curses available
    try:
        import curses
    except ImportError:
        return False
    
    return True


def get_diagnostic_info() -> str:
    """Get diagnostic information for troubleshooting"""
    lines = ["=== Terminal Environment Diagnostics ==="]
    
    # Terminal info
    info = get_terminal_info()
    lines.append("\nTerminal Information:")
    lines.append(f"  TTY: {info['is_tty']}")
    lines.append(f"  TERM: {info['term']}")
    lines.append(f"  Size: {info['columns']}x{info['lines']}")
    lines.append(f"  Color: {info['color_support']}")
    lines.append(f"  Unicode: {info['unicode_support']}")
    
    # Prerequisites
    prereqs = check_prerequisites()
    lines.append("\nPrerequisites:")
    for name, installed in prereqs.items():
        status = "✓" if installed else "✗"
        lines.append(f"  {status} {name}")
    
    # Python info
    lines.append("\nPython Information:")
    lines.append(f"  Version: {sys.version.split()[0]}")
    lines.append(f"  Executable: {sys.executable}")
    
    # Environment variables
    lines.append("\nRelevant Environment Variables:")
    for var in ["TERM", "COLORTERM", "LANG", "LC_ALL", "PYTHONPATH"]:
        value = os.environ.get(var, "not set")
        lines.append(f"  {var}: {value}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Print diagnostic info when run directly
    print(get_diagnostic_info())