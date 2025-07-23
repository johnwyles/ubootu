#!/usr/bin/env python3
"""
TUI rendering methods for the Ubootu interface
"""

import curses
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MenuItem


class TUIRenderer:
    """Handles all TUI rendering operations"""
    
    def __init__(self, stdscr, menu_items, selected_items):
        self.stdscr = stdscr
        self.menu_items = menu_items
        self.selected_items = selected_items
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
    
    def draw_header(self):
        """Draw header with title and breadcrumbs"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            # Clear header area
            self.stdscr.addstr(0, 0, " " * width)
            
            # Count total selectable items
            total_items = sum(1 for item in self.menu_items.values() 
                            if not item.is_category and item.parent != "actions")
            selected_count = len(self.selected_items)
            
            # Title with selection count
            title = f"✨ UBOOTU - Ubuntu System Setup [{selected_count}/{total_items}] ✨"
            safe_title = title.encode('ascii', 'ignore').decode('ascii')
            if not safe_title.strip():
                safe_title = f"=== UBOOTU - Ubuntu System Setup [{selected_count}/{total_items}] ==="
            
            # Center the title
            title_x = max(0, (width - len(safe_title)) // 2)
            self.stdscr.attron(curses.A_REVERSE | curses.A_BOLD)
            self.stdscr.addstr(0, title_x, safe_title[:width-2])
            self.stdscr.attroff(curses.A_REVERSE | curses.A_BOLD)
            
            # Breadcrumbs
            if self.current_menu != "root":
                self.stdscr.addstr(1, 0, " " * width)
                
                breadcrumb_path = self.get_breadcrumb()
                if breadcrumb_path:
                    breadcrumb = f"📍 {breadcrumb_path} | Press BACKSPACE/ESC/LEFT/B to go back"
                else:
                    breadcrumb = f"📍 Main Menu | Press Q to quit"
                    
                safe_breadcrumb = breadcrumb.encode('ascii', 'ignore').decode('ascii')
                if not safe_breadcrumb.strip():
                    if breadcrumb_path:
                        safe_breadcrumb = f"-> {breadcrumb_path} | BACKSPACE/ESC/LEFT/B=Back"
                    else:
                        safe_breadcrumb = f"-> Main Menu | Q=Quit"
                
                self.stdscr.addstr(1, 2, safe_breadcrumb[:width-4])
        except curses.error:
            pass
    
    def get_breadcrumb(self) -> str:
        """Get breadcrumb navigation string"""
        path = []
        current = self.current_menu
        
        while current and current != "root":
            item = self.menu_items[current]
            path.append(item.label)
            current = item.parent
        
        path.reverse()
        return " > ".join(path)
    
    def draw_menu(self, menu_items: List['MenuItem']):
        """Draw the current menu"""
        height, width = self.stdscr.getmaxyx()
        
        # Calculate display area
        start_y = 3 if self.current_menu != "root" else 3
        display_height = height - start_y - 4
        
        try:
            # Clear menu area
            for i in range(start_y, height - 4):
                self.stdscr.addstr(i, 0, " " * width)
            
            # Show current menu description
            current_item = self.menu_items[self.current_menu]
            if current_item.description:
                if "F1" in current_item.description:
                    parts = current_item.description.split("|")
                    if len(parts) >= 2:
                        # Draw navigation part
                        self.stdscr.attron(curses.A_BOLD)
                        nav_part = f"🎯 {parts[0].strip()}"
                        self.stdscr.addstr(1, 2, nav_part)
                        self.stdscr.attroff(curses.A_BOLD)
                        
                        # Draw F1 instruction
                        nav_len = len(nav_part)
                        f1_x = nav_len + 7
                        self.stdscr.attron(curses.A_BOLD)
                        f1_part = parts[1].strip()
                        if f1_x + len(f1_part) < width - 2:
                            self.stdscr.addstr(1, f1_x, f1_part)
                        self.stdscr.attroff(curses.A_BOLD)
                    else:
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, 2, current_item.description[:width-4])
                        self.stdscr.attroff(curses.A_BOLD)
                else:
                    self.stdscr.attron(curses.A_BOLD)
                    desc = f"🎯 {current_item.description}"
                    safe_desc = desc.encode('ascii', 'ignore').decode('ascii')
                    if len(safe_desc.strip()) < len(desc.strip()) * 0.7:
                        safe_desc = f">>> {current_item.description}"
                    self.stdscr.addstr(1, 2, safe_desc[:width-4])
                    self.stdscr.attroff(curses.A_BOLD)
            
            # Adjust scroll
            if self.current_item < self.scroll_offset:
                self.scroll_offset = self.current_item
            elif self.current_item >= self.scroll_offset + display_height:
                self.scroll_offset = self.current_item - display_height + 1
            
            # Draw menu items
            for i, item in enumerate(menu_items[self.scroll_offset:self.scroll_offset + display_height]):
                item_index = i + self.scroll_offset
                y = start_y + i
                
                if y >= height - 4:
                    break
                
                # Highlight current item
                if item_index == self.current_item:
                    self.stdscr.attron(curses.A_REVERSE)
                
                # Get indicators
                if item.is_category:
                    status = self.get_category_selection_status(item.id)
                    if status == 'full':
                        indicator = "●"
                    elif status == 'partial':
                        indicator = "◐"
                    else:
                        indicator = "○"
                else:
                    indicator = "●" if item.selected else "○"
                
                safe_indicator = indicator.encode('ascii', 'ignore').decode('ascii')
                if not safe_indicator:
                    safe_indicator = "*" if item.selected else " "
                
                # Format item line
                label = item.label[:width-30]
                line = f" {safe_indicator} {label}"
                
                # Add current value for configurable items
                if item.is_configurable and item.selected:
                    value_display = f"[{item.config_value}{item.config_unit}]"
                    line = f"{line} {value_display}"
                
                # Draw the line
                safe_line = line[:width-2]
                if len(safe_line) > 0:
                    self.stdscr.addstr(y, 1, safe_line)
                
                # Add description
                if item.description:
                    separator_col = min(50, width - 30)
                    desc_max_len = width - separator_col - 5
                    desc = item.description[:desc_max_len]
                    
                    if separator_col < width - 5:
                        self.stdscr.addstr(y, separator_col, "│")
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(y, separator_col + 2, desc)
                        self.stdscr.attroff(curses.A_BOLD)
                        
                        if item_index == self.current_item:
                            self.stdscr.attron(curses.A_REVERSE)
                
                # Turn off reverse video
                if item_index == self.current_item:
                    self.stdscr.attroff(curses.A_REVERSE)
                    
        except curses.error:
            pass
    
    def get_category_selection_status(self, category_id: str) -> str:
        """Get selection status for a category: 'full', 'partial', 'empty'"""
        if category_id not in self.menu_items:
            return 'empty'
        
        # Get all selectable items in this category (recursively)
        selectable_items = self.get_all_selectable_items(category_id)
        
        if not selectable_items:
            return 'empty'
        
        selected_count = sum(1 for item_id in selectable_items if item_id in self.selected_items)
        
        if selected_count == 0:
            return 'empty'
        elif selected_count == len(selectable_items):
            return 'full'
        else:
            return 'partial'
    
    def get_all_selectable_items(self, category_id: str) -> List[str]:
        """Get all selectable items in a category (recursively)"""
        items = []
        category = self.menu_items.get(category_id)
        
        if not category or not category.children:
            return items
        
        for child_id in category.children:
            child = self.menu_items.get(child_id)
            if not child:
                continue
                
            if child.is_category:
                items.extend(self.get_all_selectable_items(child_id))
            else:
                items.append(child_id)
        
        return items
    
    def draw_help(self):
        """Draw help instructions at bottom"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            # Clear help area
            for i in range(height - 4, height):
                self.stdscr.addstr(i, 0, " " * width)
            
            current_menu = self.menu_items[self.current_menu]
            
            # Context-specific help
            if self.current_menu == "actions":
                help_lines = [
                    "⌨️  NAVIGATE: H=Help | ←/ESC/B=Back to Main | ENTER=Execute Action | ↑↓/JK=Move | Q=Quit",
                    "🚀 INSTALL=Save & Install | 💾 SAVE=Save Only | 🔄 RESET=Clear All | ❌ EXIT=Cancel",
                    "📍 Use arrow keys to select action, then press ENTER to execute",
                    "💡 TIP: This menu is also accessible via F1-F10 keys • Powered by Ubootu"
                ]
                fallback_help = [
                    "NAVIGATE: H=Help | LEFT/ESC/B=Back | ENTER=Execute | UP/DOWN/JK=Move | Q=Quit",
                    "INSTALL=Save & Install | SAVE=Save Only | RESET=Clear All | EXIT=Cancel",
                    "Use arrow keys to select action, then press ENTER to execute",
                    "TIP: This menu is accessible via F1-F10 keys • Powered by Ubootu"
                ]
            elif self.current_menu == "root":
                help_lines = [
                    "⚡⚡⚡ PRESS F1 TO INSTALL YOUR SELECTIONS! ⚡⚡⚡ PRESS F1 TO INSTALL! ⚡⚡⚡",
                    "⌨️  NAVIGATE: H=Help | ←/ESC=Back | →/ENTER=Enter | ↑↓/JK=Move | SPACE=Select | Q=Quit",
                    "📊 CATEGORIES: ●=All Selected | ◐=Some Selected | ○=None Selected",
                    "🚀 F1-F10 = ACTIONS MENU → START INSTALLATION → APPLY ALL SETTINGS!"
                ]
                fallback_help = [
                    "*** PRESS F1 TO INSTALL YOUR SELECTIONS! *** PRESS F1 TO INSTALL! ***",
                    "NAVIGATE: H=Help | LEFT/ESC=Back | RIGHT/ENTER=Enter | UP/DOWN=Move | SPACE=Select",
                    "CATEGORIES: ●=All Selected | ◐=Some Selected | ○=None Selected",
                    "F1-F10 = ACTIONS MENU -> START INSTALLATION -> APPLY ALL SETTINGS!"
                ]
            else:
                help_lines = [
                    "⚡⚡⚡ PRESS F1 TO INSTALL YOUR SELECTIONS! ⚡⚡⚡ PRESS F1 TO INSTALL! ⚡⚡⚡",
                    "⌨️  NAVIGATE: H=Help | ←/ESC=Back | →/ENTER=Toggle | SPACE=Select | A=All | N=None",
                    "📍 ITEMS: ●=Selected | ○=Unselected | ↑↓/JK=Move | PgUp/Dn=Page | Q=Quit",
                    "🚀 F1-F10 = ACTIONS MENU → START INSTALLATION → APPLY ALL SETTINGS!"
                ]
                fallback_help = [
                    "*** PRESS F1 TO INSTALL YOUR SELECTIONS! *** PRESS F1 TO INSTALL! ***",
                    "NAVIGATE: H=Help | LEFT/ESC=Back | RIGHT/ENTER=Toggle | SPACE=Select | A=All | N=None",
                    "ITEMS: ●=Selected | ○=Unselected | UP/DOWN=Move | PgUp/Dn=Page",
                    "F1-F10 = ACTIONS MENU -> START INSTALLATION -> APPLY ALL SETTINGS!"
                ]
            
            # Draw help lines
            for i, line in enumerate(help_lines):
                if i < 4:
                    safe_line = line.encode('ascii', 'ignore').decode('ascii')
                    if len(safe_line.strip()) < len(line.strip()) * 0.6:
                        safe_line = fallback_help[i]
                    
                    if i == 0 and "F1" in safe_line:
                        self.stdscr.attron(curses.A_BOLD)
                    
                    if len(safe_line) > 0:
                        self.stdscr.addstr(height - 4 + i, 1, safe_line[:width-2])
                    
                    if i == 0:
                        self.stdscr.attroff(curses.A_BOLD)
        except curses.error:
            pass
    
    def draw_stats(self):
        """Draw selection statistics"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            selected_count = len(self.selected_items)
            
            current_category = self.menu_items[self.current_menu]
            category_items = self.get_all_selectable_items(self.current_menu)
            category_selected = sum(1 for item_id in category_items if item_id in self.selected_items)
            
            if category_items:
                stats = f"Category: {category_selected}/{len(category_items)} | Total: {selected_count}"
                self.stdscr.addstr(height - 1, width - len(stats) - 2, stats)
        except curses.error:
            pass