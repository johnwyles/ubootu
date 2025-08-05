#!/usr/bin/env python3
"""
Curses-based quick actions menu for Ubootu
Provides quick access to common tasks
"""

import curses
import subprocess
from typing import List, Dict, Optional

from .constants import *
from .utils import *
from .dialogs import MessageDialog, ConfirmDialog


class QuickActionsMenu:
    """Quick actions for common tasks"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_index = 0
        
        # Define quick actions
        self.actions = [
            {
                'id': 'update_system',
                'label': 'Update System',
                'description': 'Run apt update && apt upgrade',
                'icon': '🔄',
                'command': ['sudo', 'apt', 'update', '&&', 'sudo', 'apt', 'upgrade', '-y'],
                'needs_sudo': True
            },
            {
                'id': 'clean_packages',
                'label': 'Clean Packages',
                'description': 'Remove unused packages and clean cache',
                'icon': '🧹',
                'command': ['sudo', 'apt', 'autoremove', '-y', '&&', 'sudo', 'apt', 'autoclean'],
                'needs_sudo': True
            },
            {
                'id': 'check_updates',
                'label': 'Check Updates',
                'description': 'Check for available system updates',
                'icon': '🔍',
                'command': ['apt', 'list', '--upgradable'],
                'needs_sudo': False
            },
            {
                'id': 'system_info',
                'label': 'System Information',
                'description': 'Show system information',
                'icon': 'ℹ️',
                'command': ['uname', '-a', '&&', 'lsb_release', '-a'],
                'needs_sudo': False
            },
            {
                'id': 'disk_usage',
                'label': 'Disk Usage',
                'description': 'Show disk space usage',
                'icon': '💾',
                'command': ['df', '-h'],
                'needs_sudo': False
            },
            {
                'id': 'restart_network',
                'label': 'Restart Network',
                'description': 'Restart network services',
                'icon': '🌐',
                'command': ['sudo', 'systemctl', 'restart', 'NetworkManager'],
                'needs_sudo': True
            },
            {
                'id': 'view_logs',
                'label': 'View System Logs',
                'description': 'Show recent system log entries',
                'icon': '📋',
                'command': ['journalctl', '-xe', '--lines=50'],
                'needs_sudo': False
            },
            {
                'id': 'install_updates',
                'label': 'Install Security Updates',
                'description': 'Install only security updates',
                'icon': '🔒',
                'command': ['sudo', 'apt', 'upgrade', '-y', '--only-upgrade'],
                'needs_sudo': True
            }
        ]
        
        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
        except:
            pass
            
    def render(self) -> None:
        """Render the quick actions menu"""
        self.stdscr.clear()
        
        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return
            
        # Draw header
        self.render_header()
        
        # Draw actions list
        self.render_actions()
        
        # Draw help bar
        self.render_help_bar()
        
        self.stdscr.refresh()
        
    def render_size_error(self) -> None:
        """Render terminal size error"""
        msg = f"Terminal too small! Minimum {MIN_WIDTH}x{MIN_HEIGHT}"
        draw_centered_text(self.stdscr, self.height // 2, msg, bold=True)
        
    def render_header(self) -> None:
        """Render the header"""
        draw_box(self.stdscr, 0, 0, 3, self.width)
        draw_centered_text(self.stdscr, 1, "⚡ Quick Actions", bold=True)
        
    def render_actions(self) -> None:
        """Render the actions list"""
        # Calculate list area
        start_y = 4
        list_height = self.height - start_y - 4
        
        # Draw actions box
        draw_box(self.stdscr, start_y - 1, 0, list_height + 2, self.width)
        
        # Calculate visible range
        visible_start = max(0, self.current_index - list_height // 2)
        visible_end = min(len(self.actions), visible_start + list_height)
        
        # Adjust if at the end
        if visible_end - visible_start < list_height:
            visible_start = max(0, visible_end - list_height)
            
        # Draw actions
        for i, action in enumerate(self.actions[visible_start:visible_end]):
            y = start_y + i
            selected = (visible_start + i) == self.current_index
            self.render_action_item(y, 2, action, selected, self.width - 4)
            
    def render_action_item(self, y: int, x: int, action: dict, selected: bool, max_width: int) -> None:
        """Render a single action item"""
        # Build action text
        sudo_indicator = "🔐" if action['needs_sudo'] else "  "
        text = f"{sudo_indicator} {action['icon']} {action['label']} - {action['description']}"
        text = truncate_text(text, max_width)
        
        # Draw with selection highlight
        try:
            if selected:
                self.stdscr.attron(curses.A_REVERSE)
                
            self.stdscr.addstr(y, x, text.ljust(max_width))
            
            if selected:
                self.stdscr.attroff(curses.A_REVERSE)
        except curses.error:
            pass
            
    def render_help_bar(self) -> None:
        """Render the help bar at bottom"""
        y = self.height - 2
        help_text = "↑↓ Navigate  Enter Run  ESC Back  🔐=Needs sudo"
        
        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)
        
    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        # Navigation
        if key_matches(key, KEY_BINDINGS['navigate_up']):
            self.current_index = (self.current_index - 1) % len(self.actions)
            return 'navigate'
            
        elif key_matches(key, KEY_BINDINGS['navigate_down']):
            self.current_index = (self.current_index + 1) % len(self.actions)
            return 'navigate'
            
        # Run action
        elif key_matches(key, KEY_BINDINGS['select']):
            return 'run'
            
        # Back
        elif key_matches(key, KEY_BINDINGS['back']):
            return 'back'
            
        # Quit
        elif key_matches(key, KEY_BINDINGS['quit']):
            return 'quit'
            
        return None
        
    def run_action(self) -> None:
        """Run the selected action"""
        if self.current_index >= len(self.actions):
            return
            
        action = self.actions[self.current_index]
        
        # Confirm if action needs sudo
        if action['needs_sudo']:
            dialog = ConfirmDialog(self.stdscr)
            if not dialog.show(f"Run '{action['label']}'?", 
                             "This action requires administrator privileges."):
                return
                
        # Prepare command
        command = ' '.join(action['command'])
        
        # Clear screen and show command
        self.stdscr.clear()
        self.stdscr.refresh()
        
        # Exit curses temporarily to run command
        curses.endwin()
        
        try:
            # Run the command
            print(f"\n🚀 Running: {command}\n")
            result = subprocess.run(command, shell=True, text=True)
            
            if result.returncode == 0:
                print(f"\n✅ '{action['label']}' completed successfully!")
            else:
                print(f"\n❌ '{action['label']}' failed with exit code {result.returncode}")
                
            print("\nPress Enter to continue...")
            input()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Action cancelled by user")
            print("\nPress Enter to continue...")
            input()
        except Exception as e:
            print(f"\n❌ Error running action: {str(e)}")
            print("\nPress Enter to continue...")
            input()
        finally:
            # Restore curses
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.stdscr.keypad(True)
            try:
                curses.curs_set(0)
            except:
                pass
                
    def run(self) -> None:
        """Run the quick actions menu"""
        while True:
            self.render()
            
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return
                
            action = self.navigate(key)
            
            if action == 'run':
                self.run_action()
                
            elif action in ['back', 'quit']:
                return
                
            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()