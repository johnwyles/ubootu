#!/usr/bin/env python3
"""
Ubootu - The Ultimate Ubuntu Experience Engine
Hierarchical TUI with modular design for professional desktop configuration

This is now a lightweight wrapper around the refactored TUI modules.
"""

import sys
import os

# Add the lib directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# Import the new modular TUI
from tui import run_tui, main


# Maintain backward compatibility with the original interface
def run_hierarchical_tui(selected_sections=None):
    """Run the hierarchical TUI - backward compatibility wrapper"""
    return run_tui(selected_sections)


if __name__ == "__main__":
    # Run the main TUI
    main()