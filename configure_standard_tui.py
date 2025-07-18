#!/usr/bin/env python3
"""
Ubootu - The Ultimate Ubuntu Experience Engine
Hierarchical TUI with sexy design, optimized for professional desktop configuration
"""

import sys
import os
import yaml
import curses
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

@dataclass
class MenuItem:
    """Menu item"""
    id: str
    label: str
    description: str
    parent: Optional[str] = None
    children: Optional[List[str]] = None
    selected: bool = False
    default: bool = False
    is_category: bool = False
    is_configurable: bool = False  # True if this item needs configuration
    config_type: str = ""  # "slider", "dropdown", "text", etc.
    config_range: Tuple[int, int] = (1, 10)  # For sliders: (min, max)
    config_value: int = 5  # Current value for configurable items
    config_unit: str = ""  # Unit for display (e.g., "seconds", "%", "px")

class HierarchicalTUI:
    """Hierarchical TUI interface optimized for 80x24 screens"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu_items = self._build_menu_structure()
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.selected_items = set()
        self.breadcrumb_stack = []
        self.cancelled = False
        
        # Get terminal dimensions
        height, width = self.stdscr.getmaxyx()
        if height < 24 or width < 80:
            # Terminal too small, but continue anyway
            pass
        
        # NO COLORS - Monochrome interface only
        # All text will be default terminal colors (white on black)
        # Selected items will use reverse video
        pass
        
        # Apply defaults
        for item in self.menu_items.values():
            if item.default:
                item.selected = True
                self.selected_items.add(item.id)
        
        # Setup screen safely
        try:
            curses.curs_set(0)  # Hide cursor
            self.stdscr.keypad(True)
            self.stdscr.timeout(50)  # Reduced timeout for better responsiveness
        except:
            # Some terminals don't support all features
            pass
    
    def _build_menu_structure(self) -> Dict[str, MenuItem]:
        """Build hierarchical menu structure"""
        items = {}
        
        # Root menu
        items["root"] = MenuItem(
            "root", "🚀 Ubootu - Ubuntu System Setup", 
            "Navigate: ↑↓ arrows, SPACE select, ENTER enter     |     ▶▶▶ PRESS F1 FOR ACTIONS MENU TO START INSTALLATION ◀◀◀",
            is_category=True,
            children=["development", "desktop", "applications", "security", "system"]
        )
        
        # Main categories
        items["development"] = MenuItem(
            "development", "Development Tools", 
            "Programming languages, IDEs, debugging tools",
            parent="root", is_category=True,
            children=["dev-ides", "dev-languages", "dev-tools", "dev-containers"]
        )
        
        items["desktop"] = MenuItem(
            "desktop", "Desktop Environment", 
            "Window managers, themes, customization",
            parent="root", is_category=True,
            children=["desktop-env", "desktop-themes", "desktop-settings"]
        )
        
        items["applications"] = MenuItem(
            "applications", "Applications", 
            "Web browsers, media players, productivity tools",
            parent="root", is_category=True,
            children=["app-browsers", "app-media", "app-productivity", "app-communication"]
        )
        
        items["security"] = MenuItem(
            "security", "Security & Privacy", 
            "Firewalls, encryption, privacy tools",
            parent="root", is_category=True,
            children=["security-basic", "security-tools", "security-privacy"]
        )
        
        items["system"] = MenuItem(
            "system", "System Configuration", 
            "Performance, services, hardware",
            parent="root", is_category=True,
            children=["system-perf", "system-services", "system-hardware"]
        )
        
        items["actions"] = MenuItem(
            "actions", "Actions", 
            "Install, save, reset, or exit",
            parent="root", is_category=True,
            children=["action-install", "action-save", "action-reset", "action-exit"]
        )
        
        # Development subcategories
        items["dev-ides"] = MenuItem(
            "dev-ides", "IDEs & Editors", 
            "Integrated development environments",
            parent="development", is_category=True,
            children=["vscode", "intellij", "pycharm", "webstorm", "sublime", "vim", "emacs"]
        )
        
        items["dev-languages"] = MenuItem(
            "dev-languages", "Programming Languages", 
            "Runtimes, compilers, interpreters",
            parent="development", is_category=True,
            children=["python", "nodejs", "java", "go", "rust", "cpp", "php", "ruby"]
        )
        
        items["dev-tools"] = MenuItem(
            "dev-tools", "Development Tools", 
            "Debugging, profiling, testing tools",
            parent="development", is_category=True,
            children=["git", "docker", "postman", "mysql-workbench", "redis-cli", "curl"]
        )
        
        items["dev-containers"] = MenuItem(
            "dev-containers", "Containers & DevOps", 
            "Container platforms and orchestration",
            parent="development", is_category=True,
            children=["docker-desktop", "kubernetes", "terraform", "ansible"]
        )
        
        # Desktop subcategories
        items["desktop-env"] = MenuItem(
            "desktop-env", "Desktop Environment", 
            "Choose your desktop environment",
            parent="desktop", is_category=True,
            children=["gnome", "kde", "xfce", "mate", "cinnamon"]
        )
        
        items["desktop-themes"] = MenuItem(
            "desktop-themes", "Themes & Appearance", 
            "Icons, themes, wallpapers",
            parent="desktop", is_category=True,
            children=["dark-theme", "papirus-icons", "numix-theme", "arc-theme"]
        )
        
        items["desktop-settings"] = MenuItem(
            "desktop-settings", "Desktop Settings", 
            "Mouse, keyboard, display settings",
            parent="desktop", is_category=True,
            children=["mouse-settings", "keyboard-settings", "display-settings", "notifications"]
        )
        
        # Application subcategories
        items["app-browsers"] = MenuItem(
            "app-browsers", "Web Browsers", 
            "Internet browsers",
            parent="applications", is_category=True,
            children=["firefox", "chrome", "chromium", "brave", "opera", "vivaldi", "edge", "waterfox"]
        )
        
        items["app-media"] = MenuItem(
            "app-media", "Media & Entertainment", 
            "Music, video, image viewers",
            parent="applications", is_category=True,
            children=["vlc", "spotify", "gimp", "audacity", "blender"]
        )
        
        items["app-productivity"] = MenuItem(
            "app-productivity", "Productivity", 
            "Office suites, note-taking, planning",
            parent="applications", is_category=True,
            children=["libreoffice", "thunderbird", "notion", "obsidian", "slack"]
        )
        
        items["app-communication"] = MenuItem(
            "app-communication", "Communication", 
            "Chat, video calls, social media",
            parent="applications", is_category=True,
            children=["discord", "teams", "zoom", "telegram", "whatsapp"]
        )
        
        # Security subcategories
        items["security-basic"] = MenuItem(
            "security-basic", "Basic Security", 
            "Firewall, antivirus, updates",
            parent="security", is_category=True,
            children=["ufw-firewall", "clamav", "auto-updates", "fail2ban"]
        )
        
        items["security-tools"] = MenuItem(
            "security-tools", "Security Tools", 
            "Penetration testing, auditing",
            parent="security", is_category=True,
            children=["nmap", "wireshark", "metasploit", "burpsuite", "john"]
        )
        
        items["security-privacy"] = MenuItem(
            "security-privacy", "Privacy Tools", 
            "VPN, encryption, anonymous browsing",
            parent="security", is_category=True,
            children=["tor", "veracrypt", "keepassxc", "protonvpn", "signal"]
        )
        
        # System subcategories
        items["system-perf"] = MenuItem(
            "system-perf", "Performance", 
            "CPU, memory, disk optimization",
            parent="system", is_category=True,
            children=["preload", "zram", "profile-sync", "powertop", "cpu-governor", "swappiness"]
        )
        
        items["system-services"] = MenuItem(
            "system-services", "System Services", 
            "Background services, daemons",
            parent="system", is_category=True,
            children=["ssh-server", "samba", "nfs", "cups"]
        )
        
        items["system-hardware"] = MenuItem(
            "system-hardware", "Hardware Support", 
            "Drivers, firmware, peripherals",
            parent="system", is_category=True,
            children=["nvidia-drivers", "amd-drivers", "bluetooth", "printers"]
        )
        
        # Action items
        items["action-install"] = MenuItem(
            "action-install", "🚀 Start Installation", 
            "Begin installing selected software and applying configuration",
            parent="actions"
        )
        
        items["action-save"] = MenuItem(
            "action-save", "💾 Save Configuration", 
            "Save current selections without installing",
            parent="actions"
        )
        
        items["action-reset"] = MenuItem(
            "action-reset", "🔄 Reset Configuration", 
            "Clear all selections and start over",
            parent="actions"
        )
        
        items["action-exit"] = MenuItem(
            "action-exit", "❌ Exit without Saving", 
            "Exit configuration without installing anything",
            parent="actions"
        )
        
        # Individual items (examples - would be expanded)
        items["vscode"] = MenuItem(
            "vscode", "Visual Studio Code", 
            "Microsoft's popular code editor",
            parent="dev-ides", default=True
        )
        
        items["intellij"] = MenuItem(
            "intellij", "IntelliJ IDEA", 
            "JetBrains Java IDE",
            parent="dev-ides", default=True
        )
        
        items["pycharm"] = MenuItem(
            "pycharm", "PyCharm", 
            "JetBrains Python IDE",
            parent="dev-ides", default=True
        )
        
        items["webstorm"] = MenuItem(
            "webstorm", "WebStorm", 
            "JetBrains JavaScript IDE",
            parent="dev-ides"
        )
        
        items["sublime"] = MenuItem(
            "sublime", "Sublime Text", 
            "Sophisticated text editor",
            parent="dev-ides"
        )
        
        items["vim"] = MenuItem(
            "vim", "Vim/NeoVim", 
            "Terminal-based text editor",
            parent="dev-ides"
        )
        
        items["emacs"] = MenuItem(
            "emacs", "Emacs", 
            "Extensible text editor",
            parent="dev-ides"
        )
        
        # Languages
        items["python"] = MenuItem(
            "python", "Python", 
            "Python runtime and pip",
            parent="dev-languages", default=True
        )
        
        items["nodejs"] = MenuItem(
            "nodejs", "Node.js", 
            "JavaScript runtime",
            parent="dev-languages", default=True
        )
        
        items["java"] = MenuItem(
            "java", "Java", 
            "Java Development Kit",
            parent="dev-languages", default=True
        )
        
        items["go"] = MenuItem(
            "go", "Go", 
            "Go programming language",
            parent="dev-languages"
        )
        
        items["rust"] = MenuItem(
            "rust", "Rust", 
            "Rust programming language",
            parent="dev-languages"
        )
        
        items["cpp"] = MenuItem(
            "cpp", "C/C++", 
            "GCC compiler and build tools",
            parent="dev-languages"
        )
        
        items["php"] = MenuItem(
            "php", "PHP", 
            "PHP interpreter",
            parent="dev-languages"
        )
        
        items["ruby"] = MenuItem(
            "ruby", "Ruby", 
            "Ruby interpreter",
            parent="dev-languages"
        )
        
        # Tools
        items["git"] = MenuItem(
            "git", "Git", 
            "Version control system",
            parent="dev-tools", default=True
        )
        
        items["docker"] = MenuItem(
            "docker", "Docker", 
            "Container platform",
            parent="dev-tools", default=True
        )
        
        items["postman"] = MenuItem(
            "postman", "Postman", 
            "API development tool",
            parent="dev-tools"
        )
        
        items["mysql-workbench"] = MenuItem(
            "mysql-workbench", "MySQL Workbench", 
            "Database administration tool",
            parent="dev-tools"
        )
        
        items["redis-cli"] = MenuItem(
            "redis-cli", "Redis CLI", 
            "Redis command line interface",
            parent="dev-tools"
        )
        
        items["curl"] = MenuItem(
            "curl", "curl", 
            "HTTP client tool",
            parent="dev-tools", default=True
        )
        
        # Container & DevOps items
        items["docker-desktop"] = MenuItem(
            "docker-desktop", "Docker Desktop", 
            "Docker containerization platform with GUI",
            parent="dev-containers", default=True
        )
        
        items["kubernetes"] = MenuItem(
            "kubernetes", "Kubernetes Tools", 
            "Container orchestration tools (kubectl, minikube)",
            parent="dev-containers"
        )
        
        items["terraform"] = MenuItem(
            "terraform", "Terraform", 
            "Infrastructure as code tool",
            parent="dev-containers"
        )
        
        items["ansible"] = MenuItem(
            "ansible", "Ansible", 
            "Configuration management and automation",
            parent="dev-containers"
        )
        
        # Security Basic items
        items["ufw-firewall"] = MenuItem(
            "ufw-firewall", "UFW Firewall", 
            "Uncomplicated Firewall for Ubuntu",
            parent="security-basic", default=True
        )
        
        items["clamav"] = MenuItem(
            "clamav", "ClamAV", 
            "Open source antivirus",
            parent="security-basic"
        )
        
        items["auto-updates"] = MenuItem(
            "auto-updates", "Automatic Updates", 
            "Enable automatic security updates",
            parent="security-basic", default=True
        )
        
        items["fail2ban"] = MenuItem(
            "fail2ban", "Fail2Ban", 
            "Intrusion prevention system",
            parent="security-basic"
        )
        
        # Security Tools items
        items["nmap"] = MenuItem(
            "nmap", "Nmap", 
            "Network discovery and security auditing",
            parent="security-tools"
        )
        
        items["wireshark"] = MenuItem(
            "wireshark", "Wireshark", 
            "Network protocol analyzer",
            parent="security-tools"
        )
        
        items["metasploit"] = MenuItem(
            "metasploit", "Metasploit", 
            "Penetration testing framework",
            parent="security-tools"
        )
        
        items["burpsuite"] = MenuItem(
            "burpsuite", "Burp Suite", 
            "Web application security testing",
            parent="security-tools"
        )
        
        items["john"] = MenuItem(
            "john", "John the Ripper", 
            "Password cracking tool",
            parent="security-tools"
        )
        
        # Security Privacy items
        items["tor"] = MenuItem(
            "tor", "Tor Browser", 
            "Anonymous web browsing",
            parent="security-privacy"
        )
        
        items["veracrypt"] = MenuItem(
            "veracrypt", "VeraCrypt", 
            "Disk encryption software",
            parent="security-privacy"
        )
        
        items["keepassxc"] = MenuItem(
            "keepassxc", "KeePassXC", 
            "Password manager",
            parent="security-privacy", default=True
        )
        
        items["protonvpn"] = MenuItem(
            "protonvpn", "ProtonVPN", 
            "Secure VPN service",
            parent="security-privacy"
        )
        
        items["signal"] = MenuItem(
            "signal", "Signal", 
            "Secure messaging app",
            parent="security-privacy"
        )
        
        # Desktop Theme items  
        items["dark-theme"] = MenuItem(
            "dark-theme", "Dark Theme", 
            "System-wide dark theme",
            parent="desktop-themes", default=True
        )
        
        items["papirus-icons"] = MenuItem(
            "papirus-icons", "Papirus Icons", 
            "Modern icon theme",
            parent="desktop-themes"
        )
        
        items["numix-theme"] = MenuItem(
            "numix-theme", "Numix Theme", 
            "Flat design theme",
            parent="desktop-themes"
        )
        
        items["arc-theme"] = MenuItem(
            "arc-theme", "Arc Theme", 
            "Modern flat theme with transparent elements",
            parent="desktop-themes"
        )
        
        # Desktop Settings items
        items["mouse-settings"] = MenuItem(
            "mouse-settings", "Mouse Speed", 
            "Configure mouse pointer speed",
            parent="desktop-settings", default=True,
            is_configurable=True, config_type="slider",
            config_range=(1, 10), config_value=5, config_unit=""
        )
        
        items["keyboard-settings"] = MenuItem(
            "keyboard-settings", "Key Repeat Rate", 
            "Keyboard key repeat speed",
            parent="desktop-settings", default=True,
            is_configurable=True, config_type="slider",
            config_range=(1, 10), config_value=6, config_unit=""
        )
        
        items["display-settings"] = MenuItem(
            "display-settings", "Display Scaling", 
            "UI scaling percentage",
            parent="desktop-settings", default=True,
            is_configurable=True, config_type="slider",
            config_range=(100, 200), config_value=100, config_unit="%"
        )
        
        items["notifications"] = MenuItem(
            "notifications", "Notification Settings", 
            "System notification preferences",
            parent="desktop-settings"
        )
        
        # Application Browser items
        items["firefox"] = MenuItem(
            "firefox", "Firefox", 
            "Mozilla Firefox web browser",
            parent="app-browsers", default=True
        )
        
        items["chrome"] = MenuItem(
            "chrome", "Google Chrome", 
            "Google Chrome web browser",
            parent="app-browsers"
        )
        
        items["chromium"] = MenuItem(
            "chromium", "Chromium", 
            "Open source browser",
            parent="app-browsers"
        )
        
        items["brave"] = MenuItem(
            "brave", "Brave Browser", 
            "Privacy-focused browser",
            parent="app-browsers"
        )
        
        items["opera"] = MenuItem(
            "opera", "Opera", 
            "Feature-rich web browser",
            parent="app-browsers"
        )
        
        # Application Media items
        items["vlc"] = MenuItem(
            "vlc", "VLC Media Player", 
            "Versatile media player",
            parent="app-media", default=True
        )
        
        items["spotify"] = MenuItem(
            "spotify", "Spotify", 
            "Music streaming service",
            parent="app-media"
        )
        
        items["gimp"] = MenuItem(
            "gimp", "GIMP", 
            "GNU Image Manipulation Program",
            parent="app-media"
        )
        
        items["audacity"] = MenuItem(
            "audacity", "Audacity", 
            "Audio editing software",
            parent="app-media"
        )
        
        items["blender"] = MenuItem(
            "blender", "Blender", 
            "3D creation suite",
            parent="app-media"
        )
        
        # Application Productivity items
        items["libreoffice"] = MenuItem(
            "libreoffice", "LibreOffice", 
            "Free office suite",
            parent="app-productivity", default=True
        )
        
        items["thunderbird"] = MenuItem(
            "thunderbird", "Thunderbird", 
            "Email client",
            parent="app-productivity"
        )
        
        items["notion"] = MenuItem(
            "notion", "Notion", 
            "Note-taking and collaboration",
            parent="app-productivity"
        )
        
        items["obsidian"] = MenuItem(
            "obsidian", "Obsidian", 
            "Knowledge management tool",
            parent="app-productivity"
        )
        
        items["slack"] = MenuItem(
            "slack", "Slack", 
            "Team communication",
            parent="app-productivity"
        )
        
        # Application Communication items
        items["discord"] = MenuItem(
            "discord", "Discord", 
            "Voice and text chat",
            parent="app-communication"
        )
        
        items["teams"] = MenuItem(
            "teams", "Microsoft Teams", 
            "Video conferencing and collaboration",
            parent="app-communication"
        )
        
        items["zoom"] = MenuItem(
            "zoom", "Zoom", 
            "Video conferencing",
            parent="app-communication"
        )
        
        items["telegram"] = MenuItem(
            "telegram", "Telegram", 
            "Secure messaging",
            parent="app-communication"
        )
        
        items["whatsapp"] = MenuItem(
            "whatsapp", "WhatsApp", 
            "Messaging app",
            parent="app-communication"
        )
        
        # System Performance items
        items["preload"] = MenuItem(
            "preload", "Preload", 
            "Application preloader for faster startup",
            parent="system-perf", default=True
        )
        
        items["zram"] = MenuItem(
            "zram", "ZRAM", 
            "Compressed RAM for better memory usage",
            parent="system-perf"
        )
        
        items["profile-sync"] = MenuItem(
            "profile-sync", "Profile Sync Daemon", 
            "Sync browser profiles to RAM",
            parent="system-perf"
        )
        
        items["powertop"] = MenuItem(
            "powertop", "PowerTOP", 
            "Power consumption optimization",
            parent="system-perf"
        )
        
        items["cpu-governor"] = MenuItem(
            "cpu-governor", "CPU Governor", 
            "CPU power mode (1=powersave, 3=balanced, 5=performance)",
            parent="system-perf", 
            is_configurable=True, config_type="slider",
            config_range=(1, 5), config_value=3, config_unit=""
        )
        
        items["swappiness"] = MenuItem(
            "swappiness", "Swappiness", 
            "Memory swap (1=minimal swap, 100=aggressive swap)",
            parent="system-perf",
            is_configurable=True, config_type="slider", 
            config_range=(1, 100), config_value=60, config_unit=""
        )
        
        # System Services items
        items["ssh-server"] = MenuItem(
            "ssh-server", "SSH Server", 
            "Secure Shell server",
            parent="system-services"
        )
        
        items["samba"] = MenuItem(
            "samba", "Samba", 
            "Windows file sharing",
            parent="system-services"
        )
        
        items["nfs"] = MenuItem(
            "nfs", "NFS", 
            "Network File System",
            parent="system-services"
        )
        
        items["cups"] = MenuItem(
            "cups", "CUPS", 
            "Print server",
            parent="system-services", default=True
        )
        
        # System Hardware items
        items["nvidia-drivers"] = MenuItem(
            "nvidia-drivers", "NVIDIA Drivers", 
            "Proprietary NVIDIA graphics drivers",
            parent="system-hardware"
        )
        
        items["amd-drivers"] = MenuItem(
            "amd-drivers", "AMD Drivers", 
            "AMD graphics drivers",
            parent="system-hardware"
        )
        
        items["bluetooth"] = MenuItem(
            "bluetooth", "Bluetooth Support", 
            "Bluetooth connectivity",
            parent="system-hardware", default=True
        )
        
        items["printers"] = MenuItem(
            "printers", "Printer Support", 
            "Additional printer drivers",
            parent="system-hardware"
        )
        
        # Desktop environments
        items["gnome"] = MenuItem(
            "gnome", "GNOME", 
            "Default Ubuntu desktop",
            parent="desktop-env", default=True
        )
        
        items["kde"] = MenuItem(
            "kde", "KDE Plasma", 
            "Feature-rich desktop environment",
            parent="desktop-env"
        )
        
        items["xfce"] = MenuItem(
            "xfce", "XFCE", 
            "Lightweight desktop environment",
            parent="desktop-env"
        )
        
        items["mate"] = MenuItem(
            "mate", "MATE", 
            "Traditional desktop environment",
            parent="desktop-env"
        )
        
        items["cinnamon"] = MenuItem(
            "cinnamon", "Cinnamon", 
            "Modern desktop environment",
            parent="desktop-env"
        )
        
        # Browsers
        items["firefox"] = MenuItem(
            "firefox", "Firefox", 
            "Mozilla web browser",
            parent="app-browsers", default=True
        )
        
        items["chrome"] = MenuItem(
            "chrome", "Google Chrome", 
            "Google's web browser",
            parent="app-browsers"
        )
        
        items["chromium"] = MenuItem(
            "chromium", "Chromium", 
            "Open-source web browser",
            parent="app-browsers"
        )
        
        items["brave"] = MenuItem(
            "brave", "Brave Browser", 
            "Privacy-focused web browser",
            parent="app-browsers"
        )
        
        items["opera"] = MenuItem(
            "opera", "Opera", 
            "Feature-rich web browser",
            parent="app-browsers"
        )
        
        items["vivaldi"] = MenuItem(
            "vivaldi", "Vivaldi", 
            "Customizable web browser",
            parent="app-browsers"
        )
        
        items["edge"] = MenuItem(
            "edge", "Microsoft Edge", 
            "Microsoft's modern web browser",
            parent="app-browsers"
        )
        
        items["waterfox"] = MenuItem(
            "waterfox", "Waterfox", 
            "Privacy-focused Firefox fork",
            parent="app-browsers"
        )
        
        # Add more items as needed...
        
        return items
    
    def _get_current_menu_items(self) -> List[MenuItem]:
        """Get items for current menu level"""
        current = self.menu_items[self.current_menu]
        if current.children:
            return [self.menu_items[child_id] for child_id in current.children]
        return []
    
    def _get_category_selection_status(self, category_id: str) -> str:
        """Get selection status for a category: 'full', 'partial', 'empty'"""
        if category_id not in self.menu_items:
            return 'empty'
        
        # Get all selectable items in this category (recursively)
        selectable_items = self._get_all_selectable_items(category_id)
        
        if not selectable_items:
            return 'empty'
        
        selected_count = sum(1 for item_id in selectable_items if item_id in self.selected_items)
        
        if selected_count == 0:
            return 'empty'
        elif selected_count == len(selectable_items):
            return 'full'
        else:
            return 'partial'
    
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
                # Recursively get items from subcategories
                items.extend(self._get_all_selectable_items(child_id))
            else:
                # This is a selectable item
                items.append(child_id)
        
        return items
    
    def _draw_header(self):
        """Draw sexy header with title and breadcrumbs"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            # Clear header area
            self.stdscr.addstr(0, 0, " " * width)
            
            # Count total selectable items
            total_items = sum(1 for item in self.menu_items.values() 
                            if not item.is_category and item.parent != "actions")
            selected_count = len(self.selected_items)
            
            # Title with selection count
            title = f"✨ UBOOTU - Ubuntu System Setup [{selected_count}/{total_items}] ✨"
            safe_title = title.encode('ascii', 'ignore').decode('ascii')
            if not safe_title.strip():
                safe_title = f"=== UBOOTU - Ubuntu System Setup [{selected_count}/{total_items}] ==="
            
            # Center the title - use FUCKING BRIGHT YELLOW BACKGROUND
            title_x = max(0, (width - len(safe_title)) // 2)
            # Use reverse video for header
            self.stdscr.attron(curses.A_REVERSE | curses.A_BOLD)
            self.stdscr.addstr(0, title_x, safe_title[:width-2])
            self.stdscr.attroff(curses.A_REVERSE | curses.A_BOLD)
            
            # Breadcrumbs with sexy styling
            if self.current_menu != "root":
                self.stdscr.addstr(1, 0, " " * width)
                
                # Enhanced breadcrumb with back navigation hint
                breadcrumb_path = self._get_breadcrumb()
                if breadcrumb_path:
                    breadcrumb = f"📍 {breadcrumb_path} | Press BACKSPACE/ESC/LEFT/B to go back"
                else:
                    breadcrumb = f"📍 Main Menu | Press Q to quit"
                    
                safe_breadcrumb = breadcrumb.encode('ascii', 'ignore').decode('ascii')
                if not safe_breadcrumb.strip():
                    if breadcrumb_path:
                        safe_breadcrumb = f"-> {breadcrumb_path} | BACKSPACE/ESC/LEFT/B=Back"
                    else:
                        safe_breadcrumb = f"-> Main Menu | Q=Quit"
                
                self.stdscr.addstr(1, 2, safe_breadcrumb[:width-4])
        except curses.error:
            # Fallback for drawing issues
            pass
    
    def _get_breadcrumb(self) -> str:
        """Get breadcrumb navigation string"""
        path = []
        current = self.current_menu
        
        while current and current != "root":
            item = self.menu_items[current]
            path.append(item.label)
            current = item.parent
        
        path.reverse()
        return " > ".join(path)
    
    def _draw_menu(self):
        """Draw the current menu"""
        height, width = self.stdscr.getmaxyx()
        menu_items = self._get_current_menu_items()
        
        # Calculate display area - account for header and 4-line help
        start_y = 3 if self.current_menu != "root" else 3  # Header + description + space for menu
        display_height = height - start_y - 4  # Leave space for 4-line help
        
        try:
            # Clear menu area
            for i in range(start_y, height - 4):
                self.stdscr.addstr(i, 0, " " * width)
            
            # Show current menu description with F1 instruction highlighted
            current_item = self.menu_items[self.current_menu]
            if current_item.description:
                # Check if description contains F1 instruction
                if "F1" in current_item.description:
                    # Split the description to highlight F1 part
                    parts = current_item.description.split("|")
                    if len(parts) >= 2:
                        # Draw navigation part in bright cyan
                        self.stdscr.attron(curses.A_BOLD)
                        nav_part = f"🎯 {parts[0].strip()}"
                        self.stdscr.addstr(1, 2, nav_part)  # Always draw at line 1, right under header
                        self.stdscr.attroff(curses.A_BOLD)
                        # Calculate position for F1 instruction with spacing
                        nav_len = len(nav_part)
                        # Add some spacing after navigation text
                        f1_x = nav_len + 7  # Extra spacing for visual separation
                        
                        # Draw F1 instruction in bold white text (no background)
                        self.stdscr.attron(curses.A_BOLD)
                        f1_part = parts[1].strip()
                        if f1_x + len(f1_part) < width - 2:
                            self.stdscr.addstr(1, f1_x, f1_part)  # Draw at line 1
                        self.stdscr.attroff(curses.A_BOLD)
                    else:
                        # Fallback to normal display
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, 2, current_item.description[:width-4])  # Draw at line 1
                        self.stdscr.attroff(curses.A_BOLD)
                else:
                    # Normal description without F1
                    self.stdscr.attron(curses.A_BOLD)
                    desc = f"🎯 {current_item.description}"
                    safe_desc = desc.encode('ascii', 'ignore').decode('ascii')
                    if len(safe_desc.strip()) < len(desc.strip()) * 0.7:
                        safe_desc = f">>> {current_item.description}"
                    self.stdscr.addstr(1, 2, safe_desc[:width-4])  # Draw at line 1
                    self.stdscr.attroff(curses.A_BOLD)
                    start_y += 1
            
            # Adjust scroll if needed
            if self.current_item < self.scroll_offset:
                self.scroll_offset = self.current_item
            elif self.current_item >= self.scroll_offset + display_height:
                self.scroll_offset = self.current_item - display_height + 1
            
            # Draw menu items with sexy indicators
            for i, item in enumerate(menu_items[self.scroll_offset:self.scroll_offset + display_height]):
                item_index = i + self.scroll_offset
                y = start_y + i
                
                if y >= height - 4:  # Don't draw beyond help area
                    break
                
                # Highlight current item with reverse video
                if item_index == self.current_item:
                    self.stdscr.attron(curses.A_REVERSE)
                
                # Get indicators
                if item.is_category:
                    # Category indicators based on selection status - high ASCII
                    status = self._get_category_selection_status(item.id)
                    if status == 'full':
                        indicator = "●"  # Filled circle for all selected
                        safe_indicator = "●" if indicator.encode('ascii', 'ignore').decode('ascii') != indicator else indicator
                        color = 4  # Yellow for full
                    elif status == 'partial':
                        indicator = "◐"  # Half-filled circle for some selected
                        safe_indicator = "◐" if indicator.encode('ascii', 'ignore').decode('ascii') != indicator else indicator
                        color = 8  # Blue for partial
                    else:
                        indicator = "○"  # Empty circle for none selected
                        safe_indicator = "○" if indicator.encode('ascii', 'ignore').decode('ascii') != indicator else indicator
                        color = 9  # White for empty
                    
                    if item_index != self.current_item:
                        pass  # No colors
                else:
                    # Item indicators - high ASCII style
                    if item.selected:
                        indicator = "●"  # Filled circle for selected
                        safe_indicator = "●" if indicator.encode('ascii', 'ignore').decode('ascii') != indicator else indicator
                        if item_index != self.current_item:
                            # Green for selected
                            pass
                    else:
                        indicator = "○"  # Empty circle for unselected
                        safe_indicator = "○" if indicator.encode('ascii', 'ignore').decode('ascii') != indicator else indicator
                
                # Format item line with sexy styling  
                label = item.label[:width-30]
                line = f" {safe_indicator} {label}"
                
                # Add current value for configurable items
                if item.is_configurable and item.selected:
                    value_display = f"[{item.config_value}{item.config_unit}]"
                    line = f"{line} {value_display}"
                
                # Draw the label part first
                safe_line = line[:width-2]
                if len(safe_line) > 0:
                    self.stdscr.addstr(y, 1, safe_line)
                
                # Add description with fixed column alignment IN GREEN
                if item.description:
                    # Fixed column position for separator (e.g., column 50)
                    separator_col = min(50, width - 30)  # Adjust based on terminal width
                    desc_max_len = width - separator_col - 5
                    desc = item.description[:desc_max_len]
                    
                    # Draw separator and description in GREEN
                    if separator_col < width - 5:
                        # Draw separator in default color
                        self.stdscr.addstr(y, separator_col, "│")
                        
                        # Draw description in WHITE
                        # WHITE color
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(y, separator_col + 2, desc)
                        self.stdscr.attroff(curses.A_BOLD)
                        # Restore previous attributes if needed
                        if item_index == self.current_item:
                            self.stdscr.attron(curses.A_REVERSE)
                
                # Turn off reverse video if it was on
                if item_index == self.current_item:
                    self.stdscr.attroff(curses.A_REVERSE)
                    
        except curses.error:
            # Fallback for drawing issues
            pass
    
    def _draw_help(self):
        """Draw comprehensive help instructions at bottom of every page"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            # Draw bright help bar background
            # Clear help area (4 lines for comprehensive help)
            for i in range(height - 4, height):
                self.stdscr.addstr(i, 0, " " * width)
            
            # Get current menu context for contextual help
            current_menu = self.menu_items[self.current_menu]
            menu_items = self._get_current_menu_items()
            
            # Comprehensive help text with emojis and fallbacks
            if self.current_menu == "actions":
                help_lines = [
                    "⌨️  NAVIGATE: ←/ESC/B=Back to Main | ENTER=Execute Action | ↑↓/JK=Move | Q=Quit",
                    "🚀 INSTALL=Save & Install | 💾 SAVE=Save Only | 🔄 RESET=Clear All | ❌ EXIT=Cancel",
                    "📍 Use arrow keys to select action, then press ENTER to execute",
                    "💡 TIP: This menu is also accessible via F1-F10 keys • Powered by Ubootu"
                ]
                fallback_help = [
                    "NAVIGATE: LEFT/ESC/B=Back | ENTER=Execute | UP/DOWN/JK=Move | Q=Quit",
                    "INSTALL=Save & Install | SAVE=Save Only | RESET=Clear All | EXIT=Cancel",
                    "Use arrow keys to select action, then press ENTER to execute",
                    "TIP: This menu is accessible via F1-F10 keys • Powered by Ubootu"
                ]
            elif current_menu == "root":
                help_lines = [
                    "⚡⚡⚡ PRESS F1 TO INSTALL YOUR SELECTIONS! ⚡⚡⚡ PRESS F1 TO INSTALL! ⚡⚡⚡",
                    "⌨️  NAVIGATE: ←/ESC=Back | →/ENTER=Enter | ↑↓/JK=Move | SPACE=Select | Q=Quit",
                    "📊 CATEGORIES: ●=All Selected | ◐=Some Selected | ○=None Selected",
                    "🚀 F1-F10 = ACTIONS MENU → START INSTALLATION → APPLY ALL SETTINGS!"
                ]
                fallback_help = [
                    "*** PRESS F1 TO INSTALL YOUR SELECTIONS! *** PRESS F1 TO INSTALL! ***",
                    "NAVIGATE: LEFT/ESC=Back | RIGHT/ENTER=Enter | UP/DOWN=Move | SPACE=Select",
                    "CATEGORIES: ●=All Selected | ◐=Some Selected | ○=None Selected",
                    "F1-F10 = ACTIONS MENU -> START INSTALLATION -> APPLY ALL SETTINGS!"
                ]
            else:
                help_lines = [
                    "⚡⚡⚡ PRESS F1 TO INSTALL YOUR SELECTIONS! ⚡⚡⚡ PRESS F1 TO INSTALL! ⚡⚡⚡",
                    "⌨️  NAVIGATE: ←/ESC=Back | →/ENTER=Toggle | SPACE=Select | A=All | N=None",
                    "📍 ITEMS: ●=Selected | ○=Unselected | ↑↓/JK=Move | PgUp/Dn=Page | Q=Quit",
                    "🚀 F1-F10 = ACTIONS MENU → START INSTALLATION → APPLY ALL SETTINGS!"
                ]
                fallback_help = [
                    "*** PRESS F1 TO INSTALL YOUR SELECTIONS! *** PRESS F1 TO INSTALL! ***",
                    "NAVIGATE: LEFT/ESC=Back | RIGHT/ENTER=Toggle | SPACE=Select | A=All | N=None",
                    "ITEMS: ●=Selected | ○=Unselected | UP/DOWN=Move | PgUp/Dn=Page",
                    "F1-F10 = ACTIONS MENU -> START INSTALLATION -> APPLY ALL SETTINGS!"
                ]
            
            # Draw help lines
            for i, line in enumerate(help_lines):
                if i < 4:  # Show all 4 lines
                    safe_line = line.encode('ascii', 'ignore').decode('ascii')
                    if len(safe_line.strip()) < len(line.strip()) * 0.6:  # If too many chars lost
                        safe_line = fallback_help[i]
                    
                    # Make F1 instruction SUPER obvious
                    if i == 0 and "F1" in safe_line:
                        # Just use bold white text, no background
                        # White on black
                        self.stdscr.attron(curses.A_BOLD)
                    
                    # Draw help text (not centered, left-aligned for better readability)
                    if len(safe_line) > 0:
                        self.stdscr.addstr(height - 4 + i, 1, safe_line[:width-2])
                    
                    if i == 0:
                        self.stdscr.attroff(curses.A_BOLD)
        except curses.error:
            pass
    
    def _draw_stats(self):
        """Draw sexy selection statistics"""
        height, width = self.stdscr.getmaxyx()
        
        try:
            # Count selected items with sexy formatting
            selected_count = len(self.selected_items)
            
            # Get current category info
            current_category = self.menu_items[self.current_menu]
            category_items = self._get_all_selectable_items(self.current_menu)
            category_selected = sum(1 for item_id in category_items if item_id in self.selected_items)
            
            # Create sexy stats display
            if category_items:
                stats = f"✨ {selected_count} total | {category_selected}/{len(category_items)} in {current_category.label}"
            else:
                stats = f"✨ {selected_count} items selected"
            
            # Fallback for terminals without Unicode
            safe_stats = stats.encode('ascii', 'ignore').decode('ascii')
            if len(safe_stats.strip()) < len(stats.strip()) * 0.7:
                if category_items:
                    safe_stats = f"*** {selected_count} total | {category_selected}/{len(category_items)} in {current_category.label}"
                else:
                    safe_stats = f"*** {selected_count} items selected"
            
            # Position at top right of content area
            x = max(0, width - len(safe_stats) - 2)
            y = 2 if self.current_menu == "root" else 3
            
            if x > 0 and y > 0:
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(y, x, safe_stats[:width-2])
                self.stdscr.attroff(curses.A_BOLD)
        except curses.error:
            pass
    
    def _handle_key(self, key: int) -> bool:
        """Handle keyboard input"""
        menu_items = self._get_current_menu_items()
        
        if not menu_items:
            return True
        
        # Debug: Log every key press
        with open('/tmp/debug_tui.log', 'a') as f:
            f.write(f"Key pressed: {key} (char: {chr(key) if 32 <= key <= 126 else 'special'})\n")
        
        
        # Navigation
        if key == curses.KEY_UP or key == ord('k') or key == ord('K'):
            if self.current_item > 0:
                self.current_item -= 1
        elif key == curses.KEY_DOWN or key == ord('j') or key == ord('J'):
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
        elif key == ord(' '):  # Space - toggle selection or select all in category
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
        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
            current_item = menu_items[self.current_item]
            
            # Debug: Write what item we're trying to enter/select
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"ENTER (key {key}) pressed on: {current_item.id} (label: {current_item.label}) is_category: {current_item.is_category} parent: {current_item.parent} current_menu: {self.current_menu}\n")
            
            if current_item.is_category:
                # Enter subcategory
                with open('/tmp/debug_tui.log', 'a') as f:
                    f.write(f"SUCCESS: Entering category {current_item.id}, breadcrumb_stack will be: {len(self.breadcrumb_stack) + 1}\n")
                self.breadcrumb_stack.append((self.current_menu, self.current_item, self.scroll_offset))
                self.current_menu = current_item.id
                self.current_item = 0
                self.scroll_offset = 0
                
            else:
                # Handle actions if in actions menu, otherwise toggle selection
                if current_item.parent == "actions":
                    with open('/tmp/debug_tui.log', 'a') as f:
                        f.write(f"EXECUTING ACTION: {current_item.id}\n")
                    
                    if current_item.id == "action-install":
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"Calling _handle_install() - this SHOULD exit TUI\n")
                        return self._handle_install()  # This exits with installation
                    elif current_item.id == "action-save":
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"Calling _handle_save() - this should CONTINUE TUI\n")
                        result = self._handle_save()    # This continues (returns True)
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"_handle_save() returned: {result}\n")
                        return result
                    elif current_item.id == "action-reset":
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"Calling _handle_reset() - this should CONTINUE TUI\n")
                        result = self._handle_reset()   # This continues (returns True) 
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"_handle_reset() returned: {result}\n")
                        return result
                    elif current_item.id == "action-exit":
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"Calling _handle_exit() - this SHOULD exit TUI\n")
                        return self._handle_exit()    # This exits (returns False)
                    else:
                        # Unknown action - just continue
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"UNKNOWN ACTION: {current_item.id} - continuing\n")
                        return True
                else:
                    # Handle configurable items vs regular toggle items
                    if current_item.is_configurable:
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"CONFIGURING ITEM: {current_item.id} (type: {current_item.config_type})\n")
                        self._show_configuration_dialog(current_item)
                    else:
                        # For all other items, toggle selection (this should NOT cause exit)
                        with open('/tmp/debug_tui.log', 'a') as f:
                            f.write(f"TOGGLING SELECTION: {current_item.id} from {current_item.selected} to {not current_item.selected}\n")
                        current_item.selected = not current_item.selected
                        if current_item.selected:
                            self.selected_items.add(current_item.id)
                        else:
                            self.selected_items.discard(current_item.id)
        
        # Right arrow - enter submenu or toggle item
        elif key == curses.KEY_RIGHT:
            current_item = menu_items[self.current_item]
            
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"RIGHT arrow pressed on: {current_item.id} (is_category: {current_item.is_category})\n")
            
            if current_item.is_category:
                # Enter submenu (same as ENTER on category)
                self.breadcrumb_stack.append((self.current_menu, self.current_item, self.scroll_offset))
                self.current_menu = current_item.id
                self.current_item = 0
                self.scroll_offset = 0
            else:
                # Toggle item or configure if configurable
                if current_item.is_configurable:
                    self._show_configuration_dialog(current_item)
                else:
                    current_item.selected = not current_item.selected
                    if current_item.selected:
                        self.selected_items.add(current_item.id)
                    else:
                        self.selected_items.discard(current_item.id)
        
        # Back/Up one level - multiple keys for convenience
        elif key == curses.KEY_BACKSPACE or key == 127 or key == curses.KEY_LEFT or key == ord('b') or key == ord('B'):
            # ESC key is handled separately for quit, but if we're not at root, ESC goes back
            if self.breadcrumb_stack:
                with open('/tmp/debug_tui.log', 'a') as f:
                    f.write(f"Going back one level with key {key}\n")
                self.current_menu, self.current_item, self.scroll_offset = self.breadcrumb_stack.pop()
        
        # Quick select/deselect all in category
        elif key == ord('a') or key == ord('A'):
            self._select_all_in_category(True)
        elif key == ord('n') or key == ord('N'):
            self._select_all_in_category(False)
        
        # Function keys for Actions popup
        elif key >= curses.KEY_F1 and key <= curses.KEY_F10:
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"Function key pressed: F{key - curses.KEY_F1 + 1}\n")
            return self._show_actions_popup()
        
        # Quit with Q key only
        elif key == ord('q') or key == ord('Q'):
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"Q/q key pressed: {key} (ord('q')={ord('q')}, ord('Q')={ord('Q')})\n")
            return self._handle_exit()
            
        # Escape key - go back if possible, otherwise quit (immediate response)
        elif key == 27:  # Escape
            with open('/tmp/debug_tui.log', 'a') as f:
                f.write(f"ESC key (27) pressed - breadcrumb_stack length: {len(self.breadcrumb_stack)}\n")
            if self.breadcrumb_stack:
                with open('/tmp/debug_tui.log', 'a') as f:
                    f.write(f"ESC - going back one level\n")
                self.current_menu, self.current_item, self.scroll_offset = self.breadcrumb_stack.pop()
                # Force immediate refresh for responsive ESC
                return True
            else:
                with open('/tmp/debug_tui.log', 'a') as f:
                    f.write(f"ESC at root - exiting\n")
                return self._handle_exit()
        
        with open('/tmp/debug_tui.log', 'a') as f:
            f.write(f"_handle_key returning True for key {key}\n")
        return True
    
    def _select_all_in_category(self, select: bool):
        """Select or deselect all items in current category"""
        menu_items = self._get_current_menu_items()
        
        for item in menu_items:
            if not item.is_category:
                item.selected = select
                if select:
                    self.selected_items.add(item.id)
                else:
                    self.selected_items.discard(item.id)
    
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
    
    def _handle_install(self) -> bool:
        """Handle install action"""
        if not self.selected_items:
            # Show sexy error message
            try:
                # White on black
                self.stdscr.attron(curses.A_BOLD)
                height, width = self.stdscr.getmaxyx()
                msg = "🚨 No items selected! Use Space to select items first. 🚨"
                safe_msg = msg.encode('ascii', 'ignore').decode('ascii')
                if len(safe_msg.strip()) < len(msg.strip()) * 0.7:
                    safe_msg = "*** ERROR: No items selected! Use Space to select items first. ***"
                self.stdscr.addstr(height - 5, 2, safe_msg[:width-4])
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
            safe_msg = msg.encode('ascii', 'ignore').decode('ascii')
            if len(safe_msg.strip()) < len(msg.strip()) * 0.7:
                safe_msg = "*** UNBOOTU SUCCESS: Configuration saved! Continue configuring or go to Actions > Install ***"
            self.stdscr.addstr(height - 5, 2, safe_msg[:width-4])
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
            self.stdscr.addstr(height - 5, 2, msg[:width-4])
            self.stdscr.attroff(curses.A_BOLD)
            self.stdscr.refresh()
        except curses.error:
            pass
        
        # Get confirmation
        self.stdscr.timeout(30000)  # 30 second timeout
        key = self.stdscr.getch()
        self.stdscr.timeout(100)  # Reset timeout
        
        if key == ord('y') or key == ord('Y'):
            # Reset all selections
            self.selected_items.clear()
            for item in self.menu_items.values():
                item.selected = item.default
                if item.default:
                    self.selected_items.add(item.id)
            
            # Show confirmation
            try:
                msg = "SUCCESS: Configuration reset to defaults"
                self.stdscr.addstr(height - 4, 2, msg[:width-4])
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
                self.stdscr.addstr(start_y, start_x, "┌" + "─" * (popup_width - 2) + "┐")
                
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
                self.stdscr.addstr(start_y + 3, start_x, "├" + "─" * (popup_width - 2) + "┤")
                # Draw options
                for i, option in enumerate(options):
                    y = start_y + 4 + i
                    if i == selected:
                        # Highlight selected option
                        # Cyan selection
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(y, start_x + 2, f"▶ {option:<{popup_width-6}}")
                        self.stdscr.attroff(curses.A_BOLD)
                    else:
                        self.stdscr.addstr(y, start_x + 2, f"  {option:<{popup_width-6}}")
                        # Bottom border
                self.stdscr.addstr(start_y + popup_height - 1, start_x, "└" + "─" * (popup_width - 2) + "┘")
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == curses.KEY_UP:
                    selected = (selected - 1) % len(options)
                elif key == curses.KEY_DOWN:
                    selected = (selected + 1) % len(options)
                elif key == ord('\n') or key == curses.KEY_ENTER:
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
            'configuration_date': datetime.now().isoformat(),
            'selected_items': list(self.selected_items),
            'ui_version': '2.0_unbootu',
            'generated_by': 'Ubootu - Professional Ubuntu Desktop Configuration Tool'
        }
        
        # Save configurable item values
        configurable_values = {}
        for item_id, item in self.menu_items.items():
            if item.is_configurable and item.selected:
                configurable_values[item_id] = {
                    'value': item.config_value,
                    'type': item.config_type,
                    'unit': item.config_unit
                }
        
        if configurable_values:
            config['configurable_values'] = configurable_values
        
        # Organize by categories for easier processing
        categories = {}
        for item_id in self.selected_items:
            item = self.menu_items[item_id]
            if item.parent:
                if item.parent not in categories:
                    categories[item.parent] = []
                categories[item.parent].append(item_id)
        
        config['categories'] = categories
        
        try:
            with open('config.yml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        except Exception as e:
            # Handle save error
            height, width = self.stdscr.getmaxyx()
            # White on black
            self.stdscr.attron(curses.A_BOLD)
            msg = f"Error saving configuration: {str(e)}"
            self.stdscr.addstr(height - 4, 2, msg[:width-4])
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
            ("❌ Exit without Saving", "Cancel without saving")
        ]
        
        current_action = 0
        
        try:
            while True:
                # Clear the popup area
                for y in range(start_y, start_y + popup_height):
                    if y < height:
                        try:
                            self.stdscr.addstr(y, start_x, " " * min(popup_width, width - start_x))
                        except curses.error:
                            pass
                
                # Draw popup with HIGH CONTRAST colors
                try:
                    # Draw background and border
                    # White on magenta
                    for y in range(start_y, start_y + popup_height):
                        self.stdscr.addstr(y, start_x, "│" + " " * (popup_width - 2) + "│")
                    
                    # Top border
                    self.stdscr.addstr(start_y, start_x, "┌" + "─" * (popup_width - 2) + "┐")
                    
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
                    self.stdscr.addstr(start_y + 3, start_x, "├" + "─" * (popup_width - 2) + "┤")
                except curses.error:
                    pass
                
                # Draw action items
                for i, (action_title, action_desc) in enumerate(action_items):
                    item_y = start_y + 4 + i * 2
                    
                    try:
                        if i == current_action:
                            # Selected item - black on cyan (high contrast)
                            # Black on cyan
                            self.stdscr.addstr(item_y, start_x, "│" + " " * (popup_width - 2) + "│")
                            self.stdscr.attron(curses.A_BOLD)
                            self.stdscr.addstr(item_y, start_x + 3, f"▶ {action_title}")
                            self.stdscr.attroff(curses.A_BOLD)
                            self.stdscr.addstr(item_y + 1, start_x, "│" + " " * (popup_width - 2) + "│")
                            self.stdscr.addstr(item_y + 1, start_x + 5, action_desc[:popup_width - 8])
                        else:
                            # Unselected item - white on magenta
                            # White on magenta
                            self.stdscr.addstr(item_y, start_x + 3, f"  {action_title}")
                            self.stdscr.addstr(item_y + 1, start_x + 5, action_desc[:popup_width - 8])
                    except curses.error:
                        pass
                
                # Bottom border
                try:
                    self.stdscr.addstr(start_y + popup_height - 1, start_x, "└" + "─" * (popup_width - 2) + "┘")
                except curses.error:
                    pass
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == curses.KEY_UP or key == ord('k'):
                    current_action = (current_action - 1) % len(action_items)
                elif key == curses.KEY_DOWN or key == ord('j'):
                    current_action = (current_action + 1) % len(action_items)
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
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
                elif key == ord('q') or key == ord('Q'):
                    return True
                    
        except curses.error:
            # Handle any drawing errors gracefully
            pass
        
        return True
    
    def _show_configuration_dialog(self, item: MenuItem):
        """Show professional configuration dialog for settings"""
        if item.config_type == "slider":
            self._show_slider_dialog(item)
        # Future: elif item.config_type == "dropdown": etc.
    
    def _show_slider_dialog(self, item: MenuItem):
        """Show slider configuration dialog"""
        height, width = self.stdscr.getmaxyx()
        
        # Create a configuration overlay
        dialog_height = 11 if item.id in ["swappiness", "cpu-governor"] else 10
        dialog_width = 60
        start_y = (height - dialog_height) // 2
        start_x = (width - dialog_width) // 2
        
        # Store current value
        current_value = item.config_value
        min_val, max_val = item.config_range
        
        try:
            while True:
                # Clear the dialog area
                for y in range(start_y, start_y + dialog_height):
                    if y < height:
                        self.stdscr.addstr(y, start_x, " " * min(dialog_width, width - start_x))
                
                # Draw dialog border with vibrant colors
                # Black on green
                
                # Top border
                border_line = "┌" + "─" * (dialog_width - 2) + "┐"
                self.stdscr.addstr(start_y, start_x, border_line[:dialog_width])
                
                # Title
                title = f" Configure {item.label} "
                title_x = start_x + (dialog_width - len(title)) // 2
                self.stdscr.addstr(start_y + 1, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 1, title_x, title)
                
                # Separator
                self.stdscr.addstr(start_y + 2, start_x, "├" + "─" * (dialog_width - 2) + "┤")
                
                # Description with detailed explanation for specific items
                desc = item.description[:dialog_width - 4]
                desc_x = start_x + (dialog_width - len(desc)) // 2
                self.stdscr.addstr(start_y + 3, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(start_y + 3, desc_x, desc)
                
                # Add detailed explanation for specific items
                if item.id == "swappiness":
                    detail = "Low: Keeps apps in RAM | High: Frees RAM aggressively"
                    detail_x = start_x + (dialog_width - len(detail)) // 2
                    self.stdscr.addstr(start_y + 4, start_x, "│" + " " * (dialog_width - 2) + "│")
                    self.stdscr.addstr(start_y + 4, detail_x, detail)
                    slider_y_offset = 1
                elif item.id == "cpu-governor":
                    detail = "1=Save power | 3=Balanced | 5=Max performance"
                    detail_x = start_x + (dialog_width - len(detail)) // 2
                    self.stdscr.addstr(start_y + 4, start_x, "│" + " " * (dialog_width - 2) + "│")
                    self.stdscr.addstr(start_y + 4, detail_x, detail)
                    slider_y_offset = 1
                else:
                    slider_y_offset = 0
                
                # Slider
                slider_y = start_y + 4 + slider_y_offset
                self.stdscr.addstr(slider_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                
                # Slider track
                slider_width = dialog_width - 10
                slider_start = start_x + 5
                
                # Calculate slider position
                value_range = max_val - min_val
                if value_range > 0:
                    slider_pos = int((current_value - min_val) / value_range * (slider_width - 1))
                else:
                    slider_pos = 0
                
                # Draw slider track
                track = "─" * slider_width
                if slider_pos < len(track):
                    track = track[:slider_pos] + "●" + track[slider_pos + 1:]
                self.stdscr.addstr(slider_y, slider_start, track)
                
                # Value display
                value_text = f"{current_value}{item.config_unit}"
                value_y = start_y + 5 + slider_y_offset
                value_x = start_x + (dialog_width - len(value_text)) // 2
                self.stdscr.addstr(value_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                self.stdscr.addstr(value_y, value_x, value_text)
                
                # Instructions
                instructions = "← → arrows to adjust, ENTER to confirm, ESC to cancel"
                inst_y = start_y + 6 + slider_y_offset
                inst_x = start_x + (dialog_width - len(instructions)) // 2
                self.stdscr.addstr(inst_y, start_x, "│" + " " * (dialog_width - 2) + "│")
                if len(instructions) <= dialog_width - 4:
                    self.stdscr.addstr(inst_y, inst_x, instructions)
                
                # Bottom border
                self.stdscr.addstr(start_y + 7 + slider_y_offset, start_x, "└" + "─" * (dialog_width - 2) + "┘")
                
                self.stdscr.refresh()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == curses.KEY_LEFT or key == ord('h'):
                    if current_value > min_val:
                        current_value -= 1
                elif key == curses.KEY_RIGHT or key == ord('l'):
                    if current_value < max_val:
                        current_value += 1
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    # Confirm - save the value
                    item.config_value = current_value
                    item.selected = True  # Mark as configured
                    self.selected_items.add(item.id)
                    break
                elif key == 27:  # ESC - cancel
                    break
                elif key == ord('q') or key == ord('Q'):
                    break
                    
        except curses.error:
            # Handle any drawing errors gracefully
            pass
    
    def run(self):
        """Main TUI loop"""
        try:
            # Initial draw
            self.stdscr.clear()
            self._draw_header()
            self._draw_menu()
            self._draw_help()
            self._draw_stats()
            self.stdscr.refresh()
            
            while True:
                # Handle input (blocking - waits for key)
                key = self.stdscr.getch()
                if key != -1:  # Key was pressed
                    if not self._handle_key(key):
                        break
                    
                    # Redraw only after handling key
                    self.stdscr.erase()  # Clear without flashing
                    self._draw_header()
                    self._draw_menu()
                    self._draw_help()
                    self._draw_stats()
                    self.stdscr.refresh()
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

def run_tui():
    """Run the TUI with curses wrapper"""
    def tui_main(stdscr):
        tui = HierarchicalTUI(stdscr)
        return tui.run()
    
    return curses.wrapper(tui_main)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        print("🚀 Ubootu - Professional Ubuntu Desktop Configuration Tool")
        print("Usage: python3 configure_standard_tui.py")
        return 1
    
    try:
        exit_code = run_tui()
        if exit_code == 0:
            print("\n✅ Ubootu configuration saved successfully!")
            print("🚀 Installation will begin shortly...")
        else:
            print("\n❌ Ubootu configuration cancelled by user")
        return exit_code
    except KeyboardInterrupt:
        print("\n❌ Ubootu configuration cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Ubootu Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())