#!/usr/bin/env python3
"""
Section selector for the unified TUI
Allows users to select which sections to configure
"""

import curses
from typing import List, Dict, Set

from .constants import *
from .utils import *
from .dialogs import MessageDialog, ConfirmDialog


class SectionSelector:
    """Section selector using unified TUI style"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_index = 0
        self.selections: Set[str] = set()
        
        # Define available sections
        self.sections = [
            {
                'id': 'desktop',
                'label': 'Desktop Environment',
                'description': 'GNOME, KDE, XFCE, and more',
                'icon': '🖥️'
            },
            {
                'id': 'applications',
                'label': 'Applications',
                'description': 'Browsers, productivity, multimedia',
                'icon': '📦'
            },
            {
                'id': 'development',
                'label': 'Development Tools',
                'description': 'IDEs, languages, containers',
                'icon': '💻'
            },
            {
                'id': 'security',
                'label': 'Security & Privacy',
                'description': 'Firewall, VPN, encryption',
                'icon': '🔒'
            },
            {
                'id': 'themes',
                'label': 'Themes & Appearance',
                'description': 'Icons, fonts, wallpapers',
                'icon': '🎨'
            },
            {
                'id': 'system',
                'label': 'System Configuration',
                'description': 'Performance, services, hardware',
                'icon': '⚙️'
            },
        ]
        
        # Initialize curses
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
        except:
            pass
            
    def render(self) -> None:
        """Render the section selector"""
        self.stdscr.clear()
        
        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return
            
        # Draw header
        self.render_header()
        
        # Draw sections
        self.render_sections()
        
        # Draw help bar
        self.render_help_bar()
        
        self.stdscr.refresh()
        
    def render_size_error(self) -> None:
        """Render terminal size error"""
        msg = f"Terminal too small! Minimum {MIN_WIDTH}x{MIN_HEIGHT}"
        draw_centered_text(self.stdscr, self.height // 2, msg, bold=True)
        
    def render_header(self) -> None:
        """Render the header section"""
        # Draw title box
        draw_box(self.stdscr, 0, 0, 4, self.width, "Modify Setup - Select Sections")
        
        # Draw subtitle
        draw_centered_text(self.stdscr, 2, "Which sections would you like to configure?")
        
    def render_sections(self) -> None:
        """Render the section list"""
        # Calculate menu area
        start_y = 6
        menu_height = self.height - start_y - 3  # Leave room for help bar
        
        # Draw menu box
        draw_box(self.stdscr, start_y - 1, 2, menu_height + 2, self.width - 4)
        
        # Draw sections
        for i, section in enumerate(self.sections):
            if i >= menu_height:
                break
                
            y = start_y + i
            self.render_section(y, section, i == self.current_index)
            
    def render_section(self, y: int, section: Dict, selected: bool) -> None:
        """Render a single section"""
        x = 4
        max_width = self.width - 8
        
        # Build section text
        is_selected = section['id'] in self.selections
        checkbox = CHECKBOX_SELECTED if is_selected else CHECKBOX_UNSELECTED
        icon = section.get('icon', '')
        text = f"{checkbox} {icon} {section['label']} - {section['description']}"
        
        # Truncate if needed
        text = truncate_text(text, max_width)
        
        # Draw with selection highlight
        try:
            if selected:
                self.stdscr.attron(curses.A_REVERSE)
                
            self.stdscr.addstr(y, x, text.ljust(max_width - 2))
            
            if selected:
                self.stdscr.attroff(curses.A_REVERSE)
        except curses.error:
            pass
            
    def render_help_bar(self) -> None:
        """Render the help bar at bottom"""
        y = self.height - 2
        help_text = "↑↓ Navigate  Space Select  A Select All  N Clear All  Enter Continue  ESC Cancel"
        
        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)
        
    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        # Navigation
        if key_matches(key, KEY_BINDINGS['navigate_up']):
            self.current_index = (self.current_index - 1) % len(self.sections)
            return 'navigate'
            
        elif key_matches(key, KEY_BINDINGS['navigate_down']):
            self.current_index = (self.current_index + 1) % len(self.sections)
            return 'navigate'
            
        # Selection
        elif key_matches(key, KEY_BINDINGS['select']):
            self.toggle_selection()
            return 'select'
            
        # Select all
        elif key_matches(key, KEY_BINDINGS['select_all']):
            self.selections = set(section['id'] for section in self.sections)
            return 'select_all'
            
        # Deselect all
        elif key_matches(key, KEY_BINDINGS['deselect_all']):
            self.selections.clear()
            return 'deselect_all'
            
        # Continue
        elif key_matches(key, KEY_BINDINGS['enter']):
            return 'continue'
            
        # Cancel
        elif key == 27 or key_matches(key, KEY_BINDINGS['quit']):  # ESC or Q
            return 'cancel'
            
        return None
        
    def toggle_selection(self) -> None:
        """Toggle selection of current section"""
        if self.current_index >= len(self.sections):
            return
            
        section_id = self.sections[self.current_index]['id']
        
        if section_id in self.selections:
            self.selections.remove(section_id)
        else:
            self.selections.add(section_id)
            
    def run(self) -> List[str]:
        """Run the section selector and return selected sections"""
        while True:
            self.render()
            
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return []
                
            action = self.navigate(key)
            
            if action == 'continue':
                if self.selections:
                    # Confirm selections
                    selected_names = []
                    for section in self.sections:
                        if section['id'] in self.selections:
                            selected_names.append(f"{section['icon']} {section['label']}")
                            
                    confirm_msg = f"You have selected {len(self.selections)} section(s):\n\n"
                    for name in selected_names:
                        confirm_msg += f"  {name}\n"
                    confirm_msg += "\nProceed with configuration?"
                    
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Confirm Selection", confirm_msg, default=True):
                        return list(self.selections)
                    # If not confirmed, continue selecting
                else:
                    # No sections selected
                    dialog = MessageDialog(self.stdscr)
                    dialog.show("No Selection", "Please select at least one section to configure.")
                    
            elif action == 'cancel':
                return []
                
            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()


def show_section_selector(stdscr) -> List[str]:
    """Show section selector and return selected sections"""
    selector = SectionSelector(stdscr)
    return selector.run()