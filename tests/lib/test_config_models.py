"""
Unit tests for config_models.py - Configuration data models and validation.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
import yaml

from lib.config_models import (
    DesktopEnvironment, Shell, TaskbarPosition, GlobalTheme, DevelopmentLanguage,
    SystemConfig, UserConfig, DesktopConfig, SecurityConfig, DevelopmentConfig,
    ApplicationsConfig, PackageManagementConfig, DotfilesConfig, UpdatesConfig,
    BackupConfig, FeatureFlags, BootstrapConfiguration,
    create_default_config, load_config, save_config
)


class TestEnums:
    """Test enum definitions."""
    
    def test_desktop_environment_values(self):
        """Test DesktopEnvironment enum values."""
        assert DesktopEnvironment.GNOME.value == "gnome"
        assert DesktopEnvironment.KDE.value == "kde"
        assert DesktopEnvironment.XFCE.value == "xfce"
        assert DesktopEnvironment.MATE.value == "mate"
        assert DesktopEnvironment.CINNAMON.value == "cinnamon"
    
    def test_shell_values(self):
        """Test Shell enum values."""
        assert Shell.BASH.value == "/bin/bash"
        assert Shell.ZSH.value == "/bin/zsh"
        assert Shell.FISH.value == "/usr/bin/fish"
    
    def test_taskbar_position_values(self):
        """Test TaskbarPosition enum values."""
        assert TaskbarPosition.BOTTOM.value == "bottom"
        assert TaskbarPosition.TOP.value == "top"
        assert TaskbarPosition.LEFT.value == "left"
        assert TaskbarPosition.RIGHT.value == "right"
    
    def test_global_theme_values(self):
        """Test GlobalTheme enum values."""
        assert GlobalTheme.NONE.value == "none"
        assert GlobalTheme.DRACULA.value == "dracula"
        assert GlobalTheme.CATPPUCCIN.value == "catppuccin"
        assert GlobalTheme.TOKYO_NIGHT.value == "tokyo-night"
        assert GlobalTheme.NORD.value == "nord"
        assert GlobalTheme.GRUVBOX.value == "gruvbox"
    
    def test_development_language_values(self):
        """Test DevelopmentLanguage enum values."""
        languages = [
            ("PYTHON", "python"),
            ("NODEJS", "nodejs"),
            ("GO", "go"),
            ("RUST", "rust"),
            ("JAVA", "java"),
            ("CPP", "cpp"),
            ("JAVASCRIPT", "javascript"),
            ("TYPESCRIPT", "typescript")
        ]
        for attr, value in languages:
            assert getattr(DevelopmentLanguage, attr).value == value


class TestSystemConfig:
    """Test SystemConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for SystemConfig."""
        config = SystemConfig()
        assert config.timezone == "America/New_York"
        assert config.locale == "en_US.UTF-8"
        assert config.hostname is None
        assert config.enable_performance_tweaks is False
        assert config.swappiness_value == 10
        assert config.enable_tmpfs is False
    
    def test_custom_values(self):
        """Test custom values for SystemConfig."""
        config = SystemConfig(
            timezone="Europe/London",
            locale="en_GB.UTF-8",
            hostname="myubuntu",
            enable_performance_tweaks=True,
            swappiness_value=5,
            enable_tmpfs=True
        )
        assert config.timezone == "Europe/London"
        assert config.locale == "en_GB.UTF-8"
        assert config.hostname == "myubuntu"
        assert config.enable_performance_tweaks is True
        assert config.swappiness_value == 5
        assert config.enable_tmpfs is True


class TestUserConfig:
    """Test UserConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for UserConfig."""
        config = UserConfig()
        assert config.primary_user is None
        assert config.primary_user_shell == Shell.BASH
        assert config.create_user_groups == ["docker", "vboxusers"]
    
    def test_custom_values(self):
        """Test custom values for UserConfig."""
        config = UserConfig(
            primary_user="testuser",
            primary_user_shell=Shell.ZSH,
            create_user_groups=["docker", "sudo", "audio"]
        )
        assert config.primary_user == "testuser"
        assert config.primary_user_shell == Shell.ZSH
        assert config.create_user_groups == ["docker", "sudo", "audio"]


class TestDesktopConfig:
    """Test DesktopConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for DesktopConfig."""
        config = DesktopConfig()
        assert config.desktop_environment == DesktopEnvironment.GNOME
        assert config.install_desktop_environment is True
        assert config.desktop_autologin is False
        assert config.desktop_theme == "default"
        assert config.taskbar_position == TaskbarPosition.BOTTOM
        assert config.desktop_icons == ["home", "trash"]
        assert config.desktop_icon_size == 64
        assert config.trackpad_natural_scroll is False
        assert config.global_theme == GlobalTheme.NONE
    
    def test_custom_values(self):
        """Test custom values for DesktopConfig."""
        config = DesktopConfig(
            desktop_environment=DesktopEnvironment.KDE,
            install_desktop_environment=False,
            desktop_autologin=True,
            desktop_theme="breeze-dark",
            taskbar_position=TaskbarPosition.TOP,
            desktop_icons=["home", "trash", "computer"],
            desktop_icon_size=48,
            trackpad_natural_scroll=True,
            global_theme=GlobalTheme.DRACULA
        )
        assert config.desktop_environment == DesktopEnvironment.KDE
        assert config.install_desktop_environment is False
        assert config.desktop_autologin is True
        assert config.desktop_theme == "breeze-dark"
        assert config.taskbar_position == TaskbarPosition.TOP
        assert config.desktop_icons == ["home", "trash", "computer"]
        assert config.desktop_icon_size == 48
        assert config.trackpad_natural_scroll is True
        assert config.global_theme == GlobalTheme.DRACULA


class TestSecurityConfig:
    """Test SecurityConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for SecurityConfig."""
        config = SecurityConfig()
        assert config.enable_security is True
        assert config.enable_firewall is True
        assert config.enable_fail2ban is True
        assert config.ssh_permit_root_login is False
        assert config.ssh_password_authentication is False
    
    def test_validate_success(self):
        """Test successful validation."""
        config = SecurityConfig()
        errors = config.validate()
        assert errors == []
    
    def test_validate_firewall_disabled(self):
        """Test validation with firewall disabled but security enabled."""
        config = SecurityConfig(enable_security=True, enable_firewall=False)
        errors = config.validate()
        assert len(errors) == 1
        assert "Firewall should be enabled" in errors[0]
    
    def test_validate_security_disabled(self):
        """Test validation with security disabled."""
        config = SecurityConfig(enable_security=False, enable_firewall=False)
        errors = config.validate()
        assert errors == []  # No error when security is disabled


class TestDevelopmentConfig:
    """Test DevelopmentConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for DevelopmentConfig."""
        config = DevelopmentConfig()
        assert config.enable_development_tools is False
        assert config.development_languages == [DevelopmentLanguage.PYTHON, DevelopmentLanguage.NODEJS]
        assert config.install_docker is False
        assert config.install_vscode is False
        assert config.install_jetbrains_toolbox is False
        assert config.install_github_cli is False
        assert config.install_hashicorp_tools is False
    
    def test_get_required_groups(self):
        """Test get_required_groups method."""
        config = DevelopmentConfig()
        assert config.get_required_groups() == []
        
        config.install_docker = True
        assert config.get_required_groups() == ["docker"]
    
    def test_validate_docker_group(self):
        """Test validation for Docker group requirement."""
        config = DevelopmentConfig(install_docker=True)
        errors = config.validate()
        assert len(errors) == 1
        assert "Docker group should be added" in errors[0]


class TestApplicationsConfig:
    """Test ApplicationsConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for ApplicationsConfig."""
        config = ApplicationsConfig()
        assert config.install_applications is True
        assert config.default_browser == "firefox"
        assert "curl" in config.essential_packages
        assert "wget" in config.essential_packages
        assert "git" in config.essential_packages
        assert "firefox" in config.productivity_apps
        assert "vlc" in config.multimedia_apps
        assert "discord" in config.communication_apps


class TestPackageManagementConfig:
    """Test PackageManagementConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for PackageManagementConfig."""
        config = PackageManagementConfig()
        assert config.enable_flatpak is True
        assert config.enable_snap is True
        assert config.enable_appimage_support is True
        assert config.use_third_party_repos is True
        assert config.custom_apt_repositories == []
        assert config.custom_apt_keys == []


class TestDotfilesConfig:
    """Test DotfilesConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for DotfilesConfig."""
        config = DotfilesConfig()
        assert config.configure_dotfiles is True
        assert config.dotfiles_repo == ""
        assert config.dotfiles_repo_local_dest == "~/dotfiles"
        assert config.dotfiles_files_to_link == []
    
    def test_validate_missing_repo(self):
        """Test validation when repo is missing."""
        config = DotfilesConfig(configure_dotfiles=True, dotfiles_repo="")
        errors = config.validate()
        assert len(errors) == 1
        assert "Dotfiles repository URL is required" in errors[0]
    
    def test_validate_with_repo(self):
        """Test validation with repo provided."""
        config = DotfilesConfig(
            configure_dotfiles=True,
            dotfiles_repo="https://github.com/user/dotfiles"
        )
        errors = config.validate()
        assert errors == []


class TestBackupConfig:
    """Test BackupConfig dataclass."""
    
    def test_default_values(self):
        """Test default values for BackupConfig."""
        config = BackupConfig()
        assert config.enable_backup is False
        assert config.backup_directories == []
        assert config.backup_destination == ""
    
    def test_validate_missing_destination(self):
        """Test validation when destination is missing."""
        config = BackupConfig(enable_backup=True, backup_destination="")
        errors = config.validate()
        assert len(errors) == 1
        assert "Backup destination is required" in errors[0]
    
    def test_validate_with_destination(self):
        """Test validation with destination provided."""
        config = BackupConfig(
            enable_backup=True,
            backup_destination="/mnt/backup"
        )
        errors = config.validate()
        assert errors == []


class TestBootstrapConfiguration:
    """Test BootstrapConfiguration main class."""
    
    def test_default_initialization(self):
        """Test default initialization of all subsections."""
        config = BootstrapConfiguration()
        assert isinstance(config.system, SystemConfig)
        assert isinstance(config.user, UserConfig)
        assert isinstance(config.desktop, DesktopConfig)
        assert isinstance(config.security, SecurityConfig)
        assert isinstance(config.development, DevelopmentConfig)
        assert isinstance(config.applications, ApplicationsConfig)
        assert isinstance(config.package_management, PackageManagementConfig)
        assert isinstance(config.dotfiles, DotfilesConfig)
        assert isinstance(config.updates, UpdatesConfig)
        assert isinstance(config.backup, BackupConfig)
        assert isinstance(config.features, FeatureFlags)
    
    def test_validate_all_sections(self):
        """Test validation across all sections."""
        config = BootstrapConfiguration()
        errors = config.validate()
        assert errors == []
    
    def test_validate_docker_group_cross_section(self):
        """Test cross-section validation for Docker group."""
        config = BootstrapConfiguration()
        config.development.install_docker = True
        config.user.create_user_groups = ["sudo"]  # Missing docker group
        
        errors = config.validate()
        assert len(errors) == 2  # One from development, one from cross-section
        assert any("Docker group" in error for error in errors)
    
    def test_to_ansible_vars(self):
        """Test conversion to Ansible variables."""
        config = BootstrapConfiguration()
        config.system.timezone = "UTC"
        config.user.primary_user = "testuser"
        config.desktop.desktop_environment = DesktopEnvironment.KDE
        
        ansible_vars = config.to_ansible_vars()
        
        assert ansible_vars["system_timezone"] == "UTC"
        assert ansible_vars["primary_user"] == "testuser"
        assert ansible_vars["desktop_environment"] == "kde"
        assert ansible_vars["primary_user_shell"] == "/bin/bash"
        assert isinstance(ansible_vars["development_languages"], list)
    
    def test_save_to_yaml(self, tmp_path):
        """Test saving configuration to YAML file."""
        config = BootstrapConfiguration()
        config.system.timezone = "Europe/Paris"
        config.desktop.desktop_environment = DesktopEnvironment.XFCE
        
        yaml_file = tmp_path / "test_config.yml"
        config.save_to_yaml(str(yaml_file))
        
        assert yaml_file.exists()
        
        with open(yaml_file, 'r') as f:
            content = f.read()
            assert "Ubuntu Bootstrap Configuration" in content
            assert "system_timezone: Europe/Paris" in content
            assert "desktop_environment: xfce" in content
    
    def test_load_from_yaml(self, tmp_path):
        """Test loading configuration from YAML file."""
        # Create a test YAML file
        yaml_content = """
system_timezone: Asia/Tokyo
system_locale: ja_JP.UTF-8
desktop_environment: kde
primary_user_shell: /bin/zsh
development_languages:
  - python
  - rust
  - go
install_docker: true
enable_firewall: false
"""
        yaml_file = tmp_path / "test_config.yml"
        with open(yaml_file, 'w') as f:
            f.write(yaml_content)
        
        # Load configuration
        config = BootstrapConfiguration.load_from_yaml(str(yaml_file))
        
        assert config.system.timezone == "Asia/Tokyo"
        assert config.system.locale == "ja_JP.UTF-8"
        assert config.desktop.desktop_environment == DesktopEnvironment.KDE
        assert config.user.primary_user_shell == Shell.ZSH
        assert DevelopmentLanguage.PYTHON in config.development.development_languages
        assert DevelopmentLanguage.RUST in config.development.development_languages
        assert DevelopmentLanguage.GO in config.development.development_languages
        assert config.development.install_docker is True
        assert config.security.enable_firewall is False
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file returns default config."""
        config = BootstrapConfiguration.load_from_yaml("/tmp/nonexistent_file.yml")
        assert config.system.timezone == "America/New_York"  # Default value
    
    def test_load_from_empty_file(self, tmp_path):
        """Test loading from empty file returns default config."""
        empty_file = tmp_path / "empty.yml"
        empty_file.touch()
        
        config = BootstrapConfiguration.load_from_yaml(str(empty_file))
        assert config.system.timezone == "America/New_York"  # Default value
    
    def test_load_with_invalid_enum_values(self, tmp_path):
        """Test loading with invalid enum values uses defaults."""
        yaml_content = """
desktop_environment: invalid_desktop
primary_user_shell: /bin/invalid_shell
taskbar_position: invalid_position
development_languages:
  - python
  - invalid_language
  - nodejs
"""
        yaml_file = tmp_path / "invalid_config.yml"
        with open(yaml_file, 'w') as f:
            f.write(yaml_content)
        
        config = BootstrapConfiguration.load_from_yaml(str(yaml_file))
        
        # Invalid values should be ignored, defaults used
        assert config.desktop.desktop_environment == DesktopEnvironment.GNOME
        assert config.user.primary_user_shell == Shell.BASH
        assert config.desktop.taskbar_position == TaskbarPosition.BOTTOM
        
        # Valid languages should still be loaded
        assert len(config.development.development_languages) == 2
        assert DevelopmentLanguage.PYTHON in config.development.development_languages
        assert DevelopmentLanguage.NODEJS in config.development.development_languages


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_create_default_config(self):
        """Test create_default_config function."""
        config = create_default_config()
        assert isinstance(config, BootstrapConfiguration)
        assert config.system.timezone == "America/New_York"
    
    def test_load_config_default_path(self, tmp_path, monkeypatch):
        """Test load_config with default path."""
        monkeypatch.chdir(tmp_path)
        
        # Create config.yml in current directory
        yaml_content = "system_timezone: UTC"
        with open("config.yml", 'w') as f:
            f.write(yaml_content)
        
        config = load_config()
        assert config.system.timezone == "UTC"
    
    def test_load_config_custom_path(self, tmp_path):
        """Test load_config with custom path."""
        yaml_file = tmp_path / "custom_config.yml"
        yaml_content = "system_locale: fr_FR.UTF-8"
        with open(yaml_file, 'w') as f:
            f.write(yaml_content)
        
        config = load_config(str(yaml_file))
        assert config.system.locale == "fr_FR.UTF-8"
    
    def test_save_config_default_path(self, tmp_path, monkeypatch):
        """Test save_config with default path."""
        monkeypatch.chdir(tmp_path)
        
        config = BootstrapConfiguration()
        config.system.hostname = "test-host"
        save_config(config)
        
        assert Path("config.yml").exists()
        
        with open("config.yml", 'r') as f:
            content = f.read()
            assert "system_hostname: test-host" in content
    
    def test_save_config_custom_path(self, tmp_path):
        """Test save_config with custom path."""
        config = BootstrapConfiguration()
        config.desktop.global_theme = GlobalTheme.DRACULA
        
        yaml_file = tmp_path / "custom_save.yml"
        save_config(config, str(yaml_file))
        
        assert yaml_file.exists()
        
        with open(yaml_file, 'r') as f:
            content = f.read()
            assert "global_theme: dracula" in content


class TestRoundTripConversion:
    """Test round-trip conversion between config and YAML."""
    
    def test_full_round_trip(self, tmp_path):
        """Test saving and loading preserves all values."""
        # Create config with various custom values
        original = BootstrapConfiguration()
        original.system.timezone = "Australia/Sydney"
        original.system.hostname = "aussie-box"
        original.user.primary_user = "kangaroo"
        original.user.primary_user_shell = Shell.FISH
        original.desktop.desktop_environment = DesktopEnvironment.CINNAMON
        original.desktop.global_theme = GlobalTheme.CATPPUCCIN
        original.development.development_languages = [
            DevelopmentLanguage.RUST,
            DevelopmentLanguage.GO,
            DevelopmentLanguage.TYPESCRIPT
        ]
        original.applications.productivity_apps = ["firefox", "vscode", "obsidian"]
        original.security.ssh_permit_root_login = True
        original.dotfiles.dotfiles_repo = "https://github.com/user/dots"
        
        # Save to file
        yaml_file = tmp_path / "roundtrip.yml"
        original.save_to_yaml(str(yaml_file))
        
        # Load from file
        loaded = BootstrapConfiguration.load_from_yaml(str(yaml_file))
        
        # Verify all values match
        assert loaded.system.timezone == original.system.timezone
        assert loaded.system.hostname == original.system.hostname
        assert loaded.user.primary_user == original.user.primary_user
        assert loaded.user.primary_user_shell == original.user.primary_user_shell
        assert loaded.desktop.desktop_environment == original.desktop.desktop_environment
        assert loaded.desktop.global_theme == original.desktop.global_theme
        assert loaded.development.development_languages == original.development.development_languages
        assert loaded.applications.productivity_apps == original.applications.productivity_apps
        assert loaded.security.ssh_permit_root_login == original.security.ssh_permit_root_login
        assert loaded.dotfiles.dotfiles_repo == original.dotfiles.dotfiles_repo