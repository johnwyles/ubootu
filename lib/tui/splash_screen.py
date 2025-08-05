#!/usr/bin/env python3
"""
Curses-based splash screen for Ubootu
Replaces the Rich-based version with unified TUI style
"""

import curses
import time
import random
from typing import List

from .constants import *
from .utils import *


class SplashScreen:
    """Animated splash screen using curses"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.version = "3.0"
        self.tagline = "Professional Ubuntu Desktop Configuration Tool"
        
        # Initialize curses
        try:
            curses.curs_set(0)
            self.stdscr.keypad(True)
            self.stdscr.nodelay(True)  # Non-blocking input
        except:
            pass
            
    def get_ascii_logo(self) -> List[str]:
        """Get ASCII art logo"""
        return [
            "██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗",
            "██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║",
            "██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║",
            "██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║",
            "╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝",
            " ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ",
        ]
        
    def render_logo(self, y_offset: int = 0) -> None:
        """Render the ASCII logo centered"""
        logo = self.get_ascii_logo()
        
        # Calculate starting position
        logo_width = max(len(line) for line in logo)
        logo_height = len(logo)
        
        start_y = (self.height - logo_height) // 2 + y_offset
        start_x = (self.width - logo_width) // 2
        
        # Draw logo
        for i, line in enumerate(logo):
            y = start_y + i
            if 0 <= y < self.height:
                try:
                    self.stdscr.attron(curses.A_BOLD)
                    self.stdscr.addstr(y, start_x, line)
                    self.stdscr.attroff(curses.A_BOLD)
                except curses.error:
                    pass
                    
    def render_loading_bar(self, progress: float) -> None:
        """Render a loading progress bar"""
        bar_width = min(60, self.width - 20)
        bar_y = self.height - 6
        
        # Calculate filled portion
        filled = int(bar_width * progress)
        
        # Draw progress bar
        bar_x = (self.width - bar_width) // 2
        
        try:
            # Draw bar outline
            self.stdscr.addstr(bar_y, bar_x - 1, "[")
            self.stdscr.addstr(bar_y, bar_x + bar_width, "]")
            
            # Draw filled portion
            if filled > 0:
                self.stdscr.addstr(bar_y, bar_x, "█" * filled)
                
            # Draw empty portion
            if filled < bar_width:
                self.stdscr.addstr(bar_y, bar_x + filled, "░" * (bar_width - filled))
                
            # Draw percentage
            percentage = f"{int(progress * 100)}%"
            self.stdscr.addstr(bar_y + 1, (self.width - len(percentage)) // 2, percentage)
        except curses.error:
            pass
            
    def render_status(self, message: str) -> None:
        """Render status message below loading bar"""
        y = self.height - 3
        # Clear the line first
        try:
            self.stdscr.addstr(y, 0, " " * self.width)
            draw_centered_text(self.stdscr, y, message)
        except curses.error:
            pass
            
    def animate_intro(self) -> None:
        """Animate the intro sequence"""
        self.stdscr.clear()
        
        # Fade in effect (simulate with delays)
        steps = [
            ("Initializing Ubootu...", 0.1),
            ("Loading configuration system...", 0.2),
            ("Preparing Ubuntu tools...", 0.4),
            ("Setting up environment...", 0.6),
            ("Finalizing setup...", 0.8),
            ("Ready!", 1.0)
        ]
        
        for message, progress in steps:
            self.stdscr.clear()
            
            # Render logo
            self.render_logo(-3)
            
            # Render tagline
            tagline_y = (self.height // 2) + 5
            draw_centered_text(self.stdscr, tagline_y, self.tagline)
            draw_centered_text(self.stdscr, tagline_y + 1, f"Version {self.version}")
            
            # Render loading bar
            self.render_loading_bar(progress)
            
            # Render status
            self.render_status(message)
            
            self.stdscr.refresh()
            
            # Check for skip key
            key = self.stdscr.getch()
            if key == ord(' ') or key == ord('\n') or key == 27:  # Space, Enter, or ESC
                break
                
            time.sleep(0.3)
            
    def show_full_splash(self) -> None:
        """Show the full splash screen with animations"""
        # Animate intro
        self.animate_intro()
        
        # Final screen
        self.stdscr.clear()
        self.render_logo()
        
        # Add additional info
        info_y = (self.height // 2) + 8
        draw_centered_text(self.stdscr, info_y, "🚀 " + self.tagline + " 🚀", bold=True)
        draw_centered_text(self.stdscr, info_y + 2, "Created by John Wyles with Claude")
        draw_centered_text(self.stdscr, info_y + 3, f"Version {self.version}")
        
        # Add "Press any key" message
        draw_centered_text(self.stdscr, self.height - 2, "Press any key to continue...")
        
        self.stdscr.refresh()
        
        # Wait for keypress
        self.stdscr.nodelay(False)  # Blocking input
        self.stdscr.getch()
        
    def show_simple_splash(self) -> None:
        """Show a simple splash screen without animations"""
        self.stdscr.clear()
        
        # Render logo
        self.render_logo()
        
        # Render info
        info_y = (self.height // 2) + 8
        draw_centered_text(self.stdscr, info_y, self.tagline, bold=True)
        draw_centered_text(self.stdscr, info_y + 2, f"Version {self.version}")
        
        self.stdscr.refresh()
        
        # Brief pause
        time.sleep(1.5)


def show_splash(stdscr, animated: bool = True) -> None:
    """Show the splash screen"""
    splash = SplashScreen(stdscr)
    
    if animated:
        splash.show_full_splash()
    else:
        splash.show_simple_splash()