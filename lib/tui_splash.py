#!/usr/bin/env python3
"""
Ubootu TUI Splash Screen
Curses-based splash screen with loading animation
"""

import sys
import os
import curses
import time
from typing import Optional

class TUISplash:
    """TUI splash screen with loading animation"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # NO COLORS - Monochrome interface only
        pass
        
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
        except:
            pass
    
    def get_logo_lines(self):
        """Get ASCII logo lines for UBOOTU in cool 3D block style"""
        return [
            "██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗",
            "██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║", 
            "██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║",
            "██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║",
            "╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝",
            " ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ "
        ]
    
    def get_compact_logo_lines(self):
        """Get compact ASCII logo lines for UBOOTU"""
        return [
            "╔══════════════════════════════════════════════════════╗",
            "║                    🚀 U B O O T U 🚀                    ║",
            "╚══════════════════════════════════════════════════════╝"
        ]
    
    def draw_centered_text(self, y, text, color_pair=0, bold=False):
        """Draw centered text at given y position"""
        try:
            x = max(0, (self.width - len(text)) // 2)
            if y >= 0 and y < self.height and x < self.width:
                attrs = 0
                if bold:
                    attrs |= curses.A_BOLD
                self.stdscr.addstr(y, x, text[:self.width-x], attrs)
        except:
            pass
    
    def draw_left_aligned_centered_block(self, y, text, color_pair=0, bold=False):
        """Draw left-aligned text that's centered as a block"""
        try:
            # Calculate the x position to center the text block
            x = max(0, (self.width - len(text)) // 2)
            if y >= 0 and y < self.height and x < self.width:
                attrs = 0
                if bold:
                    attrs |= curses.A_BOLD
                self.stdscr.addstr(y, x, text[:self.width-x], attrs)
        except:
            pass
    
    def draw_logo(self, start_y):
        """Draw the UBOOTU logo in monochrome"""
        logo_lines = self.get_logo_lines()
        for i, line in enumerate(logo_lines):
            if start_y + i < self.height:
                self.draw_centered_text(start_y + i, line, 0, True)
    
    def draw_progress_bar(self, y, progress, width=40):
        """Draw a progress bar"""
        try:
            filled = int(progress * width / 100)
            bar = "█" * filled + "░" * (width - filled)
            progress_text = f"[{bar}] {progress}%"
            self.draw_centered_text(y, progress_text, 0, True)
        except:
            pass
    
    def show_splash_with_loading(self):
        """Show splash screen with loading animation"""
        for progress in range(101):
            self.stdscr.clear()
            
            # Calculate positions
            logo_start = max(2, (self.height - 15) // 2)
            
            # Draw logo
            self.draw_logo(logo_start)
            
            # Draw title and tagline
            self.draw_centered_text(logo_start + 8, "🚀 UBOOTU 🚀", 0, True)
            self.draw_centered_text(logo_start + 9, "Ubuntu Desktop Configuration Tool", 0)
            self.draw_centered_text(logo_start + 10, "Version 2.0", 0)
            
            # Draw loading
            self.draw_centered_text(logo_start + 12, f"Loading Ubootu... {progress}%", 0)
            self.draw_progress_bar(logo_start + 13, progress)
            
            self.stdscr.refresh()
            time.sleep(0.03)
        
        # Brief pause after loading completes
        self.draw_centered_text(logo_start + 15, "✅ Ready! Loading options...", 0, True)
        self.stdscr.refresh()
        time.sleep(1)
    
    def show_main_menu(self):
        """Show main menu options after loading"""
        while True:
            self.stdscr.clear()
            
            # Calculate positions
            logo_start = 1
            
            # Draw full logo at top (same as splash screen)
            self.draw_logo(logo_start)
            
            # Draw title
            self.draw_centered_text(logo_start + 7, "🚀 UBOOTU 🚀", 0, True)
            self.draw_centered_text(logo_start + 8, "Ubuntu Desktop Configuration Tool", 0)
            
            # Draw menu options - centered as a block but left-aligned within
            menu_start = logo_start + 10
            options = [
                "1. 🚀 Fresh Install - Configure a brand new Ubuntu installation",
                "2. 🔧 Modify Setup - Tweak your existing configuration", 
                "3. 📦 Apply Profile - Restore from a saved configuration",
                "4. 💾 Backup Config - Save your current setup",
                "5. 📜 View History - Browse configuration timeline",
                "6. 🎯 Quick Actions - Common tasks and fixes",
                "7. ❓ Help - Get help and documentation",
                "8. 🚪 Exit - See you later!"
            ]
            
            self.draw_centered_text(menu_start, "What would you like to do?", 0, True)
            
            # Find the longest option for centering the block
            max_width = max(len(option) for option in options)
            start_x = max(0, (self.width - max_width) // 2)
            
            for i, option in enumerate(options):
                if menu_start + 2 + i < self.height:
                    try:
                        self.stdscr.addstr(menu_start + 2 + i, start_x, option, 
                                         curses.A_BOLD)
                    except:
                        pass
            
            # Draw input prompt
            self.draw_centered_text(self.height - 3, "Enter your choice (1-8): ", 0, True)
            
            self.stdscr.refresh()
            
            # Get input
            try:
                curses.echo()
                curses.curs_set(1)
                choice_y = self.height - 3
                choice_x = (self.width + len("Enter your choice (1-8): ")) // 2
                choice = self.stdscr.getstr(choice_y, choice_x, 1).decode('utf-8').strip()
                curses.noecho()
                curses.curs_set(0)
                
                if choice.isdigit() and 1 <= int(choice) <= 8:
                    return choice
                elif choice == 'q' or choice == 'Q':
                    return "8"
                    
            except (KeyboardInterrupt, EOFError):
                return "8"
            except:
                continue
    
    def run(self):
        """Run the complete splash and menu sequence"""
        try:
            # Show splash with loading
            self.show_splash_with_loading()
            
            # Show main menu and get choice
            choice = self.show_main_menu()
            
            # Write choice to temp file for bash to read
            with open('/tmp/welcome_choice.txt', 'w') as f:
                f.write(choice)
                
            return True
            
        except Exception as e:
            # Fallback - write default choice
            with open('/tmp/welcome_choice.txt', 'w') as f:
                f.write("8")
            return False

def main(stdscr):
    """Main TUI function"""
    splash = TUISplash(stdscr)
    return splash.run()

def show_tui_splash():
    """Entry point for TUI splash screen"""
    try:
        return curses.wrapper(main)
    except Exception as e:
        # Fallback for terminals that don't support curses
        print("TUI not supported, falling back to basic interface")
        with open('/tmp/welcome_choice.txt', 'w') as f:
            f.write("1")  # Default to fresh install
        return False

if __name__ == "__main__":
    show_tui_splash()