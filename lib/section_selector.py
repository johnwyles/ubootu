#!/usr/bin/env python3
"""
Section Selector TUI for Ubootu
Allows users to select which sections to configure
"""

import sys
import curses
from typing import List, Tuple
from lib.overlay_dialog import SelectionOverlay, MessageOverlay, ConfirmOverlay


def show_section_selector(stdscr) -> List[str]:
    """Show section selection dialog and return selected sections"""
    
    # Define available sections
    sections = [
        ("desktop", "🖥️ Desktop Environment - GNOME, KDE, XFCE, and more"),
        ("applications", "📦 Applications - Browsers, productivity, multimedia"),
        ("development", "💻 Development Tools - IDEs, languages, containers"),
        ("security", "🔒 Security & Privacy - Firewall, VPN, encryption"),
        ("themes", "🎨 Themes & Appearance - Icons, fonts, wallpapers"),
        ("system", "⚙️ System Configuration - Performance, services, hardware"),
    ]
    
    # Custom instructions for section selection
    instructions = [
        "Which sections would you like to configure?",
        "• Use ↑↓ arrow keys to navigate between sections",
        "• Press SPACE to select/deselect a section", 
        "• Press A to select all sections",
        "• Press N to clear all selections",
        "• Press ENTER when you're ready to continue",
        "• Press ESC to cancel and return to main menu"
    ]
    
    dialog = SelectionOverlay(stdscr)
    
    # Show dialog and get selections
    selected = dialog.show(
        title="Modify Setup - Select Sections",
        items=sections,
        multi_select=True,
        selected_items=[],
        instructions=instructions
    )
    
    # If user selected sections, show confirmation
    if selected:
        # Build confirmation message
        selected_names = []
        for section_id in selected:
            for sid, name in sections:
                if sid == section_id:
                    selected_names.append(name.split(" - ")[0])  # Get just the emoji and name
                    break
                    
        confirm_msg = f"You have selected {len(selected)} section(s) to configure:\n\n"
        for name in selected_names:
            confirm_msg += f"  {name}\n"
        confirm_msg += "\nProceed with configuration?"
        
        confirm_dialog = ConfirmOverlay(stdscr)
        if not confirm_dialog.show("Confirm Selection", confirm_msg, default=True):
            # User cancelled, show message and return empty
            msg_dialog = MessageOverlay(stdscr)
            msg_dialog.show("Cancelled", "Configuration cancelled. Returning to main menu.", "info")
            return []
    else:
        # No sections selected
        msg_dialog = MessageOverlay(stdscr)
        msg_dialog.show("No Selection", "No sections were selected. Returning to main menu.", "info")
        
    return selected


def main():
    """Main entry point for section selector"""
    try:
        selected = curses.wrapper(show_section_selector)
        
        # Write selections to temp file for bash to read
        with open('/tmp/selected_sections.txt', 'w') as f:
            f.write(','.join(selected))
            
        return 0
        
    except Exception as e:
        # On error, write empty selection
        with open('/tmp/selected_sections.txt', 'w') as f:
            f.write('')
        return 1


if __name__ == "__main__":
    sys.exit(main())