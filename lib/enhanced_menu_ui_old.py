#!/usr/bin/env python3
"""
Enhanced Professional menu UI system for Ubootu with full hierarchical navigation
This replaces both the simple menu_ui.py and the complex curses-based TUI system
"""

import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from rich import box
    from rich.align import Align
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("ERROR: Rich library not found. Please install with: sudo apt install python3-rich")
    sys.exit(1)


@dataclass
class MenuItem:
    """Represents a menu item with all necessary properties"""
    id: str
    label: str
    description: str
    parent: Optional[str] = None
    children: List[str] = None
    is_category: bool = False
    is_configurable: bool = False
    default: bool = False
    selected: bool = False
    config_type: str = "slider"
    config_value: any = None
    config_range: tuple = (1, 10)
    config_unit: str = ""
    config_options: Optional[List[tuple]] = None
    ansible_var: Optional[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class EnhancedMenuUI:
    """Professional hierarchical menu UI system with Rich formatting"""

    def __init__(self):
        self.console = Console()
        
        # Navigation state
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.breadcrumb_stack = ["root"]
        
        # Data structures
        self.menu_items: Dict[str, MenuItem] = {}
        self.selected_items: Set[str] = set()
        
        # UI state
        self.cancelled = False
        
        # Build menu structure
        self._build_menu_structure()
        
        # Apply defaults
        self._apply_defaults()

    def _build_menu_structure(self):
        """Build the complete hierarchical menu structure"""
        
        # Create root menu
        self.menu_items["root"] = MenuItem(
            "root",
            "🚀 Ubootu - Ubuntu System Setup",
            "Navigate: ↑↓ arrows, SPACE select, ENTER enter     |     ▶▶▶ PRESS F1 FOR ACTIONS MENU TO START INSTALLATION ◀◀◀",
            is_category=True,
            children=["development", "desktop", "applications", "security", "system"]
        )
        
        # Build each section
        self._build_development_menu()
        self._build_desktop_menu()
        self._build_applications_menu()
        self._build_security_menu()
        self._build_system_menu()
        
        # Add actions menu
        self.menu_items["actions"] = MenuItem(
            "actions",
            "Actions",
            "Installation and configuration actions",
            parent="root",
            is_category=True,
            children=["action-install", "action-save", "action-reset", "action-exit"]
        )
        
        # Action items
        self.menu_items["action-install"] = MenuItem(
            "action-install",
            "🚀 Start Installation", 
            "Apply settings and install selected software",
            parent="actions"
        )
        
        self.menu_items["action-save"] = MenuItem(
            "action-save",
            "💾 Save Configuration",
            "Save current selections without installing", 
            parent="actions"
        )
        
        self.menu_items["action-reset"] = MenuItem(
            "action-reset",
            "🔄 Reset Configuration",
            "Clear all selections and return to defaults",
            parent="actions"
        )
        
        self.menu_items["action-exit"] = MenuItem(
            "action-exit",
            "❌ Exit without Saving",
            "Exit the configuration tool without saving",
            parent="actions"
        )

    def _build_development_menu(self):
        """Build the development tools menu section"""
        # Main development category
        self.menu_items["development"] = MenuItem(
            "development",
            "💻 Development Tools",
            "Programming languages, IDEs, debugging tools",
            parent="root",
            is_category=True,
            children=["dev-ides", "dev-languages", "dev-tools", "dev-containers", "dev-cli-modern"]
        )
        
        # Development subcategories
        self._build_ides_menu()
        self._build_languages_menu()
        self._build_dev_tools_menu()
        self._build_containers_menu()
        self._build_modern_cli_menu()

    def _build_ides_menu(self):
        """Build IDEs and editors menu"""
        self.menu_items["dev-ides"] = MenuItem(
            "dev-ides",
            "🛠️ IDEs & Editors",
            "Integrated development environments",
            parent="development",
            is_category=True,
            children=["vscode", "intellij-idea", "pycharm", "webstorm", "sublime", "vim", "emacs"]
        )
        
        # Individual IDE items
        ides = [
            ("vscode", "Visual Studio Code", "Microsoft's popular code editor", True),
            ("intellij-idea", "IntelliJ IDEA", "JetBrains Java IDE", True),
            ("pycharm", "PyCharm", "JetBrains Python IDE", True),
            ("webstorm", "WebStorm", "JetBrains JavaScript IDE", False),
            ("sublime", "Sublime Text", "Sophisticated text editor", False),
            ("vim", "Vim/NeoVim", "Terminal-based text editor", False),
            ("emacs", "Emacs", "Extensible text editor", False),
        ]
        
        for ide_id, label, desc, default in ides:
            self.menu_items[ide_id] = MenuItem(
                ide_id, label, desc,
                parent="dev-ides",
                default=default
            )

    def _build_languages_menu(self):
        """Build programming languages menu"""
        self.menu_items["dev-languages"] = MenuItem(
            "dev-languages",
            "🐍 Programming Languages",
            "Runtimes, compilers, interpreters",
            parent="development",
            is_category=True,
            children=["python", "nodejs", "java", "go", "rust", "cpp", "php", "ruby"]
        )
        
        languages = [
            ("python", "Python", "Python runtime and pip", True),
            ("nodejs", "Node.js", "JavaScript runtime", True),
            ("java", "Java", "Java Development Kit", True),
            ("go", "Go", "Go programming language", False),
            ("rust", "Rust", "Rust programming language", False),
            ("cpp", "C/C++", "GCC compiler and build tools", False),
            ("php", "PHP", "PHP interpreter", False),
            ("ruby", "Ruby", "Ruby interpreter", False),
        ]
        
        for lang_id, label, desc, default in languages:
            self.menu_items[lang_id] = MenuItem(
                lang_id, label, desc,
                parent="dev-languages",
                default=default
            )

    def _build_dev_tools_menu(self):
        """Build development tools menu"""
        self.menu_items["dev-tools"] = MenuItem(
            "dev-tools",
            "🔧 Development Tools",
            "Debugging, profiling, testing tools",
            parent="development",
            is_category=True,
            children=["git", "docker", "postman", "mysql-workbench", "redis-cli", "curl"]
        )
        
        tools = [
            ("git", "Git", "Version control system", True),
            ("docker", "Docker", "Container platform", True),
            ("postman", "Postman", "API development tool", False),
            ("mysql-workbench", "MySQL Workbench", "Database administration tool", False),
            ("redis-cli", "Redis CLI", "Redis command line interface", False),
            ("curl", "curl", "HTTP client tool", True),
        ]
        
        for tool_id, label, desc, default in tools:
            self.menu_items[tool_id] = MenuItem(
                tool_id, label, desc,
                parent="dev-tools",
                default=default
            )

    def _build_containers_menu(self):
        """Build containers and DevOps menu"""
        self.menu_items["dev-containers"] = MenuItem(
            "dev-containers",
            "🐳 Containers & DevOps",
            "Container platforms and orchestration",
            parent="development",
            is_category=True,
            children=["docker-desktop", "kubernetes", "terraform-iac", "ansible"]
        )
        
        containers = [
            ("docker-desktop", "Docker Desktop", "Docker containerization platform with GUI", True),
            ("kubernetes", "Kubernetes Tools", "Container orchestration tools (kubectl, minikube)", False),
            ("terraform-iac", "Terraform", "Infrastructure as code tool", False),
            ("ansible", "Ansible", "Configuration management and automation", False),
        ]
        
        for container_id, label, desc, default in containers:
            self.menu_items[container_id] = MenuItem(
                container_id, label, desc,
                parent="dev-containers",
                default=default
            )

    def _build_modern_cli_menu(self):
        """Build modern CLI tools menu"""
        self.menu_items["dev-cli-modern"] = MenuItem(
            "dev-cli-modern",
            "🚀 Modern CLI Tools",
            "Next-gen command line utilities",
            parent="development",
            is_category=True,
            children=["bat", "ripgrep", "fd", "htop", "fzf", "tmux"]
        )
        
        cli_tools = [
            ("bat", "bat", "Cat clone with syntax highlighting", True),
            ("ripgrep", "ripgrep (rg)", "Extremely fast grep alternative", True),
            ("fd", "fd", "Simple, fast alternative to find", True),
            ("htop", "htop", "Interactive process viewer", True),
            ("fzf", "fzf", "Fuzzy finder for terminal", True),
            ("tmux", "tmux", "Terminal multiplexer", True),
        ]
        
        for cli_id, label, desc, default in cli_tools:
            self.menu_items[cli_id] = MenuItem(
                cli_id, label, desc,
                parent="dev-cli-modern",
                default=default
            )

    def _build_desktop_menu(self):
        """Build desktop environment menu"""
        self.menu_items["desktop"] = MenuItem(
            "desktop",
            "🖥️ Desktop Environment",
            "Desktop environments, themes, and appearance",
            parent="root",
            is_category=True,
            children=["desktop-environments", "themes", "dock-config"]
        )
        
        # Desktop environment subcategory
        self.menu_items["desktop-environments"] = MenuItem(
            "desktop-environments",
            "🏠 Desktop Environments",
            "Choose your desktop environment",
            parent="desktop",
            is_category=True,
            children=["gnome", "kde", "xfce", "mate", "cinnamon"]
        )
        
        desktops = [
            ("gnome", "GNOME", "Modern and clean desktop", True),
            ("kde", "KDE Plasma", "Highly customizable desktop", False),
            ("xfce", "XFCE", "Lightweight desktop", False),
            ("mate", "MATE", "Traditional desktop", False),
            ("cinnamon", "Cinnamon", "Modern traditional desktop", False),
        ]
        
        for desktop_id, label, desc, default in desktops:
            self.menu_items[desktop_id] = MenuItem(
                desktop_id, label, desc,
                parent="desktop-environments",
                default=default
            )

        # Themes subcategory
        self.menu_items["themes"] = MenuItem(
            "themes",
            "🎨 Themes & Appearance",
            "Icons, themes, fonts, and visual customization",
            parent="desktop",
            is_category=True,
            children=["theme-dark", "theme-icons", "theme-fonts"]
        )
        
        themes = [
            ("theme-dark", "Dark Theme", "Enable dark mode system-wide", True),
            ("theme-icons", "Beautiful Icons", "Install modern icon themes", True),
            ("theme-fonts", "Better Fonts", "Install and configure better fonts", True),
        ]
        
        for theme_id, label, desc, default in themes:
            self.menu_items[theme_id] = MenuItem(
                theme_id, label, desc,
                parent="themes",
                default=default
            )

    def _build_applications_menu(self):
        """Build applications menu"""
        self.menu_items["applications"] = MenuItem(
            "applications",
            "📱 Applications",
            "Essential and productivity applications",
            parent="root",
            is_category=True,
            children=["app-browsers", "app-media", "app-office", "app-communication"]
        )
        
        # Browser subcategory
        self.menu_items["app-browsers"] = MenuItem(
            "app-browsers",
            "🌐 Web Browsers",
            "Web browsing applications",
            parent="applications",
            is_category=True,
            children=["firefox", "chrome", "brave", "edge"]
        )
        
        browsers = [
            ("firefox", "Firefox", "Mozilla Firefox browser", True),
            ("chrome", "Google Chrome", "Google Chrome browser", False),
            ("brave", "Brave", "Privacy-focused browser", False),
            ("edge", "Microsoft Edge", "Microsoft Edge browser", False),
        ]
        
        for browser_id, label, desc, default in browsers:
            self.menu_items[browser_id] = MenuItem(
                browser_id, label, desc,
                parent="app-browsers",
                default=default
            )

    def _build_security_menu(self):
        """Build security tools menu"""
        self.menu_items["security"] = MenuItem(
            "security",
            "🔒 Security & Privacy",
            "Security tools, privacy settings, and hardening",
            parent="root",
            is_category=True,
            children=["security-firewall", "security-tools", "security-privacy"]
        )
        
        # Security subcategories
        self.menu_items["security-firewall"] = MenuItem(
            "security-firewall",
            "🛡️ Firewall & Network Security",
            "Network security and firewall configuration",
            parent="security",
            is_category=True,
            children=["ufw", "fail2ban"]
        )
        
        security_items = [
            ("ufw", "UFW Firewall", "Enable and configure firewall", True),
            ("fail2ban", "Fail2ban", "Intrusion prevention system", True),
        ]
        
        for sec_id, label, desc, default in security_items:
            self.menu_items[sec_id] = MenuItem(
                sec_id, label, desc,
                parent="security-firewall",
                default=default
            )

    def _build_system_menu(self):
        """Build system configuration menu"""
        self.menu_items["system"] = MenuItem(
            "system",
            "⚙️ System Configuration",
            "System settings, performance, and tweaks",
            parent="root",
            is_category=True,
            children=["system-performance", "system-updates", "system-tweaks"]
        )
        
        # System subcategories
        self.menu_items["system-performance"] = MenuItem(
            "system-performance",
            "🚀 Performance Optimization",
            "System performance and resource management",
            parent="system",
            is_category=True,
            children=["swappiness", "preload"]
        )
        
        # Add configurable swappiness item
        self.menu_items["swappiness"] = MenuItem(
            "swappiness",
            "Memory Swappiness",
            "How aggressively system uses swap space (0-100)",
            parent="system-performance",
            is_configurable=True,
            config_type="slider",
            config_value=10,
            config_range=(0, 100),
            config_unit="%"
        )
        
        system_items = [
            ("preload", "Preload", "Preload frequently used applications", True),
        ]
        
        for sys_id, label, desc, default in system_items:
            self.menu_items[sys_id] = MenuItem(
                sys_id, label, desc,
                parent="system-performance",
                default=default
            )

    def _apply_defaults(self):
        """Apply default selections"""
        for item in self.menu_items.values():
            if item.default and not item.is_category:
                self.selected_items.add(item.id)
                item.selected = True

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")

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
            console=self.console,
        ) as progress:
            task = progress.add_task("[cyan]Loading awesomeness...", total=100)

            loading_messages = [
                "Initializing Ubuntu magic...",
                "Preparing configuration wizardry...",
                "Loading customization options...",
                "Getting everything ready...",
            ]

            for i, message in enumerate(loading_messages):
                progress.update(task, advance=25, description=f"[cyan]{message}")
                time.sleep(0.5)

        time.sleep(0.5)

    def get_current_menu_items(self) -> List[MenuItem]:
        """Get items for the current menu"""
        current = self.menu_items.get(self.current_menu)
        if not current or not current.children:
            return []
        
        return [self.menu_items[child_id] for child_id in current.children 
                if child_id in self.menu_items]

    def get_selection_indicator(self, item: MenuItem) -> str:
        """Get selection indicator for menu item"""
        if item.is_category:
            # Check children selection status
            children = [self.menu_items[child_id] for child_id in item.children 
                       if child_id in self.menu_items and not self.menu_items[child_id].is_category]
            if not children:
                return "○"  # No selectable children
            
            selected_count = sum(1 for child in children if child.selected)
            if selected_count == 0:
                return "○"  # None selected
            elif selected_count == len(children):
                return "●"  # All selected
            else:
                return "◐"  # Partial selection
        else:
            return "✓" if item.selected else " "

    def run_hierarchical_tui(self) -> int:
        """Run the main hierarchical TUI"""
        try:
            self.show_splash_screen()
            time.sleep(1)
            
            while True:
                self.clear_screen()
                
                # Display header
                header = Panel(
                    Align.center(
                        f"[bold]🚀 Ubootu Configuration Tool 🚀[/]\n"
                        f"[dim]Current section: {self.menu_items[self.current_menu].label}[/]",
                        vertical="middle",
                    ),
                    box=box.DOUBLE_EDGE,
                    border_style="bright_blue",
                    padding=(1, 2),
                )
                self.console.print(header)
                self.console.print()
                
                # Display breadcrumb
                breadcrumb_text = " > ".join([
                    self.menu_items[item_id].label.replace("🚀 ", "").replace("💻 ", "").replace("🖥️ ", "").replace("📱 ", "").replace("🔒 ", "").replace("⚙️ ", "")
                    for item_id in self.breadcrumb_stack
                ])
                self.console.print(f"[dim]Navigation: {breadcrumb_text}[/]")
                self.console.print()
                
                # Get current menu items
                menu_items = self.get_current_menu_items()
                
                if not menu_items:
                    self.console.print("[red]No items in current menu[/]")
                    break
                
                # Display menu items
                table = Table(show_header=False, box=None, padding=(0, 1))
                table.add_column("Sel", width=3)
                table.add_column("Item", ratio=1)
                table.add_column("Description", ratio=2)
                
                for i, item in enumerate(menu_items):
                    # Highlight current item
                    style = "bold cyan" if i == self.current_item else ""
                    
                    # Selection indicator
                    indicator = self.get_selection_indicator(item)
                    
                    # Item text
                    item_text = f"[{indicator}] {item.label}"
                    if item.is_configurable:
                        item_text += f" ({item.config_value}{item.config_unit})"
                    
                    table.add_row(
                        f"[{style}]{indicator}[/]",
                        f"[{style}]{item.label}[/]",
                        f"[{style} dim]{item.description}[/]"
                    )
                
                self.console.print(table)
                self.console.print()
                
                # Instructions
                instructions = (
                    "[dim]Navigation: ↑/↓ arrows, ← back, → enter/forward\n"
                    "Selection: SPACE toggle, A all, N none\n"
                    "Actions: S save, R run, Q quit[/]"
                )
                self.console.print(instructions)
                
                # Show selection summary
                selected_count = len(self.selected_items)
                self.console.print(f"\n[green]Selected items: {selected_count}[/]")
                
                # Get user input
                try:
                    choice = input("\nYour choice: ").strip().lower()
                    
                    if choice in ['q', 'quit', 'exit']:
                        break
                    elif choice in ['↑', 'up', 'k']:
                        self.current_item = max(0, self.current_item - 1)
                    elif choice in ['↓', 'down', 'j']:
                        self.current_item = min(len(menu_items) - 1, self.current_item + 1)
                    elif choice in ['←', 'back', 'b'] and len(self.breadcrumb_stack) > 1:
                        self.breadcrumb_stack.pop()
                        self.current_menu = self.breadcrumb_stack[-1]
                        self.current_item = 0
                    elif choice in ['→', 'enter', 'forward', ''] and self.current_item < len(menu_items):
                        current_menu_item = menu_items[self.current_item]
                        if current_menu_item.is_category:
                            # Navigate into category
                            self.current_menu = current_menu_item.id
                            self.breadcrumb_stack.append(current_menu_item.id)
                            self.current_item = 0
                        elif current_menu_item.is_configurable:
                            # Configure item
                            self._configure_item(current_menu_item)
                        else:
                            # Toggle selection
                            self._toggle_selection(current_menu_item)
                    elif choice == ' ' and self.current_item < len(menu_items):
                        # Toggle selection
                        current_menu_item = menu_items[self.current_item]
                        self._toggle_selection(current_menu_item)
                    elif choice == 's':
                        # Save configuration
                        self._save_configuration()
                    elif choice == 'r':
                        # Run installation
                        return self._run_installation()
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/]")
                    input("Press Enter to continue...")
            
            return 0 if not self.cancelled else 1
            
        except Exception as e:
            self.console.print(f"[red]Fatal error: {e}[/]")
            return 1

    def _toggle_selection(self, item: MenuItem):
        """Toggle selection of an item"""
        if item.is_category:
            # Toggle all children
            children = [self.menu_items[child_id] for child_id in item.children 
                       if child_id in self.menu_items and not self.menu_items[child_id].is_category]
            
            # Check if all are selected
            all_selected = all(child.selected for child in children)
            
            # Toggle all to opposite state
            for child in children:
                if all_selected:
                    child.selected = False
                    self.selected_items.discard(child.id)
                else:
                    child.selected = True
                    self.selected_items.add(child.id)
        else:
            # Toggle individual item
            if item.selected:
                item.selected = False
                self.selected_items.discard(item.id)
            else:
                item.selected = True
                self.selected_items.add(item.id)

    def _configure_item(self, item: MenuItem):
        """Configure a configurable item"""
        self.console.print(f"\n[bold]Configure {item.label}[/]")
        self.console.print(f"[dim]{item.description}[/]")
        
        if item.config_type == "slider":
            min_val, max_val = item.config_range
            current = item.config_value
            
            self.console.print(f"Current value: {current}{item.config_unit} (range: {min_val}-{max_val})")
            
            try:
                new_value = input(f"Enter new value [{min_val}-{max_val}]: ").strip()
                if new_value:
                    new_value = int(new_value)
                    if min_val <= new_value <= max_val:
                        item.config_value = new_value
                        self.console.print(f"[green]Updated to {new_value}{item.config_unit}[/]")
                    else:
                        self.console.print(f"[red]Value must be between {min_val} and {max_val}[/]")
                        
                input("Press Enter to continue...")
            except ValueError:
                self.console.print("[red]Invalid number[/]")
                input("Press Enter to continue...")

    def _save_configuration(self):
        """Save current configuration to file"""
        config_data = {
            'metadata': {
                'version': '1.0',
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'selected_items': list(self.selected_items),
            'configurable_items': {},
            'ansible_variables': {}
        }
        
        # Add configurable items
        for item in self.menu_items.values():
            if item.is_configurable and item.config_value is not None:
                config_data['configurable_items'][item.id] = {
                    'id': item.id,
                    'value': item.config_value
                }
        
        try:
            import yaml
            with open('config.yml', 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            
            self.console.print("[green]Configuration saved to config.yml[/]")
            input("Press Enter to continue...")
        except ImportError:
            self.console.print("[red]PyYAML not found. Cannot save configuration.[/]")
            input("Press Enter to continue...")
        except Exception as e:
            self.console.print(f"[red]Error saving configuration: {e}[/]")
            input("Press Enter to continue...")

    def _run_installation(self) -> int:
        """Run the installation process"""
        self.console.print("\n[bold green]🚀 Starting Installation Process[/]")
        
        if not self.selected_items:
            self.console.print("[yellow]No items selected for installation.[/]")
            input("Press Enter to continue...")
            return 0
        
        # Show what will be installed
        self.console.print(f"\n[bold]Selected items ({len(self.selected_items)}):[/]")
        for item_id in sorted(self.selected_items):
            if item_id in self.menu_items:
                item = self.menu_items[item_id]
                self.console.print(f"  • {item.label}")
        
        # Confirm installation
        try:
            confirm = Confirm.ask("\nProceed with installation?")
            if not confirm:
                return 0
        except KeyboardInterrupt:
            return 1
        
        # Save configuration first
        self._save_configuration()
        
        # Show success message
        self.console.print("\n[bold green]✅ Configuration saved successfully![/]")
        self.console.print("[dim]You can now run the Ansible playbook to apply changes.[/]")
        
        input("Press Enter to exit...")
        return 0


def create_enhanced_menu_ui():
    """Factory function to create EnhancedMenuUI instance"""
    return EnhancedMenuUI()


def run_tui(selected_sections=None):
    """Run the enhanced TUI"""
    ui = EnhancedMenuUI()
    return ui.run_hierarchical_tui()


def main():
    """Main entry point"""
    import sys
    
    # Check for help flag
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Ubootu Configuration Tool")
        print("Usage: enhanced_menu_ui.py [sections...]")
        print("\nAvailable sections:")
        print("  development - Development tools and languages")
        print("  desktop     - Desktop environments and themes")
        print("  applications - User applications")
        print("  security    - Security tools and hardening")
        print("  system      - System configuration")
        sys.exit(0)
    
    # Parse command line arguments for section selection
    selected_sections = None
    if len(sys.argv) > 1:
        args = [arg for arg in sys.argv[1:] if arg not in ["--help", "-h"]]
        if args:
            selected_sections = args
    
    # Run the TUI
    try:
        exit_code = run_tui(selected_sections)
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nError: Failed to run TUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()