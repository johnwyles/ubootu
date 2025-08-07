#!/usr/bin/env python3
"""
Visual constants for the unified TUI
"""

# Selection indicators
INDICATOR_NONE = "○"  # No items selected
INDICATOR_PARTIAL = "◐"  # Some items selected
INDICATOR_FULL = "●"  # All items selected
CHECKBOX_SELECTED = "[X]"
CHECKBOX_UNSELECTED = "[ ]"

# Key bindings
KEY_BINDINGS = {
    "navigate_up": ["KEY_UP", "k"],
    "navigate_down": ["KEY_DOWN", "j"],
    "navigate_left": ["KEY_LEFT", "h"],
    "navigate_right": ["KEY_RIGHT", "l"],
    "select": [" "],  # Space toggles selection
    "enter": ["\n", "KEY_RIGHT", "l"],  # Enter, Right arrow, and 'l' enter submenus
    "back": ["KEY_LEFT", "ESC", "h"],
    "quit": ["q", "Q"],
    "help": ["KEY_F1", "?", "H"],  # F1, ?, or H for help (not 'h' to avoid conflict)
    "save": ["s", "S"],
    "apply": ["p", "P"],
    "search": ["/"],
    "select_all": ["a", "A"],
    "deselect_all": ["d", "D"],
    "main_menu": ["m", "M"],  # Go back to main menu
}

# UI Text
TITLE = "🚀 Ubootu Configuration"
SUBTITLE = "Professional Ubuntu Desktop Configuration Tool"

# Help bar text
HELP_BAR = "↑↓ Nav  Space Select  → Menu  ← Back  S Save  P Apply  ^D Diff  ^S Scan  ^M Mode  Q Quit"
HELP_BAR_SUBMENU = "↑↓ Nav  Space Select  → Menu  ← Back  A/D All/None  ^D Diff  ^S Scan  ^M Mode  Q Quit"

# Minimum terminal size
MIN_WIDTH = 80
MIN_HEIGHT = 24

# Dialog dimensions
DIALOG_WIDTH = 60
DIALOG_HEIGHT = 10
SUDO_DIALOG_WIDTH = 50
SUDO_DIALOG_HEIGHT = 7

# Menu structure
MENU_CATEGORIES = [
    {
        "id": "development",
        "label": "Development Tools",
        "description": "Programming languages, IDEs, tools",
        "icon": "💻",
    },
    {"id": "ai-ml", "label": "AI & Machine Learning", "description": "AI tools, ML frameworks, LLMs", "icon": "🤖"},
    {"id": "desktop", "label": "Desktop Environment", "description": "Desktop environments and themes", "icon": "🖥️"},
    {"id": "applications", "label": "Applications", "description": "Browsers, productivity, multimedia", "icon": "📦"},
    {"id": "security", "label": "Security & Privacy", "description": "Firewall, VPN, encryption tools", "icon": "🔒"},
    {"id": "system", "label": "System Configuration", "description": "Performance, services, hardware", "icon": "⚙️"},
]
