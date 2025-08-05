#!/usr/bin/env python3
"""
Curses-based configuration backup tool for Ubootu
Saves current configuration as a profile
"""

import curses
import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from .constants import *
from .utils import *
from .dialogs import MessageDialog, InputDialog, ConfirmDialog


class BackupConfig:
    """Backup current configuration as a profile"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.config_file = Path("config.yml")
        self.profile_dir = Path("profiles")
        
        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
        except:
            pass
            
    def render(self) -> None:
        """Render the backup interface"""
        self.stdscr.clear()
        
        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return
            
        # Draw header
        self.render_header()
        
        # Draw instructions
        self.render_instructions()
        
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
        draw_centered_text(self.stdscr, 1, "💾 Backup Configuration", bold=True)
        
    def render_instructions(self) -> None:
        """Render backup instructions"""
        # Calculate content area
        start_y = 4
        content_height = self.height - start_y - 4
        
        # Draw content box
        draw_box(self.stdscr, start_y - 1, 0, content_height + 2, self.width)
        
        # Check if config exists
        if not self.config_file.exists():
            draw_centered_text(self.stdscr, self.height // 2, 
                             "No configuration found to backup!")
            draw_centered_text(self.stdscr, self.height // 2 + 2, 
                             "Create a configuration first using Fresh Install or Modify Setup")
            return
            
        # Show current configuration info
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
                
            items_count = len(config.get('selected_items', []))
            config_count = len(config.get('configurable_items', {}))
            
            lines = [
                "Current Configuration:",
                "",
                f"  Selected Items: {items_count}",
                f"  Configured Items: {config_count}",
                "",
                "Press Enter to create a backup profile",
                "Press ESC to go back"
            ]
            
            y = start_y + 2
            for line in lines:
                if y < self.height - 5:
                    draw_centered_text(self.stdscr, y, line)
                    y += 1
                    
        except Exception as e:
            draw_centered_text(self.stdscr, self.height // 2, 
                             f"Error reading configuration: {str(e)}")
            
    def render_help_bar(self) -> None:
        """Render the help bar at bottom"""
        y = self.height - 2
        help_text = "Enter Create Backup  ESC Back"
        
        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)
        
    def get_system_info(self) -> dict:
        """Get current system information"""
        info = {
            'hostname': os.uname().nodename,
            'version': 'Unknown',
            'kernel': os.uname().release
        }
        
        # Try to get Ubuntu version
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('VERSION='):
                        info['version'] = line.split('=')[1].strip().strip('"')
                        break
        except:
            pass
            
        return info
        
    def create_backup(self) -> bool:
        """Create a backup profile from current configuration"""
        if not self.config_file.exists():
            return False
            
        # Get profile name
        input_dialog = InputDialog(self.stdscr)
        profile_name = input_dialog.show("Profile Name", 
                                       "Enter a name for this profile:",
                                       default=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not profile_name:
            return False
            
        # Get description
        description = input_dialog.show("Profile Description", 
                                      "Enter a description (optional):",
                                      default="My Ubuntu configuration")
        
        # Create profiles directory if needed
        self.profile_dir.mkdir(exist_ok=True)
        
        # Generate filename
        safe_name = "".join(c for c in profile_name if c.isalnum() or c in ('_', '-'))
        profile_path = self.profile_dir / f"{safe_name}.yml"
        
        # Check if file exists
        if profile_path.exists():
            confirm_dialog = ConfirmDialog(self.stdscr)
            if not confirm_dialog.show("Profile Exists", 
                                     f"Profile '{safe_name}' already exists. Overwrite?"):
                return False
                
        try:
            # Load current configuration
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
                
            # Add metadata
            config['metadata'] = {
                'name': profile_name,
                'description': description,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'system_info': self.get_system_info(),
                'version': config.get('metadata', {}).get('version', '1.0')
            }
            
            # Save profile
            with open(profile_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
                
            # Show success
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Success", 
                          f"Profile '{profile_name}' created successfully!\n\n"
                          f"Saved to: {profile_path}")
            return True
            
        except Exception as e:
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Error", f"Failed to create backup: {str(e)}", "error")
            return False
            
    def run(self) -> bool:
        """Run the backup tool and return success status"""
        while True:
            self.render()
            
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                return False
                
            # Handle keys
            if key_matches(key, KEY_BINDINGS['select']):
                if self.config_file.exists():
                    if self.create_backup():
                        return True
                        
            elif key_matches(key, KEY_BINDINGS['back']) or key_matches(key, KEY_BINDINGS['quit']):
                return False
                
            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()