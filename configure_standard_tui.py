#!/usr/bin/env python3
"""
Ubootu - The Ultimate Ubuntu Experience Engine
Hierarchical TUI with modular design for professional desktop configuration

This is now a lightweight wrapper around the refactored TUI modules.
"""

import os
import sys

# Add the lib directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from tui import main, run_tui  # noqa: E402


# Maintain backward compatibility with the original interface
def run_hierarchical_tui(selected_sections=None):
    """Run the hierarchical TUI - backward compatibility wrapper"""
    return run_tui(selected_sections)


if __name__ == "__main__":
    # Run the main TUI
    main()
