"""
Menu Structure Module for Ubootu TUI
Defines menu items and builds the hierarchical menu structure
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


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


def build_menu_structure() -> Dict[str, MenuItem]:
    """Build hierarchical menu structure"""
    items = {}

    # Root menu
    items["root"] = MenuItem(
        "root",
        "🚀 Ubootu - Ubuntu System Setup",
        "Navigate: ↑↓ arrows, SPACE select, ENTER enter     |     ▶▶▶ PRESS F1 FOR ACTIONS MENU TO START INSTALLATION ◀◀◀",
        is_category=True,
        children=["development", "desktop", "applications", "security", "system"],
    )

    # Main categories
    items["development"] = MenuItem(
        "development",
        "Development Tools",
        "Programming languages, IDEs, debugging tools",
        parent="root",
        is_category=True,
        children=["dev-ides", "dev-languages", "dev-tools", "dev-containers"],
    )

    items["desktop"] = MenuItem(
        "desktop",
        "Desktop Environment",
        "Window managers, themes, customization",
        parent="root",
        is_category=True,
        children=["desktop-env", "desktop-themes", "desktop-settings"],
    )

    items["applications"] = MenuItem(
        "applications",
        "Applications",
        "Web browsers, media players, productivity tools",
        parent="root",
        is_category=True,
        children=["app-browsers", "app-media", "app-productivity", "app-communication"],
    )

    items["security"] = MenuItem(
        "security",
        "Security & Privacy",
        "Firewalls, encryption, privacy tools",
        parent="root",
        is_category=True,
        children=["security-basic", "security-tools", "security-privacy"],
    )

    items["system"] = MenuItem(
        "system",
        "System Configuration",
        "Performance, services, hardware",
        parent="root",
        is_category=True,
        children=["system-perf", "system-services", "system-hardware"],
    )

    items["actions"] = MenuItem(
        "actions",
        "Actions",
        "Install, save, reset, or exit",
        parent="root",
        is_category=True,
        children=["action-install", "action-save", "action-reset", "action-exit"],
    )

    # Development subcategories
    items["dev-ides"] = MenuItem(
        "dev-ides",
        "IDEs & Editors",
        "Integrated development environments",
        parent="development",
        is_category=True,
        children=[
            "vscode",
            "intellij",
            "pycharm",
            "webstorm",
            "sublime",
            "vim",
            "emacs",
        ],
    )

    items["dev-languages"] = MenuItem(
        "dev-languages",
        "Programming Languages",
        "Runtimes, compilers, interpreters",
        parent="development",
        is_category=True,
        children=["python", "nodejs", "java", "go", "rust", "cpp", "php", "ruby"],
    )

    items["dev-tools"] = MenuItem(
        "dev-tools",
        "Development Tools",
        "Debugging, profiling, testing tools",
        parent="development",
        is_category=True,
        children=["git", "docker", "postman", "mysql-workbench", "redis-cli", "curl"],
    )

    items["dev-containers"] = MenuItem(
        "dev-containers",
        "Containers & DevOps",
        "Container platforms and orchestration",
        parent="development",
        is_category=True,
        children=["docker-desktop", "kubernetes", "terraform", "ansible"],
    )

    # Desktop subcategories
    items["desktop-env"] = MenuItem(
        "desktop-env",
        "Desktop Environment",
        "Choose your desktop environment",
        parent="desktop",
        is_category=True,
        children=["gnome", "kde", "xfce", "mate", "cinnamon"],
    )

    items["desktop-themes"] = MenuItem(
        "desktop-themes",
        "Themes & Appearance",
        "Icons, themes, wallpapers",
        parent="desktop",
        is_category=True,
        children=["dark-theme", "papirus-icons", "numix-theme", "arc-theme"],
    )

    items["desktop-settings"] = MenuItem(
        "desktop-settings",
        "Desktop Settings",
        "Mouse, keyboard, display settings",
        parent="desktop",
        is_category=True,
        children=[
            "mouse-settings",
            "keyboard-settings",
            "display-settings",
            "notifications",
        ],
    )

    # Application subcategories
    items["app-browsers"] = MenuItem(
        "app-browsers",
        "Web Browsers",
        "Internet browsers",
        parent="applications",
        is_category=True,
        children=[
            "firefox",
            "chrome",
            "chromium",
            "brave",
            "opera",
            "vivaldi",
            "edge",
            "waterfox",
        ],
    )

    items["app-media"] = MenuItem(
        "app-media",
        "Media & Entertainment",
        "Music, video, image viewers",
        parent="applications",
        is_category=True,
        children=["vlc", "spotify", "gimp", "audacity", "blender"],
    )

    items["app-productivity"] = MenuItem(
        "app-productivity",
        "Productivity",
        "Office suites, note-taking, planning",
        parent="applications",
        is_category=True,
        children=["libreoffice", "thunderbird", "notion", "obsidian", "slack"],
    )

    items["app-communication"] = MenuItem(
        "app-communication",
        "Communication",
        "Chat, video calls, social media",
        parent="applications",
        is_category=True,
        children=["discord", "teams", "zoom", "telegram", "whatsapp"],
    )

    # Security subcategories
    items["security-basic"] = MenuItem(
        "security-basic",
        "Basic Security",
        "Firewall, antivirus, updates",
        parent="security",
        is_category=True,
        children=["ufw-firewall", "clamav", "auto-updates", "fail2ban"],
    )

    items["security-tools"] = MenuItem(
        "security-tools",
        "Security Tools",
        "Penetration testing, auditing",
        parent="security",
        is_category=True,
        children=["nmap", "wireshark", "metasploit", "burpsuite", "john"],
    )

    items["security-privacy"] = MenuItem(
        "security-privacy",
        "Privacy Tools",
        "VPN, encryption, anonymous browsing",
        parent="security",
        is_category=True,
        children=["tor", "veracrypt", "keepassxc", "protonvpn", "signal"],
    )

    # System subcategories
    items["system-perf"] = MenuItem(
        "system-perf",
        "Performance",
        "CPU, memory, disk optimization",
        parent="system",
        is_category=True,
        children=[
            "preload",
            "zram",
            "profile-sync",
            "powertop",
            "cpu-governor",
            "swappiness",
        ],
    )

    items["system-services"] = MenuItem(
        "system-services",
        "System Services",
        "Background services, daemons",
        parent="system",
        is_category=True,
        children=["ssh-server", "samba", "nfs", "cups"],
    )

    items["system-hardware"] = MenuItem(
        "system-hardware",
        "Hardware Support",
        "Drivers, firmware, peripherals",
        parent="system",
        is_category=True,
        children=["nvidia-drivers", "amd-drivers", "bluetooth", "printers"],
    )

    # Action items
    items["action-install"] = MenuItem(
        "action-install",
        "🚀 Start Installation",
        "Begin installing selected software and applying configuration",
        parent="actions",
    )

    items["action-save"] = MenuItem(
        "action-save",
        "💾 Save Configuration",
        "Save current selections without installing",
        parent="actions",
    )

    items["action-reset"] = MenuItem(
        "action-reset",
        "🔄 Reset Configuration",
        "Clear all selections and start over",
        parent="actions",
    )

    items["action-exit"] = MenuItem(
        "action-exit",
        "❌ Exit without Saving",
        "Exit configuration without installing anything",
        parent="actions",
    )

    # Individual items - IDEs
    items["vscode"] = MenuItem(
        "vscode",
        "Visual Studio Code",
        "Microsoft's popular code editor",
        parent="dev-ides",
        default=True,
    )

    items["intellij"] = MenuItem(
        "intellij",
        "IntelliJ IDEA",
        "JetBrains Java IDE",
        parent="dev-ides",
        default=True,
    )

    items["pycharm"] = MenuItem(
        "pycharm", "PyCharm", "JetBrains Python IDE", parent="dev-ides", default=True
    )

    items["webstorm"] = MenuItem(
        "webstorm", "WebStorm", "JetBrains JavaScript IDE", parent="dev-ides"
    )

    items["sublime"] = MenuItem(
        "sublime", "Sublime Text", "Sophisticated text editor", parent="dev-ides"
    )

    items["vim"] = MenuItem(
        "vim", "Vim/NeoVim", "Terminal-based text editor", parent="dev-ides"
    )

    items["emacs"] = MenuItem(
        "emacs", "Emacs", "Extensible text editor", parent="dev-ides"
    )

    # Languages
    items["python"] = MenuItem(
        "python",
        "Python",
        "Python runtime and pip",
        parent="dev-languages",
        default=True,
    )

    items["nodejs"] = MenuItem(
        "nodejs", "Node.js", "JavaScript runtime", parent="dev-languages", default=True
    )

    items["java"] = MenuItem(
        "java", "Java", "Java Development Kit", parent="dev-languages", default=True
    )

    items["go"] = MenuItem(
        "go", "Go", "Go programming language", parent="dev-languages"
    )

    items["rust"] = MenuItem(
        "rust", "Rust", "Rust programming language", parent="dev-languages"
    )

    items["cpp"] = MenuItem(
        "cpp", "C/C++", "GCC compiler and build tools", parent="dev-languages"
    )

    items["php"] = MenuItem("php", "PHP", "PHP interpreter", parent="dev-languages")

    items["ruby"] = MenuItem("ruby", "Ruby", "Ruby interpreter", parent="dev-languages")

    # Tools
    items["git"] = MenuItem(
        "git", "Git", "Version control system", parent="dev-tools", default=True
    )

    items["docker"] = MenuItem(
        "docker", "Docker", "Container platform", parent="dev-tools", default=True
    )

    items["postman"] = MenuItem(
        "postman", "Postman", "API development tool", parent="dev-tools"
    )

    items["mysql-workbench"] = MenuItem(
        "mysql-workbench",
        "MySQL Workbench",
        "Database administration tool",
        parent="dev-tools",
    )

    items["redis-cli"] = MenuItem(
        "redis-cli", "Redis CLI", "Redis command line interface", parent="dev-tools"
    )

    items["curl"] = MenuItem(
        "curl", "curl", "HTTP client tool", parent="dev-tools", default=True
    )

    # Container & DevOps items
    items["docker-desktop"] = MenuItem(
        "docker-desktop",
        "Docker Desktop",
        "Docker containerization platform with GUI",
        parent="dev-containers",
        default=True,
    )

    items["kubernetes"] = MenuItem(
        "kubernetes",
        "Kubernetes Tools",
        "Container orchestration tools (kubectl, minikube)",
        parent="dev-containers",
    )

    items["terraform"] = MenuItem(
        "terraform", "Terraform", "Infrastructure as code tool", parent="dev-containers"
    )

    items["ansible"] = MenuItem(
        "ansible",
        "Ansible",
        "Configuration management and automation",
        parent="dev-containers",
    )

    # Security Basic items
    items["ufw-firewall"] = MenuItem(
        "ufw-firewall",
        "UFW Firewall",
        "Uncomplicated Firewall for Ubuntu",
        parent="security-basic",
        default=True,
    )

    items["clamav"] = MenuItem(
        "clamav", "ClamAV", "Open source antivirus", parent="security-basic"
    )

    items["auto-updates"] = MenuItem(
        "auto-updates",
        "Automatic Updates",
        "Enable automatic security updates",
        parent="security-basic",
        default=True,
    )

    items["fail2ban"] = MenuItem(
        "fail2ban", "Fail2Ban", "Intrusion prevention system", parent="security-basic"
    )

    # Security Tools items
    items["nmap"] = MenuItem(
        "nmap",
        "Nmap",
        "Network discovery and security auditing",
        parent="security-tools",
    )

    items["wireshark"] = MenuItem(
        "wireshark", "Wireshark", "Network protocol analyzer", parent="security-tools"
    )

    items["metasploit"] = MenuItem(
        "metasploit",
        "Metasploit",
        "Penetration testing framework",
        parent="security-tools",
    )

    items["burpsuite"] = MenuItem(
        "burpsuite",
        "Burp Suite",
        "Web application security testing",
        parent="security-tools",
    )

    items["john"] = MenuItem(
        "john", "John the Ripper", "Password cracking tool", parent="security-tools"
    )

    # Security Privacy items
    items["tor"] = MenuItem(
        "tor", "Tor Browser", "Anonymous web browsing", parent="security-privacy"
    )

    items["veracrypt"] = MenuItem(
        "veracrypt", "VeraCrypt", "Disk encryption software", parent="security-privacy"
    )

    items["keepassxc"] = MenuItem(
        "keepassxc",
        "KeePassXC",
        "Password manager",
        parent="security-privacy",
        default=True,
    )

    items["protonvpn"] = MenuItem(
        "protonvpn", "ProtonVPN", "Secure VPN service", parent="security-privacy"
    )

    items["signal"] = MenuItem(
        "signal", "Signal", "Secure messaging app", parent="security-privacy"
    )

    # Desktop Theme items
    items["dark-theme"] = MenuItem(
        "dark-theme",
        "Dark Theme",
        "System-wide dark theme",
        parent="desktop-themes",
        default=True,
    )

    items["papirus-icons"] = MenuItem(
        "papirus-icons", "Papirus Icons", "Modern icon theme", parent="desktop-themes"
    )

    items["numix-theme"] = MenuItem(
        "numix-theme", "Numix Theme", "Flat design theme", parent="desktop-themes"
    )

    items["arc-theme"] = MenuItem(
        "arc-theme",
        "Arc Theme",
        "Modern flat theme with transparent elements",
        parent="desktop-themes",
    )

    # Desktop Settings items
    items["mouse-settings"] = MenuItem(
        "mouse-settings",
        "Mouse Speed",
        "Configure mouse pointer speed",
        parent="desktop-settings",
        default=True,
        is_configurable=True,
        config_type="slider",
        config_range=(1, 10),
        config_value=5,
        config_unit="",
    )

    items["keyboard-settings"] = MenuItem(
        "keyboard-settings",
        "Key Repeat Rate",
        "Keyboard key repeat speed",
        parent="desktop-settings",
        default=True,
        is_configurable=True,
        config_type="slider",
        config_range=(1, 10),
        config_value=6,
        config_unit="",
    )

    items["display-settings"] = MenuItem(
        "display-settings",
        "Display Scaling",
        "UI scaling percentage",
        parent="desktop-settings",
        default=True,
        is_configurable=True,
        config_type="slider",
        config_range=(100, 200),
        config_value=100,
        config_unit="%",
    )

    items["notifications"] = MenuItem(
        "notifications",
        "Notification Settings",
        "System notification preferences",
        parent="desktop-settings",
    )

    # Application Browser items
    items["firefox"] = MenuItem(
        "firefox",
        "Firefox",
        "Mozilla Firefox web browser",
        parent="app-browsers",
        default=True,
    )

    items["chrome"] = MenuItem(
        "chrome", "Google Chrome", "Google Chrome web browser", parent="app-browsers"
    )

    items["chromium"] = MenuItem(
        "chromium", "Chromium", "Open source browser", parent="app-browsers"
    )

    items["brave"] = MenuItem(
        "brave", "Brave Browser", "Privacy-focused browser", parent="app-browsers"
    )

    items["opera"] = MenuItem(
        "opera", "Opera", "Feature-rich web browser", parent="app-browsers"
    )

    items["vivaldi"] = MenuItem(
        "vivaldi", "Vivaldi", "Customizable web browser", parent="app-browsers"
    )

    items["edge"] = MenuItem(
        "edge",
        "Microsoft Edge",
        "Microsoft's modern web browser",
        parent="app-browsers",
    )

    items["waterfox"] = MenuItem(
        "waterfox", "Waterfox", "Privacy-focused Firefox fork", parent="app-browsers"
    )

    # Application Media items
    items["vlc"] = MenuItem(
        "vlc",
        "VLC Media Player",
        "Versatile media player",
        parent="app-media",
        default=True,
    )

    items["spotify"] = MenuItem(
        "spotify", "Spotify", "Music streaming service", parent="app-media"
    )

    items["gimp"] = MenuItem(
        "gimp", "GIMP", "GNU Image Manipulation Program", parent="app-media"
    )

    items["audacity"] = MenuItem(
        "audacity", "Audacity", "Audio editing software", parent="app-media"
    )

    items["blender"] = MenuItem(
        "blender", "Blender", "3D creation suite", parent="app-media"
    )

    # Application Productivity items
    items["libreoffice"] = MenuItem(
        "libreoffice",
        "LibreOffice",
        "Free office suite",
        parent="app-productivity",
        default=True,
    )

    items["thunderbird"] = MenuItem(
        "thunderbird", "Thunderbird", "Email client", parent="app-productivity"
    )

    items["notion"] = MenuItem(
        "notion", "Notion", "Note-taking and collaboration", parent="app-productivity"
    )

    items["obsidian"] = MenuItem(
        "obsidian", "Obsidian", "Knowledge management tool", parent="app-productivity"
    )

    items["slack"] = MenuItem(
        "slack", "Slack", "Team communication", parent="app-productivity"
    )

    # Application Communication items
    items["discord"] = MenuItem(
        "discord", "Discord", "Voice and text chat", parent="app-communication"
    )

    items["teams"] = MenuItem(
        "teams",
        "Microsoft Teams",
        "Video conferencing and collaboration",
        parent="app-communication",
    )

    items["zoom"] = MenuItem(
        "zoom", "Zoom", "Video conferencing", parent="app-communication"
    )

    items["telegram"] = MenuItem(
        "telegram", "Telegram", "Secure messaging", parent="app-communication"
    )

    items["whatsapp"] = MenuItem(
        "whatsapp", "WhatsApp", "Messaging app", parent="app-communication"
    )

    # System Performance items
    items["preload"] = MenuItem(
        "preload",
        "Preload",
        "Application preloader for faster startup",
        parent="system-perf",
        default=True,
    )

    items["zram"] = MenuItem(
        "zram", "ZRAM", "Compressed RAM for better memory usage", parent="system-perf"
    )

    items["profile-sync"] = MenuItem(
        "profile-sync",
        "Profile Sync Daemon",
        "Sync browser profiles to RAM",
        parent="system-perf",
    )

    items["powertop"] = MenuItem(
        "powertop", "PowerTOP", "Power consumption optimization", parent="system-perf"
    )

    items["cpu-governor"] = MenuItem(
        "cpu-governor",
        "CPU Governor",
        "CPU power mode (1=powersave, 3=balanced, 5=performance)",
        parent="system-perf",
        is_configurable=True,
        config_type="slider",
        config_range=(1, 5),
        config_value=3,
        config_unit="",
    )

    items["swappiness"] = MenuItem(
        "swappiness",
        "Swappiness",
        "Memory swap (1=minimal swap, 100=aggressive swap)",
        parent="system-perf",
        is_configurable=True,
        config_type="slider",
        config_range=(1, 100),
        config_value=60,
        config_unit="",
    )

    # System Services items
    items["ssh-server"] = MenuItem(
        "ssh-server", "SSH Server", "Secure Shell server", parent="system-services"
    )

    items["samba"] = MenuItem(
        "samba", "Samba", "Windows file sharing", parent="system-services"
    )

    items["nfs"] = MenuItem(
        "nfs", "NFS", "Network File System", parent="system-services"
    )

    items["cups"] = MenuItem(
        "cups", "CUPS", "Print server", parent="system-services", default=True
    )

    # System Hardware items
    items["nvidia-drivers"] = MenuItem(
        "nvidia-drivers",
        "NVIDIA Drivers",
        "Proprietary NVIDIA graphics drivers",
        parent="system-hardware",
    )

    items["amd-drivers"] = MenuItem(
        "amd-drivers", "AMD Drivers", "AMD graphics drivers", parent="system-hardware"
    )

    items["bluetooth"] = MenuItem(
        "bluetooth",
        "Bluetooth Support",
        "Bluetooth connectivity",
        parent="system-hardware",
        default=True,
    )

    items["printers"] = MenuItem(
        "printers",
        "Printer Support",
        "Additional printer drivers",
        parent="system-hardware",
    )

    # Desktop environments
    items["gnome"] = MenuItem(
        "gnome", "GNOME", "Default Ubuntu desktop", parent="desktop-env", default=True
    )

    items["kde"] = MenuItem(
        "kde", "KDE Plasma", "Feature-rich desktop environment", parent="desktop-env"
    )

    items["xfce"] = MenuItem(
        "xfce", "XFCE", "Lightweight desktop environment", parent="desktop-env"
    )

    items["mate"] = MenuItem(
        "mate", "MATE", "Traditional desktop environment", parent="desktop-env"
    )

    items["cinnamon"] = MenuItem(
        "cinnamon", "Cinnamon", "Modern desktop environment", parent="desktop-env"
    )

    return items
