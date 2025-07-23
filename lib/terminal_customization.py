#!/usr/bin/env python3
"""
Terminal Customization Module for Ubootu
Handles color schemes, fonts, and terminal settings
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ColorScheme:
    """Represents a terminal color scheme"""
    name: str
    display_name: str
    description: str
    colors: Dict[str, str]
    background: str
    foreground: str
    cursor: str
    selection: str
    preview: str  # ASCII art preview


@dataclass
class FontConfig:
    """Represents a terminal font configuration"""
    name: str
    display_name: str
    description: str
    family: str
    url: str
    ligatures: bool
    powerline: bool
    nerd_fonts: bool
    sizes: List[int]


@dataclass
class TerminalProfile:
    """Complete terminal profile with all settings"""
    name: str
    terminal_app: str
    color_scheme: str
    font: str
    font_size: int
    transparency: int
    blur: bool
    scrollback_lines: int
    cursor_style: str
    cursor_blink: bool
    bell: str
    window_size: Tuple[int, int]  # columns, rows


class TerminalCustomization:
    """Manages terminal customization options"""
    
    def __init__(self):
        self.color_schemes = self._init_color_schemes()
        self.fonts = self._init_fonts()
        self.terminal_apps = self._init_terminal_apps()
        self.cursor_styles = ["block", "underline", "beam"]
        self.bell_options = ["none", "visual", "sound"]
    
    def _init_color_schemes(self) -> Dict[str, ColorScheme]:
        """Initialize available color schemes"""
        schemes = {
            "dracula": ColorScheme(
                name="dracula",
                display_name="Dracula",
                description="A dark theme with vibrant colors",
                colors={
                    "black": "#21222C",
                    "red": "#FF5555",
                    "green": "#50FA7B",
                    "yellow": "#F1FA8C",
                    "blue": "#BD93F9",
                    "magenta": "#FF79C6",
                    "cyan": "#8BE9FD",
                    "white": "#F8F8F2",
                    "bright_black": "#6272A4",
                    "bright_red": "#FF6E6E",
                    "bright_green": "#69FF94",
                    "bright_yellow": "#FFFFA5",
                    "bright_blue": "#D6ACFF",
                    "bright_magenta": "#FF92DF",
                    "bright_cyan": "#A4FFFF",
                    "bright_white": "#FFFFFF"
                },
                background="#282A36",
                foreground="#F8F8F2",
                cursor="#F8F8F2",
                selection="#44475A",
                preview="🧛 Dark with vibrant purples and pinks"
            ),
            
            "catppuccin_mocha": ColorScheme(
                name="catppuccin_mocha",
                display_name="Catppuccin Mocha",
                description="Soothing pastel theme (dark)",
                colors={
                    "black": "#45475A",
                    "red": "#F38BA8",
                    "green": "#A6E3A1",
                    "yellow": "#F9E2AF",
                    "blue": "#89B4FA",
                    "magenta": "#F5C2E7",
                    "cyan": "#94E2D5",
                    "white": "#BAC2DE",
                    "bright_black": "#585B70",
                    "bright_red": "#F38BA8",
                    "bright_green": "#A6E3A1",
                    "bright_yellow": "#F9E2AF",
                    "bright_blue": "#89B4FA",
                    "bright_magenta": "#F5C2E7",
                    "bright_cyan": "#94E2D5",
                    "bright_white": "#A6ADC8"
                },
                background="#1E1E2E",
                foreground="#CDD6F4",
                cursor="#F5E0DC",
                selection="#313244",
                preview="🐱 Soothing pastel colors"
            ),
            
            "catppuccin_latte": ColorScheme(
                name="catppuccin_latte",
                display_name="Catppuccin Latte",
                description="Soothing pastel theme (light)",
                colors={
                    "black": "#5C5F77",
                    "red": "#D20F39",
                    "green": "#40A02B",
                    "yellow": "#DF8E1D",
                    "blue": "#1E66F5",
                    "magenta": "#EA76CB",
                    "cyan": "#179299",
                    "white": "#ACB0BE",
                    "bright_black": "#6C6F85",
                    "bright_red": "#D20F39",
                    "bright_green": "#40A02B",
                    "bright_yellow": "#DF8E1D",
                    "bright_blue": "#1E66F5",
                    "bright_magenta": "#EA76CB",
                    "bright_cyan": "#179299",
                    "bright_white": "#BCC0CC"
                },
                background="#EFF1F5",
                foreground="#4C4F69",
                cursor="#DC8A78",
                selection="#CCD0DA",
                preview="☕ Light and warm"
            ),
            
            "solarized_dark": ColorScheme(
                name="solarized_dark",
                display_name="Solarized Dark",
                description="Precision colors for machines and people",
                colors={
                    "black": "#073642",
                    "red": "#DC322F",
                    "green": "#859900",
                    "yellow": "#B58900",
                    "blue": "#268BD2",
                    "magenta": "#D33682",
                    "cyan": "#2AA198",
                    "white": "#EEE8D5",
                    "bright_black": "#002B36",
                    "bright_red": "#CB4B16",
                    "bright_green": "#586E75",
                    "bright_yellow": "#657B83",
                    "bright_blue": "#839496",
                    "bright_magenta": "#6C71C4",
                    "bright_cyan": "#93A1A1",
                    "bright_white": "#FDF6E3"
                },
                background="#002B36",
                foreground="#839496",
                cursor="#839496",
                selection="#073642",
                preview="☀️ Ethan Schoonover's precision colors"
            ),
            
            "nord": ColorScheme(
                name="nord",
                display_name="Nord",
                description="Arctic, north-bluish color palette",
                colors={
                    "black": "#3B4252",
                    "red": "#BF616A",
                    "green": "#A3BE8C",
                    "yellow": "#EBCB8B",
                    "blue": "#81A1C1",
                    "magenta": "#B48EAD",
                    "cyan": "#88C0D0",
                    "white": "#E5E9F0",
                    "bright_black": "#4C566A",
                    "bright_red": "#BF616A",
                    "bright_green": "#A3BE8C",
                    "bright_yellow": "#EBCB8B",
                    "bright_blue": "#81A1C1",
                    "bright_magenta": "#B48EAD",
                    "bright_cyan": "#8FBCBB",
                    "bright_white": "#ECEFF4"
                },
                background="#2E3440",
                foreground="#D8DEE9",
                cursor="#D8DEE9",
                selection="#434C5E",
                preview="❄️ Cool and north-bluish"
            ),
            
            "gruvbox_dark": ColorScheme(
                name="gruvbox_dark",
                display_name="Gruvbox Dark",
                description="Retro groove color scheme",
                colors={
                    "black": "#282828",
                    "red": "#CC241D",
                    "green": "#98971A",
                    "yellow": "#D79921",
                    "blue": "#458588",
                    "magenta": "#B16286",
                    "cyan": "#689D6A",
                    "white": "#A89984",
                    "bright_black": "#928374",
                    "bright_red": "#FB4934",
                    "bright_green": "#B8BB26",
                    "bright_yellow": "#FABD2F",
                    "bright_blue": "#83A598",
                    "bright_magenta": "#D3869B",
                    "bright_cyan": "#8EC07C",
                    "bright_white": "#EBDBB2"
                },
                background="#282828",
                foreground="#EBDBB2",
                cursor="#EBDBB2",
                selection="#504945",
                preview="🎸 Retro and warm"
            ),
            
            "tokyo_night": ColorScheme(
                name="tokyo_night",
                display_name="Tokyo Night",
                description="A clean dark theme inspired by Tokyo",
                colors={
                    "black": "#15161E",
                    "red": "#F7768E",
                    "green": "#9ECE6A",
                    "yellow": "#E0AF68",
                    "blue": "#7AA2F7",
                    "magenta": "#BB9AF7",
                    "cyan": "#7DCFFF",
                    "white": "#A9B1D6",
                    "bright_black": "#414868",
                    "bright_red": "#F7768E",
                    "bright_green": "#9ECE6A",
                    "bright_yellow": "#E0AF68",
                    "bright_blue": "#7AA2F7",
                    "bright_magenta": "#BB9AF7",
                    "bright_cyan": "#7DCFFF",
                    "bright_white": "#C0CAF5"
                },
                background="#1A1B26",
                foreground="#C0CAF5",
                cursor="#C0CAF5",
                selection="#33467C",
                preview="🌃 Tokyo city lights"
            ),
            
            "one_dark": ColorScheme(
                name="one_dark",
                display_name="One Dark",
                description="Atom One Dark theme",
                colors={
                    "black": "#282C34",
                    "red": "#E06C75",
                    "green": "#98C379",
                    "yellow": "#E5C07B",
                    "blue": "#61AFEF",
                    "magenta": "#C678DD",
                    "cyan": "#56B6C2",
                    "white": "#ABB2BF",
                    "bright_black": "#5C6370",
                    "bright_red": "#E06C75",
                    "bright_green": "#98C379",
                    "bright_yellow": "#E5C07B",
                    "bright_blue": "#61AFEF",
                    "bright_magenta": "#C678DD",
                    "bright_cyan": "#56B6C2",
                    "bright_white": "#FFFFFF"
                },
                background="#282C34",
                foreground="#ABB2BF",
                cursor="#ABB2BF",
                selection="#3E4451",
                preview="⚛️ Atom-inspired elegance"
            ),
            
            "material_ocean": ColorScheme(
                name="material_ocean",
                display_name="Material Ocean",
                description="Material Design ocean variant",
                colors={
                    "black": "#0F111A",
                    "red": "#FF5370",
                    "green": "#C3E88D",
                    "yellow": "#FFCB6B",
                    "blue": "#82AAFF",
                    "magenta": "#C792EA",
                    "cyan": "#89DDFF",
                    "white": "#EEFFFF",
                    "bright_black": "#464B5D",
                    "bright_red": "#FF5370",
                    "bright_green": "#C3E88D",
                    "bright_yellow": "#FFCB6B",
                    "bright_blue": "#82AAFF",
                    "bright_magenta": "#C792EA",
                    "bright_cyan": "#89DDFF",
                    "bright_white": "#FFFFFF"
                },
                background="#0F111A",
                foreground="#8F93A2",
                cursor="#FFCC00",
                selection="#1F2233",
                preview="🌊 Deep ocean material"
            ),
            
            "monokai": ColorScheme(
                name="monokai",
                display_name="Monokai",
                description="Sublime Text classic",
                colors={
                    "black": "#272822",
                    "red": "#F92672",
                    "green": "#A6E22E",
                    "yellow": "#F4BF75",
                    "blue": "#66D9EF",
                    "magenta": "#AE81FF",
                    "cyan": "#A1EFE4",
                    "white": "#F8F8F2",
                    "bright_black": "#75715E",
                    "bright_red": "#F92672",
                    "bright_green": "#A6E22E",
                    "bright_yellow": "#F4BF75",
                    "bright_blue": "#66D9EF",
                    "bright_magenta": "#AE81FF",
                    "bright_cyan": "#A1EFE4",
                    "bright_white": "#F9F8F5"
                },
                background="#272822",
                foreground="#F8F8F2",
                cursor="#F8F8F0",
                selection="#49483E",
                preview="🎨 Sublime Text classic"
            )
        }
        
        return schemes
    
    def _init_fonts(self) -> Dict[str, FontConfig]:
        """Initialize available fonts"""
        fonts = {
            "meslo": FontConfig(
                name="meslo",
                display_name="Meslo LG",
                description="Customized version of Apple's Menlo font",
                family="MesloLGS NF",
                url="https://github.com/romkatv/powerlevel10k#manual-font-installation",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "hack": FontConfig(
                name="hack",
                display_name="Hack",
                description="A typeface designed for source code",
                family="Hack Nerd Font",
                url="https://github.com/source-foundry/Hack",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "jetbrains": FontConfig(
                name="jetbrains",
                display_name="JetBrains Mono",
                description="A typeface for developers by JetBrains",
                family="JetBrainsMono Nerd Font",
                url="https://www.jetbrains.com/lp/mono/",
                ligatures=True,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "firacode": FontConfig(
                name="firacode",
                display_name="Fira Code",
                description="Monospaced font with programming ligatures",
                family="FiraCode Nerd Font",
                url="https://github.com/tonsky/FiraCode",
                ligatures=True,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "cascadia": FontConfig(
                name="cascadia",
                display_name="Cascadia Code",
                description="A monospaced font by Microsoft",
                family="CaskaydiaCove Nerd Font",
                url="https://github.com/microsoft/cascadia-code",
                ligatures=True,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "source_code_pro": FontConfig(
                name="source_code_pro",
                display_name="Source Code Pro",
                description="Monospaced font family by Adobe",
                family="SauceCodePro Nerd Font",
                url="https://github.com/adobe-fonts/source-code-pro",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "iosevka": FontConfig(
                name="iosevka",
                display_name="Iosevka",
                description="Slender typeface for code",
                family="Iosevka Nerd Font",
                url="https://github.com/be5invis/Iosevka",
                ligatures=True,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "ubuntu_mono": FontConfig(
                name="ubuntu_mono",
                display_name="Ubuntu Mono",
                description="Ubuntu's monospace font",
                family="UbuntuMono Nerd Font",
                url="https://design.ubuntu.com/font/",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "droid_sans": FontConfig(
                name="droid_sans",
                display_name="Droid Sans Mono",
                description="Droid Sans Mono for Powerline",
                family="DroidSansMono Nerd Font",
                url="https://www.droidfonts.com/",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            ),
            
            "roboto": FontConfig(
                name="roboto",
                display_name="Roboto Mono",
                description="Google's Roboto Mono font",
                family="RobotoMono Nerd Font",
                url="https://github.com/googlefonts/RobotoMono",
                ligatures=False,
                powerline=True,
                nerd_fonts=True,
                sizes=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24]
            )
        }
        
        return fonts
    
    def _init_terminal_apps(self) -> Dict[str, Dict[str, Any]]:
        """Initialize supported terminal applications"""
        apps = {
            "gnome_terminal": {
                "name": "GNOME Terminal",
                "command": "gnome-terminal",
                "config_path": "~/.config/dconf",
                "supports": {
                    "transparency": True,
                    "blur": False,
                    "ligatures": True,
                    "custom_css": False,
                    "profiles": True
                }
            },
            "konsole": {
                "name": "Konsole",
                "command": "konsole",
                "config_path": "~/.config/konsolerc",
                "supports": {
                    "transparency": True,
                    "blur": True,
                    "ligatures": True,
                    "custom_css": False,
                    "profiles": True
                }
            },
            "terminator": {
                "name": "Terminator",
                "command": "terminator",
                "config_path": "~/.config/terminator/config",
                "supports": {
                    "transparency": True,
                    "blur": False,
                    "ligatures": True,
                    "custom_css": False,
                    "profiles": True
                }
            },
            "alacritty": {
                "name": "Alacritty",
                "command": "alacritty",
                "config_path": "~/.config/alacritty/alacritty.yml",
                "supports": {
                    "transparency": True,
                    "blur": True,
                    "ligatures": True,
                    "custom_css": False,
                    "profiles": False
                }
            },
            "kitty": {
                "name": "Kitty",
                "command": "kitty",
                "config_path": "~/.config/kitty/kitty.conf",
                "supports": {
                    "transparency": True,
                    "blur": True,
                    "ligatures": True,
                    "custom_css": True,
                    "profiles": False
                }
            },
            "wezterm": {
                "name": "WezTerm",
                "command": "wezterm",
                "config_path": "~/.config/wezterm/wezterm.lua",
                "supports": {
                    "transparency": True,
                    "blur": True,
                    "ligatures": True,
                    "custom_css": True,
                    "profiles": True
                }
            },
            "tilix": {
                "name": "Tilix",
                "command": "tilix",
                "config_path": "~/.config/tilix",
                "supports": {
                    "transparency": True,
                    "blur": False,
                    "ligatures": True,
                    "custom_css": False,
                    "profiles": True
                }
            }
        }
        
        return apps
    
    def get_color_scheme(self, name: str) -> ColorScheme:
        """Get a specific color scheme"""
        return self.color_schemes.get(name)
    
    def get_font(self, name: str) -> FontConfig:
        """Get a specific font configuration"""
        return self.fonts.get(name)
    
    def get_terminal_app(self, name: str) -> Dict[str, Any]:
        """Get terminal app configuration"""
        return self.terminal_apps.get(name)
    
    def list_color_schemes(self) -> List[Tuple[str, str, str]]:
        """List all available color schemes"""
        return [(name, scheme.display_name, scheme.preview) 
                for name, scheme in self.color_schemes.items()]
    
    def list_fonts(self) -> List[Tuple[str, str, bool]]:
        """List all available fonts with ligature support"""
        return [(name, font.display_name, font.ligatures) 
                for name, font in self.fonts.items()]
    
    def create_terminal_profile(self, **kwargs) -> TerminalProfile:
        """Create a new terminal profile with settings"""
        return TerminalProfile(
            name=kwargs.get("name", "Custom Profile"),
            terminal_app=kwargs.get("terminal_app", "gnome_terminal"),
            color_scheme=kwargs.get("color_scheme", "dracula"),
            font=kwargs.get("font", "jetbrains"),
            font_size=kwargs.get("font_size", 12),
            transparency=kwargs.get("transparency", 95),
            blur=kwargs.get("blur", False),
            scrollback_lines=kwargs.get("scrollback_lines", 10000),
            cursor_style=kwargs.get("cursor_style", "block"),
            cursor_blink=kwargs.get("cursor_blink", True),
            bell=kwargs.get("bell", "visual"),
            window_size=kwargs.get("window_size", (80, 24))
        )
    
    def export_color_scheme(self, scheme_name: str, terminal_app: str) -> str:
        """Export color scheme in terminal-specific format"""
        scheme = self.color_schemes.get(scheme_name)
        if not scheme:
            return ""
        
        if terminal_app == "alacritty":
            return self._export_alacritty_colors(scheme)
        elif terminal_app == "kitty":
            return self._export_kitty_colors(scheme)
        elif terminal_app == "wezterm":
            return self._export_wezterm_colors(scheme)
        else:
            return self._export_generic_colors(scheme)
    
    def _export_alacritty_colors(self, scheme: ColorScheme) -> str:
        """Export colors in Alacritty format"""
        config = f"""# {scheme.display_name} color scheme
colors:
  primary:
    background: '{scheme.background}'
    foreground: '{scheme.foreground}'
  cursor:
    text: '{scheme.background}'
    cursor: '{scheme.cursor}'
  selection:
    text: '{scheme.foreground}'
    background: '{scheme.selection}'
  normal:
    black: '{scheme.colors["black"]}'
    red: '{scheme.colors["red"]}'
    green: '{scheme.colors["green"]}'
    yellow: '{scheme.colors["yellow"]}'
    blue: '{scheme.colors["blue"]}'
    magenta: '{scheme.colors["magenta"]}'
    cyan: '{scheme.colors["cyan"]}'
    white: '{scheme.colors["white"]}'
  bright:
    black: '{scheme.colors["bright_black"]}'
    red: '{scheme.colors["bright_red"]}'
    green: '{scheme.colors["bright_green"]}'
    yellow: '{scheme.colors["bright_yellow"]}'
    blue: '{scheme.colors["bright_blue"]}'
    magenta: '{scheme.colors["bright_magenta"]}'
    cyan: '{scheme.colors["bright_cyan"]}'
    white: '{scheme.colors["bright_white"]}'
"""
        return config
    
    def _export_kitty_colors(self, scheme: ColorScheme) -> str:
        """Export colors in Kitty format"""
        config = f"""# {scheme.display_name} color scheme
background {scheme.background}
foreground {scheme.foreground}
cursor {scheme.cursor}
selection_background {scheme.selection}
selection_foreground {scheme.foreground}

# Normal colors
color0 {scheme.colors["black"]}
color1 {scheme.colors["red"]}
color2 {scheme.colors["green"]}
color3 {scheme.colors["yellow"]}
color4 {scheme.colors["blue"]}
color5 {scheme.colors["magenta"]}
color6 {scheme.colors["cyan"]}
color7 {scheme.colors["white"]}

# Bright colors
color8 {scheme.colors["bright_black"]}
color9 {scheme.colors["bright_red"]}
color10 {scheme.colors["bright_green"]}
color11 {scheme.colors["bright_yellow"]}
color12 {scheme.colors["bright_blue"]}
color13 {scheme.colors["bright_magenta"]}
color14 {scheme.colors["bright_cyan"]}
color15 {scheme.colors["bright_white"]}
"""
        return config
    
    def _export_wezterm_colors(self, scheme: ColorScheme) -> str:
        """Export colors in WezTerm format"""
        config = f"""-- {scheme.display_name} color scheme
return {{
  foreground = "{scheme.foreground}",
  background = "{scheme.background}",
  cursor_bg = "{scheme.cursor}",
  cursor_fg = "{scheme.background}",
  selection_bg = "{scheme.selection}",
  selection_fg = "{scheme.foreground}",
  
  ansi = {{
    "{scheme.colors["black"]}",
    "{scheme.colors["red"]}",
    "{scheme.colors["green"]}",
    "{scheme.colors["yellow"]}",
    "{scheme.colors["blue"]}",
    "{scheme.colors["magenta"]}",
    "{scheme.colors["cyan"]}",
    "{scheme.colors["white"]}",
  }},
  
  brights = {{
    "{scheme.colors["bright_black"]}",
    "{scheme.colors["bright_red"]}",
    "{scheme.colors["bright_green"]}",
    "{scheme.colors["bright_yellow"]}",
    "{scheme.colors["bright_blue"]}",
    "{scheme.colors["bright_magenta"]}",
    "{scheme.colors["bright_cyan"]}",
    "{scheme.colors["bright_white"]}",
  }}
}}
"""
        return config
    
    def _export_generic_colors(self, scheme: ColorScheme) -> str:
        """Export colors in generic format"""
        config = f"""# {scheme.display_name} color scheme
# Generic color values

Background: {scheme.background}
Foreground: {scheme.foreground}
Cursor: {scheme.cursor}
Selection: {scheme.selection}

# Normal colors
Black: {scheme.colors["black"]}
Red: {scheme.colors["red"]}
Green: {scheme.colors["green"]}
Yellow: {scheme.colors["yellow"]}
Blue: {scheme.colors["blue"]}
Magenta: {scheme.colors["magenta"]}
Cyan: {scheme.colors["cyan"]}
White: {scheme.colors["white"]}

# Bright colors
Bright Black: {scheme.colors["bright_black"]}
Bright Red: {scheme.colors["bright_red"]}
Bright Green: {scheme.colors["bright_green"]}
Bright Yellow: {scheme.colors["bright_yellow"]}
Bright Blue: {scheme.colors["bright_blue"]}
Bright Magenta: {scheme.colors["bright_magenta"]}
Bright Cyan: {scheme.colors["bright_cyan"]}
Bright White: {scheme.colors["bright_white"]}
"""
        return config