#!/usr/bin/env python3
"""
Menu builders for the Ubootu TUI
"""

from lib.tui.menus.applications import ApplicationsMenuBuilder
from lib.tui.menus.base import MenuBuilder, MenuRegistry
from lib.tui.menus.desktop import DesktopMenuBuilder
from lib.tui.menus.development import DevelopmentMenuBuilder
from lib.tui.menus.security import SecurityMenuBuilder
from lib.tui.menus.system import SystemMenuBuilder

__all__ = [
    "MenuBuilder",
    "MenuRegistry",
    "DevelopmentMenuBuilder",
    "DesktopMenuBuilder",
    "ApplicationsMenuBuilder",
    "SecurityMenuBuilder",
    "SystemMenuBuilder",
]
