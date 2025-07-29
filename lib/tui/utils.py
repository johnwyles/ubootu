#!/usr/bin/env python3
"""
Utility functions for the unified TUI
"""

import curses
from typing import Optional, Tuple


def center_text(width: int, text: str) -> int:
    """Calculate x position to center text"""
    return max(0, (width - len(text)) // 2)


def draw_box(stdscr, y: int, x: int, height: int, width: int, title: Optional[str] = None) -> None:
    """Draw a box with optional title using single-line characters"""
    try:
        # Draw corners
        stdscr.addch(y, x, curses.ACS_ULCORNER)
        stdscr.addch(y, x + width - 1, curses.ACS_URCORNER)
        stdscr.addch(y + height - 1, x, curses.ACS_LLCORNER)
        stdscr.addch(y + height - 1, x + width - 1, curses.ACS_LRCORNER)
        
        # Draw horizontal lines
        for i in range(1, width - 1):
            stdscr.addch(y, x + i, curses.ACS_HLINE)
            stdscr.addch(y + height - 1, x + i, curses.ACS_HLINE)
            
        # Draw vertical lines
        for i in range(1, height - 1):
            stdscr.addch(y + i, x, curses.ACS_VLINE)
            stdscr.addch(y + i, x + width - 1, curses.ACS_VLINE)
            
        # Draw title if provided
        if title:
            title = f" {title} "
            title_x = x + center_text(width, title)
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(y, title_x, title[:width-2])
            stdscr.attroff(curses.A_BOLD)
            
    except curses.error:
        pass


def draw_centered_text(stdscr, y: int, text: str, bold: bool = False) -> None:
    """Draw centered text at given y position"""
    try:
        height, width = stdscr.getmaxyx()
        x = center_text(width, text)
        
        if bold:
            stdscr.attron(curses.A_BOLD)
            
        stdscr.addstr(y, x, text[:width])
        
        if bold:
            stdscr.attroff(curses.A_BOLD)
            
    except curses.error:
        pass


def truncate_text(text: str, max_width: int, suffix: str = "...") -> str:
    """Truncate text to fit within max_width"""
    if len(text) <= max_width:
        return text
        
    if max_width <= len(suffix):
        return text[:max_width]
        
    return text[:max_width - len(suffix)] + suffix


def get_dialog_position(screen_height: int, screen_width: int, 
                       dialog_height: int, dialog_width: int) -> Tuple[int, int]:
    """Calculate centered position for a dialog"""
    y = max(0, (screen_height - dialog_height) // 2)
    x = max(0, (screen_width - dialog_width) // 2)
    return y, x


def parse_key(key: int) -> Optional[str]:
    """Parse key code to string representation"""
    if key == curses.KEY_UP:
        return 'KEY_UP'
    elif key == curses.KEY_DOWN:
        return 'KEY_DOWN'
    elif key == curses.KEY_LEFT:
        return 'KEY_LEFT'
    elif key == curses.KEY_RIGHT:
        return 'KEY_RIGHT'
    elif key == curses.KEY_F1:
        return 'KEY_F1'
    elif key == 27:
        return 'ESC'
    elif key == ord('\n'):
        return '\n'
    elif 32 <= key <= 126:  # Printable ASCII
        return chr(key)
    return None


def key_matches(key: int, binding: list) -> bool:
    """Check if a key matches any in the binding list"""
    key_str = parse_key(key)
    if key_str and key_str in binding:
        return True
    
    # Only try chr() for printable ASCII range
    if 32 <= key <= 126:
        char = chr(key)
        if char in binding:
            return True
    
    return False