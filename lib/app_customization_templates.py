#!/usr/bin/env python3
"""
Application Customization Templates for Ubootu
Provides detailed customization options for various applications
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from menu_ui import SliderConfig, DropdownConfig, MultiSelectConfig


@dataclass
class CustomizationTemplate:
    """Template for application customization"""
    app_name: str
    display_name: str
    description: str
    icon: str
    categories: List[str]
    settings: Dict[str, Any]
    presets: Dict[str, Dict[str, Any]]


class AppCustomizationTemplates:
    """Manages customization templates for applications"""
    
    def __init__(self):
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict[str, CustomizationTemplate]:
        """Initialize all application customization templates"""
        templates = {}
        
        # Terminal Customization
        templates['terminal'] = self._create_terminal_template()
        
        # VSCode Customization
        templates['vscode'] = self._create_vscode_template()
        
        # Firefox Customization
        templates['firefox'] = self._create_firefox_template()
        
        # Git Customization
        templates['git'] = self._create_git_template()
        
        # Vim/Neovim Customization
        templates['vim'] = self._create_vim_template()
        
        # GNOME Terminal Specific
        templates['gnome_terminal'] = self._create_gnome_terminal_template()
        
        # System Preferences
        templates['system'] = self._create_system_template()
        
        # Shell Customization
        templates['shell'] = self._create_shell_template()
        
        # Desktop Environment
        templates['desktop'] = self._create_desktop_template()
        
        # Development Environment
        templates['development'] = self._create_development_template()
        
        return templates
    
    def _create_terminal_template(self) -> CustomizationTemplate:
        """Create terminal customization template"""
        return CustomizationTemplate(
            app_name="terminal",
            display_name="Terminal Emulator",
            description="Customize your terminal appearance and behavior",
            icon="🖥️",
            categories=["appearance", "behavior", "keybindings"],
            settings={
                "appearance": {
                    "color_scheme": DropdownConfig(
                        options=[
                            ("dracula", "Dracula"),
                            ("catppuccin_mocha", "Catppuccin Mocha"),
                            ("catppuccin_latte", "Catppuccin Latte"),
                            ("solarized_dark", "Solarized Dark"),
                            ("solarized_light", "Solarized Light"),
                            ("nord", "Nord"),
                            ("gruvbox_dark", "Gruvbox Dark"),
                            ("tokyo_night", "Tokyo Night"),
                            ("one_dark", "One Dark"),
                            ("material_ocean", "Material Ocean"),
                            ("monokai", "Monokai"),
                            ("custom", "Custom...")
                        ],
                        current_value="dracula",
                        allow_custom=True
                    ),
                    "font": DropdownConfig(
                        options=[
                            ("meslo", "Meslo LG Nerd Font"),
                            ("hack", "Hack Nerd Font"),
                            ("jetbrains", "JetBrains Mono Nerd Font"),
                            ("firacode", "Fira Code Nerd Font"),
                            ("cascadia", "Cascadia Code Nerd Font"),
                            ("source_code_pro", "Source Code Pro Nerd Font"),
                            ("iosevka", "Iosevka Nerd Font"),
                            ("ubuntu_mono", "Ubuntu Mono Nerd Font"),
                            ("custom", "Custom...")
                        ],
                        current_value="jetbrains",
                        allow_custom=True
                    ),
                    "font_size": SliderConfig(
                        min_value=8,
                        max_value=24,
                        current_value=12,
                        step=1,
                        unit="pt"
                    ),
                    "transparency": SliderConfig(
                        min_value=0,
                        max_value=100,
                        current_value=95,
                        step=5,
                        unit="%",
                        show_percentage=True
                    ),
                    "blur": {
                        "enabled": False,
                        "strength": SliderConfig(
                            min_value=0,
                            max_value=20,
                            current_value=5,
                            step=1
                        )
                    },
                    "cursor_style": DropdownConfig(
                        options=[
                            ("block", "Block █"),
                            ("underline", "Underline _"),
                            ("beam", "Beam |")
                        ],
                        current_value="block",
                        allow_custom=False
                    ),
                    "cursor_blink": True,
                    "cursor_color": "auto"  # or specific color
                },
                "behavior": {
                    "scrollback_lines": SliderConfig(
                        min_value=100,
                        max_value=100000,
                        current_value=10000,
                        step=1000,
                        unit=" lines"
                    ),
                    "window_size": {
                        "columns": SliderConfig(
                            min_value=40,
                            max_value=300,
                            current_value=80,
                            step=10,
                            unit=" cols"
                        ),
                        "rows": SliderConfig(
                            min_value=10,
                            max_value=100,
                            current_value=24,
                            step=2,
                            unit=" rows"
                        )
                    },
                    "bell": DropdownConfig(
                        options=[
                            ("none", "Disabled"),
                            ("visual", "Visual Bell"),
                            ("sound", "Sound Alert")
                        ],
                        current_value="visual",
                        allow_custom=False
                    ),
                    "confirm_on_close": True,
                    "copy_on_select": True,
                    "paste_on_middle_click": True,
                    "rewrap_on_resize": True,
                    "use_custom_command": False,
                    "custom_command": "/bin/zsh"
                },
                "keybindings": {
                    "copy": "Ctrl+Shift+C",
                    "paste": "Ctrl+Shift+V",
                    "new_tab": "Ctrl+Shift+T",
                    "close_tab": "Ctrl+Shift+W",
                    "next_tab": "Ctrl+PageDown",
                    "prev_tab": "Ctrl+PageUp",
                    "zoom_in": "Ctrl+Plus",
                    "zoom_out": "Ctrl+Minus",
                    "zoom_reset": "Ctrl+0",
                    "search": "Ctrl+Shift+F",
                    "fullscreen": "F11"
                },
                "advanced": {
                    "encoding": DropdownConfig(
                        options=[
                            ("UTF-8", "UTF-8 (Default)"),
                            ("ISO-8859-1", "ISO-8859-1"),
                            ("ISO-8859-15", "ISO-8859-15"),
                            ("Windows-1252", "Windows-1252")
                        ],
                        current_value="UTF-8",
                        allow_custom=False
                    ),
                    "word_chars": "-,./?%&#:_=+@~",
                    "allow_bold": True,
                    "audible_bell": False,
                    "urgent_on_bell": True,
                    "login_shell": True,
                    "use_theme_colors": False
                }
            },
            presets={
                "developer": {
                    "appearance.color_scheme": "dracula",
                    "appearance.font": "jetbrains",
                    "appearance.font_size": 13,
                    "appearance.transparency": 95,
                    "behavior.scrollback_lines": 50000,
                    "behavior.window_size.columns": 120,
                    "behavior.window_size.rows": 40
                },
                "minimal": {
                    "appearance.color_scheme": "solarized_dark",
                    "appearance.font": "ubuntu_mono",
                    "appearance.font_size": 11,
                    "appearance.transparency": 100,
                    "behavior.scrollback_lines": 5000,
                    "behavior.window_size.columns": 80,
                    "behavior.window_size.rows": 24
                },
                "presentation": {
                    "appearance.color_scheme": "solarized_light",
                    "appearance.font": "firacode",
                    "appearance.font_size": 16,
                    "appearance.transparency": 100,
                    "behavior.scrollback_lines": 1000,
                    "behavior.window_size.columns": 100,
                    "behavior.window_size.rows": 30
                }
            }
        )
    
    def _create_vscode_template(self) -> CustomizationTemplate:
        """Create VSCode customization template"""
        return CustomizationTemplate(
            app_name="vscode",
            display_name="Visual Studio Code",
            description="Customize VSCode with themes, extensions, and settings",
            icon="💻",
            categories=["appearance", "extensions", "editor", "terminal"],
            settings={
                "appearance": {
                    "theme": DropdownConfig(
                        options=[
                            ("dracula", "Dracula Official"),
                            ("one_dark_pro", "One Dark Pro"),
                            ("material_theme", "Material Theme"),
                            ("nord", "Nord"),
                            ("tokyo_night", "Tokyo Night"),
                            ("github_dark", "GitHub Dark"),
                            ("monokai_pro", "Monokai Pro"),
                            ("synthwave_84", "SynthWave '84"),
                            ("palenight", "Palenight"),
                            ("ayu", "Ayu"),
                            ("custom", "Browse more...")
                        ],
                        current_value="dracula",
                        allow_custom=True
                    ),
                    "icon_theme": DropdownConfig(
                        options=[
                            ("material", "Material Icon Theme"),
                            ("vscode_icons", "VSCode Icons"),
                            ("file_icons", "File Icons"),
                            ("monokai_pro_icons", "Monokai Pro Icons"),
                            ("simple_icons", "Simple Icons")
                        ],
                        current_value="material",
                        allow_custom=False
                    ),
                    "font_family": DropdownConfig(
                        options=[
                            ("JetBrains Mono", "JetBrains Mono"),
                            ("Fira Code", "Fira Code"),
                            ("Cascadia Code", "Cascadia Code"),
                            ("Source Code Pro", "Source Code Pro"),
                            ("Hack", "Hack"),
                            ("Consolas", "Consolas")
                        ],
                        current_value="JetBrains Mono",
                        allow_custom=True
                    ),
                    "font_size": SliderConfig(
                        min_value=10,
                        max_value=20,
                        current_value=14,
                        step=1,
                        unit="px"
                    ),
                    "line_height": SliderConfig(
                        min_value=1.0,
                        max_value=3.0,
                        current_value=1.5,
                        step=0.1
                    ),
                    "enable_ligatures": True,
                    "cursor_style": DropdownConfig(
                        options=[
                            ("line", "Line"),
                            ("block", "Block"),
                            ("underline", "Underline"),
                            ("line-thin", "Thin Line"),
                            ("block-outline", "Block Outline"),
                            ("underline-thin", "Thin Underline")
                        ],
                        current_value="line",
                        allow_custom=False
                    ),
                    "cursor_blinking": DropdownConfig(
                        options=[
                            ("blink", "Blink"),
                            ("smooth", "Smooth"),
                            ("phase", "Phase"),
                            ("expand", "Expand"),
                            ("solid", "Solid")
                        ],
                        current_value="blink",
                        allow_custom=False
                    )
                },
                "extensions": {
                    "essential": MultiSelectConfig(
                        options=[
                            ("python", "Python", True),
                            ("jupyter", "Jupyter", True),
                            ("gitlens", "GitLens", True),
                            ("prettier", "Prettier", True),
                            ("eslint", "ESLint", True),
                            ("live_server", "Live Server", True),
                            ("docker", "Docker", True),
                            ("remote_ssh", "Remote SSH", True),
                            ("bracket_pair", "Bracket Pair Colorizer", True),
                            ("path_intellisense", "Path Intellisense", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "languages": MultiSelectConfig(
                        options=[
                            ("cpp", "C/C++", False),
                            ("csharp", "C#", False),
                            ("go", "Go", False),
                            ("rust", "Rust", False),
                            ("java", "Java Extension Pack", False),
                            ("ruby", "Ruby", False),
                            ("php", "PHP", False),
                            ("dart", "Dart", False),
                            ("julia", "Julia", False),
                            ("r", "R", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "productivity": MultiSelectConfig(
                        options=[
                            ("copilot", "GitHub Copilot", True),
                            ("tabnine", "TabNine", False),
                            ("code_spell", "Code Spell Checker", True),
                            ("todo_highlight", "TODO Highlight", True),
                            ("bookmarks", "Bookmarks", True),
                            ("project_manager", "Project Manager", True),
                            ("peacock", "Peacock", False),
                            ("polacode", "Polacode", False),
                            ("wakatime", "WakaTime", False),
                            ("settings_sync", "Settings Sync", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "editor": {
                    "tab_size": SliderConfig(
                        min_value=2,
                        max_value=8,
                        current_value=4,
                        step=2,
                        unit=" spaces"
                    ),
                    "insert_spaces": True,
                    "word_wrap": DropdownConfig(
                        options=[
                            ("off", "Off"),
                            ("on", "On"),
                            ("wordWrapColumn", "At Column"),
                            ("bounded", "Bounded")
                        ],
                        current_value="off",
                        allow_custom=False
                    ),
                    "minimap_enabled": True,
                    "minimap_position": DropdownConfig(
                        options=[
                            ("right", "Right"),
                            ("left", "Left")
                        ],
                        current_value="right",
                        allow_custom=False
                    ),
                    "rulers": [80, 120],
                    "render_whitespace": DropdownConfig(
                        options=[
                            ("none", "None"),
                            ("boundary", "Boundary"),
                            ("selection", "Selection"),
                            ("trailing", "Trailing"),
                            ("all", "All")
                        ],
                        current_value="selection",
                        allow_custom=False
                    ),
                    "bracket_pair_colorization": True,
                    "indent_guides": True,
                    "sticky_scroll": True,
                    "folding": True,
                    "format_on_save": True,
                    "format_on_paste": False,
                    "auto_save": DropdownConfig(
                        options=[
                            ("off", "Off"),
                            ("afterDelay", "After Delay"),
                            ("onFocusChange", "On Focus Change"),
                            ("onWindowChange", "On Window Change")
                        ],
                        current_value="off",
                        allow_custom=False
                    )
                },
                "terminal": {
                    "integrated_font_size": SliderConfig(
                        min_value=10,
                        max_value=20,
                        current_value=13,
                        step=1,
                        unit="px"
                    ),
                    "integrated_cursor_style": DropdownConfig(
                        options=[
                            ("block", "Block"),
                            ("line", "Line"),
                            ("underline", "Underline")
                        ],
                        current_value="block",
                        allow_custom=False
                    ),
                    "integrated_shell": DropdownConfig(
                        options=[
                            ("/bin/bash", "Bash"),
                            ("/bin/zsh", "Zsh"),
                            ("/usr/bin/fish", "Fish"),
                            ("/usr/bin/pwsh", "PowerShell"),
                            ("custom", "Custom...")
                        ],
                        current_value="/bin/bash",
                        allow_custom=True
                    ),
                    "integrated_scrollback": SliderConfig(
                        min_value=1000,
                        max_value=50000,
                        current_value=10000,
                        step=1000,
                        unit=" lines"
                    )
                }
            },
            presets={
                "web_developer": {
                    "appearance.theme": "one_dark_pro",
                    "extensions.essential": ["prettier", "eslint", "live_server", "gitlens"],
                    "editor.format_on_save": True,
                    "editor.tab_size": 2
                },
                "python_developer": {
                    "appearance.theme": "monokai_pro",
                    "extensions.essential": ["python", "jupyter", "gitlens"],
                    "editor.tab_size": 4,
                    "editor.rulers": [79, 120]
                },
                "minimal": {
                    "appearance.theme": "github_dark",
                    "extensions.essential": ["gitlens"],
                    "editor.minimap_enabled": False,
                    "editor.bracket_pair_colorization": False
                }
            }
        )
    
    def _create_firefox_template(self) -> CustomizationTemplate:
        """Create Firefox customization template"""
        return CustomizationTemplate(
            app_name="firefox",
            display_name="Firefox",
            description="Privacy-focused browser configuration",
            icon="🦊",
            categories=["privacy", "performance", "appearance", "extensions"],
            settings={
                "privacy": {
                    "tracking_protection": DropdownConfig(
                        options=[
                            ("standard", "Standard"),
                            ("strict", "Strict"),
                            ("custom", "Custom")
                        ],
                        current_value="strict",
                        allow_custom=False
                    ),
                    "cookie_behavior": DropdownConfig(
                        options=[
                            ("standard", "Standard"),
                            ("strict", "Strict - may break sites"),
                            ("custom", "Custom")
                        ],
                        current_value="standard",
                        allow_custom=False
                    ),
                    "dns_over_https": DropdownConfig(
                        options=[
                            ("off", "Off"),
                            ("default", "Default Protection"),
                            ("increased", "Increased Protection"),
                            ("max", "Max Protection"),
                            ("cloudflare", "Cloudflare"),
                            ("nextdns", "NextDNS")
                        ],
                        current_value="default",
                        allow_custom=True
                    ),
                    "resist_fingerprinting": True,
                    "webrtc_prevent_leak": True,
                    "https_only_mode": True,
                    "clear_on_close": MultiSelectConfig(
                        options=[
                            ("cache", "Cache", True),
                            ("cookies", "Cookies", False),
                            ("history", "History", False),
                            ("downloads", "Download History", True),
                            ("forms", "Form Data", True),
                            ("sessions", "Active Sessions", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "performance": {
                    "hardware_acceleration": True,
                    "process_limit": SliderConfig(
                        min_value=1,
                        max_value=8,
                        current_value=4,
                        step=1,
                        unit=" processes"
                    ),
                    "ram_cache_size": SliderConfig(
                        min_value=128,
                        max_value=2048,
                        current_value=512,
                        step=128,
                        unit=" MB"
                    )
                },
                "appearance": {
                    "theme": DropdownConfig(
                        options=[
                            ("default", "Default"),
                            ("dark", "Dark"),
                            ("light", "Light"),
                            ("alpenglow", "Alpenglow"),
                            ("colorways", "Colorways")
                        ],
                        current_value="dark",
                        allow_custom=False
                    ),
                    "density": DropdownConfig(
                        options=[
                            ("normal", "Normal"),
                            ("compact", "Compact"),
                            ("touch", "Touch")
                        ],
                        current_value="normal",
                        allow_custom=False
                    ),
                    "toolbar_bookmarks": True,
                    "tab_position": DropdownConfig(
                        options=[
                            ("top", "Top"),
                            ("bottom", "Bottom")
                        ],
                        current_value="top",
                        allow_custom=False
                    )
                },
                "extensions": {
                    "privacy": MultiSelectConfig(
                        options=[
                            ("ublock_origin", "uBlock Origin", True),
                            ("privacy_badger", "Privacy Badger", True),
                            ("https_everywhere", "HTTPS Everywhere", True),
                            ("decentraleyes", "Decentraleyes", True),
                            ("clearurls", "ClearURLs", True),
                            ("cookie_autodelete", "Cookie AutoDelete", True),
                            ("temporary_containers", "Temporary Containers", False),
                            ("multi_account_containers", "Multi-Account Containers", True),
                            ("facebook_container", "Facebook Container", False),
                            ("noscript", "NoScript", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "productivity": MultiSelectConfig(
                        options=[
                            ("bitwarden", "Bitwarden", True),
                            ("dark_reader", "Dark Reader", True),
                            ("tree_style_tab", "Tree Style Tab", False),
                            ("sidebery", "Sidebery", False),
                            ("vimium", "Vimium", False),
                            ("tab_session_manager", "Tab Session Manager", True),
                            ("single_file", "SingleFile", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                }
            },
            presets={
                "maximum_privacy": {
                    "privacy.tracking_protection": "strict",
                    "privacy.resist_fingerprinting": True,
                    "privacy.https_only_mode": True,
                    "extensions.privacy": ["ublock_origin", "privacy_badger", "noscript", "temporary_containers"]
                },
                "balanced": {
                    "privacy.tracking_protection": "standard",
                    "privacy.resist_fingerprinting": False,
                    "extensions.privacy": ["ublock_origin", "https_everywhere"]
                },
                "performance": {
                    "performance.hardware_acceleration": True,
                    "performance.process_limit": 8,
                    "extensions.privacy": ["ublock_origin"]
                }
            }
        )
    
    def _create_git_template(self) -> CustomizationTemplate:
        """Create Git customization template"""
        return CustomizationTemplate(
            app_name="git",
            display_name="Git",
            description="Configure Git with aliases, hooks, and settings",
            icon="🔀",
            categories=["user", "aliases", "behavior", "hooks"],
            settings={
                "user": {
                    "name": "",
                    "email": "",
                    "signing_key": "",
                    "sign_commits": False
                },
                "core": {
                    "editor": DropdownConfig(
                        options=[
                            ("vim", "Vim"),
                            ("nano", "Nano"),
                            ("code", "VS Code"),
                            ("emacs", "Emacs"),
                            ("sublime", "Sublime Text"),
                            ("atom", "Atom")
                        ],
                        current_value="vim",
                        allow_custom=True
                    ),
                    "pager": DropdownConfig(
                        options=[
                            ("less", "Less (default)"),
                            ("more", "More"),
                            ("cat", "Cat (no paging)"),
                            ("delta", "Delta (better diff)"),
                            ("diff-so-fancy", "diff-so-fancy")
                        ],
                        current_value="less",
                        allow_custom=True
                    ),
                    "autocrlf": DropdownConfig(
                        options=[
                            ("true", "True (Windows)"),
                            ("input", "Input (Mac/Linux)"),
                            ("false", "False")
                        ],
                        current_value="input",
                        allow_custom=False
                    ),
                    "whitespace": "fix,-indent-with-non-tab,trailing-space,cr-at-eol"
                },
                "aliases": {
                    "common": MultiSelectConfig(
                        options=[
                            ("st", "status", True),
                            ("co", "checkout", True),
                            ("br", "branch", True),
                            ("ci", "commit", True),
                            ("df", "diff", True),
                            ("lg", "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'", True),
                            ("last", "log -1 HEAD", True),
                            ("unstage", "reset HEAD --", True),
                            ("amend", "commit --amend", True),
                            ("aliases", "config --get-regexp alias", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "advanced": MultiSelectConfig(
                        options=[
                            ("undo", "reset --soft HEAD~1", False),
                            ("wip", "commit -am 'WIP'", False),
                            ("pushf", "push --force-with-lease", False),
                            ("pullr", "pull --rebase", False),
                            ("stash-all", "stash save --include-untracked", False),
                            ("cleanup", "!git branch --merged | grep -v '\\*' | xargs -n 1 git branch -d", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "behavior": {
                    "push_default": DropdownConfig(
                        options=[
                            ("simple", "Simple (default)"),
                            ("current", "Current"),
                            ("upstream", "Upstream"),
                            ("matching", "Matching")
                        ],
                        current_value="simple",
                        allow_custom=False
                    ),
                    "pull_rebase": DropdownConfig(
                        options=[
                            ("false", "Merge (default)"),
                            ("true", "Rebase"),
                            ("preserve", "Rebase preserving merges"),
                            ("interactive", "Interactive rebase")
                        ],
                        current_value="false",
                        allow_custom=False
                    ),
                    "rerere_enabled": True,
                    "auto_stash": True,
                    "commit_verbose": True,
                    "status_short_branch": True
                },
                "diff": {
                    "algorithm": DropdownConfig(
                        options=[
                            ("myers", "Myers (default)"),
                            ("minimal", "Minimal"),
                            ("patience", "Patience"),
                            ("histogram", "Histogram")
                        ],
                        current_value="histogram",
                        allow_custom=False
                    ),
                    "color_moved": DropdownConfig(
                        options=[
                            ("no", "No"),
                            ("default", "Default"),
                            ("plain", "Plain"),
                            ("blocks", "Blocks"),
                            ("zebra", "Zebra"),
                            ("dimmed-zebra", "Dimmed Zebra")
                        ],
                        current_value="zebra",
                        allow_custom=False
                    ),
                    "context_lines": SliderConfig(
                        min_value=1,
                        max_value=10,
                        current_value=3,
                        step=1,
                        unit=" lines"
                    )
                }
            },
            presets={
                "developer": {
                    "core.editor": "code",
                    "aliases.common": ["st", "co", "br", "ci", "df", "lg"],
                    "behavior.pull_rebase": "true",
                    "diff.algorithm": "histogram"
                },
                "simple": {
                    "core.editor": "nano",
                    "aliases.common": ["st", "co", "br", "ci"],
                    "behavior.pull_rebase": "false"
                }
            }
        )
    
    def _create_vim_template(self) -> CustomizationTemplate:
        """Create Vim/Neovim customization template"""
        return CustomizationTemplate(
            app_name="vim",
            display_name="Vim/Neovim",
            description="Configure Vim with plugins, themes, and settings",
            icon="📝",
            categories=["appearance", "plugins", "keybindings", "behavior"],
            settings={
                "appearance": {
                    "colorscheme": DropdownConfig(
                        options=[
                            ("dracula", "Dracula"),
                            ("gruvbox", "Gruvbox"),
                            ("nord", "Nord"),
                            ("onedark", "One Dark"),
                            ("monokai", "Monokai"),
                            ("solarized", "Solarized"),
                            ("tokyonight", "Tokyo Night"),
                            ("catppuccin", "Catppuccin"),
                            ("material", "Material"),
                            ("palenight", "Palenight")
                        ],
                        current_value="dracula",
                        allow_custom=True
                    ),
                    "background": DropdownConfig(
                        options=[
                            ("dark", "Dark"),
                            ("light", "Light")
                        ],
                        current_value="dark",
                        allow_custom=False
                    ),
                    "font": DropdownConfig(
                        options=[
                            ("JetBrainsMono Nerd Font", "JetBrains Mono"),
                            ("FiraCode Nerd Font", "Fira Code"),
                            ("Hack Nerd Font", "Hack"),
                            ("SourceCodePro Nerd Font", "Source Code Pro")
                        ],
                        current_value="JetBrainsMono Nerd Font",
                        allow_custom=True
                    ),
                    "font_size": SliderConfig(
                        min_value=10,
                        max_value=20,
                        current_value=13,
                        step=1,
                        unit="pt"
                    ),
                    "line_numbers": DropdownConfig(
                        options=[
                            ("number", "Absolute"),
                            ("relativenumber", "Relative"),
                            ("number relativenumber", "Hybrid"),
                            ("nonumber", "None")
                        ],
                        current_value="number relativenumber",
                        allow_custom=False
                    ),
                    "cursorline": True,
                    "colorcolumn": "80,120",
                    "signcolumn": "yes"
                },
                "plugins": {
                    "plugin_manager": DropdownConfig(
                        options=[
                            ("vim-plug", "vim-plug"),
                            ("packer", "packer.nvim"),
                            ("lazy", "lazy.nvim"),
                            ("dein", "dein.vim"),
                            ("vundle", "Vundle")
                        ],
                        current_value="lazy",
                        allow_custom=False
                    ),
                    "essential": MultiSelectConfig(
                        options=[
                            ("nvim-treesitter", "Treesitter (syntax)", True),
                            ("nvim-lspconfig", "LSP Config", True),
                            ("nvim-cmp", "Completion", True),
                            ("telescope", "Telescope (fuzzy finder)", True),
                            ("nvim-tree", "File explorer", True),
                            ("gitsigns", "Git signs", True),
                            ("lualine", "Status line", True),
                            ("bufferline", "Buffer line", True),
                            ("indent-blankline", "Indent guides", True),
                            ("comment", "Easy commenting", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "languages": MultiSelectConfig(
                        options=[
                            ("python", "Python support", False),
                            ("go", "Go support", False),
                            ("rust", "Rust support", False),
                            ("javascript", "JS/TS support", False),
                            ("java", "Java support", False),
                            ("cpp", "C/C++ support", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "behavior": {
                    "tab_size": SliderConfig(
                        min_value=2,
                        max_value=8,
                        current_value=4,
                        step=2,
                        unit=" spaces"
                    ),
                    "expand_tab": True,
                    "auto_indent": True,
                    "smart_indent": True,
                    "wrap": False,
                    "mouse": DropdownConfig(
                        options=[
                            ("a", "All modes"),
                            ("n", "Normal mode only"),
                            ("v", "Visual mode only"),
                            ("", "Disabled")
                        ],
                        current_value="a",
                        allow_custom=False
                    ),
                    "clipboard": DropdownConfig(
                        options=[
                            ("unnamedplus", "System clipboard"),
                            ("unnamed", "Selection clipboard"),
                            ("", "Vim only")
                        ],
                        current_value="unnamedplus",
                        allow_custom=False
                    ),
                    "timeout_len": SliderConfig(
                        min_value=100,
                        max_value=2000,
                        current_value=500,
                        step=100,
                        unit="ms"
                    ),
                    "update_time": SliderConfig(
                        min_value=100,
                        max_value=1000,
                        current_value=300,
                        step=100,
                        unit="ms"
                    )
                },
                "keybindings": {
                    "leader": DropdownConfig(
                        options=[
                            (" ", "Space"),
                            (",", "Comma"),
                            ("\\", "Backslash"),
                            (";", "Semicolon")
                        ],
                        current_value=" ",
                        allow_custom=True
                    ),
                    "save": "<leader>w",
                    "quit": "<leader>q",
                    "save_quit": "<leader>wq",
                    "split_horizontal": "<leader>h",
                    "split_vertical": "<leader>v",
                    "next_buffer": "<Tab>",
                    "prev_buffer": "<S-Tab>",
                    "find_files": "<leader>ff",
                    "find_grep": "<leader>fg",
                    "file_tree": "<leader>e"
                }
            },
            presets={
                "modern": {
                    "appearance.colorscheme": "tokyonight",
                    "plugins.essential": ["nvim-treesitter", "nvim-lspconfig", "telescope", "nvim-tree"],
                    "behavior.mouse": "a",
                    "keybindings.leader": " "
                },
                "classic": {
                    "appearance.colorscheme": "solarized",
                    "plugins.essential": [],
                    "behavior.mouse": "",
                    "keybindings.leader": "\\"
                },
                "ide": {
                    "appearance.colorscheme": "onedark",
                    "plugins.essential": ["nvim-treesitter", "nvim-lspconfig", "nvim-cmp", "telescope", "nvim-tree", "gitsigns", "lualine", "bufferline"],
                    "behavior.mouse": "a",
                    "keybindings.leader": " "
                }
            }
        )
    
    def _create_gnome_terminal_template(self) -> CustomizationTemplate:
        """Create GNOME Terminal specific customization template"""
        return CustomizationTemplate(
            app_name="gnome_terminal",
            display_name="GNOME Terminal",
            description="GNOME Terminal specific settings",
            icon="🖥️",
            categories=["profiles", "shortcuts", "behavior"],
            settings={
                "profiles": {
                    "default_profile": {
                        "visible_name": "Default",
                        "use_theme_colors": False,
                        "use_theme_transparency": False,
                        "use_transparent_background": True,
                        "background_transparency_percent": SliderConfig(
                            min_value=0,
                            max_value=100,
                            current_value=95,
                            step=5,
                            unit="%",
                            show_percentage=True
                        ),
                        "scrollbar_policy": DropdownConfig(
                            options=[
                                ("always", "Always visible"),
                                ("automatic", "Automatic"),
                                ("never", "Never")
                            ],
                            current_value="automatic",
                            allow_custom=False
                        ),
                        "scroll_on_output": False,
                        "scroll_on_keystroke": True,
                        "unlimited_scrollback": False,
                        "scrollback_lines": SliderConfig(
                            min_value=512,
                            max_value=100000,
                            current_value=10000,
                            step=1000,
                            unit=" lines"
                        )
                    }
                },
                "window": {
                    "default_size_columns": SliderConfig(
                        min_value=40,
                        max_value=300,
                        current_value=80,
                        step=10,
                        unit=" cols"
                    ),
                    "default_size_rows": SliderConfig(
                        min_value=10,
                        max_value=100,
                        current_value=24,
                        step=2,
                        unit=" rows"
                    ),
                    "hide_menubar": True,
                    "default_show_menubar": False
                },
                "shortcuts": {
                    "new_tab": "Ctrl+Shift+T",
                    "new_window": "Ctrl+Shift+N",
                    "close_tab": "Ctrl+Shift+W",
                    "close_window": "Ctrl+Shift+Q",
                    "copy": "Ctrl+Shift+C",
                    "paste": "Ctrl+Shift+V",
                    "select_all": "Ctrl+Shift+A",
                    "find": "Ctrl+Shift+F",
                    "find_next": "Ctrl+G",
                    "find_previous": "Ctrl+Shift+G",
                    "clear": "Ctrl+Shift+K",
                    "reset": "Ctrl+Shift+R",
                    "zoom_in": "Ctrl+Plus",
                    "zoom_out": "Ctrl+Minus",
                    "normal_size": "Ctrl+0"
                }
            },
            presets={
                "default": {},
                "transparent": {
                    "profiles.default_profile.use_transparent_background": True,
                    "profiles.default_profile.background_transparency_percent": 85
                },
                "opaque": {
                    "profiles.default_profile.use_transparent_background": False,
                    "profiles.default_profile.background_transparency_percent": 100
                }
            }
        )
    
    def _create_system_template(self) -> CustomizationTemplate:
        """Create system preferences template"""
        return CustomizationTemplate(
            app_name="system",
            display_name="System Preferences",
            description="System-wide settings and preferences",
            icon="⚙️",
            categories=["mouse", "keyboard", "display", "power", "sound"],
            settings={
                "mouse": {
                    "speed": SliderConfig(
                        min_value=-1.0,
                        max_value=1.0,
                        current_value=0.0,
                        step=0.1
                    ),
                    "acceleration": SliderConfig(
                        min_value=1.0,
                        max_value=10.0,
                        current_value=2.0,
                        step=0.5
                    ),
                    "natural_scrolling": True,
                    "tap_to_click": True,
                    "two_finger_scrolling": True,
                    "edge_scrolling": False
                },
                "keyboard": {
                    "repeat_delay": SliderConfig(
                        min_value=100,
                        max_value=1000,
                        current_value=500,
                        step=50,
                        unit="ms"
                    ),
                    "repeat_rate": SliderConfig(
                        min_value=10,
                        max_value=100,
                        current_value=30,
                        step=5,
                        unit=" keys/sec"
                    ),
                    "layout": DropdownConfig(
                        options=[
                            ("us", "US"),
                            ("uk", "UK"),
                            ("de", "German"),
                            ("fr", "French"),
                            ("es", "Spanish"),
                            ("it", "Italian"),
                            ("ru", "Russian"),
                            ("jp", "Japanese")
                        ],
                        current_value="us",
                        allow_custom=True
                    ),
                    "compose_key": DropdownConfig(
                        options=[
                            ("", "Disabled"),
                            ("ralt", "Right Alt"),
                            ("lwin", "Left Windows"),
                            ("rwin", "Right Windows"),
                            ("menu", "Menu"),
                            ("rctrl", "Right Ctrl")
                        ],
                        current_value="",
                        allow_custom=False
                    )
                },
                "display": {
                    "scaling": SliderConfig(
                        min_value=100,
                        max_value=200,
                        current_value=100,
                        step=25,
                        unit="%",
                        show_percentage=True
                    ),
                    "night_light": {
                        "enabled": True,
                        "temperature": SliderConfig(
                            min_value=3000,
                            max_value=6500,
                            current_value=4000,
                            step=100,
                            unit="K"
                        ),
                        "schedule": DropdownConfig(
                            options=[
                                ("sunset", "Sunset to Sunrise"),
                                ("manual", "Manual Schedule"),
                                ("always", "Always On")
                            ],
                            current_value="sunset",
                            allow_custom=False
                        )
                    },
                    "fractional_scaling": False,
                    "orientation": DropdownConfig(
                        options=[
                            ("normal", "Normal"),
                            ("left", "90° Left"),
                            ("inverted", "180° Inverted"),
                            ("right", "90° Right")
                        ],
                        current_value="normal",
                        allow_custom=False
                    )
                },
                "power": {
                    "screen_blank": SliderConfig(
                        min_value=1,
                        max_value=60,
                        current_value=5,
                        step=1,
                        unit=" minutes"
                    ),
                    "suspend_on_battery": SliderConfig(
                        min_value=5,
                        max_value=120,
                        current_value=20,
                        step=5,
                        unit=" minutes"
                    ),
                    "suspend_on_ac": SliderConfig(
                        min_value=5,
                        max_value=120,
                        current_value=30,
                        step=5,
                        unit=" minutes"
                    ),
                    "power_button_action": DropdownConfig(
                        options=[
                            ("suspend", "Suspend"),
                            ("hibernate", "Hibernate"),
                            ("shutdown", "Shutdown"),
                            ("nothing", "Do Nothing"),
                            ("interactive", "Ask")
                        ],
                        current_value="suspend",
                        allow_custom=False
                    ),
                    "lid_close_battery": DropdownConfig(
                        options=[
                            ("suspend", "Suspend"),
                            ("hibernate", "Hibernate"),
                            ("shutdown", "Shutdown"),
                            ("nothing", "Do Nothing")
                        ],
                        current_value="suspend",
                        allow_custom=False
                    ),
                    "lid_close_ac": DropdownConfig(
                        options=[
                            ("suspend", "Suspend"),
                            ("hibernate", "Hibernate"),
                            ("shutdown", "Shutdown"),
                            ("nothing", "Do Nothing")
                        ],
                        current_value="nothing",
                        allow_custom=False
                    )
                },
                "sound": {
                    "output_volume": SliderConfig(
                        min_value=0,
                        max_value=150,
                        current_value=75,
                        step=5,
                        unit="%",
                        show_percentage=True
                    ),
                    "input_volume": SliderConfig(
                        min_value=0,
                        max_value=100,
                        current_value=50,
                        step=5,
                        unit="%",
                        show_percentage=True
                    ),
                    "over_amplification": True,
                    "system_sounds": True,
                    "alert_volume": SliderConfig(
                        min_value=0,
                        max_value=100,
                        current_value=100,
                        step=10,
                        unit="%",
                        show_percentage=True
                    )
                }
            },
            presets={
                "laptop": {
                    "mouse.tap_to_click": True,
                    "power.suspend_on_battery": 15,
                    "power.lid_close_battery": "suspend",
                    "display.scaling": 125
                },
                "desktop": {
                    "mouse.tap_to_click": False,
                    "power.suspend_on_ac": 60,
                    "power.lid_close_ac": "nothing",
                    "display.scaling": 100
                },
                "presentation": {
                    "power.screen_blank": 60,
                    "power.suspend_on_battery": 120,
                    "power.lid_close_battery": "nothing",
                    "power.lid_close_ac": "nothing"
                }
            }
        )
    
    def _create_shell_template(self) -> CustomizationTemplate:
        """Create shell customization template"""
        return CustomizationTemplate(
            app_name="shell",
            display_name="Shell Environment",
            description="Configure your shell (Bash, Zsh, Fish)",
            icon="🐚",
            categories=["general", "prompt", "aliases", "plugins"],
            settings={
                "general": {
                    "shell": DropdownConfig(
                        options=[
                            ("/bin/bash", "Bash"),
                            ("/usr/bin/zsh", "Zsh"),
                            ("/usr/bin/fish", "Fish"),
                            ("/usr/bin/dash", "Dash"),
                            ("/usr/bin/tcsh", "Tcsh")
                        ],
                        current_value="/bin/bash",
                        allow_custom=True
                    ),
                    "default_editor": DropdownConfig(
                        options=[
                            ("vim", "Vim"),
                            ("nano", "Nano"),
                            ("emacs", "Emacs"),
                            ("code", "VS Code"),
                            ("subl", "Sublime Text")
                        ],
                        current_value="vim",
                        allow_custom=True
                    ),
                    "history_size": SliderConfig(
                        min_value=1000,
                        max_value=100000,
                        current_value=10000,
                        step=1000,
                        unit=" commands"
                    ),
                    "history_ignore_duplicates": True,
                    "history_ignore_space": True,
                    "auto_cd": True,
                    "correct_commands": True
                },
                "prompt": {
                    "style": DropdownConfig(
                        options=[
                            ("starship", "Starship"),
                            ("powerlevel10k", "Powerlevel10k"),
                            ("oh-my-posh", "Oh My Posh"),
                            ("pure", "Pure"),
                            ("spaceship", "Spaceship"),
                            ("agnoster", "Agnoster"),
                            ("robbyrussell", "Robby Russell"),
                            ("minimal", "Minimal"),
                            ("custom", "Custom")
                        ],
                        current_value="starship",
                        allow_custom=True
                    ),
                    "show_git_status": True,
                    "show_python_env": True,
                    "show_node_version": True,
                    "show_time": False,
                    "show_battery": False,
                    "show_kubernetes": False,
                    "prompt_colors": {
                        "primary": "blue",
                        "success": "green",
                        "error": "red",
                        "warning": "yellow"
                    }
                },
                "aliases": {
                    "navigation": MultiSelectConfig(
                        options=[
                            ("ll", "ls -alF", True),
                            ("la", "ls -A", True),
                            ("l", "ls -CF", True),
                            ("..", "cd ..", True),
                            ("...", "cd ../..", True),
                            ("~", "cd ~", True),
                            ("-", "cd -", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "shortcuts": MultiSelectConfig(
                        options=[
                            ("g", "git", True),
                            ("gc", "git commit", True),
                            ("gp", "git push", True),
                            ("gl", "git pull", True),
                            ("gs", "git status", True),
                            ("d", "docker", True),
                            ("dc", "docker-compose", True),
                            ("k", "kubectl", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "safety": MultiSelectConfig(
                        options=[
                            ("rm", "rm -i", True),
                            ("cp", "cp -i", True),
                            ("mv", "mv -i", True),
                            ("ln", "ln -i", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "plugins": {
                    "zsh_framework": DropdownConfig(
                        options=[
                            ("oh-my-zsh", "Oh My Zsh"),
                            ("prezto", "Prezto"),
                            ("antigen", "Antigen"),
                            ("zplug", "Zplug"),
                            ("zinit", "Zinit"),
                            ("none", "None")
                        ],
                        current_value="oh-my-zsh",
                        allow_custom=False
                    ),
                    "zsh_plugins": MultiSelectConfig(
                        options=[
                            ("git", "Git", True),
                            ("docker", "Docker", True),
                            ("kubectl", "Kubectl", True),
                            ("npm", "NPM", True),
                            ("python", "Python", True),
                            ("zsh-autosuggestions", "Auto Suggestions", True),
                            ("zsh-syntax-highlighting", "Syntax Highlighting", True),
                            ("history-substring-search", "History Search", True),
                            ("fzf", "FZF Integration", True),
                            ("autojump", "Autojump", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "fish_plugins": MultiSelectConfig(
                        options=[
                            ("pure", "Pure prompt", True),
                            ("z", "Z directory jumper", True),
                            ("fzf", "FZF integration", True),
                            ("nvm", "Node version manager", True),
                            ("done", "Notification on completion", True),
                            ("bass", "Bash script compatibility", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                }
            },
            presets={
                "developer": {
                    "general.shell": "/usr/bin/zsh",
                    "prompt.style": "powerlevel10k",
                    "prompt.show_git_status": True,
                    "plugins.zsh_plugins": ["git", "docker", "kubectl", "zsh-autosuggestions", "zsh-syntax-highlighting"]
                },
                "minimal": {
                    "general.shell": "/bin/bash",
                    "prompt.style": "minimal",
                    "aliases.navigation": ["ll", "la", ".."],
                    "plugins.zsh_framework": "none"
                },
                "power_user": {
                    "general.shell": "/usr/bin/fish",
                    "prompt.style": "starship",
                    "general.history_size": 50000,
                    "plugins.fish_plugins": ["pure", "z", "fzf", "done"]
                }
            }
        )
    
    def _create_desktop_template(self) -> CustomizationTemplate:
        """Create desktop environment customization template"""
        return CustomizationTemplate(
            app_name="desktop",
            display_name="Desktop Environment",
            description="Customize your desktop appearance and behavior",
            icon="🖥️",
            categories=["appearance", "behavior", "extensions", "shortcuts"],
            settings={
                "appearance": {
                    "theme": DropdownConfig(
                        options=[
                            ("adwaita", "Adwaita (Default)"),
                            ("adwaita-dark", "Adwaita Dark"),
                            ("arc", "Arc"),
                            ("arc-dark", "Arc Dark"),
                            ("materia", "Materia"),
                            ("materia-dark", "Materia Dark"),
                            ("nordic", "Nordic"),
                            ("dracula", "Dracula"),
                            ("gruvbox", "Gruvbox"),
                            ("custom", "Custom...")
                        ],
                        current_value="adwaita-dark",
                        allow_custom=True
                    ),
                    "icon_theme": DropdownConfig(
                        options=[
                            ("adwaita", "Adwaita"),
                            ("papirus", "Papirus"),
                            ("numix", "Numix"),
                            ("numix-circle", "Numix Circle"),
                            ("la-capitaine", "La Capitaine"),
                            ("tela", "Tela"),
                            ("qogir", "Qogir"),
                            ("custom", "Custom...")
                        ],
                        current_value="papirus",
                        allow_custom=True
                    ),
                    "cursor_theme": DropdownConfig(
                        options=[
                            ("adwaita", "Adwaita"),
                            ("capitaine", "Capitaine"),
                            ("bibata", "Bibata Modern"),
                            ("mcmojave", "McMojave"),
                            ("breeze", "Breeze")
                        ],
                        current_value="capitaine",
                        allow_custom=True
                    ),
                    "wallpaper_mode": DropdownConfig(
                        options=[
                            ("wallpaper", "Single Image"),
                            ("centered", "Centered"),
                            ("scaled", "Scaled"),
                            ("stretched", "Stretched"),
                            ("zoom", "Zoom"),
                            ("spanned", "Spanned"),
                            ("slideshow", "Slideshow")
                        ],
                        current_value="zoom",
                        allow_custom=False
                    ),
                    "enable_animations": True,
                    "animation_speed": SliderConfig(
                        min_value=0.1,
                        max_value=2.0,
                        current_value=1.0,
                        step=0.1
                    )
                },
                "behavior": {
                    "click_action": DropdownConfig(
                        options=[
                            ("single", "Single Click"),
                            ("double", "Double Click")
                        ],
                        current_value="double",
                        allow_custom=False
                    ),
                    "workspace_behavior": DropdownConfig(
                        options=[
                            ("dynamic", "Dynamic Workspaces"),
                            ("static", "Static Number")
                        ],
                        current_value="dynamic",
                        allow_custom=False
                    ),
                    "num_workspaces": SliderConfig(
                        min_value=1,
                        max_value=10,
                        current_value=4,
                        step=1,
                        unit=" workspaces"
                    ),
                    "hot_corner": DropdownConfig(
                        options=[
                            ("", "Disabled"),
                            ("activities", "Show Activities"),
                            ("applications", "Show Applications"),
                            ("desktop", "Show Desktop")
                        ],
                        current_value="activities",
                        allow_custom=False
                    ),
                    "edge_tiling": True,
                    "center_new_windows": True,
                    "attach_modal_dialogs": True,
                    "focus_mode": DropdownConfig(
                        options=[
                            ("click", "Click to Focus"),
                            ("sloppy", "Focus on Hover"),
                            ("mouse", "Focus Follows Mouse")
                        ],
                        current_value="click",
                        allow_custom=False
                    )
                },
                "dock": {
                    "position": DropdownConfig(
                        options=[
                            ("left", "Left"),
                            ("bottom", "Bottom"),
                            ("right", "Right"),
                            ("top", "Top")
                        ],
                        current_value="left",
                        allow_custom=False
                    ),
                    "icon_size": SliderConfig(
                        min_value=16,
                        max_value=128,
                        current_value=48,
                        step=8,
                        unit="px"
                    ),
                    "autohide": True,
                    "autohide_delay": SliderConfig(
                        min_value=0.0,
                        max_value=1.0,
                        current_value=0.2,
                        step=0.1,
                        unit="s"
                    ),
                    "show_trash": True,
                    "show_mounted": True,
                    "click_action": DropdownConfig(
                        options=[
                            ("minimize", "Minimize"),
                            ("previews", "Show Previews"),
                            ("minimize-or-previews", "Minimize or Previews"),
                            ("cycle-windows", "Cycle Windows"),
                            ("launch", "Launch New")
                        ],
                        current_value="minimize-or-previews",
                        allow_custom=False
                    )
                },
                "extensions": {
                    "gnome_extensions": MultiSelectConfig(
                        options=[
                            ("dash-to-dock", "Dash to Dock", True),
                            ("appindicator", "AppIndicator Support", True),
                            ("blur-my-shell", "Blur My Shell", True),
                            ("vitals", "Vitals", True),
                            ("clipboard-indicator", "Clipboard Indicator", True),
                            ("caffeine", "Caffeine", True),
                            ("gsconnect", "GSConnect", False),
                            ("arc-menu", "Arc Menu", False),
                            ("dash-to-panel", "Dash to Panel", False),
                            ("material-shell", "Material Shell", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                }
            },
            presets={
                "macos_like": {
                    "appearance.theme": "materia",
                    "dock.position": "bottom",
                    "dock.icon_size": 48,
                    "behavior.click_action": "single",
                    "extensions.gnome_extensions": ["dash-to-dock", "blur-my-shell"]
                },
                "windows_like": {
                    "appearance.theme": "arc",
                    "dock.position": "bottom",
                    "extensions.gnome_extensions": ["dash-to-panel", "arc-menu"]
                },
                "minimal": {
                    "appearance.theme": "adwaita-dark",
                    "dock.autohide": True,
                    "appearance.enable_animations": False,
                    "extensions.gnome_extensions": []
                }
            }
        )
    
    def _create_development_template(self) -> CustomizationTemplate:
        """Create development environment customization template"""
        return CustomizationTemplate(
            app_name="development",
            display_name="Development Environment",
            description="Configure your development tools and workflow",
            icon="👨‍💻",
            categories=["languages", "tools", "environment", "workflow"],
            settings={
                "languages": {
                    "primary": DropdownConfig(
                        options=[
                            ("python", "Python"),
                            ("javascript", "JavaScript/TypeScript"),
                            ("go", "Go"),
                            ("rust", "Rust"),
                            ("java", "Java"),
                            ("cpp", "C/C++"),
                            ("csharp", "C#"),
                            ("ruby", "Ruby"),
                            ("php", "PHP")
                        ],
                        current_value="python",
                        allow_custom=True
                    ),
                    "additional": MultiSelectConfig(
                        options=[
                            ("python", "Python", True),
                            ("javascript", "JavaScript", True),
                            ("typescript", "TypeScript", True),
                            ("go", "Go", False),
                            ("rust", "Rust", False),
                            ("java", "Java", False),
                            ("cpp", "C/C++", False),
                            ("csharp", "C#", False),
                            ("ruby", "Ruby", False),
                            ("php", "PHP", False),
                            ("dart", "Dart", False),
                            ("swift", "Swift", False),
                            ("kotlin", "Kotlin", False),
                            ("scala", "Scala", False),
                            ("elixir", "Elixir", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "tools": {
                    "package_managers": MultiSelectConfig(
                        options=[
                            ("npm", "NPM", True),
                            ("yarn", "Yarn", False),
                            ("pnpm", "PNPM", False),
                            ("pip", "Pip", True),
                            ("poetry", "Poetry", False),
                            ("cargo", "Cargo", False),
                            ("gem", "Gem", False),
                            ("composer", "Composer", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "version_managers": MultiSelectConfig(
                        options=[
                            ("nvm", "NVM (Node)", True),
                            ("pyenv", "Pyenv (Python)", True),
                            ("rbenv", "Rbenv (Ruby)", False),
                            ("gvm", "GVM (Go)", False),
                            ("rustup", "Rustup (Rust)", False),
                            ("sdkman", "SDKMAN (Java)", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "containers": MultiSelectConfig(
                        options=[
                            ("docker", "Docker", True),
                            ("podman", "Podman", False),
                            ("kubernetes", "Kubernetes", True),
                            ("docker-compose", "Docker Compose", True),
                            ("minikube", "Minikube", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                },
                "environment": {
                    "default_branch": DropdownConfig(
                        options=[
                            ("main", "main"),
                            ("master", "master"),
                            ("develop", "develop"),
                            ("trunk", "trunk")
                        ],
                        current_value="main",
                        allow_custom=True
                    ),
                    "commit_style": DropdownConfig(
                        options=[
                            ("conventional", "Conventional Commits"),
                            ("angular", "Angular Style"),
                            ("emoji", "Gitmoji"),
                            ("simple", "Simple"),
                            ("custom", "Custom")
                        ],
                        current_value="conventional",
                        allow_custom=False
                    ),
                    "code_style": {
                        "indent_style": DropdownConfig(
                            options=[
                                ("space", "Spaces"),
                                ("tab", "Tabs")
                            ],
                            current_value="space",
                            allow_custom=False
                        ),
                        "indent_size": SliderConfig(
                            min_value=2,
                            max_value=8,
                            current_value=4,
                            step=2,
                            unit=" spaces"
                        ),
                        "line_length": SliderConfig(
                            min_value=80,
                            max_value=120,
                            current_value=100,
                            step=10,
                            unit=" chars"
                        ),
                        "insert_final_newline": True,
                        "trim_trailing_whitespace": True
                    }
                },
                "workflow": {
                    "auto_format": True,
                    "auto_lint": True,
                    "pre_commit_hooks": MultiSelectConfig(
                        options=[
                            ("prettier", "Prettier", True),
                            ("eslint", "ESLint", True),
                            ("black", "Black", True),
                            ("isort", "isort", True),
                            ("flake8", "Flake8", True),
                            ("mypy", "Mypy", False),
                            ("pytest", "Pytest", True),
                            ("commitlint", "Commitlint", True)
                        ],
                        max_selections=None,
                        min_selections=0
                    ),
                    "test_runner": DropdownConfig(
                        options=[
                            ("pytest", "Pytest"),
                            ("jest", "Jest"),
                            ("mocha", "Mocha"),
                            ("go-test", "Go Test"),
                            ("cargo-test", "Cargo Test"),
                            ("junit", "JUnit")
                        ],
                        current_value="pytest",
                        allow_custom=True
                    ),
                    "continuous_integration": MultiSelectConfig(
                        options=[
                            ("github-actions", "GitHub Actions", True),
                            ("gitlab-ci", "GitLab CI", False),
                            ("circleci", "CircleCI", False),
                            ("travis", "Travis CI", False),
                            ("jenkins", "Jenkins", False),
                            ("azure-pipelines", "Azure Pipelines", False)
                        ],
                        max_selections=None,
                        min_selections=0
                    )
                }
            },
            presets={
                "fullstack": {
                    "languages.primary": "javascript",
                    "languages.additional": ["javascript", "typescript", "python"],
                    "tools.package_managers": ["npm", "yarn", "pip"],
                    "workflow.pre_commit_hooks": ["prettier", "eslint", "commitlint"]
                },
                "backend": {
                    "languages.primary": "python",
                    "languages.additional": ["python", "go"],
                    "tools.package_managers": ["pip", "poetry"],
                    "workflow.pre_commit_hooks": ["black", "isort", "flake8", "pytest"]
                },
                "data_science": {
                    "languages.primary": "python",
                    "languages.additional": ["python", "r"],
                    "tools.package_managers": ["pip", "poetry"],
                    "environment.code_style.line_length": 88
                }
            }
        )
    
    def get_template(self, app_name: str) -> CustomizationTemplate:
        """Get a specific application template"""
        return self.templates.get(app_name)
    
    def list_templates(self) -> List[Tuple[str, str, str]]:
        """List all available templates"""
        return [(name, template.display_name, template.icon) 
                for name, template in self.templates.items()]
    
    def apply_preset(self, template_name: str, preset_name: str) -> Dict[str, Any]:
        """Apply a preset to get settings"""
        template = self.get_template(template_name)
        if not template or preset_name not in template.presets:
            return {}
        
        return template.presets[preset_name]
    
    def get_setting_widget(self, template_name: str, setting_path: str) -> Any:
        """Get the widget configuration for a specific setting"""
        template = self.get_template(template_name)
        if not template:
            return None
        
        # Navigate through the settings path
        parts = setting_path.split('.')
        current = template.settings
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current