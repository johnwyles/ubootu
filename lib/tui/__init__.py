#!/usr/bin/env python3
"""
TUI package for Ubootu - Ubuntu System Configuration Tool
"""

from lib.tui.config import TUIConfigManager
from lib.tui.core import UbootuTUI, main, run_tui
from lib.tui.dialogs import TUIDialogs
from lib.tui.handlers import TUIEventHandler
from lib.tui.models import MenuItem
from lib.tui.renderer import TUIRenderer

__all__ = [
    "UbootuTUI",
    "run_tui",
    "main",
    "MenuItem",
    "TUIRenderer",
    "TUIDialogs",
    "TUIEventHandler",
    "TUIConfigManager",
]
