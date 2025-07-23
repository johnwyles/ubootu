#!/usr/bin/env python3
"""
Core TUI class that orchestrates all TUI components for Ubootu
"""

import curses
from typing import Dict, Set, Optional

from .models import MenuItem
from .renderer import TUIRenderer
from .dialogs import TUIDialogs
from .handlers import TUIEventHandler
from .config import TUIConfigManager
from .menus import (
    MenuRegistry, DevelopmentMenuBuilder, DesktopMenuBuilder, 
    ApplicationsMenuBuilder, SecurityMenuBuilder, SystemMenuBuilder
)


class UbootuTUI:
    """Main TUI class that coordinates all components"""
    
    def __init__(self, stdscr, selected_sections=None):
        self.stdscr = stdscr
        self.selected_sections = selected_sections
        self.cancelled = False
        
        # Build menu structure
        self.menu_items = self._build_menu_structure()
        self.selected_items: Set[str] = set()
        
        # Initialize components
        self.config_manager = TUIConfigManager(self.menu_items, self.selected_items)
        self.renderer = TUIRenderer(stdscr, self.menu_items, self.selected_items)
        self.dialogs = TUIDialogs(stdscr, self.selected_items)
        self.event_handler = TUIEventHandler(stdscr, self.menu_items, self.selected_items)
        
        # Connect components
        self.event_handler.set_dialog_handler(self.dialogs)
        
        # Sync state between components
        self._sync_component_state()
        
        # Setup screen
        self._setup_screen()
        
        # Apply defaults
        self.config_manager.apply_defaults()
    
    def _build_menu_structure(self) -> Dict[str, MenuItem]:
        """Build hierarchical menu structure using menu builders"""
        registry = MenuRegistry()
        
        # Register all menu builders
        registry.register('development', DevelopmentMenuBuilder())
        registry.register('desktop', DesktopMenuBuilder())
        registry.register('applications', ApplicationsMenuBuilder())
        registry.register('security', SecurityMenuBuilder())
        registry.register('system', SystemMenuBuilder())
        
        # Build all menus
        items = {}
        
        # Build each section
        for builder_name, builder in registry.builders.items():
            section_items = builder.build()
            items.update(section_items)
        
        # Create root menu
        all_sections = ["development", "desktop", "applications", "security", "system"]
        if self.selected_sections:
            # Map themes to desktop since themes is part of desktop in the TUI
            mapped_sections = []
            for s in self.selected_sections:
                if s == "themes":
                    mapped_sections.append("desktop")
                elif s in all_sections:
                    mapped_sections.append(s)
            # Remove duplicates while preserving order
            seen = set()
            root_children = []
            for s in mapped_sections:
                if s not in seen:
                    seen.add(s)
                    root_children.append(s)
            
            if root_children:
                root_desc = f"Configuring selected sections: {', '.join(root_children)}"
            else:
                # No valid sections selected, show all
                root_children = all_sections
                root_desc = "Navigate: ↑↓ arrows, SPACE select, ENTER enter     |     ▶▶▶ PRESS F1 FOR ACTIONS MENU TO START INSTALLATION ◀◀◀"
        else:
            # Show all sections
            root_children = all_sections
            root_desc = "Navigate: ↑↓ arrows, SPACE select, ENTER enter     |     ▶▶▶ PRESS F1 FOR ACTIONS MENU TO START INSTALLATION ◀◀◀"
        
        items["root"] = MenuItem(
            "root", "🚀 Ubootu - Ubuntu System Setup", 
            root_desc,
            is_category=True,
            children=root_children
        )
        
        # Add actions menu
        items["actions"] = MenuItem(
            "actions", "Actions", 
            "Installation and configuration actions",
            parent="root", is_category=True,
            children=["action-install", "action-save", "action-reset", "action-exit"]
        )
        
        # Action items
        items["action-install"] = MenuItem(
            "action-install", "🚀 Start Installation", 
            "Apply settings and install selected software",
            parent="actions"
        )
        
        items["action-save"] = MenuItem(
            "action-save", "💾 Save Configuration", 
            "Save current selections without installing",
            parent="actions"
        )
        
        items["action-reset"] = MenuItem(
            "action-reset", "🔄 Reset Configuration", 
            "Clear all selections and return to defaults",
            parent="actions"
        )
        
        items["action-exit"] = MenuItem(
            "action-exit", "❌ Exit without Saving", 
            "Exit the configuration tool without saving",
            parent="actions"
        )
        
        return items
    
    def _setup_screen(self):
        """Setup terminal screen for TUI"""
        # Get terminal dimensions
        height, width = self.stdscr.getmaxyx()
        if height < 24 or width < 80:
            # Terminal too small, but continue anyway
            pass
        
        # Setup screen safely
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
            self.stdscr.timeout(50)  # Reduced timeout for better responsiveness
        except:
            # Some terminals don't support all features
            pass
    
    def _sync_component_state(self):
        """Synchronize state between all components"""
        # Update renderer state
        self.renderer.current_menu = self.config_manager.current_menu
        self.renderer.current_item = self.config_manager.current_item
        self.renderer.scroll_offset = self.config_manager.scroll_offset
        
        # Update event handler state
        self.event_handler.current_menu = self.config_manager.current_menu
        self.event_handler.current_item = self.config_manager.current_item
        self.event_handler.scroll_offset = self.config_manager.scroll_offset
        self.event_handler.breadcrumb_stack = self.config_manager.breadcrumb_stack
        self.event_handler.cancelled = self.cancelled
    
    def _update_state_from_event_handler(self):
        """Update state from event handler after event processing"""
        self.config_manager.current_menu = self.event_handler.current_menu
        self.config_manager.current_item = self.event_handler.current_item
        self.config_manager.scroll_offset = self.event_handler.scroll_offset
        self.config_manager.breadcrumb_stack = self.event_handler.breadcrumb_stack
        self.cancelled = self.event_handler.cancelled
        
        # Sync renderer
        self._sync_component_state()
    
    def run(self) -> int:
        """Main TUI loop"""
        try:
            # Initial draw
            self.stdscr.clear()
            self._draw_interface()
            
            while True:
                # Handle input (blocking - waits for key)
                key = self.stdscr.getch()
                if key != -1:  # Key was pressed
                    # Handle the key event
                    continue_running = self.event_handler.handle_key(
                        key,
                        self.config_manager.get_current_menu_items,
                        self.dialogs.show_help_popup
                    )
                    
                    # Update state from event handler
                    self._update_state_from_event_handler()
                    
                    if not continue_running:
                        break
                    
                    # Redraw only after handling key
                    self.stdscr.erase()  # Clear without flashing
                    self._draw_interface()
                    
        except KeyboardInterrupt:
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"TUI LOOP: KeyboardInterrupt caught - setting cancelled=True\n")
            self.cancelled = True
        except Exception as e:
            # Handle any other errors gracefully
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"TUI LOOP: Exception caught: {e} - setting cancelled=True\n")
            self.cancelled = True
        
        # Return exit status
        with open('/tmp/debug_tui.log', 'a') as f:
            f.write(f"TUI LOOP ENDED: cancelled={self.cancelled}, returning {0 if not self.cancelled else 1}\n")
        return 0 if not self.cancelled else 1
    
    def _draw_interface(self):
        """Draw the complete TUI interface"""
        menu_items = self.config_manager.get_current_menu_items()
        
        self.renderer.draw_header()
        self.renderer.draw_menu(menu_items)
        self.renderer.draw_help()
        self.renderer.draw_stats()
        self.stdscr.refresh()


def run_tui(selected_sections=None):
    """Run the TUI with curses wrapper"""
    def tui_main(stdscr):
        tui = UbootuTUI(stdscr, selected_sections)
        return tui.run()
    
    return curses.wrapper(tui_main)


def main():
    """Main entry point"""
    import sys
    
    # Parse command line arguments for section selection
    selected_sections = None
    if len(sys.argv) > 1:
        selected_sections = sys.argv[1:]
    
    # Run the TUI
    exit_code = run_tui(selected_sections)
    sys.exit(exit_code)