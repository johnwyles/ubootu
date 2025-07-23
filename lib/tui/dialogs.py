#!/usr/bin/env python3
"""
Dialog system for the Ubootu TUI interface
"""

import curses
from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MenuItem


class TUIDialogs:
    """Handles all dialog operations for the TUI"""
    
    def __init__(self, stdscr, selected_items: Set[str]):
        self.stdscr = stdscr
        self.selected_items = selected_items
    
    def show_configuration_dialog(self, item: 'MenuItem'):
        """Show professional configuration dialog for settings"""
        if item.config_type == "slider":
            self._show_slider_dialog(item)
        elif item.config_type == "dropdown":
            self._show_dropdown_dialog(item)
        elif item.config_type == "toggle":
            self._show_toggle_dialog(item)
        elif item.config_type == "text":
            self._show_text_dialog(item)
    
    def _show_slider_dialog(self, item: 'MenuItem'):
        """Show slider configuration dialog"""
        height, width = self.stdscr.getmaxyx()
        
        # Create a configuration overlay
        dialog_height = 11 if item.id in ["swappiness", "cpu-governor"] else 10
        dialog_width = 60
        start_y = (height - dialog_height) // 2
        start_x = (width - dialog_width) // 2
        
        # Store current value
        current_value = item.config_value
        min_val, max_val = item.config_range
        
        try:
            while True:
                # Clear the dialog area
                for y in range(start_y, start_y + dialog_height):
                    if y < height:
                        self.stdscr.addstr(y, start_x, " " * min(dialog_width, width - start_x))
                
                # Draw dialog border with vibrant colors
                # Black on green
                
                # Top border
                border_line = "┌" + "─" * (dialog_width - 2) + "┐"
                self.stdscr.addstr(start_y, start_x, border_line[:dialog_width])
                
                # Title
                title = f" Configure {item.label} "
                title_x = start_x + (dialog_width - len(title)) // 2
                self.stdscr.addstr(start_y + 1, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 1, title_x, title)
                
                # Separator
                self.stdscr.addstr(start_y + 2, start_x, "├" + "─" * (dialog_width - 2) + "┤")
                
                # Description with detailed explanation for specific items
                desc = item.description[:dialog_width - 4]
                desc_x = start_x + (dialog_width - len(desc)) // 2
                self.stdscr.addstr(start_y + 3, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 3, desc_x, desc)
                
                # Add detailed explanation for specific items
                if item.id == "swappiness":
                    detail = "Low: Keeps apps in RAM | High: Frees RAM aggressively"
                    detail_x = start_x + (dialog_width - len(detail)) // 2
                    self.stdscr.addstr(start_y + 4, start_x, "│" + " " * (dialog_width - 2) + "│")
                    self.stdscr.addstr(start_y + 4, detail_x, detail)
                    slider_y_offset = 1
                elif item.id == "cpu-governor":
                    detail = "1=Save power | 3=Balanced | 5=Max performance"
                    detail_x = start_x + (dialog_width - len(detail)) // 2
                    self.stdscr.addstr(start_y + 4, start_x, "│" + " " * (dialog_width - 2) + "│")
                    self.stdscr.addstr(start_y + 4, detail_x, detail)
                    slider_y_offset = 1
                else:
                    slider_y_offset = 0
                
                # Slider
                slider_y = start_y + 4 + slider_y_offset
                self.stdscr.addstr(slider_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                
                # Slider track
                slider_width = dialog_width - 10
                slider_start = start_x + 5
                
                # Calculate slider position
                value_range = max_val - min_val
                if value_range > 0:
                    slider_pos = int((current_value - min_val) / value_range * (slider_width - 1))
                else:
                    slider_pos = 0
                
                # Draw slider track
                track = "─" * slider_width
                if slider_pos < len(track):
                    track = track[:slider_pos] + "●" + track[slider_pos + 1:]
                self.stdscr.addstr(slider_y, slider_start, track)
                
                # Value display
                value_text = f"{current_value}{item.config_unit}"
                value_y = start_y + 5 + slider_y_offset
                value_x = start_x + (dialog_width - len(value_text)) // 2
                self.stdscr.addstr(value_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(value_y, value_x, value_text)
                
                # Instructions
                instructions = "← → arrows to adjust, ENTER to confirm, ESC to cancel"
                inst_y = start_y + 6 + slider_y_offset
                inst_x = start_x + (dialog_width - len(instructions)) // 2
                self.stdscr.addstr(inst_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                if len(instructions) <= dialog_width - 4:
                    self.stdscr.addstr(inst_y, inst_x, instructions)
                
                # Bottom border
                self.stdscr.addstr(start_y + 7 + slider_y_offset, start_x, "└" + "─" * (dialog_width - 2) + "┘")
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == curses.KEY_LEFT or key == ord('h'):
                    if current_value > min_val:
                        current_value -= 1
                elif key == curses.KEY_RIGHT or key == ord('l'):
                    if current_value < max_val:
                        current_value += 1
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    # Confirm - save the value
                    item.config_value = current_value
                    item.selected = True  # Mark as configured
                    self.selected_items.add(item.id)
                    break
                elif key == 27:  # ESC - cancel
                    break
                elif key == ord('q') or key == ord('Q'):
                    break
                    
        except curses.error:
            # Handle any drawing errors gracefully
            pass
    
    def _show_dropdown_dialog(self, item: 'MenuItem'):
        """Show dropdown selection dialog"""
        height, width = self.stdscr.getmaxyx()
        
        if not item.config_options:
            return  # No options to show
            
        # Create a configuration overlay
        dialog_height = 7 + len(item.config_options)
        dialog_width = 60
        start_y = (height - dialog_height) // 2
        start_x = (width - dialog_width) // 2
        
        # Find current selection index
        current_index = 0
        for i, (value, _) in enumerate(item.config_options):
            if value == item.config_value:
                current_index = i
                break
        
        try:
            while True:
                # Clear the dialog area
                for y in range(start_y, start_y + dialog_height):
                    if y < height:
                        self.stdscr.addstr(y, start_x, " " * min(dialog_width, width - start_x))
                
                # Draw dialog border
                # Top border
                border_line = "┌" + "─" * (dialog_width - 2) + "┐"
                self.stdscr.addstr(start_y, start_x, border_line[:dialog_width])
                
                # Title
                title = f" Configure {item.label} "
                title_x = start_x + (dialog_width - len(title)) // 2
                self.stdscr.addstr(start_y + 1, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 1, title_x, title)
                
                # Separator
                self.stdscr.addstr(start_y + 2, start_x, "├" + "─" * (dialog_width - 2) + "┤")
                
                # Description
                desc = item.description[:dialog_width - 4]
                desc_x = start_x + (dialog_width - len(desc)) // 2
                self.stdscr.addstr(start_y + 3, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 3, desc_x, desc)
                
                # Options
                for i, (value, label) in enumerate(item.config_options):
                    y = start_y + 4 + i
                    self.stdscr.addstr(y, start_x, "│" + " " * (dialog_width - 2) + "│")
                    
                    # Highlight current selection
                    if i == current_index:
                        self.stdscr.attron(curses.A_REVERSE)
                        option_text = f"  ► {label}  "
                    else:
                        option_text = f"    {label}  "
                    
                    self.stdscr.addstr(y, start_x + 2, option_text[:dialog_width - 4])
                    
                    if i == current_index:
                        self.stdscr.attroff(curses.A_REVERSE)
                
                # Instructions
                instructions = "↑↓ to select, ENTER to confirm, ESC to cancel"
                inst_y = start_y + 4 + len(item.config_options) + 1
                inst_x = start_x + (dialog_width - len(instructions)) // 2
                self.stdscr.addstr(inst_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(inst_y, inst_x, instructions)
                
                # Bottom border
                self.stdscr.addstr(inst_y + 1, start_x, "└" + "─" * (dialog_width - 2) + "┘")
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == curses.KEY_UP or key == ord('k'):
                    if current_index > 0:
                        current_index -= 1
                elif key == curses.KEY_DOWN or key == ord('j'):
                    if current_index < len(item.config_options) - 1:
                        current_index += 1
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    # Confirm - save the value
                    item.config_value = item.config_options[current_index][0]
                    item.selected = True
                    self.selected_items.add(item.id)
                    break
                elif key == 27:  # ESC - cancel
                    break
                elif key == ord('q') or key == ord('Q'):
                    break
                    
        except curses.error:
            pass
    
    def _show_toggle_dialog(self, item: 'MenuItem'):
        """Show toggle (on/off) dialog"""
        height, width = self.stdscr.getmaxyx()
        
        # Create a configuration overlay
        dialog_height = 8
        dialog_width = 50
        start_y = (height - dialog_height) // 2
        start_x = (width - dialog_width) // 2
        
        # Get current value as boolean
        current_value = bool(item.config_value)
        
        try:
            while True:
                # Clear the dialog area
                for y in range(start_y, start_y + dialog_height):
                    if y < height:
                        self.stdscr.addstr(y, start_x, " " * min(dialog_width, width - start_x))
                
                # Draw dialog border
                # Top border
                self.stdscr.addstr(start_y, start_x, "┌" + "─" * (dialog_width - 2) + "┐")
                
                # Title
                title = f" Configure {item.label} "
                title_x = start_x + (dialog_width - len(title)) // 2
                self.stdscr.addstr(start_y + 1, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 1, title_x, title)
                
                # Separator
                self.stdscr.addstr(start_y + 2, start_x, "├" + "─" * (dialog_width - 2) + "┤")
                
                # Description
                desc = item.description[:dialog_width - 4]
                desc_x = start_x + (dialog_width - len(desc)) // 2
                self.stdscr.addstr(start_y + 3, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 3, desc_x, desc)
                
                # Toggle switch
                toggle_y = start_y + 4
                self.stdscr.addstr(toggle_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                
                # Draw toggle visualization
                if current_value:
                    toggle_visual = "  [━━━━━●] ON  "
                    self.stdscr.attron(curses.A_BOLD)
                else:
                    toggle_visual = "  [●━━━━━] OFF "
                
                toggle_x = start_x + (dialog_width - len(toggle_visual)) // 2
                self.stdscr.addstr(toggle_y, toggle_x, toggle_visual)
                
                if current_value:
                    self.stdscr.attroff(curses.A_BOLD)
                
                # Instructions
                instructions = "SPACE to toggle, ENTER to confirm, ESC to cancel"
                inst_y = start_y + 5
                inst_x = start_x + (dialog_width - len(instructions)) // 2
                self.stdscr.addstr(inst_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(inst_y, inst_x, instructions[:dialog_width - 4])
                
                # Bottom border
                self.stdscr.addstr(start_y + 6, start_x, "└" + "─" * (dialog_width - 2) + "┘")
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == ord(' '):
                    current_value = not current_value
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    # Confirm - save the value
                    item.config_value = current_value
                    item.selected = True
                    self.selected_items.add(item.id)
                    break
                elif key == 27:  # ESC - cancel
                    break
                elif key == ord('q') or key == ord('Q'):
                    break
                    
        except curses.error:
            pass
    
    def _show_text_dialog(self, item: 'MenuItem'):
        """Show text input dialog"""
        height, width = self.stdscr.getmaxyx()
        
        # Create a configuration overlay
        dialog_height = 9
        dialog_width = 60
        start_y = (height - dialog_height) // 2
        start_x = (width - dialog_width) // 2
        
        # Get current value as string
        current_value = str(item.config_value) if item.config_value else ""
        
        # Enable cursor for text input
        try:
            curses.curs_set(1)
        except:
            pass
        
        try:
            while True:
                # Clear the dialog area
                for y in range(start_y, start_y + dialog_height):
                    if y < height:
                        self.stdscr.addstr(y, start_x, " " * min(dialog_width, width - start_x))
                
                # Draw dialog border
                # Top border
                self.stdscr.addstr(start_y, start_x, "┌" + "─" * (dialog_width - 2) + "┐")
                
                # Title
                title = f" Configure {item.label} "
                title_x = start_x + (dialog_width - len(title)) // 2
                self.stdscr.addstr(start_y + 1, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 1, title_x, title)
                
                # Separator
                self.stdscr.addstr(start_y + 2, start_x, "├" + "─" * (dialog_width - 2) + "┤")
                
                # Description
                desc = item.description[:dialog_width - 4]
                desc_x = start_x + (dialog_width - len(desc)) // 2
                self.stdscr.addstr(start_y + 3, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 3, desc_x, desc)
                
                # Text input field
                input_y = start_y + 4
                self.stdscr.addstr(input_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                
                # Draw input box
                input_width = dialog_width - 8
                input_x = start_x + 4
                self.stdscr.addstr(input_y, input_x - 1, "[")
                self.stdscr.addstr(input_y, input_x + input_width, "]")
                
                # Display current value
                display_value = current_value[-input_width:] if len(current_value) > input_width else current_value
                self.stdscr.addstr(input_y, input_x, display_value + " " * (input_width - len(display_value)))
                
                # Place cursor at end of text
                cursor_x = input_x + len(display_value)
                if cursor_x < input_x + input_width:
                    self.stdscr.move(input_y, cursor_x)
                
                # Instructions
                instructions = "Type to edit, ENTER to confirm, ESC to cancel"
                inst_y = start_y + 6
                inst_x = start_x + (dialog_width - len(instructions)) // 2
                self.stdscr.addstr(inst_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(inst_y, inst_x, instructions)
                
                # Bottom border
                self.stdscr.addstr(start_y + 7, start_x, "└" + "─" * (dialog_width - 2) + "┘")
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    # Confirm - save the value
                    item.config_value = current_value
                    item.selected = True
                    self.selected_items.add(item.id)
                    break
                elif key == 27:  # ESC - cancel
                    break
                elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                    if len(current_value) > 0:
                        current_value = current_value[:-1]
                elif 32 <= key <= 126:  # Printable characters
                    current_value += chr(key)
                elif key == ord('q') or key == ord('Q'):
                    break
                    
        except curses.error:
            pass
        finally:
            # Hide cursor again
            try:
                curses.curs_set(0)
            except:
                pass
    
    def show_help_popup(self, item: 'MenuItem'):
        """Show context-sensitive help popup for current item"""
        height, width = self.stdscr.getmaxyx()
        
        # Create help content based on item type
        help_lines = []
        
        # Title
        help_lines.append(f"Help: {item.label}")
        
        # Description
        help_lines.append("Description:")
        # Wrap description to fit in popup
        desc_width = min(width - 10, 70)
        wrapped_desc = self._wrap_text(item.description, desc_width)
        help_lines.extend(wrapped_desc)
        
        # Item-specific help
        if item.is_category:
            help_lines.append("Type: Category/Submenu")
            help_lines.append("Actions:")
            help_lines.append("• ENTER or → : Enter this submenu")
            help_lines.append("• SPACE     : Select/deselect all items")
            help_lines.append("• ← or ESC  : Go back to parent menu")
            if item.children:
                help_lines.append(f"Contains {len(item.children)} items")
        elif item.is_configurable:
            help_lines.append(f"Type: Configurable ({item.config_type})")
            help_lines.append("Actions:")
            help_lines.append("• ENTER or → : Configure this setting")
            help_lines.append("• SPACE     : Toggle selection")
            
            # Configuration-specific info
            help_lines.append("Configuration:")
            if item.config_type == "slider":
                help_lines.append(f"• Range: {item.config_range[0]} to {item.config_range[1]}{item.config_unit}")
                help_lines.append(f"• Current: {item.config_value}{item.config_unit}")
            elif item.config_type == "dropdown":
                help_lines.append(f"• Current: {item.config_value}")
                if item.config_options:
                    help_lines.append(f"• Options: {len(item.config_options)} choices")
            elif item.config_type == "toggle":
                help_lines.append(f"• Current: {'Enabled' if item.config_value else 'Disabled'}")
            elif item.config_type == "text":
                help_lines.append(f"• Current: {item.config_value or '(not set)'}")
        else:
            help_lines.append("Type: Toggle Item")
            help_lines.append("Actions:")
            help_lines.append("• SPACE or ENTER : Select/deselect")
            help_lines.append(f"• Status: {'Selected' if item.selected else 'Not selected'}")
        
        # Ansible variable mapping
        if item.ansible_var:
            help_lines.append("Technical Details:")
            help_lines.append(f"• Ansible variable: {item.ansible_var}")
        
        # Default status
        if item.default:
            help_lines.append("ℹ️ This item is selected by default")
        
        # Add navigation help
        help_lines.append("─" * (desc_width - 2))
        help_lines.append("Press any key to close this help")
        
        # Calculate popup dimensions
        popup_width = max(len(line) for line in help_lines) + 6
        popup_width = min(popup_width, width - 4)
        popup_height = min(len(help_lines) + 4, height - 4)
        
        # Center popup
        start_y = (height - popup_height) // 2
        start_x = (width - popup_width) // 2
        
        try:
            # Draw popup background
            for y in range(start_y, start_y + popup_height):
                if y < height:
                    self.stdscr.addstr(y, start_x, " " * min(popup_width, width - start_x))
            
            # Draw border
            # Top border
            self.stdscr.addstr(start_y, start_x, "╔" + "═" * (popup_width - 2) + "╗")
            
            # Content with side borders
            for i, line in enumerate(help_lines[:popup_height - 4]):
                y = start_y + i + 2
                if y < height - 1:
                    self.stdscr.addstr(y, start_x, "║ ")
                    # Truncate line if too long
                    display_line = line[:popup_width - 4]
                    self.stdscr.addstr(y, start_x + 2, display_line)
                    # Right border
                    padding = popup_width - len(display_line) - 3
                    self.stdscr.addstr(y, start_x + 2 + len(display_line), " " * padding + "║")
            
            # Bottom border
            bottom_y = start_y + popup_height - 1
            if bottom_y < height:
                self.stdscr.addstr(bottom_y, start_x, "╚" + "═" * (popup_width - 2) + "╝")
            
            self.stdscr.refresh()
            
            # Save current timeout and set to blocking mode for help popup
            old_timeout = self.stdscr.timeout(-1)  # Set to blocking mode
            
            # Wait for any key
            self.stdscr.getch()
            
            # Restore original timeout
            self.stdscr.timeout(50)  # Restore the default timeout
            
        except curses.error:
            pass
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        if not text:
            return []
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            if current_length + word_length + len(current_line) <= width:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines