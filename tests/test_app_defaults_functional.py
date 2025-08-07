#!/usr/bin/env python3
"""
Functional tests for app_defaults module
Tests application default configurations and file generation
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from lib.app_defaults import AppDefaults, get_app_defaults


class TestAppDefaultsFunctional:
    """Test AppDefaults functionality"""

    def setup_method(self):
        """Setup test instance"""
        self.app_defaults = AppDefaults()

    def test_init(self):
        """Test AppDefaults initialization"""
        app_defaults = AppDefaults()

        assert app_defaults is not None
        assert hasattr(app_defaults, "developer_apps")
        assert hasattr(app_defaults, "user_apps")
        assert isinstance(app_defaults.developer_apps, dict)
        assert isinstance(app_defaults.user_apps, dict)

    def test_load_developer_defaults(self):
        """Test loading developer defaults"""
        developer_apps = self.app_defaults._load_developer_defaults()

        # Check key developer apps exist
        assert "vscode" in developer_apps
        assert "git" in developer_apps
        assert "terminal" in developer_apps
        assert "docker" in developer_apps

        # Check vscode structure
        vscode = developer_apps["vscode"]
        assert "name" in vscode
        assert vscode["name"] == "Visual Studio Code"
        assert "features" in vscode
        assert "extensions" in vscode
        assert "settings" in vscode
        assert isinstance(vscode["features"], list)
        assert isinstance(vscode["extensions"], list)
        assert isinstance(vscode["settings"], dict)

        # Check vscode settings
        assert vscode["settings"]["editor.formatOnSave"] is True
        assert vscode["settings"]["files.autoSave"] == "afterDelay"

    def test_load_user_defaults(self):
        """Test loading user defaults"""
        user_apps = self.app_defaults._load_user_defaults()

        # Check key user apps exist
        assert "firefox" in user_apps
        assert "vlc" in user_apps
        assert "thunderbird" in user_apps
        assert "libreoffice" in user_apps
        assert "system" in user_apps

        # Check firefox structure
        firefox = user_apps["firefox"]
        assert "name" in firefox
        assert firefox["name"] == "Firefox Web Browser"
        assert "features" in firefox
        assert "extensions" in firefox
        assert "settings" in firefox
        assert "preview" in firefox
        assert "help" in firefox

    def test_get_app_config_developer(self):
        """Test getting developer app configuration"""
        config = self.app_defaults.get_app_config("vscode", "developer")

        assert config is not None
        assert config["name"] == "Visual Studio Code"
        assert "settings" in config
        assert config["settings"]["editor.formatOnSave"] is True

    def test_get_app_config_user(self):
        """Test getting user app configuration"""
        config = self.app_defaults.get_app_config("firefox", "user")

        assert config is not None
        assert config["name"] == "Firefox Web Browser"
        assert "settings" in config
        assert config["settings"]["privacy.trackingprotection.enabled"] is True

    def test_get_app_config_nonexistent(self):
        """Test getting config for non-existent app"""
        config = self.app_defaults.get_app_config("nonexistent", "developer")

        assert config == {}

    def test_get_all_apps_developer(self):
        """Test getting all developer apps"""
        apps = self.app_defaults.get_all_apps("developer")

        assert isinstance(apps, list)
        assert "vscode" in apps
        assert "git" in apps
        assert "terminal" in apps
        assert "docker" in apps

    def test_get_all_apps_user(self):
        """Test getting all user apps"""
        apps = self.app_defaults.get_all_apps("user")

        assert isinstance(apps, list)
        assert "firefox" in apps
        assert "vlc" in apps
        assert "thunderbird" in apps
        assert "system" in apps

    def test_generate_config_files_vscode(self):
        """Test generating VS Code configuration files"""
        settings = {
            "settings": {"editor.formatOnSave": True, "editor.fontSize": 14, "workbench.colorTheme": "Dark+"},
            "extensions": ["GitLens - Supercharged", "Prettier - Code formatter", "Python - Language support"],
        }

        config_files = self.app_defaults.generate_config_files("vscode", settings)

        assert "settings.json" in config_files
        assert "extensions.txt" in config_files

        # Check settings.json
        settings_json = json.loads(config_files["settings.json"])
        assert settings_json["editor.formatOnSave"] is True
        assert settings_json["editor.fontSize"] == 14

        # Check extensions.txt
        extensions = config_files["extensions.txt"].split("\n")
        assert "gitlens" in extensions
        assert "prettier" in extensions
        assert "python" in extensions

    def test_generate_config_files_git(self):
        """Test generating Git configuration files"""
        settings = {
            "aliases": {"st": "status", "co": "checkout", "br": "branch"},
            "settings": {"init.defaultBranch": "main", "color.ui": "auto", "pull.rebase": True},
        }

        config_files = self.app_defaults.generate_config_files("git", settings)

        assert ".gitconfig" in config_files

        gitconfig = config_files[".gitconfig"]

        # Check aliases
        assert "[alias]" in gitconfig
        assert "st = status" in gitconfig
        assert "co = checkout" in gitconfig
        assert "br = branch" in gitconfig

        # Check settings
        assert "[init]" in gitconfig
        assert "defaultBranch = main" in gitconfig
        assert "[color]" in gitconfig
        assert "ui = auto" in gitconfig

    def test_generate_config_files_terminal(self):
        """Test generating terminal configuration files"""
        settings = {"aliases": {"ll": "ls -la", "gs": "git status", "..": "cd .."}}

        config_files = self.app_defaults.generate_config_files("terminal", settings)

        assert ".zshrc" in config_files

        zshrc = config_files[".zshrc"]

        # Check header
        assert "Ubuntu Bootstrap Terminal Configuration" in zshrc

        # Check aliases
        assert "alias ll='ls -la'" in zshrc
        assert "alias gs='git status'" in zshrc
        assert "alias ..='cd ..'" in zshrc

    def test_generate_config_files_firefox(self):
        """Test generating Firefox configuration files"""
        settings = {
            "settings": {
                "privacy.trackingprotection.enabled": True,
                "browser.download.useDownloadDir": False,
                "browser.tabs.closeWindowWithLastTab": False,
                "media.autoplay.default": 1,
                "browser.newtabpage.activity-stream.showSponsored": False,
            }
        }

        config_files = self.app_defaults.generate_config_files("firefox", settings)

        assert "user.js" in config_files

        userjs = config_files["user.js"]

        # Check header
        assert "Ubuntu Bootstrap Firefox Configuration" in userjs

        # Check preferences
        assert 'user_pref("privacy.trackingprotection.enabled", true);' in userjs
        assert 'user_pref("browser.download.useDownloadDir", false);' in userjs
        assert 'user_pref("media.autoplay.default", 1);' in userjs

    def test_generate_config_files_unsupported(self):
        """Test generating config for unsupported app"""
        settings = {"some": "settings"}

        config_files = self.app_defaults.generate_config_files("unsupported", settings)

        assert config_files == {}

    def test_generate_vscode_config_detailed(self):
        """Test detailed VS Code config generation"""
        settings = {
            "settings": {
                "editor.formatOnSave": True,
                "editor.bracketPairColorization.enabled": True,
                "files.autoSave": "afterDelay",
                "files.autoSaveDelay": 1000,
                "terminal.integrated.fontFamily": "MesloLGS NF",
            },
            "extensions": [
                "GitLens - Git supercharged",
                "Error Lens - Show errors inline",
                "TODO Highlight - Highlight TODOs",
            ],
        }

        config = self.app_defaults._generate_vscode_config(settings)

        assert "settings.json" in config
        assert "extensions.txt" in config

        # Verify JSON is valid
        settings_obj = json.loads(config["settings.json"])
        assert settings_obj["editor.formatOnSave"] is True
        assert settings_obj["files.autoSaveDelay"] == 1000

        # Verify extension format
        assert "gitlens" in config["extensions.txt"]
        assert "error-lens" in config["extensions.txt"]
        assert "todo-highlight" in config["extensions.txt"]

    def test_generate_git_config_comprehensive(self):
        """Test comprehensive Git config generation"""
        settings = {
            "aliases": {
                "st": "status",
                "visual": "log --graph --pretty=format:'%h - %s'",
                "undo": "reset --soft HEAD~1",
            },
            "settings": {
                "user.name": "Test User",
                "user.email": "test@example.com",
                "init.defaultBranch": "main",
                "core.editor": "vim",
                "pull.rebase": True,
                "diff.algorithm": "histogram",
            },
        }

        config = self.app_defaults._generate_git_config(settings)

        gitconfig = config[".gitconfig"]

        # Check structure
        assert "[user]" in gitconfig
        assert "[alias]" in gitconfig
        assert "[init]" in gitconfig
        assert "[core]" in gitconfig
        assert "[pull]" in gitconfig
        assert "[diff]" in gitconfig

        # Check values
        assert "defaultBranch = main" in gitconfig
        assert "editor = vim" in gitconfig
        assert "rebase = True" in gitconfig
        assert "algorithm = histogram" in gitconfig

    def test_system_preferences_comprehensive(self):
        """Test system preferences are comprehensive"""
        system_config = self.app_defaults.user_apps.get("system", {})

        # Check all major sections exist
        assert "mouse_touchpad" in system_config
        assert "keyboard" in system_config
        assert "clipboard" in system_config
        assert "workspaces" in system_config
        assert "notifications" in system_config
        assert "window_management" in system_config
        assert "display" in system_config
        assert "fonts" in system_config
        assert "accessibility" in system_config
        assert "shortcuts" in system_config
        assert "power" in system_config
        assert "dock_panel" in system_config
        assert "privacy" in system_config

        # Check mouse/touchpad settings
        mouse = system_config["mouse_touchpad"]
        assert "natural_scrolling" in mouse
        assert "tap_to_click" in mouse
        assert "palm_detection" in mouse

        # Check keyboard settings
        keyboard = system_config["keyboard"]
        assert "repeat_delay" in keyboard
        assert "caps_lock_behavior" in keyboard

        # Check shortcuts
        shortcuts = system_config["shortcuts"]
        assert "Super+T" in shortcuts
        assert "Alt+Tab" in shortcuts
        assert "Super+L" in shortcuts

    def test_firefox_config_with_types(self):
        """Test Firefox config handles different value types"""
        settings = {"settings": {"boolean.pref": True, "string.pref": "value", "number.pref": 42, "float.pref": 3.14}}

        config = self.app_defaults._generate_firefox_config(settings)
        userjs = config["user.js"]

        assert 'user_pref("boolean.pref", true);' in userjs
        assert 'user_pref("string.pref", "value");' in userjs
        assert 'user_pref("number.pref", 42);' in userjs
        assert 'user_pref("float.pref", 3.14);' in userjs

    def test_get_app_defaults_factory(self):
        """Test factory function for creating AppDefaults"""
        app_defaults = get_app_defaults()

        assert isinstance(app_defaults, AppDefaults)
        assert hasattr(app_defaults, "developer_apps")
        assert hasattr(app_defaults, "user_apps")

    def test_docker_configuration(self):
        """Test Docker configuration exists and is valid"""
        docker_config = self.app_defaults.developer_apps.get("docker", {})

        assert docker_config is not None
        assert "name" in docker_config
        assert "features" in docker_config
        assert "aliases" in docker_config
        assert "settings" in docker_config

        # Check aliases
        aliases = docker_config["aliases"]
        assert "dps" in aliases
        assert aliases["dps"] == "docker ps"
        assert "dc" in aliases
        assert aliases["dc"] == "docker compose"

    def test_vlc_configuration(self):
        """Test VLC configuration exists and is valid"""
        vlc_config = self.app_defaults.user_apps.get("vlc", {})

        assert vlc_config is not None
        assert "name" in vlc_config
        assert "features" in vlc_config
        assert "settings" in vlc_config
        assert "shortcuts" in vlc_config

        # Check shortcuts
        shortcuts = vlc_config["shortcuts"]
        assert "Space" in shortcuts
        assert "F" in shortcuts
        assert shortcuts["Space"] == "Play/Pause"
        assert shortcuts["F"] == "Fullscreen"

    def test_thunderbird_configuration(self):
        """Test Thunderbird configuration exists and is valid"""
        thunderbird_config = self.app_defaults.user_apps.get("thunderbird", {})

        assert thunderbird_config is not None
        assert "name" in thunderbird_config
        assert "features" in thunderbird_config
        assert "settings" in thunderbird_config

        # Check settings
        settings = thunderbird_config["settings"]
        assert "mail.compose.attachment_reminder" in settings
        assert settings["mail.compose.attachment_reminder"] is True

    def test_libreoffice_configuration(self):
        """Test LibreOffice configuration exists and is valid"""
        libreoffice_config = self.app_defaults.user_apps.get("libreoffice", {})

        assert libreoffice_config is not None
        assert "name" in libreoffice_config
        assert "features" in libreoffice_config
        assert "settings" in libreoffice_config

        # Check settings
        settings = libreoffice_config["settings"]
        assert "save.auto_save" in settings
        assert settings["save.auto_save"] is True
        assert "save.auto_save_interval" in settings
        assert settings["save.auto_save_interval"] == 10
