#!/usr/bin/env python3
"""
Base class for menu builders in the Ubootu TUI
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tui.models import MenuItem


class MenuBuilder(ABC):
    """Abstract base class for building menu sections"""
    
    def __init__(self):
        self.items: Dict[str, MenuItem] = {}
        
    @abstractmethod
    def build(self) -> Dict[str, MenuItem]:
        """Build and return menu items for this section"""
        pass
        
    def add_item(self, item: MenuItem) -> None:
        """Add a menu item to the collection"""
        self.items[item.id] = item
        
    def add_category(self, id: str, label: str, description: str, 
                    parent: Optional[str] = None, 
                    children: Optional[List[str]] = None) -> MenuItem:
        """Helper to add a category menu item"""
        item = MenuItem(
            id=id,
            label=label,
            description=description,
            parent=parent,
            children=children or [],
            is_category=True
        )
        self.add_item(item)
        return item
        
    def add_selectable(self, id: str, label: str, description: str,
                      parent: Optional[str] = None,
                      default: bool = False,
                      ansible_var: Optional[str] = None) -> MenuItem:
        """Helper to add a selectable menu item"""
        item = MenuItem(
            id=id,
            label=label,
            description=description,
            parent=parent,
            default=default,
            ansible_var=ansible_var
        )
        self.add_item(item)
        return item
        
    def add_configurable(self, id: str, label: str, description: str,
                        parent: Optional[str] = None,
                        config_type: str = "slider",
                        config_value: any = None,
                        config_range: tuple = (1, 10),
                        config_unit: str = "",
                        config_options: Optional[List[tuple]] = None,
                        ansible_var: Optional[str] = None) -> MenuItem:
        """Helper to add a configurable menu item"""
        item = MenuItem(
            id=id,
            label=label,
            description=description,
            parent=parent,
            is_configurable=True,
            config_type=config_type,
            config_value=config_value or (config_range[0] if config_type == "slider" else ""),
            config_range=config_range,
            config_unit=config_unit,
            config_options=config_options,
            ansible_var=ansible_var
        )
        self.add_item(item)
        return item


class MenuRegistry:
    """Registry to collect menu items from all builders"""
    
    def __init__(self):
        self.builders: List[MenuBuilder] = []
        self.items: Dict[str, MenuItem] = {}
        
    def register(self, builder: MenuBuilder) -> None:
        """Register a menu builder"""
        self.builders.append(builder)
        
    def build_all(self) -> Dict[str, MenuItem]:
        """Build all menus and return combined items"""
        self.items.clear()
        
        for builder in self.builders:
            builder_items = builder.build()
            self.items.update(builder_items)
            
        return self.items