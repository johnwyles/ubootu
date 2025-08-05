#!/usr/bin/env python3
"""
Unified menu system for Ubootu
Single consistent curses-based menu implementation
"""

import curses
import yaml
import time
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
        
        # Track application state
        self.config_applied = False  # Track if current config was applied
        self.applied_config_hash = None  # Hash of last applied config
        self.saved_config_hash = None  # Hash of last saved config
        self.changes_since_apply = False  # Track if any changes made since last apply
        
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
                
            # Validate config structure
            if not self.validate_config(config):
                self.show_corruption_message()
                return
                
            # Clear all selections (including defaults) before loading saved config
            self.selections = {}
            self.configurable_values = {}
            
            # Load selected items
            selected = config.get('selected_items', [])
            if isinstance(selected, list):
                # First pass: identify all categories and their descendants
                category_descendants = {}
                for item_id in selected:
                    if item_id in self.category_items:
                        # Get all descendants for this category
                        descendants = self.get_all_descendant_items(item_id)
                        category_descendants[item_id] = descendants
                
                # Second pass: build selection structure
                for item_id in selected:
                    # Check if it's a category
                    if item_id in self.category_items:
                        # Find all its descendants that are in the selected list
                        self.selections[item_id] = set()
                        descendants = category_descendants.get(item_id, set())
                        for desc in descendants:
                            if desc in selected:
                                self.selections[item_id].add(desc)
                    else:
                        # For non-category items, only add as direct selection if not part of any category
                        is_in_category = False
                        for cat_id, desc_set in category_descendants.items():
                            if item_id in desc_set and cat_id in selected:
                                is_in_category = True
                                break
                        
                        if not is_in_category:
                            self.selections[item_id] = True
                    
            # Load configurable values
            configurable = config.get('configurable_items', {})
            if isinstance(configurable, dict):
                for item_id, item_config in configurable.items():
                    if isinstance(item_config, dict) and 'value' in item_config:
                        self.configurable_values[item_id] = item_config.get('value')
            
            # Update saved config hash
            self.saved_config_hash = self._get_saved_config_hash()
                        
        except yaml.YAMLError as e:
            self.show_corruption_message(f"Invalid YAML format: {str(e)}")
        except Exception as e:
            self.show_corruption_message(f"Error loading config: {str(e)}")
            
    def save_configuration(self, silent: bool = False) -> bool:
        """Save current configuration to file
        
        Args:
            silent: If True, don't show error messages
            
        Returns:
            True if save was successful, False otherwise
        """
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
            
        try:
            # Write to file
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Update saved config hash
            self.saved_config_hash = self._get_config_hash()
            
            return True
        except Exception as e:
            if not silent:
                from .dialogs import MessageDialog
                dialog = MessageDialog(self.stdscr)
                dialog.show("Save Error", f"Could not save configuration:\n{str(e)}", "error")
            return False
            
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
    
    def is_item_selected(self, item_id: str) -> bool:
        """Check if an item is selected through any parent in the hierarchy"""
        # Direct selection (top-level items)
        if item_id in self.selections and self.selections[item_id] is True:
            return True
        
        # Check if item is in any category's selection set
        for cat_id, selections in self.selections.items():
            if isinstance(selections, set) and item_id in selections:
                return True
        
        return False
            
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
                is_selected = self.is_item_selected(item['id'])
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
        
        # Handle navigation keys that should work even in empty menus
        # Go back
        if key_matches(key, KEY_BINDINGS['back']):
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
        
        # If no items, we can't do item-specific navigation
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
            
        # Space toggles selection on any item (including categories)
        elif key_matches(key, KEY_BINDINGS['select']):
            self.toggle_selection()
            return 'select'
            
        # Enter key - enters submenu for categories
        elif key_matches(key, KEY_BINDINGS['enter']):
            if is_category:
                self.enter_submenu(current_item['id'])
                return 'enter'
            else:
                # For non-categories, Enter also toggles selection
                self.toggle_selection()
                return 'select'
            
        # Select all
        elif key_matches(key, KEY_BINDINGS['select_all']):
            self.select_all()
            return 'select_all'
            
        # Deselect all
        elif key_matches(key, KEY_BINDINGS['deselect_all']):
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
            # Toggle all items in this category
            descendants = self.get_all_descendant_items(item_id)
            if descendants:
                # Check if ANY descendants are currently selected anywhere
                any_selected = any(
                    self.is_item_selected(desc_id) for desc_id in descendants
                )
                
                if any_selected:
                    # Deselect all descendants from wherever they are stored
                    for cat_id, selections in list(self.selections.items()):
                        if isinstance(selections, set):
                            # Remove descendants from this category's selections
                            selections.difference_update(descendants)
                            # If category is now empty, remove it
                            if not selections:
                                del self.selections[cat_id]
                    
                    # Also remove this category itself if it's a key
                    if item_id in self.selections:
                        del self.selections[item_id]
                else:
                    # Select all descendants under this category
                    self.selections[item_id] = descendants.copy()
                
                # Mark that changes have been made
                self.changes_since_apply = True
                # Auto-save after selection change
                self.save_configuration(silent=True)
            return
            
        # Handle configurable items
        if item.get('is_configurable'):
            self.show_config_dialog(item)
            return
            
        # Handle regular item selection/deselection
        is_currently_selected = self.is_item_selected(item_id)
        
        if is_currently_selected:
            # Remove from ALL categories that contain it
            for cat_id, selections in list(self.selections.items()):
                if isinstance(selections, set) and item_id in selections:
                    selections.remove(item_id)
                    # If category is now empty, remove it
                    if not selections:
                        del self.selections[cat_id]
        else:
            # Add to immediate parent
            parent = item.get('parent')
            if parent and parent in self.category_items:
                # Item is part of a category
                if parent not in self.selections:
                    self.selections[parent] = set()
                self.selections[parent].add(item_id)
            else:
                # Top-level item
                self.selections[item_id] = True
                
        # Mark that changes have been made
        self.changes_since_apply = True
        # Auto-save after selection change
        self.save_configuration(silent=True)
                
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
            # Mark that changes have been made
            self.changes_since_apply = True
            # Auto-save after configuration change
            self.save_configuration(silent=True)
                
    def select_all(self) -> None:
        """Select all items in current category and all subcategories"""
        if self.current_menu == 'root':
            # At root level, select all non-category items recursively
            for item in self.items:
                if item.get('is_category') and item.get('parent') is None:
                    # Get all descendant items for each root category
                    descendants = self.get_all_descendant_items(item['id'])
                    if descendants:
                        self.selections[item['id']] = descendants
                elif not item.get('is_category') and item.get('parent') is None:
                    # Direct root-level items
                    self.selections[item['id']] = True
        else:
            # In a category, select all descendant items
            descendants = self.get_all_descendant_items(self.current_menu)
            if descendants:
                # First, remove these items from any other categories
                # This ensures they're only stored in one place
                for cat_id, selections in list(self.selections.items()):
                    if isinstance(selections, set) and cat_id != self.current_menu:
                        selections.difference_update(descendants)
                        if not selections:
                            del self.selections[cat_id]
                
                # Now add them to the current category
                self.selections[self.current_menu] = descendants
        
        # Mark that changes have been made
        self.changes_since_apply = True
        # Auto-save after bulk selection
        self.save_configuration(silent=True)
        
    def deselect_all(self) -> None:
        """Deselect all items in current category and all subcategories"""
        if self.current_menu == 'root':
            # At root level, clear all selections
            self.selections.clear()
        else:
            # Get all items that should be deselected (all descendants of current menu)
            items_to_deselect = self.get_all_descendant_items(self.current_menu)
            
            if items_to_deselect:
                # Remove these items from ALL categories that contain them
                for cat_id, selections in list(self.selections.items()):
                    if isinstance(selections, set):
                        # Remove any items that are descendants of current menu
                        selections.difference_update(items_to_deselect)
                        # If category is now empty, remove it
                        if not selections:
                            del self.selections[cat_id]
            
            # Also remove the current category itself if it exists as a key
            if self.current_menu in self.selections:
                del self.selections[self.current_menu]
            
            # Clear any direct subcategory selections
            for item in self.items:
                if item.get('is_category') and item.get('parent') == self.current_menu:
                    if item['id'] in self.selections:
                        del self.selections[item['id']]
        
        # Mark that changes have been made
        self.changes_since_apply = True
        # Auto-save after bulk deselection
        self.save_configuration(silent=True)
    
    def _clear_category_selections(self, category_id: str) -> None:
        """Recursively clear selections for a category and its subcategories"""
        # Clear this category's selections
        if category_id in self.selections:
            del self.selections[category_id]
        
        # Clear subcategory selections
        for item in self.items:
            if item.get('is_category') and item.get('parent') == category_id:
                self._clear_category_selections(item['id'])
            
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
        # DEBUG: Start of apply_configuration
        import sys
        sys.stderr.write(f"\n[DEBUG] apply_configuration called at {time.strftime('%H:%M:%S')}\n")
        sys.stderr.flush()
        
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
            "The installer will show:\n"
            "• Current task being performed\n"
            "• Number of completed tasks\n"
            "• Detailed output for troubleshooting\n\n"
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
            
        # Show detailed information about what will happen
        info_dialog = MessageDialog(self.stdscr)
        info_dialog.show(
            "System Configuration Required",
            "This will install and configure selected software on your system.\n\n"
            "What happens next:\n"
            "• You'll be asked for your sudo password\n"
            "• Ansible will install selected packages\n"
            "• System configuration will be applied\n"
            "• Process takes 5-20 minutes depending on selections\n\n"
            "Your sudo password is needed for:\n"
            "• Installing packages (apt install)\n"
            "• Creating system directories\n"
            "• Configuring system services\n"
            "• Writing system configuration files",
            "info"
        )
            
        # Get sudo password using our secure dialog
        sudo_password = sudo_dialog.get_password(
            "Enter your sudo password to install selected software:"
        )
        
        if not sudo_password:
            MessageDialog(self.stdscr).show(
                "Installation Cancelled",
                "Sudo password is required to install software and configure your system.\n\n"
                "No changes have been made to your system.",
                "info"
            )
            return False
        
        # Create a temporary file for sudo password with proper permissions
        import tempfile
        import os
        import stat
        
        # Create password file with secure permissions
        fd, password_file = tempfile.mkstemp(text=True)
        try:
            # Write password and ensure proper permissions
            with os.fdopen(fd, 'w') as f:
                f.write(sudo_password)
                f.write('\n')  # Ensure newline at end
            # Set permissions to 0600 (read/write for owner only)
            os.chmod(password_file, stat.S_IRUSR | stat.S_IWUSR)
        except:
            os.close(fd)
            raise
        
        # Create a temporary inventory to avoid vault template issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as inv_file:
            inv_file.write("""[local]
localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3
""")
            temp_inventory = inv_file.name

        try:
            # Set up environment for Ansible
            env = {
                'ANSIBLE_BECOME_PASS': sudo_password,      # Primary method
                'ANSIBLE_BECOME_PASSWORD': sudo_password,  # Alternate name
                'ANSIBLE_ASK_PASS': 'False',              # Don't prompt
                'ANSIBLE_ASK_BECOME_PASS': 'False',       # Don't prompt for sudo
            }
            
            # Run ansible-playbook with progress dialog
            # Simplified command with fewer parameters
            sys.stderr.write(f"[DEBUG] About to call progress_dialog.run_command\n")
            sys.stderr.write(f"[DEBUG] Password file: {password_file}\n")
            sys.stderr.write(f"[DEBUG] Inventory: {temp_inventory}\n")
            sys.stderr.flush()
            
            # Build complete ansible command with all variables
            ansible_cmd = self._build_ansible_command(temp_inventory, password_file)
            
            result = progress_dialog.run_command(
                ansible_cmd,
                "Applying Configuration - Installing Selected Software",
                show_output=True,
                sudo_dialog=sudo_dialog,
                env=env
            )
            
            sys.stderr.write(f"[DEBUG] progress_dialog.run_command returned: {result}\n")
            sys.stderr.flush()
        finally:
            # Always remove temporary files
            try:
                os.unlink(password_file)
            except:
                pass
            try:
                os.unlink(temp_inventory)
            except:
                pass
        
        sys.stderr.write(f"[DEBUG] Checking result: {result}\n")
        sys.stderr.flush()
        
        if result == 0:
            # Update applied config tracking
            self.applied_config_hash = self._get_config_hash()
            self.config_applied = True
            self.changes_since_apply = False  # Reset change tracking after successful apply
            
            # Build detailed summary
            summary = self._build_execution_summary(progress_dialog)
            
            MessageDialog(self.stdscr).show(
                "Configuration Applied",
                summary,
                "success"
            )
            return True
        else:
            # Check if debug log exists
            debug_info = ""
            emergency_log = "/tmp/ubootu_emergency.log"
            
            sys.stderr.write(f"[DEBUG] Configuration failed with result: {result}\n")
            
            # List all debug logs
            import glob
            debug_logs = glob.glob('/tmp/ubootu_debug_*.log')
            if debug_logs:
                debug_info = "\n\nDebug logs found:\n"
                for log in debug_logs[-3:]:  # Show last 3
                    debug_info += f"  {log}\n"
            
            if os.path.exists(emergency_log):
                debug_info += f"\nEmergency log: {emergency_log}"
                # Read last few lines
                try:
                    with open(emergency_log, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            debug_info += "\n\nLast lines from emergency log:"
                            for line in lines[-5:]:
                                debug_info += f"\n  {line.strip()}"
                except:
                    pass
            
            if os.path.exists('/tmp/ubootu_ansible.log'):
                debug_info += "\nAnsible log saved to: /tmp/ubootu_ansible.log"
                
            sys.stderr.write(f"[DEBUG] Showing error dialog\n")
            sys.stderr.flush()
                
            # Build failure summary
            failure_summary = self._build_failure_summary(progress_dialog, result)
            
            MessageDialog(self.stdscr).show(
                "Configuration Failed",
                failure_summary + debug_info,
                "error"
            )
            return False
        
    def run(self) -> int:
        """Main menu loop - returns 0 for success, 1 for cancelled"""
        self.load_menu_structure()
        
        # Load configuration if it exists, otherwise load defaults
        if Path(self.config_file).exists():
            # First load defaults to get default configurable values
            self.load_defaults()
            # Then load saved configuration which will override
            self.load_configuration()
        else:
            # No config file, just load defaults
            self.load_defaults()
        
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
                # User wants to quit - check state
                current_hash = self._get_config_hash()
                saved_hash = self._get_saved_config_hash()
                
                # First check if there are actual changes since last apply
                if not self.changes_since_apply:
                    # No changes since apply, just confirm quit
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Quit?", "Exit Ubootu?"):
                        exit_code = 0
                        break
                elif current_hash != saved_hash:
                    # Unsaved changes
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Save changes?", "You have unsaved changes. Save before exit?"):
                        self.save_configuration()
                        exit_code = 0
                    else:
                        exit_code = 1
                    break
                elif self.changes_since_apply:
                    # Saved but unapplied changes
                    dialog = SelectDialog(self.stdscr)
                    response = dialog.show(
                        "Unapplied Changes", 
                        "Configuration saved but not applied. What would you like to do?",
                        ["Apply Now", "Quit Without Applying", "Cancel"]
                    )
                    if response == 0:  # Apply Now
                        if self.apply_configuration():
                            exit_code = 0
                            break
                    elif response == 1:  # Quit without applying
                        exit_code = 0
                        break
                    # else Cancel - continue loop
                else:
                    # No changes at all, just quit
                    dialog = ConfirmDialog(self.stdscr)
                    if dialog.show("Quit?", "Exit Ubootu?"):
                        exit_code = 0
                        break
                
            elif action == 'help':
                help_text = self.get_current_help()
                if help_text:
                    dialog = HelpDialog(self.stdscr)
                    dialog.show(help_text)
                    
            elif action == 'save':
                if self.save_configuration():
                    dialog = MessageDialog(self.stdscr)
                    dialog.show(
                        "Configuration Saved",
                        "Your selections have been saved to config.yml\n\n" +
                        "• Configuration is automatically saved after each change\n" +
                        "• You can version control this file with Git\n" +
                        "• Run './setup.sh --restore config.yml' to restore later\n" +
                        "• Press 'P' to apply configuration and install software",
                        "success"
                    )
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
        
    def validate_config(self, config: Dict) -> bool:
        """Validate configuration structure"""
        if not isinstance(config, dict):
            return False
            
        # Check for required or expected keys
        if 'selected_items' in config and not isinstance(config['selected_items'], list):
            return False
            
        if 'configurable_items' in config and not isinstance(config['configurable_items'], dict):
            return False
            
        return True
        
    def show_corruption_message(self, details: str = "") -> None:
        """Show message about corrupted config"""
        from .dialogs import ConfirmDialog, MessageDialog
        
        dialog = ConfirmDialog(self.stdscr)
        message = "Configuration file appears to be corrupted.\n\n"
        if details:
            message += f"Error: {details}\n\n"
        message += "Would you like to reset to defaults?"
        
        if dialog.show("Configuration Error", message):
            # Reset to defaults
            self.selections = {}
            self.configurable_values = {}
            self.load_defaults()
            # Save clean config
            self.save_configuration()
            
            msg_dialog = MessageDialog(self.stdscr)
            msg_dialog.show("Reset Complete", "Configuration has been reset to defaults.")
    
    def _get_config_data(self) -> Dict[str, Any]:
        """Get current configuration as a dictionary"""
        # Build selected items list
        selected_items = []
        for item_id, value in self.selections.items():
            if isinstance(value, bool) and value:
                selected_items.append(item_id)
            elif isinstance(value, set):
                selected_items.append(item_id)
                selected_items.extend(list(value))
        
        # Build configurable items
        configurable_items = {}
        for item_id, value in self.configurable_values.items():
            configurable_items[item_id] = {
                'id': item_id,
                'value': value
            }
        
        return {
            'selected_items': sorted(selected_items),
            'configurable_items': configurable_items
        }
    
    def _get_config_hash(self) -> str:
        """Generate hash of current configuration"""
        import hashlib
        import json
        
        config_data = self._get_config_data()
        # Sort keys for consistent hashing
        config_str = json.dumps(config_data, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()
    
    def _get_saved_config_hash(self) -> Optional[str]:
        """Get hash of saved configuration from file"""
        if not Path(self.config_file).exists():
            return None
            
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            # Extract relevant parts
            config_data = {
                'selected_items': sorted(config.get('selected_items', [])),
                'configurable_items': config.get('configurable_items', {})
            }
            
            import hashlib
            import json
            config_str = json.dumps(config_data, sort_keys=True)
            return hashlib.sha256(config_str.encode()).hexdigest()
        except:
            return None
    
    def _prepare_ansible_variables(self) -> Dict[str, Any]:
        """Prepare all variables to pass to Ansible"""
        extra_vars = {}
        
        # Add selected items as a simple list
        selected_items = []
        for item_id, value in self.selections.items():
            if isinstance(value, bool) and value:
                selected_items.append(item_id)
            elif isinstance(value, set):
                selected_items.extend(list(value))
        
        extra_vars['selected_items'] = selected_items
        
        # Add configurable items with proper ansible variable names
        for item_id, value in self.configurable_values.items():
            ansible_var_name = self._get_ansible_var_name(item_id)
            extra_vars[ansible_var_name] = value
        
        # Add desktop environment display manager mapping
        extra_vars['de_display_manager'] = {
            'gnome': 'gdm3',
            'kde': 'sddm',
            'xfce': 'lightdm',
            'mate': 'lightdm',
            'cinnamon': 'lightdm',
            'hyprland': 'greetd'
        }
        
        # Add Ubuntu version handling for repository compatibility
        extra_vars['ubuntu_version'] = '25.04'
        extra_vars['ubuntu_codename'] = 'plucky'
        extra_vars['fallback_codename'] = 'noble'  # Fallback to 24.04 LTS
        
        # Add default ansible variables
        import os
        extra_vars.update({
            'primary_user': os.environ.get('USER', 'ubuntu'),
            'desktop_environment': 'gnome',  # Default
            'de_environment': 'gnome',       # For display manager tasks
            'de_autologin': False,
            'enable_firewall': True,
            'enable_fail2ban': True
        })
        
        # Load config.yml if it exists and merge ansible_variables
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    if config and 'ansible_variables' in config:
                        extra_vars.update(config['ansible_variables'])
            except:
                pass  # Continue with defaults if config can't be loaded
        
        return extra_vars
    
    def _get_ansible_var_name(self, config_name: str) -> str:
        """Convert config item name to ansible variable name"""
        # Mapping of config names to ansible variable names
        mappings = {
            'swappiness': 'system_swappiness',
            'terminal-font-size': 'terminal_font_size',
            'terminal-font-family': 'terminal_font_family',
            'terminal-transparency': 'terminal_transparency',
            'terminal-padding': 'terminal_padding',
            'terminal-scrollback': 'terminal_scrollback',
            'terminal-cursor-style': 'terminal_cursor_style',
            'terminal-bell': 'terminal_bell',
            'terminal-blur': 'terminal_blur',
            'custom-accent': 'theme_custom_accent',
            'custom-background': 'theme_custom_background',
            'custom-foreground': 'theme_custom_foreground',
            'theme-terminal-opacity': 'theme_terminal_opacity',
            'theme-ui-scale': 'theme_ui_scale',
            'editor-font-family': 'editor_font_family',
            'editor-line-height': 'editor_line_height',
            'vscode-font-size': 'vscode_font_size'
        }
        
        return mappings.get(config_name, config_name.replace('-', '_'))
    
    def _create_extra_vars_file(self, temp_dir: Path = None) -> Path:
        """Create temporary extra vars file for ansible"""
        import tempfile
        
        if temp_dir is None:
            temp_dir = Path(tempfile.gettempdir())
        
        extra_vars = self._prepare_ansible_variables()
        
        vars_file = temp_dir / f"ubootu_extra_vars_{int(time.time())}.yml"
        with open(vars_file, 'w') as f:
            yaml.dump(extra_vars, f, default_flow_style=False)
        
        return vars_file
    
    def _build_ansible_command(self, temp_inventory: str = None, password_file: str = None) -> List[str]:
        """Build the complete ansible-playbook command with all options"""
        # Create extra vars file
        vars_file = self._create_extra_vars_file()
        
        cmd = [
            'ansible-playbook',
            'site.yml',
            '-i', temp_inventory or 'localhost,',
            '--diff',
            '-v',  # Moderate verbosity - actionable callback controls output format
            '--extra-vars', f'@{vars_file}',
            '--connection', 'local',
            '--forks', '1',
            '--become-method', 'sudo'
        ]
        
        if password_file:
            cmd.extend(['--become-password-file', password_file])
        
        return cmd
    
    def _build_execution_summary(self, progress_dialog) -> str:
        """Build a detailed summary of what happened during execution"""
        lines = ["Your system has been successfully configured!", ""]
        
        # Overall stats
        completed = getattr(progress_dialog, 'completed_tasks', 0)
        skipped = getattr(progress_dialog, 'skipped_tasks', 0)
        failed = getattr(progress_dialog, 'failed_tasks', 0)
        total = completed + skipped + failed
        lines.append(f"Total tasks processed: {total}")
        lines.append(f"✓ Completed: {completed}")
        lines.append(f"⚪ Skipped: {skipped}")
        if failed > 0:
            lines.append(f"✗ Failed: {failed}")
        lines.append("")
        
        # Success details (limit to show most important)
        success_details = getattr(progress_dialog, 'success_details', {})
        if success_details:
            lines.append("Successfully installed/configured:")
            for category, actions in list(success_details.items())[:5]:
                if actions:
                    lines.append(f"  {category}: {len(actions)} items")
        
        # Skip reasons summary
        skip_reasons = getattr(progress_dialog, 'skip_reasons', {})
        if skip_reasons:
            lines.append("")
            lines.append("Items skipped because:")
            for reason, count in skip_reasons.items():
                lines.append(f"  • {reason}: {count}")
        
        # Failure summary (if any)
        failure_details = getattr(progress_dialog, 'failure_details', {})
        if failure_details:
            lines.append("")
            lines.append("⚠️ Failed items:")
            for category, actions in failure_details.items():
                if actions:
                    lines.append(f"  {category}: {', '.join(actions[:3])}")
                    if len(actions) > 3:
                        lines.append(f"    ... and {len(actions) - 3} more")
        
        return "\n".join(lines)
    
    def _build_failure_summary(self, progress_dialog, exit_code: int) -> str:
        """Build a detailed summary of what failed during execution"""
        lines = [f"Configuration process failed with exit code {exit_code}", ""]
        
        # Overall stats
        completed = getattr(progress_dialog, 'completed_tasks', 0)
        skipped = getattr(progress_dialog, 'skipped_tasks', 0)
        failed = getattr(progress_dialog, 'failed_tasks', 0)
        total = completed + skipped + failed
        lines.append(f"Tasks processed before failure: {total}")
        if completed > 0:
            lines.append(f"✓ Succeeded: {completed}")
        if skipped > 0:
            lines.append(f"⚪ Skipped: {skipped}")
        if failed > 0:
            lines.append(f"✗ Failed: {failed}")
        lines.append("")
        
        # What succeeded before failure
        success_details = getattr(progress_dialog, 'success_details', {})
        if success_details:
            lines.append("Completed before failure:")
            count = 0
            for category, actions in success_details.items():
                if actions and count < 3:
                    lines.append(f"  • {category}: {len(actions)} items")
                    count += 1
            lines.append("")
        
        # What failed
        failure_details = getattr(progress_dialog, 'failure_details', {})
        if failure_details:
            lines.append("Failed tasks:")
            for category, actions in failure_details.items():
                if actions:
                    for action in actions[:3]:  # Show first 3
                        lines.append(f"  ✗ {action}")
                    if len(actions) > 3:
                        lines.append(f"    ... and {len(actions) - 3} more in {category}")
            lines.append("")
        
        lines.append("Common causes:")
        lines.append("• Network connectivity issues")
        lines.append("• Repository unavailability")
        lines.append("• Package conflicts")
        lines.append("• Missing dependencies")
        
        return "\n".join(lines)