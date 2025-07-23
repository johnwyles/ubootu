#!/usr/bin/env python3
"""
Configuration management for the Ubootu TUI interface
"""

from typing import Dict, List, Set, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MenuItem


class TUIConfigManager:
    """Handles configuration state and menu navigation for the TUI"""
    
    def __init__(self, menu_items: Dict[str, 'MenuItem'], selected_items: Set[str]):
        self.menu_items = menu_items
        self.selected_items = selected_items
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.breadcrumb_stack = []
    
    def get_current_menu_items(self) -> List['MenuItem']:
        """Get items for current menu level"""
        current = self.menu_items[self.current_menu]
        if current.children:
            return [self.menu_items[child_id] for child_id in current.children]
        return []
    
    def navigate_to_menu(self, menu_id: str, save_breadcrumb: bool = True):
        """Navigate to a specific menu"""
        if save_breadcrumb:
            self.breadcrumb_stack.append((self.current_menu, self.current_item, self.scroll_offset))
        self.current_menu = menu_id
        self.current_item = 0
        self.scroll_offset = 0
    
    def navigate_back(self) -> bool:
        """Navigate back to previous menu"""
        if self.breadcrumb_stack:
            self.current_menu, self.current_item, self.scroll_offset = self.breadcrumb_stack.pop()
            return True
        return False
    
    def reset_to_root(self):
        """Reset navigation to root menu"""
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.breadcrumb_stack = []
    
    def get_breadcrumb(self) -> str:
        """Get breadcrumb navigation string"""
        path = []
        current = self.current_menu
        
        while current and current != "root":
            if current in self.menu_items:
                item = self.menu_items[current]
                path.append(item.label)
                current = item.parent
            else:
                break
        
        path.reverse()
        return " > ".join(path)
    
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
                # Recursively get items from subcategories
                items.extend(self.get_all_selectable_items(child_id))
            else:
                # This is a selectable item
                items.append(child_id)
        
        return items
    
    def select_all_in_category(self, category_id: str, select: bool):
        """Select or deselect all items in a specific category"""
        category_items = self.get_all_selectable_items(category_id)
        
        for item_id in category_items:
            if item_id in self.menu_items:
                item = self.menu_items[item_id]
                item.selected = select
                if select:
                    self.selected_items.add(item_id)
                else:
                    self.selected_items.discard(item_id)
    
    def select_all_in_current_menu(self, select: bool):
        """Select or deselect all items in the current menu"""
        menu_items = self.get_current_menu_items()
        
        for item in menu_items:
            if not item.is_category:
                item.selected = select
                if select:
                    self.selected_items.add(item.id)
                else:
                    self.selected_items.discard(item.id)
    
    def toggle_item_selection(self, item: 'MenuItem'):
        """Toggle selection of a single item"""
        item.selected = not item.selected
        if item.selected:
            self.selected_items.add(item.id)
        else:
            self.selected_items.discard(item.id)
    
    def apply_defaults(self):
        """Apply default selections to items marked as default"""
        for item in self.menu_items.values():
            if item.default:
                item.selected = True
                self.selected_items.add(item.id)
    
    def reset_all_selections(self):
        """Reset all selections to defaults"""
        self.selected_items.clear()
        for item in self.menu_items.values():
            item.selected = item.default
            if item.default:
                self.selected_items.add(item.id)
    
    def get_selection_counts(self) -> tuple[int, int]:
        """Get total selected items and total selectable items"""
        total_selectable = sum(1 for item in self.menu_items.values() 
                              if not item.is_category and item.parent != "actions")
        selected_count = len(self.selected_items)
        return selected_count, total_selectable
    
    def get_category_selection_counts(self, category_id: str) -> tuple[int, int]:
        """Get selection counts for a specific category"""
        category_items = self.get_all_selectable_items(category_id)
        selected_count = sum(1 for item_id in category_items if item_id in self.selected_items)
        return selected_count, len(category_items)
    
    def has_selections(self) -> bool:
        """Check if any items are selected"""
        return len(self.selected_items) > 0
    
    def validate_menu_structure(self) -> List[str]:
        """Validate the menu structure and return any issues found"""
        issues = []
        
        # Check for orphaned items
        for item_id, item in self.menu_items.items():
            if item.parent and item.parent not in self.menu_items:
                issues.append(f"Item {item_id} has invalid parent: {item.parent}")
        
        # Check for circular references
        visited = set()
        for item_id in self.menu_items:
            if self._has_circular_reference(item_id, visited, set()):
                issues.append(f"Circular reference detected involving item: {item_id}")
        
        return issues
    
    def _has_circular_reference(self, item_id: str, visited: set, path: set) -> bool:
        """Check for circular references in menu structure"""
        if item_id in path:
            return True
        if item_id in visited:
            return False
        
        visited.add(item_id)
        path.add(item_id)
        
        item = self.menu_items.get(item_id)
        if item and item.children:
            for child_id in item.children:
                if self._has_circular_reference(child_id, visited, path):
                    return True
        
        path.remove(item_id)
        return False