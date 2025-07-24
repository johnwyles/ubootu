#!/usr/bin/env python3
"""
Desktop environment menu for the Ubootu TUI
"""

from typing import Dict
from lib.tui.menus.base import MenuBuilder, MenuItem


class DesktopMenuBuilder(MenuBuilder):
    """Builds the desktop environment menu section"""
    
    def build(self) -> Dict[str, MenuItem]:
        """Build desktop menu structure"""
        self.items.clear()
        
        # Main desktop category
        self.add_category(
            "desktop", "Desktop Environment", 
            "Window managers, themes, customization",
            parent="root",
            children=["desktop-env", "window-managers", "desktop-themes", "desktop-settings"]
        )
        
        # Desktop subcategories
        self._build_desktop_environments()
        self._build_window_managers()
        self._build_themes()
        self._build_settings()
        
        return self.items
    
    def _build_desktop_environments(self):
        """Build desktop environment selection menu"""
        self.add_category(
            "desktop-env", "Desktop Environment", 
            "Choose your desktop environment",
            parent="desktop",
            children=["gnome", "kde", "xfce", "mate", "cinnamon"]
        )
        
        # Desktop environment items
        self.add_selectable("gnome", "GNOME", 
            "Default Ubuntu desktop",
            parent="desktop-env")
        
        self.add_selectable("kde", "KDE Plasma", 
            "Feature-rich desktop environment",
            parent="desktop-env")
        
        self.add_selectable("xfce", "XFCE", 
            "Lightweight desktop environment",
            parent="desktop-env")
        
        self.add_selectable("mate", "MATE", 
            "Traditional desktop environment",
            parent="desktop-env")
        
        self.add_selectable("cinnamon", "Cinnamon", 
            "Modern desktop environment",
            parent="desktop-env")
    
    def _build_window_managers(self):
        """Build window managers menu"""
        self.add_category(
            "window-managers", "🪟 Window Managers", 
            "Tiling and compositing window managers",
            parent="desktop",
            children=["wm-wayland", "wm-x11"]
        )
        
        # Wayland compositors
        self.add_category(
            "wm-wayland", "Wayland Compositors", 
            "Modern Wayland-based window managers",
            parent="window-managers",
            children=["hyprland", "sway", "river", "wayfire"]
        )
        
        self.add_selectable("hyprland", "Hyprland", 
            "Dynamic tiling Wayland compositor with animations",
            parent="wm-wayland", ansible_var="de_hyprland_enabled")
        
        self.add_selectable("sway", "Sway", 
            "i3-compatible Wayland compositor",
            parent="wm-wayland", ansible_var="de_sway_enabled")
        
        self.add_selectable("river", "River", 
            "Dynamic tiling Wayland compositor",
            parent="wm-wayland", ansible_var="de_river_enabled")
        
        self.add_selectable("wayfire", "Wayfire", 
            "3D Wayland compositor with effects",
            parent="wm-wayland", ansible_var="de_wayfire_enabled")
        
        # X11 window managers
        self.add_category(
            "wm-x11", "X11 Window Managers", 
            "Traditional X11-based window managers",
            parent="window-managers",
            children=["i3", "awesome", "bspwm", "dwm", "openbox", "qtile"]
        )
        
        self.add_selectable("i3", "i3", 
            "Popular tiling window manager",
            parent="wm-x11", ansible_var="de_i3_enabled")
        
        self.add_selectable("awesome", "Awesome", 
            "Highly configurable framework WM",
            parent="wm-x11", ansible_var="de_awesome_enabled")
        
        self.add_selectable("bspwm", "bspwm", 
            "Binary space partitioning WM",
            parent="wm-x11", ansible_var="de_bspwm_enabled")
        
        self.add_selectable("dwm", "dwm", 
            "Dynamic window manager (suckless)",
            parent="wm-x11", ansible_var="de_dwm_enabled")
        
        self.add_selectable("openbox", "Openbox", 
            "Lightweight floating window manager",
            parent="wm-x11", ansible_var="de_openbox_enabled")
        
        self.add_selectable("qtile", "Qtile", 
            "Python-based tiling window manager",
            parent="wm-x11", ansible_var="de_qtile_enabled")
    
    def _build_themes(self):
        """Build themes and appearance menu"""
        self.add_category(
            "desktop-themes", "🎨 Themes & Appearance", 
            "Complete visual customization",
            parent="desktop",
            children=["global-theme", "fonts-installation", "wallpaper-collections", "shell-prompts", 
                      "icon-themes", "cursor-themes", "terminal-themes"]
        )
        
        # Global theme selection
        self.add_configurable(
            "global-theme", "🌐 Global Theme", 
            "Apply theme system-wide",
            parent="desktop-themes",
            config_type="dropdown",
            config_value="dracula",
            config_options=[
                ("dracula", "Dracula - Dark elegant theme"),
                ("catppuccin-mocha", "Catppuccin Mocha - Soothing pastel dark"),
                ("catppuccin-latte", "Catppuccin Latte - Soothing pastel light"),
                ("nord", "Nord - Arctic blue palette"),
                ("gruvbox-dark", "Gruvbox Dark - Retro warm colors"),
                ("gruvbox-light", "Gruvbox Light - Retro warm light"),
                ("solarized-dark", "Solarized Dark - Precision colors"),
                ("solarized-light", "Solarized Light - Precision light"),
                ("tokyo-night", "Tokyo Night - Modern dark theme"),
                ("one-dark", "One Dark - Atom-inspired dark"),
                ("material", "Material - Google Material Design"),
                ("monokai-pro", "Monokai Pro - Vibrant colors"),
                ("default", "System Default")
            ],
            ansible_var="themes_system_theme"
        )
        
        # Font subcategories
        self._build_fonts()
        self._build_wallpapers()
        self._build_shell_prompts()
        self._build_icon_themes()
        self._build_cursor_themes()
        self._build_terminal_themes()
    
    def _build_fonts(self):
        """Build fonts and typography menu"""
        self.add_category(
            "fonts-installation", "🔤 Fonts & Typography", 
            "Professional coding fonts",
            parent="desktop-themes",
            children=["nerd-fonts-pack", "font-size-scaling", "font-rendering"]
        )
        
        self.add_configurable(
            "nerd-fonts-pack", "Nerd Fonts Collection", 
            "JetBrains Mono, Hack, FiraCode, etc.",
            parent="fonts-installation",
            config_type="dropdown",
            config_value="jetbrains-mono",
            config_options=[
                ("jetbrains-mono", "JetBrains Mono - Modern coding font"),
                ("hack", "Hack - Source code font"),
                ("fira-code", "Fira Code - Font with ligatures"),
                ("cascadia-code", "Cascadia Code - Microsoft font"),
                ("source-code-pro", "Source Code Pro - Adobe font"),
                ("ubuntu-mono", "Ubuntu Mono - Ubuntu default"),
                ("inconsolata", "Inconsolata - Monospace font"),
                ("meslo", "Meslo LG - Customized Menlo")
            ],
            ansible_var="fonts_nerd_font_selection"
        )
        
        self.add_configurable(
            "font-size-scaling", "Font Size Scaling", 
            "Global font size adjustment",
            parent="fonts-installation",
            config_type="slider",
            config_range=(80, 150), config_value=100, config_unit="%",
            ansible_var="fonts_global_scaling"
        )
        
        self.add_configurable(
            "font-rendering", "Font Rendering", 
            "Optimize font display",
            parent="fonts-installation",
            config_type="dropdown",
            config_value="subpixel",
            config_options=[
                ("subpixel", "Subpixel (Best for LCD)"),
                ("grayscale", "Grayscale (Sharp)"),
                ("none", "No antialiasing")
            ],
            ansible_var="fonts_rendering_mode"
        )
    
    def _build_wallpapers(self):
        """Build wallpaper collections menu"""
        self.add_category(
            "wallpaper-collections", "🌄 Wallpaper Collections", 
            "Curated wallpaper packs",
            parent="desktop-themes",
            children=["wallpaper-abstract", "wallpaper-nature", "wallpaper-space", 
                      "wallpaper-minimal", "wallpaper-dynamic"]
        )
        
        self.add_selectable("wallpaper-abstract", "Abstract Minimal", 
            "Geometric and abstract designs",
            parent="wallpaper-collections", ansible_var="wallpaper_pack_abstract")
        
        self.add_selectable("wallpaper-nature", "Nature Photography", 
            "Landscapes and nature scenes",
            parent="wallpaper-collections", ansible_var="wallpaper_pack_nature")
        
        self.add_selectable("wallpaper-space", "Space & Astronomy", 
            "Cosmos and celestial imagery",
            parent="wallpaper-collections", ansible_var="wallpaper_pack_space")
        
        self.add_selectable("wallpaper-minimal", "Minimal & Clean", 
            "Simple, clean backgrounds",
            parent="wallpaper-collections", ansible_var="wallpaper_pack_minimal")
        
        self.add_selectable("wallpaper-dynamic", "Dynamic Wallpapers", 
            "Time-based changing wallpapers",
            parent="wallpaper-collections", ansible_var="wallpaper_dynamic_enabled")
    
    def _build_shell_prompts(self):
        """Build shell prompt themes menu"""
        self.add_category(
            "shell-prompts", "💻 Shell Prompts", 
            "Terminal prompt frameworks",
            parent="desktop-themes",
            children=["prompt-starship", "prompt-ohmyposh", "prompt-pure", 
                      "prompt-spaceship", "prompt-powerlevel10k"]
        )
        
        self.add_selectable("prompt-starship", "Starship", 
            "Fast, customizable, cross-shell prompt",
            parent="shell-prompts", ansible_var="shell_prompt_starship")
        
        self.add_selectable("prompt-ohmyposh", "Oh My Posh", 
            "Powerful prompt theme engine",
            parent="shell-prompts", ansible_var="shell_prompt_ohmyposh")
        
        self.add_selectable("prompt-pure", "Pure", 
            "Minimal and fast ZSH prompt",
            parent="shell-prompts", ansible_var="shell_prompt_pure")
        
        self.add_selectable("prompt-spaceship", "Spaceship", 
            "Minimalistic ZSH prompt",
            parent="shell-prompts", ansible_var="shell_prompt_spaceship")
        
        self.add_selectable("prompt-powerlevel10k", "Powerlevel10k", 
            "Feature-rich ZSH theme",
            parent="shell-prompts", ansible_var="shell_prompt_p10k")
    
    def _build_icon_themes(self):
        """Build icon themes menu"""
        self.add_category(
            "icon-themes", "🎯 Icon Themes", 
            "System icon packs",
            parent="desktop-themes",
            children=["icons-papirus", "icons-numix", "icons-flatremix", "icons-tela"]
        )
        
        self.add_selectable("icons-papirus", "Papirus Icons", 
            "Modern flat icon theme",
            parent="icon-themes", ansible_var="icon_theme_papirus")
        
        self.add_selectable("icons-numix", "Numix Icons", 
            "Circle icon theme",
            parent="icon-themes", ansible_var="icon_theme_numix")
        
        self.add_selectable("icons-flatremix", "Flat Remix Icons", 
            "Colorful flat icons",
            parent="icon-themes", ansible_var="icon_theme_flatremix")
        
        self.add_selectable("icons-tela", "Tela Icons", 
            "Material design icons",
            parent="icon-themes", ansible_var="icon_theme_tela")
    
    def _build_cursor_themes(self):
        """Build cursor themes menu"""
        self.add_category(
            "cursor-themes", "🖱️ Cursor Themes", 
            "Mouse cursor styles",
            parent="desktop-themes",
            children=["cursor-breeze", "cursor-bibata", "cursor-capitaine"]
        )
        
        self.add_selectable("cursor-breeze", "Breeze Cursors", 
            "KDE default cursors",
            parent="cursor-themes", ansible_var="cursor_theme_breeze")
        
        self.add_selectable("cursor-bibata", "Bibata Cursors", 
            "Modern animated cursors",
            parent="cursor-themes", ansible_var="cursor_theme_bibata")
        
        self.add_selectable("cursor-capitaine", "Capitaine Cursors", 
            "macOS-inspired cursors",
            parent="cursor-themes", ansible_var="cursor_theme_capitaine")
    
    def _build_terminal_themes(self):
        """Build terminal color schemes menu"""
        self.add_category(
            "terminal-themes", "🖥️ Terminal Themes", 
            "Terminal color schemes",
            parent="desktop-themes",
            children=["term-dracula", "term-catppuccin", "term-nord", "term-gruvbox"]
        )
        
        self.add_selectable("term-dracula", "Dracula Terminal", 
            "Dark theme for terminal",
            parent="terminal-themes", ansible_var="terminal_theme_dracula")
        
        self.add_selectable("term-catppuccin", "Catppuccin Terminal", 
            "Soothing pastel theme",
            parent="terminal-themes", ansible_var="terminal_theme_catppuccin")
        
        self.add_selectable("term-nord", "Nord Terminal", 
            "Arctic color palette",
            parent="terminal-themes", ansible_var="terminal_theme_nord")
        
        self.add_selectable("term-gruvbox", "Gruvbox Terminal", 
            "Retro groove colors",
            parent="terminal-themes", ansible_var="terminal_theme_gruvbox")
    
    def _build_settings(self):
        """Build desktop settings menu"""
        self.add_category(
            "desktop-settings", "🎛️ System Settings", 
            "Comprehensive system customization",
            parent="desktop",
            children=["mouse-touchpad", "keyboard-input", "displays", "notifications", "power-management", 
                      "window-management", "desktop-effects", "panel-taskbar", "fonts-text", "sound-audio"]
        )
        
        # Build all settings subcategories
        self._build_mouse_touchpad_settings()
        self._build_keyboard_settings()
        self._build_display_settings()
        self._build_notification_settings()
        self._build_power_settings()
        self._build_window_settings()
        self._build_effects_settings()
        self._build_panel_settings()
        self._build_font_settings()
        self._build_sound_settings()
    
    def _build_mouse_touchpad_settings(self):
        """Build mouse and touchpad settings menu"""
        self.add_category(
            "mouse-touchpad", "🖱️ Mouse & Touchpad", 
            "Pointer device configuration",
            parent="desktop-settings",
            children=["mouse-speed", "mouse-acceleration", "scroll-speed", "natural-scroll",
                      "touchpad-tap-click", "touchpad-two-finger", "touchpad-edge-scroll", 
                      "touchpad-gestures", "touchpad-disable-typing"]
        )
        
        self.add_configurable(
            "mouse-speed", "Mouse Speed", 
            "Pointer movement speed",
            parent="mouse-touchpad",
            config_type="slider",
            config_range=(-10, 10), config_value=0, config_unit="",
            ansible_var="de_mouse_speed"
        )
        
        self.add_configurable(
            "mouse-acceleration", "Mouse Acceleration", 
            "Enable adaptive pointer speed",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=True,
            ansible_var="de_mouse_acceleration"
        )
        
        self.add_configurable(
            "scroll-speed", "Scroll Speed", 
            "Mouse wheel scroll speed",
            parent="mouse-touchpad",
            config_type="slider",
            config_range=(1, 20), config_value=10, config_unit="",
            ansible_var="de_scroll_speed"
        )
        
        self.add_configurable(
            "natural-scroll", "Natural Scrolling", 
            "Reverse scroll direction",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=False,
            ansible_var="de_natural_scroll"
        )
        
        self.add_configurable(
            "touchpad-tap-click", "Tap to Click", 
            "Tap touchpad to click",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=True,
            ansible_var="de_touchpad_tap_to_click"
        )
        
        self.add_configurable(
            "touchpad-two-finger", "Two-Finger Scrolling", 
            "Scroll with two fingers",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=True,
            ansible_var="de_touchpad_two_finger_scroll"
        )
        
        self.add_configurable(
            "touchpad-edge-scroll", "Edge Scrolling", 
            "Scroll at touchpad edge",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=False,
            ansible_var="de_touchpad_edge_scroll"
        )
        
        self.add_configurable(
            "touchpad-gestures", "Multi-touch Gestures", 
            "Enable touchpad gestures",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=True,
            ansible_var="de_touchpad_gestures"
        )
        
        self.add_configurable(
            "touchpad-disable-typing", "Disable While Typing", 
            "Disable touchpad while typing",
            parent="mouse-touchpad",
            config_type="toggle",
            config_value=True,
            ansible_var="de_touchpad_disable_while_typing"
        )
    
    def _build_keyboard_settings(self):
        """Build keyboard settings menu"""
        self.add_category(
            "keyboard-input", "⌨️ Keyboard", 
            "Keyboard settings and shortcuts",
            parent="desktop-settings",
            children=["key-repeat-delay", "key-repeat-rate", "compose-key", "caps-lock-behavior",
                      "media-keys", "super-key-action", "custom-shortcuts"]
        )
        
        self.add_configurable(
            "key-repeat-delay", "Key Repeat Delay", 
            "Delay before key repeat",
            parent="keyboard-input",
            config_type="slider",
            config_range=(100, 1000), config_value=500, config_unit="ms",
            ansible_var="de_key_repeat_delay"
        )
        
        self.add_configurable(
            "key-repeat-rate", "Key Repeat Rate", 
            "Speed of key repeat",
            parent="keyboard-input",
            config_type="slider",
            config_range=(10, 100), config_value=30, config_unit="/s",
            ansible_var="de_key_repeat_interval"
        )
        
        self.add_configurable(
            "compose-key", "Compose Key", 
            "Key for special characters",
            parent="keyboard-input",
            config_type="dropdown",
            config_value="",
            config_options=[
                ("", "Disabled"),
                ("ralt", "Right Alt"),
                ("rctrl", "Right Ctrl"),
                ("caps", "Caps Lock"),
                ("menu", "Menu Key")
            ],
            ansible_var="de_compose_key"
        )
        
        self.add_configurable(
            "caps-lock-behavior", "Caps Lock Behavior", 
            "Caps Lock key function",
            parent="keyboard-input",
            config_type="dropdown",
            config_value="caps",
            config_options=[
                ("caps", "Caps Lock"),
                ("ctrl", "Control"),
                ("escape", "Escape"),
                ("none", "Disabled")
            ],
            ansible_var="de_caps_lock_behavior"
        )
        
        self.add_configurable(
            "media-keys", "Media Keys", 
            "Enable media control keys",
            parent="keyboard-input",
            config_type="toggle",
            config_value=True,
            ansible_var="de_media_keys_enabled"
        )
        
        self.add_configurable(
            "super-key-action", "Super Key Action", 
            "Windows/Super key behavior",
            parent="keyboard-input",
            config_type="dropdown",
            config_value="overlay",
            config_options=[
                ("overlay", "Activities Overview"),
                ("menu", "Application Menu"),
                ("none", "Nothing")
            ],
            ansible_var="de_super_key_action"
        )
        
        self.add_selectable("custom-shortcuts", "Custom Shortcuts", 
            "Configure keyboard shortcuts",
            parent="keyboard-input")
    
    def _build_display_settings(self):
        """Build display settings menu"""
        self.add_category(
            "displays", "🖥️ Displays", 
            "Monitor and display configuration",
            parent="desktop-settings",
            children=["display-resolution", "display-scale", "refresh-rate", "fractional-scaling",
                      "night-light", "night-light-temp", "night-light-schedule", "multi-monitor"]
        )
        
        self.add_configurable(
            "display-resolution", "Display Resolution", 
            "Screen resolution",
            parent="displays",
            config_type="dropdown",
            config_value="auto",
            config_options=[
                ("auto", "Automatic"),
                ("1920x1080", "1920×1080 (Full HD)"),
                ("2560x1440", "2560×1440 (2K)"),
                ("3840x2160", "3840×2160 (4K)"),
                ("1366x768", "1366×768"),
                ("1600x900", "1600×900")
            ],
            ansible_var="de_display_resolution"
        )
        
        self.add_configurable(
            "display-scale", "Display Scaling", 
            "UI scaling factor",
            parent="displays",
            config_type="dropdown",
            config_value=1.0,
            config_options=[
                (1.0, "100%"),
                (1.25, "125%"),
                (1.5, "150%"),
                (2.0, "200%")
            ],
            ansible_var="de_display_scale"
        )
        
        self.add_configurable(
            "refresh-rate", "Refresh Rate", 
            "Display refresh rate",
            parent="displays",
            config_type="dropdown",
            config_value="auto",
            config_options=[
                ("auto", "Automatic"),
                ("60", "60 Hz"),
                ("75", "75 Hz"),
                ("120", "120 Hz"),
                ("144", "144 Hz"),
                ("240", "240 Hz")
            ],
            ansible_var="de_display_refresh_rate"
        )
        
        self.add_configurable(
            "fractional-scaling", "Fractional Scaling", 
            "Enable fractional scaling",
            parent="displays",
            config_type="toggle",
            config_value=False,
            ansible_var="de_fractional_scaling_enabled"
        )
        
        self.add_configurable(
            "night-light", "Night Light", 
            "Blue light filter",
            parent="displays",
            config_type="toggle",
            config_value=False,
            ansible_var="de_night_light_enabled"
        )
        
        self.add_configurable(
            "night-light-temp", "Night Light Temperature", 
            "Color temperature",
            parent="displays",
            config_type="slider",
            config_range=(1000, 6500), config_value=4000, config_unit="K",
            ansible_var="de_night_light_temperature"
        )
        
        self.add_configurable(
            "night-light-schedule", "Night Light Schedule", 
            "When to enable night light",
            parent="displays",
            config_type="dropdown",
            config_value="sunset-to-sunrise",
            config_options=[
                ("sunset-to-sunrise", "Sunset to Sunrise"),
                ("manual", "Manual Schedule")
            ],
            ansible_var="de_night_light_schedule"
        )
        
        self.add_configurable(
            "multi-monitor", "Multi-Monitor Mode", 
            "Multiple display configuration",
            parent="displays",
            config_type="dropdown",
            config_value="extend",
            config_options=[
                ("extend", "Extend Desktop"),
                ("mirror", "Mirror Displays"),
                ("single", "Single Display")
            ],
            ansible_var="de_multi_monitor_mode"
        )
    
    def _build_notification_settings(self):
        """Build notification settings menu"""
        self.add_category(
            "notifications", "🔔 Notifications", 
            "Alert and notification settings",
            parent="desktop-settings",
            children=["notif-position", "notif-duration", "notif-dnd", "notif-sounds",
                      "notif-lockscreen", "notif-bubbles", "notif-history", "urgent-hints"]
        )
        
        self.add_configurable(
            "notif-position", "Notification Position", 
            "Where notifications appear",
            parent="notifications",
            config_type="dropdown",
            config_value="top-right",
            config_options=[
                ("top-right", "Top Right"),
                ("top-left", "Top Left"),
                ("bottom-right", "Bottom Right"),
                ("bottom-left", "Bottom Left"),
                ("top-center", "Top Center"),
                ("bottom-center", "Bottom Center")
            ],
            ansible_var="de_notification_position"
        )
        
        self.add_configurable(
            "notif-duration", "Notification Duration", 
            "How long notifications show",
            parent="notifications",
            config_type="slider",
            config_range=(3, 30), config_value=5, config_unit="s",
            ansible_var="de_notification_duration"
        )
        
        self.add_configurable(
            "notif-dnd", "Do Not Disturb", 
            "Silence all notifications",
            parent="notifications",
            config_type="toggle",
            config_value=False,
            ansible_var="de_notification_dnd"
        )
        
        self.add_configurable(
            "notif-sounds", "Notification Sounds", 
            "Play sounds for notifications",
            parent="notifications",
            config_type="toggle",
            config_value=True,
            ansible_var="de_notification_sounds"
        )
        
        self.add_configurable(
            "notif-lockscreen", "Show on Lock Screen", 
            "Display notifications when locked",
            parent="notifications",
            config_type="toggle",
            config_value=False,
            ansible_var="de_notification_show_in_lock_screen"
        )
        
        self.add_configurable(
            "notif-bubbles", "Notification Bubbles", 
            "Show notification popups",
            parent="notifications",
            config_type="toggle",
            config_value=True,
            ansible_var="de_notification_bubble_enabled"
        )
        
        self.add_configurable(
            "notif-history", "Notification History", 
            "Keep notification history",
            parent="notifications",
            config_type="toggle",
            config_value=True,
            ansible_var="de_notification_history_enabled"
        )
        
        self.add_configurable(
            "urgent-hints", "Urgent Window Hints", 
            "Flash windows needing attention",
            parent="notifications",
            config_type="toggle",
            config_value=True,
            ansible_var="de_urgent_window_hint"
        )
    
    def _build_power_settings(self):
        """Build power management settings menu"""
        self.add_category(
            "power-management", "🔋 Power Management", 
            "Energy and power settings",
            parent="desktop-settings",
            children=["lid-close-action", "power-button", "idle-delay", "screen-blank",
                      "screen-lock", "lock-delay", "lock-on-suspend"]
        )
        
        self.add_configurable(
            "lid-close-action", "Lid Close Action", 
            "Action when laptop lid closes",
            parent="power-management",
            config_type="dropdown",
            config_value="suspend",
            config_options=[
                ("suspend", "Suspend"),
                ("hibernate", "Hibernate"),
                ("shutdown", "Shutdown"),
                ("nothing", "Do Nothing"),
                ("logout", "Log Out")
            ],
            ansible_var="de_laptop_lid_close_action"
        )
        
        self.add_configurable(
            "power-button", "Power Button Action", 
            "Action when power button pressed",
            parent="power-management",
            config_type="dropdown",
            config_value="interactive",
            config_options=[
                ("interactive", "Ask What to Do"),
                ("suspend", "Suspend"),
                ("hibernate", "Hibernate"),
                ("shutdown", "Shutdown"),
                ("nothing", "Do Nothing")
            ],
            ansible_var="de_power_button_action"
        )
        
        self.add_configurable(
            "idle-delay", "Idle Timeout", 
            "Time before system sleeps",
            parent="power-management",
            config_type="slider",
            config_range=(0, 3600), config_value=900, config_unit="s",
            ansible_var="de_idle_delay"
        )
        
        self.add_configurable(
            "screen-blank", "Screen Blank Delay", 
            "Time before screen turns off",
            parent="power-management",
            config_type="slider",
            config_range=(0, 900), config_value=300, config_unit="s",
            ansible_var="de_screen_blank_delay"
        )
        
        self.add_configurable(
            "screen-lock", "Automatic Screen Lock", 
            "Lock screen automatically",
            parent="power-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_screen_lock_enabled"
        )
        
        self.add_configurable(
            "lock-delay", "Lock Delay After Blank", 
            "Time after blank to lock",
            parent="power-management",
            config_type="slider",
            config_range=(0, 300), config_value=0, config_unit="s",
            ansible_var="de_screen_lock_delay"
        )
        
        self.add_configurable(
            "lock-on-suspend", "Lock on Suspend", 
            "Lock screen when suspending",
            parent="power-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_lock_on_suspend"
        )
    
    def _build_window_settings(self):
        """Build window management settings menu"""
        self.add_category(
            "window-management", "🪟 Windows & Workspaces", 
            "Window behavior and workspaces",
            parent="desktop-settings",
            children=["window-snapping", "window-tiling", "focus-mode", "raise-on-click",
                      "workspaces-enable", "workspace-number", "workspace-grid", "hot-corners"]
        )
        
        self.add_configurable(
            "window-snapping", "Window Snapping", 
            "Snap windows to edges",
            parent="window-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_window_snapping"
        )
        
        self.add_configurable(
            "window-tiling", "Window Tiling", 
            "Enable window tiling",
            parent="window-management",
            config_type="toggle",
            config_value=False,
            ansible_var="de_window_tiling"
        )
        
        self.add_configurable(
            "focus-mode", "Focus Mode", 
            "How windows gain focus",
            parent="window-management",
            config_type="dropdown",
            config_value="click",
            config_options=[
                ("click", "Click to Focus"),
                ("mouse", "Focus Follows Mouse")
            ],
            ansible_var="de_focus_mode"
        )
        
        self.add_configurable(
            "raise-on-click", "Raise on Click", 
            "Bring window to front on click",
            parent="window-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_raise_on_click"
        )
        
        self.add_configurable(
            "workspaces-enable", "Enable Workspaces", 
            "Use multiple workspaces",
            parent="window-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_workspaces_enabled"
        )
        
        self.add_configurable(
            "workspace-number", "Number of Workspaces", 
            "How many workspaces",
            parent="window-management",
            config_type="slider",
            config_range=(1, 9), config_value=4, config_unit="",
            ansible_var="de_workspaces_number"
        )
        
        self.add_configurable(
            "workspace-grid", "Workspace Grid Layout", 
            "2D grid vs linear layout",
            parent="window-management",
            config_type="toggle",
            config_value=False,
            ansible_var="de_workspace_grid"
        )
        
        self.add_configurable(
            "hot-corners", "Hot Corners", 
            "Enable screen corner actions",
            parent="window-management",
            config_type="toggle",
            config_value=True,
            ansible_var="de_hot_corners_enabled"
        )
    
    def _build_effects_settings(self):
        """Build desktop effects settings menu"""
        self.add_category(
            "desktop-effects", "✨ Effects & Animations", 
            "Visual effects and animations",
            parent="desktop-settings",
            children=["animations-enable", "animation-speed", "transparency", "blur-effects",
                      "window-shadows", "minimize-anim", "maximize-anim", "compositor"]
        )
        
        self.add_configurable(
            "animations-enable", "Enable Animations", 
            "Desktop animations",
            parent="desktop-effects",
            config_type="toggle",
            config_value=True,
            ansible_var="de_animations_enabled"
        )
        
        self.add_configurable(
            "animation-speed", "Animation Speed", 
            "Speed of animations",
            parent="desktop-effects",
            config_type="slider",
            config_range=(1, 50), config_value=10, config_unit="",
            ansible_var="de_animation_speed"
        )
        
        self.add_configurable(
            "transparency", "Transparency Effects", 
            "Enable window transparency",
            parent="desktop-effects",
            config_type="toggle",
            config_value=True,
            ansible_var="de_transparency_enabled"
        )
        
        self.add_configurable(
            "blur-effects", "Blur Effects", 
            "Enable blur behind windows",
            parent="desktop-effects",
            config_type="toggle",
            config_value=True,
            ansible_var="de_blur_enabled"
        )
        
        self.add_configurable(
            "window-shadows", "Window Shadows", 
            "Drop shadows on windows",
            parent="desktop-effects",
            config_type="toggle",
            config_value=True,
            ansible_var="de_window_shadows"
        )
        
        self.add_configurable(
            "minimize-anim", "Minimize Animation", 
            "Window minimize effect",
            parent="desktop-effects",
            config_type="dropdown",
            config_value="scale",
            config_options=[
                ("scale", "Scale"),
                ("fade", "Fade"),
                ("none", "None")
            ],
            ansible_var="de_minimize_animation"
        )
        
        self.add_configurable(
            "maximize-anim", "Maximize Animation", 
            "Window maximize effect",
            parent="desktop-effects",
            config_type="dropdown",
            config_value="scale",
            config_options=[
                ("scale", "Scale"),
                ("fade", "Fade"),
                ("none", "None")
            ],
            ansible_var="de_maximize_animation"
        )
        
        self.add_configurable(
            "compositor", "Enable Compositor", 
            "Desktop compositing effects",
            parent="desktop-effects",
            config_type="toggle",
            config_value=True,
            ansible_var="de_compositor_enabled"
        )
    
    def _build_panel_settings(self):
        """Build panel/taskbar settings menu"""
        self.add_category(
            "panel-taskbar", "📊 Panel & Taskbar", 
            "Panel/taskbar configuration",
            parent="desktop-settings",
            children=["panel-position", "panel-autohide", "panel-size", "panel-transparency",
                      "clock-format", "clock-date", "clock-seconds", "system-tray"]
        )
        
        self.add_configurable(
            "panel-position", "Panel Position", 
            "Where the panel appears",
            parent="panel-taskbar",
            config_type="dropdown",
            config_value="bottom",
            config_options=[
                ("top", "Top"),
                ("bottom", "Bottom"),
                ("left", "Left"),
                ("right", "Right")
            ],
            ansible_var="de_panel_position"
        )
        
        self.add_configurable(
            "panel-autohide", "Auto-hide Panel", 
            "Hide panel when not in use",
            parent="panel-taskbar",
            config_type="toggle",
            config_value=False,
            ansible_var="de_panel_autohide"
        )
        
        self.add_configurable(
            "panel-size", "Panel Size", 
            "Height/width of panel",
            parent="panel-taskbar",
            config_type="slider",
            config_range=(24, 128), config_value=48, config_unit="px",
            ansible_var="de_panel_size"
        )
        
        self.add_configurable(
            "panel-transparency", "Panel Transparency", 
            "Panel opacity level",
            parent="panel-taskbar",
            config_type="slider",
            config_range=(0, 100), config_value=0, config_unit="%",
            ansible_var="de_panel_transparency"
        )
        
        self.add_configurable(
            "clock-format", "Clock Format", 
            "12 or 24 hour format",
            parent="panel-taskbar",
            config_type="dropdown",
            config_value="24h",
            config_options=[
                ("12h", "12 Hour (AM/PM)"),
                ("24h", "24 Hour")
            ],
            ansible_var="de_clock_format"
        )
        
        self.add_configurable(
            "clock-date", "Show Date in Clock", 
            "Display date with time",
            parent="panel-taskbar",
            config_type="toggle",
            config_value=True,
            ansible_var="de_clock_show_date"
        )
        
        self.add_configurable(
            "clock-seconds", "Show Seconds", 
            "Display seconds in clock",
            parent="panel-taskbar",
            config_type="toggle",
            config_value=False,
            ansible_var="de_clock_show_seconds"
        )
        
        self.add_configurable(
            "system-tray", "System Tray", 
            "Enable system tray icons",
            parent="panel-taskbar",
            config_type="toggle",
            config_value=True,
            ansible_var="de_system_tray_enabled"
        )
    
    def _build_font_settings(self):
        """Build font configuration settings menu"""
        self.add_category(
            "fonts-text", "🔤 Fonts & Text", 
            "Font configuration",
            parent="desktop-settings",
            children=["font-interface", "font-document", "font-monospace", "font-title",
                      "font-antialiasing", "font-hinting"]
        )
        
        self.add_configurable(
            "font-interface", "Interface Font", 
            "System UI font",
            parent="fonts-text",
            config_type="dropdown",
            config_value="Ubuntu 11",
            config_options=[
                ("Ubuntu 11", "Ubuntu 11pt"),
                ("Ubuntu 10", "Ubuntu 10pt"),
                ("Ubuntu 12", "Ubuntu 12pt"),
                ("Noto Sans 11", "Noto Sans 11pt"),
                ("DejaVu Sans 11", "DejaVu Sans 11pt"),
                ("Liberation Sans 11", "Liberation Sans 11pt"),
                ("Roboto 11", "Roboto 11pt"),
                ("Cantarell 11", "Cantarell 11pt"),
                ("Sans 11", "System Sans 11pt")
            ],
            ansible_var="de_font_interface"
        )
        
        self.add_configurable(
            "font-document", "Document Font", 
            "Default document font",
            parent="fonts-text",
            config_type="dropdown",
            config_value="Sans 11",
            config_options=[
                ("Sans 11", "Sans Serif 11pt"),
                ("Serif 11", "Serif 11pt"),
                ("Ubuntu 11", "Ubuntu 11pt"),
                ("Liberation Sans 11", "Liberation Sans 11pt"),
                ("Liberation Serif 11", "Liberation Serif 11pt"),
                ("DejaVu Sans 11", "DejaVu Sans 11pt"),
                ("DejaVu Serif 11", "DejaVu Serif 11pt"),
                ("Noto Sans 11", "Noto Sans 11pt"),
                ("Noto Serif 11", "Noto Serif 11pt")
            ],
            ansible_var="de_font_document"
        )
        
        self.add_configurable(
            "font-monospace", "Monospace Font", 
            "Terminal and code font",
            parent="fonts-text",
            config_type="dropdown",
            config_value="Ubuntu Mono 13",
            config_options=[
                ("Ubuntu Mono 13", "Ubuntu Mono 13pt"),
                ("Ubuntu Mono 12", "Ubuntu Mono 12pt"),
                ("Ubuntu Mono 14", "Ubuntu Mono 14pt"),
                ("JetBrains Mono 12", "JetBrains Mono 12pt"),
                ("Hack 12", "Hack 12pt"),
                ("Fira Code 12", "Fira Code 12pt"),
                ("Source Code Pro 12", "Source Code Pro 12pt"),
                ("Inconsolata 13", "Inconsolata 13pt"),
                ("Cascadia Code 12", "Cascadia Code 12pt"),
                ("DejaVu Sans Mono 12", "DejaVu Sans Mono 12pt"),
                ("Liberation Mono 12", "Liberation Mono 12pt")
            ],
            ansible_var="de_font_monospace"
        )
        
        self.add_configurable(
            "font-title", "Window Title Font", 
            "Window titlebar font",
            parent="fonts-text",
            config_type="dropdown",
            config_value="Ubuntu Bold 11",
            config_options=[
                ("Ubuntu Bold 11", "Ubuntu Bold 11pt"),
                ("Ubuntu Bold 10", "Ubuntu Bold 10pt"),
                ("Ubuntu Bold 12", "Ubuntu Bold 12pt"),
                ("Ubuntu Medium 11", "Ubuntu Medium 11pt"),
                ("Noto Sans Bold 11", "Noto Sans Bold 11pt"),
                ("DejaVu Sans Bold 11", "DejaVu Sans Bold 11pt"),
                ("Liberation Sans Bold 11", "Liberation Sans Bold 11pt"),
                ("Roboto Bold 11", "Roboto Bold 11pt"),
                ("Cantarell Bold 11", "Cantarell Bold 11pt")
            ],
            ansible_var="de_font_window_title"
        )
        
        self.add_configurable(
            "font-antialiasing", "Font Antialiasing", 
            "Font smoothing method",
            parent="fonts-text",
            config_type="dropdown",
            config_value="rgba",
            config_options=[
                ("none", "None"),
                ("grayscale", "Grayscale"),
                ("rgba", "Subpixel (RGBA)")
            ],
            ansible_var="de_font_antialiasing"
        )
        
        self.add_configurable(
            "font-hinting", "Font Hinting", 
            "Font hinting level",
            parent="fonts-text",
            config_type="dropdown",
            config_value="slight",
            config_options=[
                ("none", "None"),
                ("slight", "Slight"),
                ("medium", "Medium"),
                ("full", "Full")
            ],
            ansible_var="de_font_hinting"
        )
    
    def _build_sound_settings(self):
        """Build sound settings menu"""
        self.add_category(
            "sound-audio", "🔊 Sound", 
            "Audio settings",
            parent="desktop-settings",
            children=["startup-sound", "notification-sounds-global"]
        )
        
        self.add_configurable(
            "startup-sound", "Startup Sound", 
            "Play sound at login",
            parent="sound-audio",
            config_type="toggle",
            config_value=False,
            ansible_var="de_startup_sound"
        )
        
        self.add_configurable(
            "notification-sounds-global", "System Sounds", 
            "Enable system event sounds",
            parent="sound-audio",
            config_type="toggle",
            config_value=True,
            ansible_var="de_notification_sounds"
        )