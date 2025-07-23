#!/usr/bin/env python3
"""
Unified Configuration Model Layer for Ubuntu Bootstrap Project

This module provides data classes and validation for all configuration options,
serving as the single source of truth for the configuration schema.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import yaml
import os


class DesktopEnvironment(Enum):
    """Supported desktop environments"""
    GNOME = "gnome"
    KDE = "kde"
    XFCE = "xfce"
    MATE = "mate"
    CINNAMON = "cinnamon"


class Shell(Enum):
    """Supported shell options"""
    BASH = "/bin/bash"
    ZSH = "/bin/zsh"
    FISH = "/usr/bin/fish"


class TaskbarPosition(Enum):
    """Taskbar/panel position options"""
    BOTTOM = "bottom"
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"


class GlobalTheme(Enum):
    """Global theme options"""
    NONE = "none"
    DRACULA = "dracula"
    CATPPUCCIN = "catppuccin"
    TOKYO_NIGHT = "tokyo-night"
    NORD = "nord"
    GRUVBOX = "gruvbox"


class DevelopmentLanguage(Enum):
    """Supported development languages"""
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    CPP = "cpp"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


@dataclass
class SystemConfig:
    """System-level configuration options"""
    timezone: str = "America/New_York"
    locale: str = "en_US.UTF-8"
    hostname: Optional[str] = None
    enable_performance_tweaks: bool = False
    swappiness_value: int = 10
    enable_tmpfs: bool = False


@dataclass
class UserConfig:
    """User account configuration"""
    primary_user: Optional[str] = None
    primary_user_shell: Shell = Shell.BASH
    create_user_groups: List[str] = field(default_factory=lambda: ["docker", "vboxusers"])


@dataclass
class DesktopConfig:
    """Desktop environment configuration"""
    desktop_environment: DesktopEnvironment = DesktopEnvironment.GNOME
    install_desktop_environment: bool = True
    desktop_autologin: bool = False
    desktop_theme: str = "default"
    taskbar_position: TaskbarPosition = TaskbarPosition.BOTTOM
    desktop_icons: List[str] = field(default_factory=lambda: ["home", "trash"])
    desktop_icon_size: int = 64
    trackpad_natural_scroll: bool = False
    global_theme: GlobalTheme = GlobalTheme.NONE


@dataclass
class SecurityConfig:
    """Security and hardening configuration"""
    enable_security: bool = True
    enable_firewall: bool = True
    enable_fail2ban: bool = True
    ssh_permit_root_login: bool = False
    ssh_password_authentication: bool = False
    
    def validate(self) -> List[str]:
        """Validate security configuration"""
        errors = []
        if self.enable_security and not self.enable_firewall:
            errors.append("Firewall should be enabled when security is enabled")
        return errors


@dataclass
class DevelopmentConfig:
    """Development tools configuration"""
    enable_development_tools: bool = False
    development_languages: List[DevelopmentLanguage] = field(
        default_factory=lambda: [DevelopmentLanguage.PYTHON, DevelopmentLanguage.NODEJS]
    )
    install_docker: bool = False
    install_vscode: bool = False
    install_jetbrains_toolbox: bool = False
    install_github_cli: bool = False
    install_hashicorp_tools: bool = False
    
    def validate(self) -> List[str]:
        """Validate development configuration"""
        errors = []
        if self.install_docker and "docker" not in self.get_required_groups():
            errors.append("Docker group should be added when Docker is enabled")
        return errors
    
    def get_required_groups(self) -> List[str]:
        """Get required user groups based on selected tools"""
        groups = []
        if self.install_docker:
            groups.append("docker")
        return groups


@dataclass
class ApplicationsConfig:
    """Application installation configuration"""
    install_applications: bool = True
    default_browser: str = "firefox"
    
    essential_packages: List[str] = field(default_factory=lambda: [
        "curl", "wget", "git", "vim", "htop", "build-essential", "software-properties-common"
    ])
    
    productivity_apps: List[str] = field(default_factory=lambda: [
        "firefox", "thunderbird", "libreoffice", "keepassxc"
    ])
    
    multimedia_apps: List[str] = field(default_factory=lambda: [
        "vlc", "gimp", "audacity"
    ])
    
    communication_apps: List[str] = field(default_factory=lambda: [
        "discord", "slack", "zoom"
    ])


@dataclass
class PackageManagementConfig:
    """Package management configuration"""
    enable_flatpak: bool = True
    enable_snap: bool = True
    enable_appimage_support: bool = True
    use_third_party_repos: bool = True
    custom_apt_repositories: List[str] = field(default_factory=list)
    custom_apt_keys: List[str] = field(default_factory=list)


@dataclass
class DotfilesConfig:
    """Dotfiles management configuration"""
    configure_dotfiles: bool = True
    dotfiles_repo: str = ""
    dotfiles_repo_local_dest: str = "~/dotfiles"
    dotfiles_files_to_link: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate dotfiles configuration"""
        errors = []
        if self.configure_dotfiles and not self.dotfiles_repo:
            errors.append("Dotfiles repository URL is required when dotfiles are enabled")
        return errors


@dataclass
class UpdatesConfig:
    """System updates configuration"""
    enable_automatic_updates: bool = False
    automatic_reboot: bool = False
    automatic_reboot_time: str = "03:00"


@dataclass
class BackupConfig:
    """Backup configuration"""
    enable_backup: bool = False
    backup_directories: List[str] = field(default_factory=list)
    backup_destination: str = ""
    
    def validate(self) -> List[str]:
        """Validate backup configuration"""
        errors = []
        if self.enable_backup and not self.backup_destination:
            errors.append("Backup destination is required when backup is enabled")
        return errors


@dataclass
class FeatureFlags:
    """Experimental and feature flags"""
    experimental_features: bool = False
    bleeding_edge_packages: bool = False


@dataclass
class BootstrapConfiguration:
    """Main configuration class that contains all subsections"""
    
    system: SystemConfig = field(default_factory=SystemConfig)
    user: UserConfig = field(default_factory=UserConfig)
    desktop: DesktopConfig = field(default_factory=DesktopConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    development: DevelopmentConfig = field(default_factory=DevelopmentConfig)
    applications: ApplicationsConfig = field(default_factory=ApplicationsConfig)
    package_management: PackageManagementConfig = field(default_factory=PackageManagementConfig)
    dotfiles: DotfilesConfig = field(default_factory=DotfilesConfig)
    updates: UpdatesConfig = field(default_factory=UpdatesConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    features: FeatureFlags = field(default_factory=FeatureFlags)
    
    def validate(self) -> List[str]:
        """Validate entire configuration and return list of errors"""
        errors = []
        
        # Validate individual sections
        errors.extend(self.security.validate())
        errors.extend(self.development.validate())
        errors.extend(self.dotfiles.validate())
        errors.extend(self.backup.validate())
        
        # Cross-section validation
        if self.development.install_docker and "docker" not in self.user.create_user_groups:
            errors.append("Docker group should be added to user groups when Docker is enabled")
            
        return errors
    
    def to_ansible_vars(self) -> Dict[str, Any]:
        """Convert configuration to Ansible variables format"""
        return {
            # System
            "system_timezone": self.system.timezone,
            "system_locale": self.system.locale,
            "system_hostname": self.system.hostname or "{{ inventory_hostname }}",
            "enable_performance_tweaks": self.system.enable_performance_tweaks,
            "swappiness_value": self.system.swappiness_value,
            "enable_tmpfs": self.system.enable_tmpfs,
            
            # User
            "primary_user": self.user.primary_user or "{{ ansible_user_id }}",
            "primary_user_shell": self.user.primary_user_shell.value,
            "create_user_groups": self.user.create_user_groups,
            
            # Desktop
            "desktop_environment": self.desktop.desktop_environment.value,
            "install_desktop_environment": self.desktop.install_desktop_environment,
            "desktop_autologin": self.desktop.desktop_autologin,
            "desktop_theme": self.desktop.desktop_theme,
            "taskbar_position": self.desktop.taskbar_position.value,
            "desktop_icons": self.desktop.desktop_icons,
            "desktop_icon_size": self.desktop.desktop_icon_size,
            "trackpad_natural_scroll": self.desktop.trackpad_natural_scroll,
            "global_theme": self.desktop.global_theme.value,
            
            # Security
            "enable_security": self.security.enable_security,
            "enable_firewall": self.security.enable_firewall,
            "enable_fail2ban": self.security.enable_fail2ban,
            "ssh_permit_root_login": self.security.ssh_permit_root_login,
            "ssh_password_authentication": self.security.ssh_password_authentication,
            
            # Development
            "enable_development_tools": self.development.enable_development_tools,
            "development_languages": [lang.value for lang in self.development.development_languages],
            "install_docker": self.development.install_docker,
            "install_vscode": self.development.install_vscode,
            "install_jetbrains_toolbox": self.development.install_jetbrains_toolbox,
            "install_github_cli": self.development.install_github_cli,
            "install_hashicorp_tools": self.development.install_hashicorp_tools,
            
            # Applications
            "install_applications": self.applications.install_applications,
            "default_browser": self.applications.default_browser,
            "essential_packages": self.applications.essential_packages,
            "productivity_apps": self.applications.productivity_apps,
            "multimedia_apps": self.applications.multimedia_apps,
            "communication_apps": self.applications.communication_apps,
            
            # Package Management
            "enable_flatpak": self.package_management.enable_flatpak,
            "enable_snap": self.package_management.enable_snap,
            "enable_appimage_support": self.package_management.enable_appimage_support,
            "use_third_party_repos": self.package_management.use_third_party_repos,
            "custom_apt_repositories": self.package_management.custom_apt_repositories,
            "custom_apt_keys": self.package_management.custom_apt_keys,
            
            # Dotfiles
            "configure_dotfiles": self.dotfiles.configure_dotfiles,
            "dotfiles_repo": self.dotfiles.dotfiles_repo,
            "dotfiles_repo_local_dest": self.dotfiles.dotfiles_repo_local_dest,
            "dotfiles_files_to_link": self.dotfiles.dotfiles_files_to_link,
            
            # Updates
            "enable_automatic_updates": self.updates.enable_automatic_updates,
            "automatic_reboot": self.updates.automatic_reboot,
            "automatic_reboot_time": self.updates.automatic_reboot_time,
            
            # Backup
            "enable_backup": self.backup.enable_backup,
            "backup_directories": self.backup.backup_directories,
            "backup_destination": self.backup.backup_destination,
            
            # Features
            "experimental_features": self.features.experimental_features,
            "bleeding_edge_packages": self.features.bleeding_edge_packages,
        }
    
    def save_to_yaml(self, filepath: str) -> None:
        """Save configuration to YAML file"""
        ansible_vars = self.to_ansible_vars()
        
        # Add header comment
        header = [
            "# Ubuntu Bootstrap Configuration",
            "# Generated by configuration wizard",
            f"# Created: {yaml.dump({'timestamp': str(yaml.safe_load(yaml.dump({'timestamp': 'now'})))}).strip()}",
            "",
        ]
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(header))
            yaml.dump(ansible_vars, f, default_flow_style=False, sort_keys=False)
    
    @classmethod
    def load_from_yaml(cls, filepath: str) -> 'BootstrapConfiguration':
        """Load configuration from YAML file"""
        if not os.path.exists(filepath):
            return cls()
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            return cls()
        
        config = cls()
        
        # System
        config.system.timezone = data.get('system_timezone', config.system.timezone)
        config.system.locale = data.get('system_locale', config.system.locale)
        config.system.hostname = data.get('system_hostname')
        config.system.enable_performance_tweaks = data.get('enable_performance_tweaks', config.system.enable_performance_tweaks)
        config.system.swappiness_value = data.get('swappiness_value', config.system.swappiness_value)
        config.system.enable_tmpfs = data.get('enable_tmpfs', config.system.enable_tmpfs)
        
        # User
        config.user.primary_user = data.get('primary_user')
        if 'primary_user_shell' in data:
            try:
                config.user.primary_user_shell = Shell(data['primary_user_shell'])
            except ValueError:
                pass  # Keep default
        config.user.create_user_groups = data.get('create_user_groups', config.user.create_user_groups)
        
        # Desktop
        if 'desktop_environment' in data:
            try:
                config.desktop.desktop_environment = DesktopEnvironment(data['desktop_environment'])
            except ValueError:
                pass  # Keep default
        config.desktop.install_desktop_environment = data.get('install_desktop_environment', config.desktop.install_desktop_environment)
        config.desktop.desktop_autologin = data.get('desktop_autologin', config.desktop.desktop_autologin)
        config.desktop.desktop_theme = data.get('desktop_theme', config.desktop.desktop_theme)
        if 'taskbar_position' in data:
            try:
                config.desktop.taskbar_position = TaskbarPosition(data['taskbar_position'])
            except ValueError:
                pass  # Keep default
        config.desktop.desktop_icons = data.get('desktop_icons', config.desktop.desktop_icons)
        config.desktop.desktop_icon_size = data.get('desktop_icon_size', config.desktop.desktop_icon_size)
        config.desktop.trackpad_natural_scroll = data.get('trackpad_natural_scroll', config.desktop.trackpad_natural_scroll)
        if 'global_theme' in data:
            try:
                config.desktop.global_theme = GlobalTheme(data['global_theme'])
            except ValueError:
                pass  # Keep default
        
        # Security
        config.security.enable_security = data.get('enable_security', config.security.enable_security)
        config.security.enable_firewall = data.get('enable_firewall', config.security.enable_firewall)
        config.security.enable_fail2ban = data.get('enable_fail2ban', config.security.enable_fail2ban)
        config.security.ssh_permit_root_login = data.get('ssh_permit_root_login', config.security.ssh_permit_root_login)
        config.security.ssh_password_authentication = data.get('ssh_password_authentication', config.security.ssh_password_authentication)
        
        # Development
        config.development.enable_development_tools = data.get('enable_development_tools', config.development.enable_development_tools)
        if 'development_languages' in data:
            config.development.development_languages = []
            for lang_str in data['development_languages']:
                try:
                    config.development.development_languages.append(DevelopmentLanguage(lang_str))
                except ValueError:
                    pass  # Skip invalid languages
        config.development.install_docker = data.get('install_docker', config.development.install_docker)
        config.development.install_vscode = data.get('install_vscode', config.development.install_vscode)
        config.development.install_jetbrains_toolbox = data.get('install_jetbrains_toolbox', config.development.install_jetbrains_toolbox)
        config.development.install_github_cli = data.get('install_github_cli', config.development.install_github_cli)
        config.development.install_hashicorp_tools = data.get('install_hashicorp_tools', config.development.install_hashicorp_tools)
        
        # Applications
        config.applications.install_applications = data.get('install_applications', config.applications.install_applications)
        config.applications.default_browser = data.get('default_browser', config.applications.default_browser)
        config.applications.essential_packages = data.get('essential_packages', config.applications.essential_packages)
        config.applications.productivity_apps = data.get('productivity_apps', config.applications.productivity_apps)
        config.applications.multimedia_apps = data.get('multimedia_apps', config.applications.multimedia_apps)
        config.applications.communication_apps = data.get('communication_apps', config.applications.communication_apps)
        
        # Package Management
        config.package_management.enable_flatpak = data.get('enable_flatpak', config.package_management.enable_flatpak)
        config.package_management.enable_snap = data.get('enable_snap', config.package_management.enable_snap)
        config.package_management.enable_appimage_support = data.get('enable_appimage_support', config.package_management.enable_appimage_support)
        config.package_management.use_third_party_repos = data.get('use_third_party_repos', config.package_management.use_third_party_repos)
        config.package_management.custom_apt_repositories = data.get('custom_apt_repositories', config.package_management.custom_apt_repositories)
        config.package_management.custom_apt_keys = data.get('custom_apt_keys', config.package_management.custom_apt_keys)
        
        # Dotfiles
        config.dotfiles.configure_dotfiles = data.get('configure_dotfiles', config.dotfiles.configure_dotfiles)
        config.dotfiles.dotfiles_repo = data.get('dotfiles_repo', config.dotfiles.dotfiles_repo)
        config.dotfiles.dotfiles_repo_local_dest = data.get('dotfiles_repo_local_dest', config.dotfiles.dotfiles_repo_local_dest)
        config.dotfiles.dotfiles_files_to_link = data.get('dotfiles_files_to_link', config.dotfiles.dotfiles_files_to_link)
        
        # Updates
        config.updates.enable_automatic_updates = data.get('enable_automatic_updates', config.updates.enable_automatic_updates)
        config.updates.automatic_reboot = data.get('automatic_reboot', config.updates.automatic_reboot)
        config.updates.automatic_reboot_time = data.get('automatic_reboot_time', config.updates.automatic_reboot_time)
        
        # Backup
        config.backup.enable_backup = data.get('enable_backup', config.backup.enable_backup)
        config.backup.backup_directories = data.get('backup_directories', config.backup.backup_directories)
        config.backup.backup_destination = data.get('backup_destination', config.backup.backup_destination)
        
        # Features
        config.features.experimental_features = data.get('experimental_features', config.features.experimental_features)
        config.features.bleeding_edge_packages = data.get('bleeding_edge_packages', config.features.bleeding_edge_packages)
        
        return config


# Utility functions for backward compatibility
def create_default_config() -> BootstrapConfiguration:
    """Create a default configuration"""
    return BootstrapConfiguration()


def load_config(filepath: str = "config.yml") -> BootstrapConfiguration:
    """Load configuration from file"""
    return BootstrapConfiguration.load_from_yaml(filepath)


def save_config(config: BootstrapConfiguration, filepath: str = "config.yml") -> None:
    """Save configuration to file"""
    config.save_to_yaml(filepath)