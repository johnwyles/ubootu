#!/usr/bin/env python3
"""
Ubootu - The Ultimate Ubuntu Experience Engine
Unified curses-based TUI for professional desktop configuration
"""

import os
import sys
import curses
import argparse

# Add the lib directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from tui.unified_menu import UnifiedMenu  # noqa: E402
from tui.main_menu import MainMenu  # noqa: E402


def run_unified_tui(stdscr, selected_sections=None):
    """Run the unified TUI"""
    while True:
        # Show the main menu
        main_menu = MainMenu(stdscr)
        choice = main_menu.run()
        
        # Handle main menu choices
        if choice == '1' or choice == '2':  # Fresh Install or Modify Setup
            # Show the configuration menu
            config_menu = UnifiedMenu(stdscr)
            config_exit_code = config_menu.run()
            if config_exit_code == 0:
                return 0  # Configuration saved successfully
            elif config_exit_code == 2:
                # User wants to return to main menu
                continue
            else:
                return 1  # Configuration cancelled
        elif choice == '3':  # Apply Profile
            # TODO: Implement profile selection
            continue  # Return to main menu
        elif choice == '4':  # Backup Config
            # TODO: Implement backup functionality
            continue  # Return to main menu
        elif choice == '5':  # View History
            # TODO: Implement history viewer
            continue  # Return to main menu
        elif choice == '6':  # Quick Actions
            # TODO: Implement quick actions menu
            continue  # Return to main menu
        elif choice == '7':  # Help
            # TODO: Show help
            continue  # Return to main menu
        elif choice == '8':  # Exit
            return 1  # User chose to exit
        
        return 1  # Default to cancelled


def check_terminal_environment():
    """Check if we're in a proper terminal environment"""
    if not sys.stdout.isatty():
        print("Error: This program requires an interactive terminal.", file=sys.stderr)
        print("\nYou appear to be running this script in a non-interactive environment.", file=sys.stderr)
        print("Please try one of the following:", file=sys.stderr)
        print("  1. Run this script directly in a terminal", file=sys.stderr)
        print("  2. Use ./setup.sh for the full installation process", file=sys.stderr)
        print("  3. Use --help to see available options", file=sys.stderr)
        return False
    
    # Check TERM environment variable
    if not os.environ.get('TERM'):
        print("Warning: TERM environment variable is not set.", file=sys.stderr)
        print("Some terminal features may not work correctly.", file=sys.stderr)
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Ubootu Configuration Tool')
    parser.add_argument('--sections', type=str, help='Comma-separated list of sections to configure')
    parser.add_argument('--no-tui', action='store_true', help='Run in non-interactive mode (show information only)')
    args = parser.parse_args()
    
    # Handle non-interactive mode
    if args.no_tui:
        print("Running in non-interactive mode.")
        print("\nTo generate a configuration file:")
        print("  1. Run this script in an interactive terminal")
        print("  2. Or use ./setup.sh for the full setup process")
        print("\nFor more information, see the documentation.")
        sys.exit(0)
    
    # Check terminal environment
    if not check_terminal_environment():
        sys.exit(1)
    
    # Parse sections if provided
    selected_sections = None
    if args.sections:
        selected_sections = [s.strip() for s in args.sections.split(',')]
    
    try:
        # Run the TUI
        exit_code = curses.wrapper(run_unified_tui, selected_sections)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nConfiguration cancelled by user")
        sys.exit(1)
    except curses.error as e:
        print(f"\nError initializing terminal interface: {e}", file=sys.stderr)
        print("Please ensure you are running this in a proper terminal.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


# Maintain backward compatibility
def run_hierarchical_tui(selected_sections=None):
    """Run the hierarchical TUI - backward compatibility wrapper"""
    return curses.wrapper(run_unified_tui, selected_sections)


if __name__ == "__main__":
    main()
