#!/usr/bin/env python3
"""
Unified menu system for Ubootu
Single consistent curses-based menu implementation
"""

import curses
import yaml
from typing import Dict, List, Optional, Set, Union, Any
from pathlib import Path

from .constants import *
from .utils import *
from .menu_items import load_menu_structure
from .dialogs import HelpDialog, MessageDialog, ConfirmDialog, SliderDialog, SpinnerDialog, SelectDialog
from .sudo_dialog import SudoDialog
from .progress_dialog import ProgressDialog

# Import missing dependencies
try:
    from .menu_items import load_menu_structure
except ImportError:
    # Fallback for testing
    def load_menu_structure():
        return []


class UnifiedMenu:
    """Unified menu system for entire application"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Menu state
        self.current_menu = 'root'
        self.current_index = 0
        self.selections: Dict[str, Union[bool, Set[str]]] = {}
        self.configurable_values: Dict[str, Any] = {}
        self.breadcrumb: List[str] = ['Root']
        
        # Menu structure
        self.items: List[Dict] = []
        self.menu_stack: List[str] = []
        self.category_items: Dict[str, Set[str]] = {}
        
        # Configuration
        self.config_file = 'config.yml'
        
        # Initialize curses
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
        except:
            pass
            
    def load_menu_structure(self) -> None:
        """Load the complete menu structure"""
        self.items = load_menu_structure()
        
        # Build category mappings AFTER items are fully loaded
        # This ensures we get the final children arrays, not the initial empty ones
        self.category_items = {}
        for item in self.items:
            if item.get('is_category'):
                # Get all children (both categories and items)
                children = item.get('children', [])
                if children:
                    self.category_items[item['id']] = set(children)
                
    def load_defaults(self) -> None:
        """Load default selections from menu items"""
        for item in self.items:
            item_id = item['id']
            
            # Load default selections
            if item.get('default', False) and not item.get('is_category'):
                parent = item.get('parent')
                
                if parent and parent in self.category_items:
                    # Item is part of a category
                    if parent not in self.selections:
                        self.selections[parent] = set()
                    self.selections[parent].add(item_id)
                else:
                    # Top-level item
                    self.selections[item_id] = True
                    
            # Load default configurable values
            if item.get('is_configurable') and 'default_value' in item:
                self.configurable_values[item_id] = item['default_value']
    
    def load_configuration(self) -> None:
        """Load existing configuration from file"""
        if not Path(self.config_file).exists():
            return
            
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
                
            # Clear all selections (including defaults) before loading saved config
            self.selections = {}
            
            # Load selected items
            selected = config.get('selected_items', [])
            for item_id in selected:
                # Check if it's a category
                if item_id in self.category_items:
                    # Load category selections
                    self.selections[item_id] = set()
                    for child in self.category_items[item_id]:
                        if child in selected:
                            self.selections[item_id].add(child)
                else:
                    self.selections[item_id] = True
                    
            # Load configurable values
            configurable = config.get('configurable_items', {})
            for item_id, item_config in configurable.items():
                self.configurable_values[item_id] = item_config.get('value')
                
        except Exception:
            pass
            
    def save_configuration(self) -> None:
        """Save current configuration to file"""
        config = {
            'metadata': {
                'version': '1.0',
                'created_by': 'ubootu_unified_tui'
            },
            'selected_items': [],
            'configurable_items': {}
        }
        
        # Save selections
        for item_id, value in self.selections.items():
            if isinstance(value, set):
                # Category with selected children
                config['selected_items'].append(item_id)
                config['selected_items'].extend(list(value))
            elif value:
                config['selected_items'].append(item_id)
                
        # Save configurable values
        for item_id, value in self.configurable_values.items():
            config['configurable_items'][item_id] = {
                'id': item_id,
                'value': value
            }
            
        # Write to file
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
    def get_current_items(self) -> List[Dict]:
        """Get items for current menu level"""
        if self.current_menu == 'root':
            return [item for item in self.items if item.get('parent') is None]
        else:
            return [item for item in self.items if item.get('parent') == self.current_menu]
            
    def get_all_descendant_items(self, category_id: str) -> Set[str]:
        """Get all non-category descendant items recursively"""
        descendants = set()
        
        # Get direct children
        children = self.category_items.get(category_id, set())
        
        for child_id in children:
            # Find the child item
            child = next((item for item in self.items if item['id'] == child_id), None)
            if child:
                if child.get('is_category'):
                    # Recursively get descendants of subcategory
                    descendants.update(self.get_all_descendant_items(child_id))
                else:
                    # It's a regular item
                    descendants.add(child_id)
                    
        return descendants
            
    def get_selection_indicator(self, item_id: str, selections: Set[str]) -> str:
        """Get selection indicator for a category"""
        # Get all descendant items (recursive)
        all_items = self.get_all_descendant_items(item_id)
        
        if not all_items:
            return INDICATOR_NONE
            
        # Count selected items
        selected_count = 0
        for item in all_items:
            # Check if item is selected directly
            if item in self.selections:
                selected_count += 1
            else:
                # Check if selected through any parent category
                for parent_id, parent_selections in self.selections.items():
                    if isinstance(parent_selections, set) and item in parent_selections:
                        selected_count += 1
                        break
        
        total = len(all_items)
        if selected_count == 0:
            return INDICATOR_NONE
        elif selected_count == total:
            return INDICATOR_FULL
        else:
            return INDICATOR_PARTIAL
            
    def render(self) -> None:
        """Render the current menu state"""
        self.stdscr.clear()
        
        # Check terminal size
        self.height, self.width = self.stdscr.getmaxyx()
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            self.render_size_error()
            return
            
        # Draw header
        self.render_header()
        
        # Draw menu items
        self.render_menu_items()
        
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
        draw_box(self.stdscr, 0, 0, 4, self.width, TITLE)
        
        # Draw subtitle
        draw_centered_text(self.stdscr, 2, SUBTITLE)
        
        # Draw breadcrumb if not at root
        if len(self.breadcrumb) > 1:
            breadcrumb_text = " > ".join(self.breadcrumb)
            draw_centered_text(self.stdscr, 5, breadcrumb_text)
            
    def render_menu_items(self) -> None:
        """Render the menu items"""
        items = self.get_current_items()
        if not items:
            return
            
        # Calculate menu area
        start_y = 7
        menu_height = self.height - start_y - 3  # Leave room for help bar
        
        # Draw menu box
        draw_box(self.stdscr, start_y - 1, 2, menu_height + 2, self.width - 4)
        
        # Draw items
        visible_start = max(0, self.current_index - menu_height // 2)
        visible_end = min(len(items), visible_start + menu_height)
        
        for i, item in enumerate(items[visible_start:visible_end]):
            y = start_y + i
            self.render_menu_item(y, item, visible_start + i == self.current_index)
            
    def render_menu_item(self, y: int, item: Dict, selected: bool) -> None:
        """Render a single menu item"""
        x = 4
        max_width = self.width - 8
        
        # Build item text
        if item.get('is_category'):
            # Category with selection indicator
            indicator = self.get_selection_indicator(
                item['id'], 
                self.selections.get(item['id'], set())
            )
            icon = item.get('icon', '')
            text = f"{indicator} {icon} {item['label']}"
        else:
            # Check if it's a configurable item
            if item.get('is_configurable'):
                # Show current value
                current_value = self.configurable_values.get(
                    item['id'], 
                    item.get('default_value', '')
                )
                unit = item.get('unit', '')
                if unit:
                    value_text = f"[{current_value}{unit}]"
                else:
                    value_text = f"[{current_value}]"
                text = f"    {item['label']} {value_text}"
            else:
                # Regular item with checkbox
                is_selected = (
                    item['id'] in self.selections or
                    (item.get('parent') and 
                     item['id'] in self.selections.get(item['parent'], set()))
                )
                checkbox = CHECKBOX_SELECTED if is_selected else CHECKBOX_UNSELECTED
                text = f"  {checkbox} {item['label']}"
            
        # Add description on same line if space allows
        description = item.get('description', '')
        if description and len(text) + len(description) + 3 < max_width:
            text += f" - {description}"
            
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
        help_text = HELP_BAR_SUBMENU if self.current_menu != 'root' else HELP_BAR
        
        draw_box(self.stdscr, y - 1, 0, 3, self.width)
        draw_centered_text(self.stdscr, y, help_text)
        
    def navigate(self, key: int) -> Optional[str]:
        """Handle navigation keys and return action"""
        items = self.get_current_items()
        if not items:
            return None
            
        current_item = items[self.current_index] if items else None
        is_category = current_item.get('is_category', False) if current_item else False
        
        # Navigation
        if key_matches(key, KEY_BINDINGS['navigate_up']):
            self.current_index = (self.current_index - 1) % len(items)
            return 'navigate'
            
        elif key_matches(key, KEY_BINDINGS['navigate_down']):
            self.current_index = (self.current_index + 1) % len(items)
            return 'navigate'
            
        # Space and Enter behavior
        elif key_matches(key, KEY_BINDINGS['select']):
            if is_category:
                # For categories, enter submenu
                self.enter_submenu(current_item['id'])
                return 'enter'
            else:
                # For items, toggle selection
                self.toggle_selection()
                return 'select'
            
        # Right arrow - only enters submenu for categories
        elif key == curses.KEY_RIGHT or (key < 256 and chr(key) in ['l']):
            if is_category:
                self.enter_submenu(current_item['id'])
                return 'enter'
            return None
                
        # Go back
        elif key_matches(key, KEY_BINDINGS['back']):
            if self.current_menu != 'root':
                self.go_back()
                return 'back'
            else:
                # At root level, go back to main menu
                return 'main_menu'
                
        # Go to main menu (M key)
        elif key_matches(key, KEY_BINDINGS['main_menu']):
            return 'main_menu'
                
        # Quit
        elif key_matches(key, KEY_BINDINGS['quit']):
            return 'quit'
            
        # Help
        elif key_matches(key, KEY_BINDINGS['help']):
            return 'help'
            
        # Save
        elif key_matches(key, KEY_BINDINGS['save']):
            self.save_configuration()
            return 'save'
            
        # Apply
        elif key_matches(key, KEY_BINDINGS['apply']):
            return 'apply'
            
        # Select all (in submenu)
        elif key_matches(key, KEY_BINDINGS['select_all']) and self.current_menu != 'root':
            self.select_all()
            return 'select_all'
            
        # Deselect all (in submenu)
        elif key_matches(key, KEY_BINDINGS['deselect_all']) and self.current_menu != 'root':
            self.deselect_all()
            return 'deselect_all'
            
        return None
        
    def toggle_selection(self) -> None:
        """Toggle selection of current item"""
        items = self.get_current_items()
        if not items or self.current_index >= len(items):
            return
            
        item = items[self.current_index]
        item_id = item['id']
        
        if item.get('is_category'):
            # Can't directly select categories
            return
            
        # Handle configurable items
        if item.get('is_configurable'):
            self.show_config_dialog(item)
            return
            
        # Handle selection based on parent
        parent = item.get('parent')
        if parent and parent in self.category_items:
            # Item is part of a category
            if parent not in self.selections:
                self.selections[parent] = set()
                
            if item_id in self.selections[parent]:
                self.selections[parent].remove(item_id)
            else:
                self.selections[parent].add(item_id)
        else:
            # Top-level item
            if item_id in self.selections:
                del self.selections[item_id]
            else:
                self.selections[item_id] = True
                
    def show_config_dialog(self, item: Dict) -> None:
        """Show configuration dialog for configurable item"""
        item_id = item['id']
        config_type = item.get('config_type', 'text')
        current_value = self.configurable_values.get(item_id, item.get('default_value'))
        
        new_value = None
        
        if config_type == 'slider':
            dialog = SliderDialog(self.stdscr)
            # Convert to int if necessary
            if isinstance(current_value, float) and item.get('step', 1) >= 1:
                current_val = int(current_value)
            else:
                current_val = current_value
            new_value = dialog.show(
                item['label'],
                current_val,
                item.get('min_value', 0),
                item.get('max_value', 100),
                item.get('step', 1),
                item.get('unit', '')
            )
        elif config_type == 'spinner':
            dialog = SpinnerDialog(self.stdscr)
            values = item.get('values', [])
            if values:
                new_value = dialog.show(
                    item['label'],
                    current_value,
                    values,
                    item.get('unit', '')
                )
        elif config_type == 'select':
            dialog = SelectDialog(self.stdscr)
            options = item.get('options', [])
            if options:
                new_value = dialog.show(
                    item['label'],
                    options,
                    str(current_value)
                )
        else:
            # Default to text input
            from .dialogs import InputDialog
            dialog = InputDialog(self.stdscr)
            new_value = dialog.show(
                item['label'],
                item.get('description', 'Enter value:'),
                str(current_value)
            )
        
        # Update value if changed
        if new_value is not None:
            self.configurable_values[item_id] = new_value
                
    def select_all(self) -> None:
        """Select all items in current category"""
        if self.current_menu not in self.category_items:
            return
            
        self.selections[self.current_menu] = set(self.category_items[self.current_menu])
        
    def deselect_all(self) -> None:
        """Deselect all items in current category"""
        if self.current_menu in self.selections:
            self.selections[self.current_menu] = set()
            
    def enter_submenu(self, menu_id: str) -> None:
        """Enter a submenu"""
        self.menu_stack.append(self.current_menu)
        self.current_menu = menu_id
        self.current_index = 0
        
        # Update breadcrumb
        for item in self.items:
            if item['id'] == menu_id:
                self.breadcrumb.append(item['label'])
                break
                
    def go_back(self) -> None:
        """Go back to previous menu"""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            self.current_index = 0
            self.breadcrumb.pop()
            
    def get_current_help(self) -> Optional[str]:
        """Get help text for current item"""
        items = self.get_current_items()
        if not items or self.current_index >= len(items):
            return None
            
        item = items[self.current_index]
        return item.get('help', f"No help available for {item['label']}")
        
    def apply_configuration(self) -> bool:
        """Apply the configuration using Ansible with sudo dialog"""
        # Create sudo dialog
        sudo_dialog = SudoDialog(self.stdscr)
        progress_dialog = ProgressDialog(self.stdscr)
        
        # Show confirmation
        confirm = ConfirmDialog(self.stdscr)
        if not confirm.show(
            "Install Selected Software?",
            "This will install and configure all selected items using Ansible.\n\n"
            "• Requires administrator (sudo) access\n"
            "• May take several minutes depending on selections\n"
            "• Internet connection required for downloads\n\n"
            "Continue with installation?"
        ):
            return False
            
        # Check if config.yml exists
        if not Path("config.yml").exists():
            MessageDialog(self.stdscr).show(
                "No Configuration",
                "No configuration file found. Please save your selections first.",
                "error"
            )
            return False
            
        # Run ansible-playbook with progress dialog
        result = progress_dialog.run_command(
            ['ansible-playbook', 'site.yml', '-i', 'inventories/local/hosts'],
            "Applying Configuration",
            show_output=True,
            sudo_dialog=sudo_dialog
        )
        
        if result == 0:
            MessageDialog(self.stdscr).show(
                "Configuration Applied",
                "Your system has been successfully configured!",
                "success"
            )
            return True
        else:
            MessageDialog(self.stdscr).show(
                "Configuration Failed",
                "There was an error applying the configuration.\n"
                "Please check the output for details.",
                "error"
            )
            return False
        
    def run(self) -> int:
        """Main menu loop - returns 0 for success, 1 for cancelled"""
        self.load_menu_structure()
        self.load_defaults()  # Load defaults first
        self.load_configuration()  # Then override with saved config if it exists
        
        exit_code = 1  # Default to cancelled
        
        while True:
            self.render()
            
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                # Ctrl+C pressed - exit with cancel
                exit_code = 1
                break
                
            action = self.navigate(key)
            
            if action == 'quit':
                # User wants to quit
                if self.selections:
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Save changes?", "You have unsaved selections. Save before exit?"):
                        self.save_configuration()
                        exit_code = 0  # Saved successfully
                    else:
                        exit_code = 1  # Cancelled without saving
                else:
                    exit_code = 1  # No selections, just cancelled
                break
                
            elif action == 'help':
                help_text = self.get_current_help()
                if help_text:
                    dialog = HelpDialog(self.stdscr)
                    dialog.show(help_text)
                    
            elif action == 'save':
                self.save_configuration()
                dialog = MessageDialog(self.stdscr)
                dialog.show("Configuration Saved", "Your selections have been saved to config.yml")
                exit_code = 0  # Saved successfully
                
            elif action == 'apply':
                # Save first if needed
                if self.selections and not Path("config.yml").exists():
                    self.save_configuration()
                    
                # Apply configuration
                if self.apply_configuration():
                    exit_code = 0  # Applied successfully
                    
            elif action == 'main_menu':
                # User wants to go back to main menu
                if self.selections:
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Save changes?", "Save your selections before returning to main menu?"):
                        self.save_configuration()
                        exit_code = 0  # Saved successfully
                    else:
                        exit_code = 2  # Return to main menu without saving
                else:
                    exit_code = 2  # Return to main menu (no selections to save)
                break
                
            # Handle terminal resize
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()
                
        return exit_code