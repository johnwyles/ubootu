#!/usr/bin/env python3
"""
Application default configurations and customizations
Provides sensible defaults for developers and regular users
"""

from typing import Any, Dict, List


class AppDefaults:
    """Manages application-specific default configurations"""

    def __init__(self):
        self.developer_apps = self._load_developer_defaults()
        self.user_apps = self._load_user_defaults()

    def _load_developer_defaults(self) -> Dict[str, Dict[str, Any]]:
        """Load developer-focused application defaults"""
        return {
            "vscode": {
                "name": "Visual Studio Code",
                "description": "Powerful code editor with developer-friendly defaults",
                "features": [
                    "Auto-save after 1 second delay (never lose work)",
                    "Format on save (keeps code clean)",
                    "Bracket pair colorization (never lose track)",
                    "Minimap for code navigation",
                    "Sticky scroll (maintain context)",
                    "Git integration in sidebar",
                ],
                "extensions": [
                    "GitLens - Visualize code authorship and history",
                    "Prettier - Auto-format code on save",
                    "ESLint - Catch JavaScript errors",
                    "Docker - Manage containers from VS Code",
                    "Remote-SSH - Edit remote files",
                    "Thunder Client - API testing inside VS Code",
                    "Error Lens - See errors inline",
                    "TODO Highlight - Never miss a TODO",
                ],
                "settings": {
                    "editor.formatOnSave": True,
                    "editor.bracketPairColorization.enabled": True,
                    "editor.minimap.enabled": True,
                    "editor.stickyScroll.enabled": True,
                    "files.autoSave": "afterDelay",
                    "files.autoSaveDelay": 1000,
                    "workbench.colorTheme": "One Dark Pro",
                    "terminal.integrated.fontFamily": "MesloLGS NF",
                },
                "help": "These VS Code customizations are based on what 90% of developers configure manually. Auto-save prevents losing work, format-on-save keeps code clean, and the selected extensions provide essential functionality for modern development workflows.",
                "preview": """
[VS Code Preview]
┌─ Explorer ──┬─ editor.py ─────────────────┐
│ 📁 project  │ 1  def hello_world():       │
│  📄 app.py  │ 2  ▶   print("Hello!")      │
│  📄 test.py │ 3                           │
└─────────────┴──────────────────────────────┘
                """,
            },
            "git": {
                "name": "Git Version Control",
                "description": "Modern Git configuration with helpful aliases",
                "features": [
                    "Default branch name: 'main' (modern standard)",
                    "Auto-correct typos (git stauts → git status)",
                    "Colorful output for better readability",
                    "Rebase by default on pull (cleaner history)",
                    "Automatic stash on rebase",
                    "Better diff algorithm",
                ],
                "aliases": {
                    "st": "status",
                    "co": "checkout",
                    "br": "branch",
                    "cm": "commit -m",
                    "unstage": "reset HEAD --",
                    "last": "log -1 HEAD",
                    "visual": "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'",
                    "undo": "reset --soft HEAD~1",
                    "amend": "commit --amend --no-edit",
                    "sync": "!git pull --rebase && git push",
                },
                "settings": {
                    "init.defaultBranch": "main",
                    "color.ui": "auto",
                    "pull.rebase": True,
                    "rebase.autoStash": True,
                    "diff.algorithm": "histogram",
                    "help.autocorrect": 10,
                    "core.editor": "code --wait",
                },
                "help": "These Git settings include the most commonly used configurations that developers set up manually. The aliases save typing time, and the settings provide sensible defaults for modern Git workflows.",
            },
            "terminal": {
                "name": "Terminal & Shell",
                "description": "Supercharged terminal with modern tools",
                "features": [
                    "Zsh with Oh My Zsh framework",
                    "Powerlevel10k theme (beautiful prompts)",
                    "Syntax highlighting as you type",
                    "Auto-suggestions from history",
                    "Git status in prompt",
                    "Directory jumping with 'z'",
                    "Better tab completion",
                ],
                "tools": [
                    "bat - cat with syntax highlighting",
                    "exa - ls with colors and git status",
                    "ripgrep - faster grep",
                    "fzf - fuzzy file finder",
                    "htop - better process viewer",
                    "ncdu - disk usage analyzer",
                    "tldr - simplified man pages",
                ],
                "aliases": {
                    "ll": "exa -la --icons",
                    "lt": "exa --tree --level=2",
                    "..": "cd ..",
                    "...": "cd ../..",
                    "gs": "git status",
                    "ga": "git add",
                    "gc": "git commit",
                    "gp": "git push",
                    "gl": "git pull",
                    "cat": "bat",
                    "ls": "exa --icons",
                    "find": "fd",
                    "ps": "procs",
                    "du": "dust",
                    "grep": "rg",
                    "vim": "nvim",
                    "top": "htop",
                },
            },
            "docker": {
                "name": "Docker",
                "description": "Container management made easy",
                "features": [
                    "Docker Desktop with GUI",
                    "Docker Compose v2",
                    "Buildkit enabled by default",
                    "Useful command aliases",
                    "Auto-cleanup of unused resources",
                    "Better build caching",
                ],
                "aliases": {
                    "dps": "docker ps",
                    "dpsa": "docker ps -a",
                    "di": "docker images",
                    "drm": "docker rm $(docker ps -aq)",
                    "drmi": "docker rmi $(docker images -q)",
                    "dc": "docker compose",
                    "dcup": "docker compose up -d",
                    "dcdown": "docker compose down",
                    "dclogs": "docker compose logs -f",
                    "dprune": "docker system prune -af",
                },
                "settings": {
                    "features.buildkit": True,
                    "features.containerd-snapshotter": True,
                },
            },
        }

    def _load_user_defaults(self) -> Dict[str, Dict[str, Any]]:
        """Load regular user application defaults"""
        return {
            "firefox": {
                "name": "Firefox Web Browser",
                "description": "Privacy-focused browsing with productivity enhancements",
                "features": [
                    "Enhanced Tracking Protection: Strict mode",
                    "HTTPS-Only mode for security",
                    "Container tabs for organization",
                    "Picture-in-Picture for videos",
                    "Reader mode for articles",
                    "Sync across devices",
                ],
                "extensions": [
                    "uBlock Origin - Block ads and trackers",
                    "Bitwarden - Password management",
                    "Dark Reader - Dark mode for all sites",
                    "OneTab - Tab management",
                    "Enhancer for YouTube - Better video controls",
                    "SponsorBlock - Skip sponsored segments",
                ],
                "settings": {
                    "privacy.trackingprotection.enabled": True,
                    "privacy.trackingprotection.socialtracking.enabled": True,
                    "dom.security.https_only_mode": True,
                    "browser.compactmode.show": True,
                    "browser.tabs.closeWindowWithLastTab": False,
                    "browser.download.useDownloadDir": False,
                    "media.videocontrols.picture-in-picture.enabled": True,
                },
                "preview": """
┌─ Firefox ────────────────────────────────┐
│ 🔒 https://example.com                   │
│ ┌──────┬────────┬─────────┐            │
│ │ Work │ Social │ Shopping │ ← Containers│
│ └──────┴────────┴─────────┘            │
│  Enhanced tracking protection active ✓   │
└──────────────────────────────────────────┘
                """,
                "help": "These Firefox settings prioritize privacy and security while maintaining usability. Container tabs help separate work/personal browsing, and the extensions block ads and trackers for a cleaner browsing experience.",
            },
            "vlc": {
                "name": "VLC Media Player",
                "description": "Universal media player with smart defaults",
                "features": [
                    "Hardware acceleration for smooth playback",
                    "Remember playback position",
                    "Auto-load subtitles from folder",
                    "Minimal interface mode",
                    "Network stream support",
                    "Audio normalization",
                ],
                "settings": {
                    "video.hardware-acceleration": "auto",
                    "resume-playback": True,
                    "sub-autodetect-file": True,
                    "audio.volume-normalization": True,
                    "interface.minimal-view": True,
                    "skip-frames": True,
                },
                "shortcuts": {
                    "Space": "Play/Pause",
                    "F": "Fullscreen",
                    "M": "Mute",
                    "Shift+Right": "Jump forward 1 min",
                    "Shift+Left": "Jump back 1 min",
                },
                "help": "These VLC settings optimize media playback for modern systems. Hardware acceleration improves performance, and the configured shortcuts provide quick access to common functions.",
            },
            "thunderbird": {
                "name": "Thunderbird Email",
                "description": "Professional email client with productivity features",
                "features": [
                    "Unified inbox for multiple accounts",
                    "Conversation threading",
                    "Quick filter toolbar",
                    "Calendar integration",
                    "Dark theme support",
                    "Spam filtering",
                ],
                "settings": {
                    "mail.thread_pane.use_correspondents": True,
                    "mail.adaptive_junk_mail": True,
                    "calendar.integration.notify": True,
                    "mail.compose.attachment_reminder": True,
                    "mail.tabs.autoHide": False,
                },
                "help": "These Thunderbird settings improve email productivity with conversation threading, better spam detection, and helpful reminders for attachments.",
            },
            "libreoffice": {
                "name": "LibreOffice Suite",
                "description": "Office productivity with modern defaults",
                "features": [
                    "Microsoft Office compatibility mode",
                    "Auto-save every 10 minutes",
                    "Modern icon theme",
                    "Sidebar enabled by default",
                    "PDF export optimizations",
                    "Grammar checking enabled",
                ],
                "settings": {
                    "save.auto_save": True,
                    "save.auto_save_interval": 10,
                    "ui.icon_theme": "breeze",
                    "compatibility.ms_format_default": True,
                    "tools.grammar_checking": True,
                },
                "help": "These LibreOffice settings improve compatibility with Microsoft Office files and add modern conveniences like auto-save and grammar checking.",
            },
            "system": {
                "name": "System Preferences",
                "description": "Comprehensive system-wide customizations for optimal UX",
                "features": [
                    "Mouse and touchpad optimization",
                    "Natural scrolling and gesture configuration",
                    "Clipboard management with history",
                    "Multi-workspace productivity setup",
                    "Smart notification management",
                    "Window tiling and management",
                    "Display scaling and font optimization",
                    "Keyboard shortcuts and accessibility",
                    "Power management profiles",
                    "Night light and blue light filtering",
                ],
                "mouse_touchpad": {
                    "natural_scrolling": "Ask user preference",
                    "tap_to_click": True,
                    "two_finger_right_click": True,
                    "three_finger_middle_click": True,
                    "scroll_speed": "medium",
                    "pointer_speed": "medium",
                    "pointer_acceleration": "adaptive",
                    "click_method": "default",
                    "disable_while_typing": True,
                    "edge_scrolling": False,
                    "horizontal_scrolling": True,
                    "palm_detection": True,
                    "mouse_scroll_direction": "natural",
                },
                "keyboard": {
                    "repeat_delay": 250,
                    "repeat_speed": 30,
                    "caps_lock_behavior": "escape",  # Popular with developers
                    "compose_key": "right_alt",
                    "numlock_on_startup": True,
                    "show_layout_indicator": True,
                    "switch_layout_shortcut": "Alt+Shift",
                    "accessibility_sticky_keys": False,
                    "accessibility_slow_keys": False,
                    "accessibility_bounce_keys": False,
                },
                "clipboard": {
                    "history_size": 50,
                    "auto_clear_after_hours": 24,
                    "middle_click_paste": True,
                    "sync_clipboard_selection": True,
                    "exclude_passwords": True,
                    "show_thumbnails": True,
                    "private_mode_shortcut": "Ctrl+Alt+P",
                },
                "workspaces": {
                    "number_of_workspaces": 4,
                    "dynamic_workspaces": True,
                    "workspaces_on_all_displays": True,
                    "switch_animation": "slide",
                    "wraparound_switching": True,
                    "auto_move_windows": True,
                    "show_workspace_indicator": True,
                    "workspace_switcher_popup": True,
                },
                "notifications": {
                    "show_banners": True,
                    "show_in_lock_screen": False,
                    "show_details_in_lock_screen": False,
                    "notification_timeout": 5,
                    "do_not_disturb_schedule": False,
                    "dnd_start_hour": 22,
                    "dnd_end_hour": 8,
                    "show_notification_count": True,
                    "play_sounds": True,
                    "priority_notifications": ["calls", "alarms", "calendar"],
                    "group_notifications": True,
                },
                "window_management": {
                    "auto_maximize": False,
                    "auto_raise": False,
                    "click_to_focus": True,
                    "focus_follows_mouse": False,
                    "raise_on_focus": True,
                    "window_snapping": True,
                    "edge_tiling": True,
                    "quarter_tiling": True,
                    "show_window_thumbnails": True,
                    "alt_tab_current_workspace": False,
                    "window_switcher_style": "thumbnail",
                    "minimize_animation": "genie",
                },
                "display": {
                    "scale_factor": 1.0,
                    "font_scaling": 1.0,
                    "night_light_enabled": True,
                    "night_light_temperature": 4000,
                    "night_light_schedule": "sunset-to-sunrise",
                    "night_light_manual_start": 20,
                    "night_light_manual_end": 6,
                    "auto_brightness": True,
                    "screen_blank_timeout": 15,
                    "lock_screen_timeout": 5,
                    "show_battery_percentage": True,
                    "show_weekday_in_clock": True,
                    "show_date_in_clock": True,
                    "show_seconds_in_clock": False,
                    "clock_format": "12h",
                },
                "fonts": {
                    "interface_font": "Ubuntu",
                    "document_font": "Sans",
                    "monospace_font": "Ubuntu Mono",
                    "font_antialiasing": "grayscale",
                    "font_hinting": "slight",
                    "font_size_interface": 11,
                    "font_size_document": 11,
                    "font_size_monospace": 11,
                    "font_size_window_title": 11,
                },
                "accessibility": {
                    "high_contrast": False,
                    "large_text": False,
                    "screen_reader": False,
                    "magnifier": False,
                    "on_screen_keyboard": False,
                    "visual_bell": False,
                    "sticky_keys": False,
                    "slow_keys": False,
                    "bounce_keys": False,
                    "mouse_keys": False,
                    "reduce_animation": False,
                },
                "shortcuts": {
                    "Super+T": "Open terminal",
                    "Super+E": "Open file manager",
                    "Alt+Space": "Application launcher",
                    "Super+L": "Lock screen",
                    "Super+D": "Show desktop",
                    "Ctrl+Alt+Arrow": "Switch workspace",
                    "Super+Arrow": "Window tiling",
                    "Alt+F2": "Run command",
                    "Alt+F4": "Close window",
                    "Ctrl+Alt+T": "Open terminal",
                    "Super+P": "Display settings",
                    "Super+A": "Show applications",
                    "Super+M": "Show notification tray",
                    "Print": "Screenshot",
                    "Shift+Print": "Screenshot area",
                    "Alt+Print": "Screenshot window",
                    "Super+V": "Show clipboard history",
                    "Super+Space": "Switch input source",
                    "Ctrl+Alt+Del": "Log out",
                    "Super+H": "Hide window",
                    "Super+Up": "Maximize window",
                    "Super+Down": "Restore/minimize window",
                    "Super+Left": "Tile window left",
                    "Super+Right": "Tile window right",
                    "Alt+Tab": "Switch applications",
                    "Alt+Shift+Tab": "Switch applications reverse",
                    "Super+Tab": "Switch windows",
                    "Ctrl+Alt+O": "Turn on screen reader",
                    "Super+Plus": "Zoom in",
                    "Super+Minus": "Zoom out",
                },
                "power": {
                    "lid_close_battery": "suspend",
                    "lid_close_ac": "nothing",
                    "auto_suspend_battery": 15,
                    "auto_suspend_ac": "never",
                    "screen_brightness_battery": 70,
                    "screen_brightness_ac": 100,
                    "keyboard_brightness_battery": 50,
                    "keyboard_brightness_ac": 100,
                    "wifi_power_saving": True,
                    "bluetooth_power_saving": True,
                    "usb_power_saving": True,
                    "cpu_governor_battery": "powersave",
                    "cpu_governor_ac": "performance",
                    "show_power_button": True,
                    "power_button_action": "interactive",
                    "critical_battery_action": "hibernate",
                    "low_battery_threshold": 10,
                },
                "dock_panel": {
                    "position": "bottom",
                    "size": "medium",
                    "auto_hide": False,
                    "dodge_windows": False,
                    "extend_to_edge": False,
                    "show_mounts": True,
                    "show_trash": True,
                    "show_running_apps": True,
                    "click_action": "cycle-windows",
                    "scroll_action": "cycle-windows",
                    "middle_click_action": "new-window",
                    "transparency": "fixed",
                    "background_opacity": 0.8,
                    "customize_theme": True,
                    "show_favorites": True,
                    "isolate_workspaces": False,
                    "isolate_monitors": False,
                    "hot_keys": True,
                    "show_applications_button": True,
                    "animation": True,
                },
                "privacy": {
                    "hide_identity": False,
                    "show_full_name_in_top_bar": False,
                    "remember_recent_files": True,
                    "recent_files_max_age": 30,
                    "clear_recent_files_on_logout": False,
                    "disable_microphone": False,
                    "disable_camera": False,
                    "location_services": False,
                    "usage_reporting": False,
                    "problem_reporting": True,
                    "clear_trash_automatically": False,
                    "clear_temp_files_automatically": True,
                    "file_history_enabled": True,
                    "retain_file_history_days": 30,
                },
                "help": "These comprehensive system settings optimize your Ubuntu desktop for productivity and usability. From mouse sensitivity to clipboard management, workspace configuration to notification control, these settings create a personalized and efficient desktop environment. Each setting is carefully chosen based on common user preferences and productivity best practices.",
            },
        }

    def get_app_config(
        self, app_name: str, user_type: str = "developer"
    ) -> Dict[str, Any]:
        """Get configuration for a specific application"""
        apps = self.developer_apps if user_type == "developer" else self.user_apps
        return apps.get(app_name, {})

    def get_all_apps(self, user_type: str = "developer") -> List[str]:
        """Get list of all available applications"""
        apps = self.developer_apps if user_type == "developer" else self.user_apps
        return list(apps.keys())

    def generate_config_files(
        self, app_name: str, settings: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate configuration file contents for an application"""
        generators = {
            "vscode": self._generate_vscode_config,
            "git": self._generate_git_config,
            "terminal": self._generate_terminal_config,
            "firefox": self._generate_firefox_config,
        }

        generator = generators.get(app_name)
        if generator:
            return generator(settings)
        return {}

    def _generate_vscode_config(self, settings: Dict[str, Any]) -> Dict[str, str]:
        """Generate VS Code settings.json"""
        import json

        config = {
            "settings.json": json.dumps(settings.get("settings", {}), indent=2),
            "extensions.txt": "\n".join(
                [
                    ext.split(" - ")[0].lower().replace(" ", "-")
                    for ext in settings.get("extensions", [])
                ]
            ),
        }
        return config

    def _generate_git_config(self, settings: Dict[str, Any]) -> Dict[str, str]:
        """Generate .gitconfig content"""
        config_lines = ["[user]", "\tname = ", "\temail = ", ""]

        # Add aliases
        config_lines.append("[alias]")
        for alias, command in settings.get("aliases", {}).items():
            config_lines.append(f"\t{alias} = {command}")

        # Add settings
        for key, value in settings.get("settings", {}).items():
            section, option = key.split(".", 1)
            if f"[{section}]" not in config_lines:
                config_lines.append(f"\n[{section}]")
            config_lines.append(f"\t{option} = {value}")

        return {".gitconfig": "\n".join(config_lines)}

    def _generate_terminal_config(self, settings: Dict[str, Any]) -> Dict[str, str]:
        """Generate shell configuration"""
        zshrc_lines = ["# Ubuntu Bootstrap Terminal Configuration", ""]

        # Add aliases
        zshrc_lines.append("# Aliases")
        for alias, command in settings.get("aliases", {}).items():
            zshrc_lines.append(f"alias {alias}='{command}'")

        return {".zshrc": "\n".join(zshrc_lines)}

    def _generate_firefox_config(self, settings: Dict[str, Any]) -> Dict[str, str]:
        """Generate Firefox user.js preferences"""
        prefs_lines = ["// Ubuntu Bootstrap Firefox Configuration", ""]

        for pref, value in settings.get("settings", {}).items():
            if isinstance(value, bool):
                value_str = "true" if value else "false"
            elif isinstance(value, str):
                value_str = f'"{value}"'
            else:
                value_str = str(value)
            prefs_lines.append(f'user_pref("{pref}", {value_str});')

        return {"user.js": "\n".join(prefs_lines)}


# Helper function for external use
def get_app_defaults():
    """Factory function to create AppDefaults instance"""
    return AppDefaults()
