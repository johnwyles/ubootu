#!/usr/bin/env python3
"""
Data models for the Ubootu TUI
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class MenuItem:
    """Represents a menu item in the hierarchical TUI"""

    id: str
    label: str
    description: str
    parent: Optional[str] = None
    children: Optional[List[str]] = None
    selected: bool = False
    default: bool = False
    is_category: bool = False
    is_configurable: bool = False  # True if this item needs configuration
    config_type: str = ""  # "slider", "dropdown", "text", "toggle", etc.
    config_range: Tuple[int, int] = (1, 10)  # For sliders: (min, max)
    config_value: Any = 5  # Current value for configurable items (int, str, bool, etc.)
    config_unit: str = ""  # Unit for display (e.g., "seconds", "%", "px")
    config_options: Optional[List[Tuple[str, str]]] = (
        None  # For dropdowns: [(value, display_label)]
    )
    ansible_var: Optional[str] = None  # Maps to Ansible variable name
