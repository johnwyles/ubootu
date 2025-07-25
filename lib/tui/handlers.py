#!/usr/bin/env python3
"""
Event handling system for the Ubootu TUI interface
"""

import curses
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Dict, List, Set, Tuple

import yaml

if TYPE_CHECKING:
    from .models import MenuItem


class TUIEventHandler:
    """Handles all event processing for the TUI"""

    def __init__(
        self, stdscr, menu_items: Dict[str, "MenuItem"], selected_items: Set[str]
    ):
        self.stdscr = stdscr
        self.menu_items = menu_items
        self.selected_items = selected_items
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.breadcrumb_stack: List[Tuple[str, int, int]] = []
        self.cancelled = False

        # Dialog handler will be injected
        self.dialog_handler = None

    def set_dialog_handler(self, dialog_handler):
        """Set the dialog handler for configuration dialogs"""
        self.dialog_handler = dialog_handler

    def handle_key(
        self, key: int, menu_items_getter: Callable, show_help_callback: Callable
    ) -> bool:
        """Handle keyboard input"""
        menu_items = menu_items_getter()

        if not menu_items:
            return True

        # Debug: Log every key press
        with open("/tmp/debug_tui.log", "a") as f:
            f.write(
                f"Key pressed: {key} (char: {chr(key) if 32 <= key <= 126 else 'special'})\n"
            )

        # Navigation
        if key == curses.KEY_UP or key == ord("k") or key == ord("K"):
            if self.current_item > 0:
                self.current_item -= 1
        elif key == curses.KEY_DOWN or key == ord("j") or key == ord("J"):
            if self.current_item < len(menu_items) - 1:
                self.current_item += 1

        # Page navigation
        elif key == curses.KEY_NPAGE:  # Page Down
            self.current_item = min(self.current_item + 10, len(menu_items) - 1)
        elif key == curses.KEY_PPAGE:  # Page Up
            self.current_item = max(self.current_item - 10, 0)

        # Home/End
        elif key == curses.KEY_HOME:
            self.current_item = 0
        elif key == curses.KEY_END:
            self.current_item = len(menu_items) - 1

        # Selection
        elif key == ord(" "):  # Space - toggle selection or select all in category
            current_item = menu_items[self.current_item]
            if current_item.is_category:
                # Select all items in this category
                self._select_all_in_category_toggle(current_item.id)
            else:
                # Toggle individual item selection
                current_item.selected = not current_item.selected
                if current_item.selected:
                    self.selected_items.add(current_item.id)
                else:
                    self.selected_items.discard(current_item.id)

        # Enter menu/category or execute action
        elif key == ord("\n") or key == curses.KEY_ENTER or key == 10 or key == 13:
            current_item = menu_items[self.current_item]

            # Debug: Write what item we're trying to enter/select
            with open("/tmp/debug_tui.log", "a") as f:
                f.write(
                    f"ENTER (key {key}) pressed on: {current_item.id} (label: {current_item.label}) is_category: {current_item.is_category} parent: {current_item.parent} current_menu: {self.current_menu}\n"
                )

            if current_item.is_category:
                # Enter subcategory
                with open("/tmp/debug_tui.log", "a") as f:
                    f.write(
                        f"SUCCESS: Entering category {current_item.id}, breadcrumb_stack will be: {len(self.breadcrumb_stack) + 1}\n"
                    )
                self.breadcrumb_stack.append(
                    (self.current_menu, self.current_item, self.scroll_offset)
                )
                self.current_menu = current_item.id
                self.current_item = 0
                self.scroll_offset = 0

            else:
                # Handle actions if in actions menu, otherwise toggle selection
                if current_item.parent == "actions":
                    with open("/tmp/debug_tui.log", "a") as f:
                        f.write(f"EXECUTING ACTION: {current_item.id}\n")

                    if current_item.id == "action-install":
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(
                                f"Calling _handle_install() - this SHOULD exit TUI\n"
                            )
                        return self._handle_install()  # This exits with installation
                    elif current_item.id == "action-save":
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(
                                f"Calling _handle_save() - this should CONTINUE TUI\n"
                            )
                        result = self._handle_save()  # This continues (returns True)
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(f"_handle_save() returned: {result}\n")
                        return result
                    elif current_item.id == "action-reset":
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(
                                f"Calling _handle_reset() - this should CONTINUE TUI\n"
                            )
                        result = self._handle_reset()  # This continues (returns True)
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(f"_handle_reset() returned: {result}\n")
                        return result
                    elif current_item.id == "action-exit":
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(f"Calling _handle_exit() - this SHOULD exit TUI\n")
                        return self._handle_exit()  # This exits (returns False)
                    else:
                        # Unknown action - just continue
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(f"UNKNOWN ACTION: {current_item.id} - continuing\n")
                        return True
                else:
                    # Handle configurable items vs regular toggle items
                    if current_item.is_configurable and self.dialog_handler:
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(
                                f"CONFIGURING ITEM: {current_item.id} (type: {current_item.config_type})\n"
                            )
                        self.dialog_handler.show_configuration_dialog(current_item)
                    else:
                        # For all other items, toggle selection (this should NOT cause exit)
                        with open("/tmp/debug_tui.log", "a") as f:
                            f.write(
                                f"TOGGLING SELECTION: {current_item.id} from {current_item.selected} to {not current_item.selected}\n"
                            )
                        current_item.selected = not current_item.selected
                        if current_item.selected:
                            self.selected_items.add(current_item.id)
                        else:
                            self.selected_items.discard(current_item.id)

        # Right arrow - enter submenu or toggle item
        elif key == curses.KEY_RIGHT:
            current_item = menu_items[self.current_item]

            with open("/tmp/debug_tui.log", "a") as f:
                f.write(
                    f"RIGHT arrow pressed on: {current_item.id} (is_category: {current_item.is_category})\n"
                )

            if current_item.is_category:
                # Enter submenu (same as ENTER on category)
                self.breadcrumb_stack.append(
                    (self.current_menu, self.current_item, self.scroll_offset)
                )
                self.current_menu = current_item.id
                self.current_item = 0
                self.scroll_offset = 0
            else:
                # Toggle item or configure if configurable
                if current_item.is_configurable and self.dialog_handler:
                    self.dialog_handler.show_configuration_dialog(current_item)
                else:
                    current_item.selected = not current_item.selected
                    if current_item.selected:
                        self.selected_items.add(current_item.id)
                    else:
                        self.selected_items.discard(current_item.id)

        # Back/Up one level - multiple keys for convenience
        elif (
            key == curses.KEY_BACKSPACE
            or key == 127
            or key == curses.KEY_LEFT
            or key == ord("b")
            or key == ord("B")
        ):
            # ESC key is handled separately for quit, but if we're not at root, ESC goes back
            if self.breadcrumb_stack:
                with open("/tmp/debug_tui.log", "a") as f:
                    f.write(f"Going back one level with key {key}\n")
                self.current_menu, self.current_item, self.scroll_offset = (
                    self.breadcrumb_stack.pop()
                )

        # Quick select/deselect all in category
        elif key == ord("a") or key == ord("A"):
            self._select_all_in_category(True)
        elif key == ord("n") or key == ord("N"):
            self._select_all_in_category(False)

        # Function keys for Actions popup
        elif key >= curses.KEY_F1 and key <= curses.KEY_F10:
            with open("/tmp/debug_tui.log", "a") as f:
                f.write(f"Function key pressed: F{key - curses.KEY_F1 + 1}\n")
            return self._show_actions_popup()

        # Help key - show context-sensitive help
        elif key == ord("h") or key == ord("H") or key == ord("?"):
            current_item = menu_items[self.current_item]
            show_help_callback(current_item)

        # Quit with Q key only
        elif key == ord("q") or key == ord("Q"):
            with open("/tmp/debug_tui.log", "a") as f:
                f.write(
                    f"Q/q key pressed: {key} (ord('q')={ord('q')}, ord('Q')={ord('Q')})\n"
                )
            return self._handle_exit()

        # Escape key - go back if possible, otherwise quit (immediate response)
        elif key == 27:  # Escape
            with open("/tmp/debug_tui.log", "a") as f:
                f.write(
                    f"ESC key (27) pressed - breadcrumb_stack length: {len(self.breadcrumb_stack)}\n"
                )
            if self.breadcrumb_stack:
                with open("/tmp/debug_tui.log", "a") as f:
                    f.write(f"ESC - going back one level\n")
                self.current_menu, self.current_item, self.scroll_offset = (
                    self.breadcrumb_stack.pop()
                )
                # Force immediate refresh for responsive ESC
                return True
            else:
                with open("/tmp/debug_tui.log", "a") as f:
                    f.write(f"ESC at root - exiting\n")
                return self._handle_exit()

        with open("/tmp/debug_tui.log", "a") as f:
            f.write(f"_handle_key returning True for key {key}\n")
        return True

    def _select_all_in_category(self, select: bool):
        """Select or deselect all items in current category"""
        from .renderer import TUIRenderer

        # We need a way to get current menu items - this will need to be passed in
        pass  # Implementation will be handled by the caller

    def _select_all_in_category_toggle(self, category_id: str):
        """Toggle selection of all items in a specific category"""
        # Get all selectable items in this category
        category_items = self._get_all_selectable_items(category_id)

        if not category_items:
            return

        # Check if all items are selected
        all_selected = all(item_id in self.selected_items for item_id in category_items)

        # If all are selected, deselect all; otherwise select all
        select_all = not all_selected

        for item_id in category_items:
            if item_id in self.menu_items:
                item = self.menu_items[item_id]
                item.selected = select_all
                if select_all:
                    self.selected_items.add(item_id)
                else:
                    self.selected_items.discard(item_id)

    def _get_all_selectable_items(self, category_id: str) -> List[str]:
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
                items.extend(self._get_all_selectable_items(child_id))
            else:
                items.append(child_id)

        return items

    def _handle_install(self) -> bool:
        """Handle install action"""
        if not self.selected_items:
            # Show sexy error message
            try:
                # White on black
                self.stdscr.attron(curses.A_BOLD)
                height, width = self.stdscr.getmaxyx()
                msg = "🚨 No items selected! Use Space to select items first. 🚨"
                safe_msg = msg.encode("ascii", "ignore").decode("ascii")
                if len(safe_msg.strip()) < len(msg.strip()) * 0.7:
                    safe_msg = "*** ERROR: No items selected! Use Space to select items first. ***"
                self.stdscr.addstr(height - 5, 2, safe_msg[: width - 4])
                self.stdscr.attroff(curses.A_BOLD)
                self.stdscr.refresh()
                curses.napms(2000)  # Wait 2 seconds
            except curses.error:
                pass
            return True

        # Save configuration and exit
        self._save_configuration()
        return False

    def _handle_save(self) -> bool:
        """Handle save configuration action"""
        try:
            self._save_configuration()

            # Show success message
            height, width = self.stdscr.getmaxyx()
            msg = "✅ Ubootu configuration saved successfully! Continue configuring or go to Actions > Install"
            safe_msg = msg.encode("ascii", "ignore").decode("ascii")
            if len(safe_msg.strip()) < len(msg.strip()) * 0.7:
                safe_msg = "*** UNBOOTU SUCCESS: Configuration saved! Continue configuring or go to Actions > Install ***"
            self.stdscr.addstr(height - 5, 2, safe_msg[: width - 4])
            self.stdscr.refresh()
            curses.napms(2000)  # Wait 2 seconds

            # Return to main menu
            self.current_menu = "root"
            self.current_item = 0
            self.scroll_offset = 0
            self.breadcrumb_stack = []

        except curses.error:
            pass

        return True

    def _handle_reset(self) -> bool:
        """Handle reset action with confirmation"""
        height, width = self.stdscr.getmaxyx()

        # Clear message area
        for i in range(height - 6, height - 3):
            self.stdscr.addstr(i, 0, " " * width)

        # Show confirmation
        try:
            # White on black
            self.stdscr.attron(curses.A_BOLD)
            msg = "WARNING: Reset all selections? This cannot be undone! (y/N)"
            self.stdscr.addstr(height - 5, 2, msg[: width - 4])
            self.stdscr.attroff(curses.A_BOLD)
            self.stdscr.refresh()
        except curses.error:
            pass

        # Get confirmation
        self.stdscr.timeout(30000)  # 30 second timeout
        key = self.stdscr.getch()
        self.stdscr.timeout(100)  # Reset timeout

        if key == ord("y") or key == ord("Y"):
            # Reset all selections
            self.selected_items.clear()
            for item in self.menu_items.values():
                item.selected = item.default
                if item.default:
                    self.selected_items.add(item.id)

            # Show confirmation
            try:
                msg = "SUCCESS: Configuration reset to defaults"
                self.stdscr.addstr(height - 4, 2, msg[: width - 4])
                self.stdscr.refresh()
                curses.napms(1500)
            except curses.error:
                pass

        return True

    def _handle_exit(self) -> bool:
        """Handle exit action with confirmation"""
        return self._show_exit_confirmation()

    def _show_exit_confirmation(self) -> bool:
        """Show exit confirmation dialog - defaults to NO"""
        height, width = self.stdscr.getmaxyx()

        # Create a popup overlay
        popup_height = 8
        popup_width = 50
        start_y = (height - popup_height) // 2
        start_x = (width - popup_width) // 2

        # Options with NO as default (index 1)
        options = ["YES - Exit without saving", "NO - Continue configuring"]
        selected = 1  # Default to NO

        try:
            while True:
                # Draw popup background
                for i in range(popup_height):
                    # Magenta popup
                    self.stdscr.addstr(start_y + i, start_x, " " * popup_width)
                    # Draw border and title
                self.stdscr.addstr(
                    start_y, start_x, "┌" + "─" * (popup_width - 2) + "┐"
                )

                # Title
                title = "⚠️  EXIT CONFIRMATION  ⚠️"
                title_x = start_x + (popup_width - len(title)) // 2
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(start_y + 1, title_x, title)
                self.stdscr.attroff(curses.A_BOLD)

                # Warning message
                msg = "Are you sure you want to exit?"
                msg_x = start_x + (popup_width - len(msg)) // 2
                self.stdscr.addstr(start_y + 2, msg_x, msg)

                # Separator
                self.stdscr.addstr(
                    start_y + 3, start_x, "├" + "─" * (popup_width - 2) + "┤"
                )
                # Draw options
                for i, option in enumerate(options):
                    y = start_y + 4 + i
                    if i == selected:
                        # Highlight selected option
                        # Cyan selection
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(
                            y, start_x + 2, f"▶ {option:<{popup_width-6}}"
                        )
                        self.stdscr.attroff(curses.A_BOLD)
                    else:
                        self.stdscr.addstr(
                            y, start_x + 2, f"  {option:<{popup_width-6}}"
                        )
                        # Bottom border
                self.stdscr.addstr(
                    start_y + popup_height - 1,
                    start_x,
                    "└" + "─" * (popup_width - 2) + "┘",
                )
                self.stdscr.refresh()

                # Handle input
                key = self.stdscr.getch()

                if key == curses.KEY_UP:
                    selected = (selected - 1) % len(options)
                elif key == curses.KEY_DOWN:
                    selected = (selected + 1) % len(options)
                elif key == ord("\n") or key == curses.KEY_ENTER:
                    if selected == 0:  # YES - Exit
                        self.cancelled = True
                        return False  # Exit the TUI
                    else:  # NO - Continue
                        return True  # Continue running
                elif key == 27:  # ESC also defaults to NO
                    return True  # Continue running

        except curses.error:
            pass

        return True  # Default to continuing

    def _save_configuration(self):
        """Save configuration to file"""
        config = {
            "configuration_date": datetime.now().isoformat(),
            "selected_items": list(self.selected_items),
            "ui_version": "2.0_unbootu",
            "generated_by": "Ubootu - Professional Ubuntu Desktop Configuration Tool",
        }

        # Save configurable item values
        configurable_values = {}
        for item_id, item in self.menu_items.items():
            if item.is_configurable and item.selected:
                configurable_values[item_id] = {
                    "value": item.config_value,
                    "type": item.config_type,
                    "unit": item.config_unit,
                }

        if configurable_values:
            config["configurable_values"] = configurable_values

        # Create Ansible variables mapping
        ansible_vars = {}
        desktop_env_vars = {}
        other_vars = {}

        for item_id, item in self.menu_items.items():
            if item.selected and item.ansible_var:
                # Store the actual value for Ansible
                if item.is_configurable:
                    value = item.config_value
                else:
                    value = True  # Non-configurable items are just enabled/disabled

                # Group desktop environment variables
                if item.ansible_var.startswith("de_"):
                    desktop_env_vars[item.ansible_var] = value
                else:
                    other_vars[item.ansible_var] = value

        # Add desktop environment settings as a group
        if desktop_env_vars:
            ansible_vars["desktop_environment_settings"] = desktop_env_vars

        # Add other variables at top level
        ansible_vars.update(other_vars)

        # Add to config
        if ansible_vars:
            config["ansible_variables"] = ansible_vars

        # Organize by categories for easier processing
        categories = {}
        for item_id in self.selected_items:
            item = self.menu_items[item_id]
            if item.parent:
                if item.parent not in categories:
                    categories[item.parent] = []
                categories[item.parent].append(item_id)

        config["categories"] = categories

        try:
            with open("config.yml", "w") as f:
                yaml.dump(config, f, default_flow_style=False)
        except Exception as e:
            # Handle save error
            height, width = self.stdscr.getmaxyx()
            # White on black
            self.stdscr.attron(curses.A_BOLD)
            msg = f"Error saving configuration: {str(e)}"
            self.stdscr.addstr(height - 4, 2, msg[: width - 4])
            self.stdscr.attroff(curses.A_BOLD)
            self.stdscr.refresh()
            curses.napms(3000)

    def _show_actions_popup(self) -> bool:
        """Show Actions popup overlay accessible via Function keys"""
        height, width = self.stdscr.getmaxyx()

        # Create a popup overlay
        popup_height = 14
        popup_width = 60
        start_y = (height - popup_height) // 2
        start_x = (width - popup_width) // 2

        # Actions menu items
        action_items = [
            ("🚀 Start Installation", "Apply settings & install software"),
            ("💾 Save Configuration", "Save selections without installing"),
            ("🔄 Reset Configuration", "Clear all selections"),
            ("❌ Exit without Saving", "Cancel without saving"),
        ]

        current_action = 0

        try:
            while True:
                # Clear the popup area
                for y in range(start_y, start_y + popup_height):
                    if y < height:
                        try:
                            self.stdscr.addstr(
                                y, start_x, " " * min(popup_width, width - start_x)
                            )
                        except curses.error:
                            pass

                # Draw popup with HIGH CONTRAST colors
                try:
                    # Draw background and border
                    # White on magenta
                    for y in range(start_y, start_y + popup_height):
                        self.stdscr.addstr(
                            y, start_x, "│" + " " * (popup_width - 2) + "│"
                        )

                    # Top border
                    self.stdscr.addstr(
                        start_y, start_x, "┌" + "─" * (popup_width - 2) + "┐"
                    )

                    # Title
                    title = "ACTIONS MENU (F1-F10)"
                    title_x = start_x + (popup_width - len(title)) // 2
                    self.stdscr.attron(curses.A_BOLD)
                    self.stdscr.addstr(start_y + 1, title_x, title)
                    self.stdscr.attroff(curses.A_BOLD)

                    # Instructions
                    inst = "↑↓ Select   ENTER Execute   ESC Cancel"
                    inst_x = start_x + (popup_width - len(inst)) // 2
                    self.stdscr.addstr(start_y + 2, inst_x, inst)

                    # Separator
                    self.stdscr.addstr(
                        start_y + 3, start_x, "├" + "─" * (popup_width - 2) + "┤"
                    )
                except curses.error:
                    pass

                # Draw action items
                for i, (action_title, action_desc) in enumerate(action_items):
                    item_y = start_y + 4 + i * 2

                    try:
                        if i == current_action:
                            # Selected item - black on cyan (high contrast)
                            # Black on cyan
                            self.stdscr.addstr(
                                item_y, start_x, "│" + " " * (popup_width - 2) + "│"
                            )
                            self.stdscr.attron(curses.A_BOLD)
                            self.stdscr.addstr(item_y, start_x + 3, f"▶ {action_title}")
                            self.stdscr.attroff(curses.A_BOLD)
                            self.stdscr.addstr(
                                item_y + 1, start_x, "│" + " " * (popup_width - 2) + "│"
                            )
                            self.stdscr.addstr(
                                item_y + 1, start_x + 5, action_desc[: popup_width - 8]
                            )
                        else:
                            # Unselected item - white on magenta
                            # White on magenta
                            self.stdscr.addstr(item_y, start_x + 3, f"  {action_title}")
                            self.stdscr.addstr(
                                item_y + 1, start_x + 5, action_desc[: popup_width - 8]
                            )
                    except curses.error:
                        pass

                # Bottom border
                try:
                    self.stdscr.addstr(
                        start_y + popup_height - 1,
                        start_x,
                        "└" + "─" * (popup_width - 2) + "┘",
                    )
                except curses.error:
                    pass

                self.stdscr.refresh()

                # Handle input
                key = self.stdscr.getch()

                if key == curses.KEY_UP or key == ord("k"):
                    current_action = (current_action - 1) % len(action_items)
                elif key == curses.KEY_DOWN or key == ord("j"):
                    current_action = (current_action + 1) % len(action_items)
                elif (
                    key == ord("\n")
                    or key == curses.KEY_ENTER
                    or key == 10
                    or key == 13
                ):
                    # Execute selected action
                    if current_action == 0:  # Install
                        return self._handle_install()
                    elif current_action == 1:  # Save
                        self._handle_save()
                        return True
                    elif current_action == 2:  # Reset
                        self._handle_reset()
                        return True
                    elif current_action == 3:  # Exit
                        return self._handle_exit()
                elif key == 27:  # ESC - close popup
                    return True
                elif key == ord("q") or key == ord("Q"):
                    return True

        except curses.error:
            # Handle any drawing errors gracefully
            pass

        return True
