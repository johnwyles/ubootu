#!/usr/bin/env python3
"""
Professional and fun menu UI system for Ubootu
Uses rich library for beautiful terminal formatting
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.align import Align
    from rich import box
    from rich.live import Live
except ImportError:
    print("ERROR: Rich library not found. Please install with: sudo apt install python3-rich")
    sys.exit(1)

# Try to import keyboard, but make it optional
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Note: keyboard module not available. Arrow key navigation will be disabled.")
    print("Install with: sudo apt install python3-keyboard or use number keys for navigation.")


@dataclass
class MenuOption:
    """Represents a menu option"""
    key: str
    icon: str
    title: str
    description: str
    action: Optional[str] = None
    visible: bool = True


class MenuUI:
    """Professional menu UI system with rich formatting"""
    
    def __init__(self):
        self.console = Console()
        self.current_selection = 0
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def show_splash_screen(self):
        """Display animated splash screen"""
        self.clear_screen()
        
        splash_text = """
[bold cyan]     ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱[/]
[bold cyan]    ╱                                                          ╱[/]
[bold cyan]   ╱   [bold white]██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗[/] ╱[/]
[bold cyan]  ╱    [bold white]██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║[/]╱[/]
[bold cyan] ╱     [bold white]██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║[/][/]
[bold cyan]╱      [bold white]██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║[/][/]
       [bold white]╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝[/]
        [bold white]╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝[/] 
                    
                    [bold magenta]Professional Ubuntu Desktop Configuration Tool[/]
        """
        
        panel = Panel(splash_text, box=box.ROUNDED, border_style="bright_blue")
        self.console.print(panel)
        
        # Animated loading bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Loading awesomeness...", total=100)
            
            loading_messages = [
                "Initializing Ubuntu magic...",
                "Preparing configuration wizardry...",
                "Loading customization options...",
                "Getting everything ready..."
            ]
            
            for i, message in enumerate(loading_messages):
                progress.update(task, advance=25, description=f"[cyan]{message}")
                time.sleep(0.5)
                
        time.sleep(0.5)
        
    def show_main_menu(self, has_config: bool = False) -> str:
        """Display the main menu and return selected option"""
        self.clear_screen()
        
        # Header
        header = Panel(
            Align.center(
                "[bold]🚀 Ubootu 🚀[/]\n"
                "[dim]Professional Ubuntu Desktop Configuration Tool[/]",
                vertical="middle"
            ),
            box=box.DOUBLE_EDGE,
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(header)
        self.console.print()
        
        # Menu options
        options = [
            MenuOption("1", "🚀", "Fresh Install", "Configure a brand new Ubuntu installation"),
            MenuOption("2", "🔧", "Modify Setup", "Tweak your existing configuration", visible=has_config),
            MenuOption("3", "📦", "Apply Profile", "Restore from a saved configuration"),
            MenuOption("4", "💾", "Backup Config", "Save your current setup", visible=has_config),
            MenuOption("5", "📜", "View History", "Browse configuration timeline", visible=has_config),
            MenuOption("6", "🎯", "Quick Actions", "Common tasks and fixes"),
            MenuOption("7", "❓", "Help", "Get help and documentation"),
            MenuOption("8", "🚪", "Exit", "See you later!"),
        ]
        
        # Filter visible options
        visible_options = [opt for opt in options if opt.visible]
        
        # Display options
        for i, option in enumerate(visible_options):
            style = "bold cyan" if i == self.current_selection else "dim"
            self.console.print(
                f"  [{style}]{option.icon} {option.title}[/]".ljust(30) + 
                f"[dim]{option.description}[/]"
            )
            
        self.console.print()
        self.console.print("[dim]Use ↑/↓ arrows to navigate, Enter to select, or press the number key[/]")
        
        if has_config:
            self.console.print()
            self.console.print("[dim][Current Profile: work-laptop] [Last Updated: 2 days ago][/]")
            
        # Get user input
        try:
            choice = Prompt.ask("\n[bold]Enter your choice[/]", 
                               choices=[opt.key for opt in visible_options])
            return choice
        except (EOFError, KeyboardInterrupt):
            # Fallback to simple input
            self.console.print()
            try:
                valid_choices = [opt.key for opt in visible_options]
                choice = input(f"Enter your choice [{'/'.join(valid_choices)}]: ").strip()
                if choice not in valid_choices:
                    return "8"  # Default to exit
                return choice
            except (EOFError, KeyboardInterrupt):
                return "8"
        
    def show_profile_templates(self) -> str:
        """Display profile template selection"""
        self.clear_screen()
        
        header = Panel(
            "[bold]Choose Your Profile[/]\n"
            "[dim]Select a pre-configured profile or customize your own[/]\n\n"
            "[yellow]Options:[/]\n"
            "• [bold]1-5[/]: Choose a pre-configured profile with common tools\n"
            "• [bold]C[/]: Custom configuration - pick exactly what you want",
            box=box.ROUNDED,
            border_style="bright_blue"
        )
        self.console.print(header)
        self.console.print()
        
        profiles = [
            {
                "key": "1",
                "icon": "👨‍💻",
                "name": "Full-Stack Developer",
                "items": [
                    "VS Code + extensions for web development",
                    "Docker & Docker Compose for containers",
                    "Node.js, Python, Go development environments",
                    "Database clients (pgAdmin, MongoDB Compass)",
                    "API testing tools (Postman, Insomnia)",
                    "Git with advanced aliases and tools",
                    "Terminal enhancements with dev-focused aliases"
                ]
            },
            {
                "key": "2",
                "icon": "🎮",
                "name": "Gaming Station",
                "items": [
                    "Steam, Lutris for game management",
                    "Latest GPU drivers with performance mode",
                    "Discord, TeamSpeak for communication",
                    "OBS Studio for streaming",
                    "Performance monitoring tools",
                    "Game-specific optimizations"
                ]
            },
            {
                "key": "3",
                "icon": "🎨",
                "name": "Creative Professional",
                "items": [
                    "GIMP, Inkscape, Blender for graphics",
                    "Kdenlive, OBS Studio for video",
                    "Audacity, Ardour for audio",
                    "Color calibration tools",
                    "Wacom tablet support",
                    "High-performance graphics drivers"
                ]
            },
            {
                "key": "4",
                "icon": "🔒",
                "name": "Security Fortress",
                "items": [
                    "VPN clients and Tor browser",
                    "Encryption tools (VeraCrypt, GnuPG)",
                    "Password managers with 2FA",
                    "System hardening configurations",
                    "Privacy-focused browser settings",
                    "Secure communication tools"
                ]
            },
            {
                "key": "5",
                "icon": "⚡",
                "name": "Minimal & Fast",
                "items": [
                    "Lightweight desktop environment",
                    "Essential applications only",
                    "Performance optimizations",
                    "Minimal background services",
                    "Fast boot configuration"
                ]
            }
        ]
        
        for profile in profiles:
            # Profile header
            self.console.print(f"[bold]{profile['icon']} {profile['name']}[/]")
            
            # Profile items
            for item in profile['items']:
                self.console.print(f"  [dim]├─ {item}[/]")
            self.console.print()
            
        self.console.print("[bold][C][/]ustom configuration")
        self.console.print()
        
        prompt_text = "\n[yellow]Enter your choice:[/]\n" \
                     "  • [bold]1-5[/] for a pre-configured profile\n" \
                     "  • [bold]C[/] for custom configuration\n\n" \
                     "[bold]Select a profile[/]"
        
        # First try with rich Prompt
        try:
            # Check if we have a valid terminal for rich input
            if sys.stdin.isatty() and sys.stdout.isatty():
                choice = Prompt.ask(
                    prompt_text,
                    choices=["1", "2", "3", "4", "5", "c", "C"],
                    default="c"
                )
                return choice.lower()
            else:
                raise Exception("Not in interactive terminal")
        except:
            # Fallback to simple input
            self.console.print()
            self.console.print("[yellow]Please type your choice and press Enter:[/]")
            self.console.print("  • Type 1, 2, 3, 4, or 5 for a pre-configured profile")
            self.console.print("  • Type C for custom configuration")
            
            # Flush output to ensure prompt is shown
            sys.stdout.flush()
            
            try:
                choice = input("\nYour choice [1/2/3/4/5/c/C]: ").strip()
                if not choice:
                    choice = "c"
                elif choice not in ["1", "2", "3", "4", "5", "c", "C"]:
                    self.console.print("[dim]Invalid choice, defaulting to custom configuration[/]")
                    choice = "c"
                return choice.lower()
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[dim]Selection cancelled, defaulting to custom configuration[/]")
                return "c"
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/]")
                self.console.print("[dim]Defaulting to custom configuration[/]")
                return "c"
        
    def show_section_selection(self) -> List[str]:
        """Interactive section selection with checkboxes"""
        self.clear_screen()
        
        header = Panel(
            "[bold]Choose What to Configure[/]\n"
            "[dim]Select the sections you want to set up[/]",
            box=box.ROUNDED,
            border_style="bright_blue"
        )
        self.console.print(header)
        self.console.print()
        
        sections = [
            ("desktop", "🖥️", "Desktop Environment", "GNOME, KDE, XFCE, and more"),
            ("themes", "🎨", "Themes & Appearance", "Make it beautiful"),
            ("development", "💻", "Development Tools", "Code like a pro"),
            ("applications", "📱", "Applications", "Essential software"),
            ("security", "🔒", "Security & Privacy", "Lock it down"),
            ("performance", "🚀", "Performance Tuning", "Speed things up"),
            ("network", "🌐", "Network & Connectivity", "Stay connected"),
            ("system", "⚙️", "System Preferences", "Fine-tune everything"),
        ]
        
        selected = []
        current = 0
        
        self.console.print("[dim]Press Space to toggle, Enter to continue, Q to go back[/]\n")
        
        # For simplicity in this implementation, we'll use a prompt-based approach
        # In a real implementation, this would be interactive with keyboard events
        
        for key, icon, name, desc in sections:
            checked = Confirm.ask(f"{icon} {name} - {desc}")
            if checked:
                selected.append(key)
                
        return selected
        
    def show_app_customization(self, app_name: str, customizations: Dict[str, Any]):
        """Display application customization options with explanations"""
        self.clear_screen()
        
        panel = Panel(
            f"[bold]{app_name} Customization[/]\n"
            f"[dim]{customizations.get('description', '')}[/]",
            box=box.ROUNDED,
            border_style="bright_blue"
        )
        self.console.print(panel)
        self.console.print()
        
        # Show what will be configured
        if "features" in customizations:
            self.console.print("[bold]📦 Features to Configure:[/]")
            for feature in customizations["features"]:
                self.console.print(f"  ✓ {feature}")
            self.console.print()
            
        # Handle system preferences specially with organized sections
        if app_name == "System Preferences":
            self._show_system_preferences_overview(customizations)
        else:
            # Regular application customization display
            if "settings" in customizations:
                self.console.print("[bold]⚙️ Settings:[/]")
                for setting, value in customizations["settings"].items():
                    self.console.print(f"  • {setting}: {value}")
                self.console.print()
                
            if "extensions" in customizations:
                self.console.print("[bold]🧩 Extensions/Plugins:[/]")
                for ext in customizations["extensions"]:
                    self.console.print(f"  ✓ {ext}")
                self.console.print()
                
            # Show shortcuts if available
            if "shortcuts" in customizations:
                self.console.print("[bold]⌨️ Keyboard Shortcuts:[/]")
                # Show only first 8 shortcuts to avoid overwhelming
                shortcuts_items = list(customizations["shortcuts"].items())[:8]
                for shortcut, action in shortcuts_items:
                    self.console.print(f"  • {shortcut}: {action}")
                if len(customizations["shortcuts"]) > 8:
                    self.console.print(f"  ... and {len(customizations['shortcuts']) - 8} more shortcuts")
                self.console.print()
        
        # Show preview if available
        if "preview" in customizations:
            preview_panel = Panel(
                customizations["preview"],
                title="Preview",
                box=box.ROUNDED,
                border_style="dim"
            )
            self.console.print(preview_panel)
            self.console.print()
            
        # Get user choice
        options_text = (
            "[bold]Choose an option:[/]\n"
            "[green]A[/]ccept All - Apply all customizations\n"
            "[yellow]C[/]ustomize - Pick specific settings\n"
            "[red]S[/]kip - Don't customize this application\n"
            "[blue]?[/] - Learn more about these customizations"
        )
        self.console.print(options_text)
        
        try:
            choice = Prompt.ask(
                "[bold]Your choice[/]",
                choices=["a", "c", "s", "?"],
                default="a"
            )
        except (EOFError, KeyboardInterrupt):
            # Fallback to simple input
            self.console.print()
            try:
                choice = input("Your choice [a/c/s/?]: ").strip().lower()
                if choice not in ["a", "c", "s", "?"]:
                    choice = "a"
            except (EOFError, KeyboardInterrupt):
                choice = "s"  # Skip on error
        
        if choice == "?":
            self.show_customization_help(app_name, customizations)
            return self.show_app_customization(app_name, customizations)
        
        return choice
    
    def _show_system_preferences_overview(self, customizations: Dict[str, Any]):
        """Show organized overview of system preferences"""
        categories = [
            ("mouse_touchpad", "🖱️ Mouse & Touchpad", "Pointer speed, scrolling, gestures"),
            ("keyboard", "⌨️ Keyboard", "Key repeat, shortcuts, accessibility"),
            ("clipboard", "📋 Clipboard", "History, management, behavior"),
            ("workspaces", "🖥️ Workspaces", "Virtual desktops, switching, layout"),
            ("notifications", "🔔 Notifications", "Alerts, timing, do-not-disturb"),
            ("window_management", "🪟 Window Management", "Tiling, focus, switching"),
            ("display", "🖼️ Display", "Scaling, brightness, night light"),
            ("fonts", "🔤 Fonts", "Interface, sizes, rendering"),
            ("dock_panel", "📌 Dock & Panel", "Position, behavior, appearance"),
            ("power", "🔋 Power", "Battery, suspend, brightness"),
            ("privacy", "🔒 Privacy", "History, tracking, permissions"),
            ("accessibility", "♿ Accessibility", "Screen reader, magnifier, assistance")
        ]
        
        self.console.print("[bold]🎛️ System Configuration Categories:[/]")
        for key, title, description in categories:
            if key in customizations:
                category_data = customizations[key]
                settings_count = len(category_data) if isinstance(category_data, dict) else 0
                self.console.print(f"  {title}")
                self.console.print(f"    [dim]{description} ({settings_count} settings)[/]")
        self.console.print()
        
        # Show sample of keyboard shortcuts
        if "shortcuts" in customizations:
            self.console.print("[bold]⌨️ Key Shortcuts (sample):[/]")
            shortcuts_items = list(customizations["shortcuts"].items())[:6]
            for shortcut, action in shortcuts_items:
                self.console.print(f"  • {shortcut}: {action}")
            total_shortcuts = len(customizations["shortcuts"])
            if total_shortcuts > 6:
                self.console.print(f"  ... and {total_shortcuts - 6} more shortcuts")
            self.console.print()
    
    def show_customization_help(self, app_name: str, customizations: Dict[str, Any]):
        """Show detailed help about customizations"""
        self.clear_screen()
        
        help_panel = Panel(
            f"[bold]Why These {app_name} Customizations?[/]",
            box=box.ROUNDED,
            border_style="bright_blue"
        )
        self.console.print(help_panel)
        self.console.print()
        
        if "help" in customizations:
            self.console.print(customizations["help"])
        else:
            self.console.print(f"These customizations are designed to provide a better out-of-the-box experience for {app_name}.")
            self.console.print("They include common settings that developers and users typically configure manually.")
        
        self.console.print()
        self.console.print("[dim]Press Enter to continue...[/]")
        input()
    
    def show_detailed_customization(self, app_name: str, customizations: Dict[str, Any]):
        """Show detailed customization options for user to pick and choose"""
        self.clear_screen()
        
        panel = Panel(
            f"[bold]Customize {app_name} Settings[/]",
            box=box.ROUNDED,
            border_style="bright_blue"
        )
        self.console.print(panel)
        self.console.print()
        
        selected_customizations = {}
        
        # Handle system preferences specially
        if app_name == "System Preferences":
            return self._show_system_detailed_customization(customizations)
        
        # Let user choose features
        if "features" in customizations:
            self.console.print("[bold]📦 Select Features:[/]")
            selected_features = []
            for feature in customizations["features"]:
                if Confirm.ask(f"  Enable: {feature}"):
                    selected_features.append(feature)
            selected_customizations["features"] = selected_features
            self.console.print()
        
        # Let user choose settings
        if "settings" in customizations:
            self.console.print("[bold]⚙️ Configure Settings:[/]")
            selected_settings = {}
            for setting, default_value in customizations["settings"].items():
                if Confirm.ask(f"  {setting} (default: {default_value})"):
                    selected_settings[setting] = default_value
            selected_customizations["settings"] = selected_settings
            self.console.print()
        
        # Let user choose extensions
        if "extensions" in customizations:
            self.console.print("[bold]🧩 Select Extensions:[/]")
            selected_extensions = []
            for ext in customizations["extensions"]:
                if Confirm.ask(f"  Install: {ext}"):
                    selected_extensions.append(ext)
            selected_customizations["extensions"] = selected_extensions
            self.console.print()
        
        return selected_customizations
    
    def _show_system_detailed_customization(self, customizations: Dict[str, Any]):
        """Show detailed system customization with categories"""
        selected_customizations = {}
        
        categories = [
            ("mouse_touchpad", "🖱️ Mouse & Touchpad"),
            ("keyboard", "⌨️ Keyboard"),
            ("clipboard", "📋 Clipboard"),
            ("workspaces", "🖥️ Workspaces"),
            ("notifications", "🔔 Notifications"),
            ("window_management", "🪟 Window Management"),
            ("display", "🖼️ Display"),
            ("fonts", "🔤 Fonts"),
            ("dock_panel", "📌 Dock & Panel"),
            ("power", "🔋 Power"),
            ("privacy", "🔒 Privacy"),
            ("accessibility", "♿ Accessibility")
        ]
        
        self.console.print("[bold]Select system categories to configure:[/]")
        self.console.print("[dim]Choose which areas you want to customize[/]")
        self.console.print()
        
        for key, title in categories:
            if key in customizations:
                category_data = customizations[key]
                settings_count = len(category_data) if isinstance(category_data, dict) else 0
                
                if Confirm.ask(f"  {title} ({settings_count} settings)"):
                    selected_customizations[key] = category_data
        
        # Always include features and help
        if "features" in customizations:
            selected_customizations["features"] = customizations["features"]
        if "help" in customizations:
            selected_customizations["help"] = customizations["help"]
        
        return selected_customizations
        
    def show_progress(self, task_name: str, steps: List[str]):
        """Display progress for ongoing operations"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            task = progress.add_task(f"[cyan]{task_name}", total=len(steps))
            
            for step in steps:
                progress.update(task, advance=1, description=f"[cyan]{step}")
                time.sleep(1)  # Simulate work
                
    def show_success_screen(self, stats: Dict[str, Any]):
        """Display success celebration screen"""
        self.clear_screen()
        
        success_text = """
[bold green]╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                        🎉 Setup Complete! 🎉                     ║
║                                                                  ║
║                    Your Ubuntu is now awesome!                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝[/]
        """
        
        self.console.print(success_text)
        self.console.print()
        
        # Configuration summary
        self.console.print("[bold]What we configured:[/]")
        for item in stats.get("configured", []):
            self.console.print(f"  ✨ {item}")
        self.console.print()
        
        # Quick stats
        self.console.print("[bold]Quick Stats:[/]")
        self.console.print(f"  📦 Packages Installed: {stats.get('packages', 0)}")
        self.console.print(f"  ⚡ Boot Time Improved: ~{stats.get('boot_improvement', '0')}s")
        self.console.print(f"  🔒 Security Score: {stats.get('security_score', 'A+')}")
        self.console.print()
        
        # Next steps
        self.console.print("[bold]Next Steps:[/]")
        self.console.print("  • Restart to apply all changes (recommended)")
        self.console.print("  • Check out your new terminal with Ctrl+Alt+T")
        self.console.print("  • Launch VS Code to see your new theme")
        self.console.print()
        
        try:
            choice = Prompt.ask(
                "[bold]What would you like to do?[/]",
                choices=["r", "l", "v"],
                default="r"
            )
        except (EOFError, KeyboardInterrupt):
            # Fallback to simple input
            self.console.print()
            try:
                choice = input("What would you like to do? [r/l/v]: ").strip().lower()
                if choice not in ["r", "l", "v"]:
                    choice = "r"
            except (EOFError, KeyboardInterrupt):
                choice = "v"  # View log on error
        
        return choice


# Configuration dataclasses for app customization
@dataclass
class SliderConfig:
    """Configuration for slider inputs"""
    min_value: int
    max_value: int
    current_value: int
    step: int = 1
    unit: str = ""


@dataclass
class DropdownConfig:
    """Configuration for dropdown selections"""
    options: List[Tuple[str, str]]
    current_value: str
    allow_custom: bool = False


@dataclass 
class MultiSelectConfig:
    """Configuration for multi-select options"""
    options: List[Tuple[str, str, bool]]
    max_selections: Optional[int] = None
    min_selections: int = 0


# Helper functions for the main script
def create_menu_ui():
    """Factory function to create MenuUI instance"""
    return MenuUI()