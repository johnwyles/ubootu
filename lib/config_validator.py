#!/usr/bin/env python3
"""
Configuration Validation and Schema Enforcement

This module provides comprehensive validation for all configuration options,
ensuring data integrity and catching conflicts before they cause issues.
"""

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from lib.config_models import (
    BootstrapConfiguration,
    DesktopEnvironment,
    DevelopmentLanguage,
    GlobalTheme,
    Shell,
    TaskbarPosition,
)
from lib.error_handling import (
    BootstrapError,
    ErrorCode,
    ValidationError,
    get_logger,
    raise_config_error,
)


@dataclass
class ValidationRule:
    """Individual validation rule"""

    field_path: str
    rule_type: str
    params: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationResult:
    """Result of validation check"""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message"""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message"""
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Add an info message"""
        self.info.append(message)

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one"""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)
        if not other.is_valid:
            self.is_valid = False


class ConfigurationValidator:
    """Comprehensive configuration validator"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.rules = self._build_validation_rules()

    def validate(self, config: BootstrapConfiguration) -> ValidationResult:
        """
        Validate entire configuration

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult with all validation issues
        """
        result = ValidationResult(is_valid=True)

        try:
            # Run basic field validation
            self._validate_basic_fields(config, result)

            # Run business logic validation
            self._validate_business_logic(config, result)

            # Run dependency validation
            self._validate_dependencies(config, result)

            # Run security validation
            self._validate_security_settings(config, result)

            # Run compatibility validation
            self._validate_compatibility(config, result)

            return result

        except Exception as e:
            self.logger.error(f"Validation failed with exception: {e}")
            result.add_error(f"Validation system error: {e}")
            return result

    def _validate_basic_fields(
        self, config: BootstrapConfiguration, result: ValidationResult
    ) -> None:
        """Validate basic field constraints"""

        # System validation
        if config.system.swappiness_value < 0 or config.system.swappiness_value > 100:
            result.add_error("Swappiness value must be between 0 and 100")

        if config.system.timezone and not self._is_valid_timezone(
            config.system.timezone
        ):
            result.add_warning(f"Timezone '{config.system.timezone}' may not be valid")

        # Desktop validation
        if (
            config.desktop.desktop_icon_size < 16
            or config.desktop.desktop_icon_size > 256
        ):
            result.add_error("Desktop icon size must be between 16 and 256 pixels")

        # User validation
        if config.user.primary_user and not self._is_valid_username(
            config.user.primary_user
        ):
            result.add_error(f"Invalid username format: {config.user.primary_user}")

        # Development validation
        if config.development.development_languages:
            for lang in config.development.development_languages:
                if not isinstance(lang, DevelopmentLanguage):
                    result.add_error(f"Invalid development language: {lang}")

        # Dotfiles validation
        if config.dotfiles.configure_dotfiles and config.dotfiles.dotfiles_repo:
            if not self._is_valid_git_url(config.dotfiles.dotfiles_repo):
                result.add_error(
                    f"Invalid Git repository URL: {config.dotfiles.dotfiles_repo}"
                )

        # Updates validation
        if config.updates.automatic_reboot_time:
            if not self._is_valid_time_format(config.updates.automatic_reboot_time):
                result.add_error(
                    f"Invalid time format: {config.updates.automatic_reboot_time}"
                )

    def _validate_business_logic(
        self, config: BootstrapConfiguration, result: ValidationResult
    ) -> None:
        """Validate business logic and application-specific rules"""

        # If development tools are disabled, warn about related settings
        if not config.development.enable_development_tools:
            if config.development.install_vscode:
                result.add_warning(
                    "VS Code selected but development tools are disabled"
                )
            if config.development.install_docker:
                result.add_warning("Docker selected but development tools are disabled")

        # Desktop environment specific validation
        if config.desktop.desktop_environment == DesktopEnvironment.KDE:
            if config.desktop.global_theme == GlobalTheme.NONE:
                result.add_info(
                    "Consider selecting a global theme for better KDE experience"
                )

        # Security validation
        if config.security.enable_security:
            if not config.security.enable_firewall:
                result.add_warning("Security enabled but firewall is disabled")
            if not config.security.enable_fail2ban:
                result.add_info("Consider enabling Fail2Ban for additional security")

        # Application validation
        if config.applications.install_applications:
            if not config.applications.productivity_apps:
                result.add_info("No productivity applications selected")
            if not config.applications.multimedia_apps:
                result.add_info("No multimedia applications selected")

        # Backup validation
        if config.backup.enable_backup:
            if not config.backup.backup_directories:
                result.add_error("Backup enabled but no directories specified")
            if not config.backup.backup_destination:
                result.add_error("Backup enabled but no destination specified")

    def _validate_dependencies(
        self, config: BootstrapConfiguration, result: ValidationResult
    ) -> None:
        """Validate dependencies between configuration options"""

        # Docker requires docker group
        if config.development.install_docker:
            if "docker" not in config.user.create_user_groups:
                result.add_error(
                    "Docker installation requires 'docker' group in user groups"
                )

        # SSH security settings dependencies
        if (
            not config.security.ssh_password_authentication
            and not config.security.ssh_permit_root_login
        ):
            # This is actually good security practice
            result.add_info(
                "SSH configured with key-based authentication only - ensure SSH keys are set up"
            )

        # Desktop environment and applications
        if config.desktop.desktop_environment == DesktopEnvironment.GNOME:
            # Check for GNOME-specific applications
            gnome_specific = ["gnome-tweaks", "gnome-shell-extensions"]
            for app in gnome_specific:
                if app in config.applications.essential_packages:
                    result.add_info(f"GNOME detected, {app} is a good choice")

        # Development language dependencies
        if DevelopmentLanguage.TYPESCRIPT in config.development.development_languages:
            if (
                DevelopmentLanguage.NODEJS
                not in config.development.development_languages
            ):
                result.add_warning(
                    "TypeScript selected but Node.js is not - consider adding Node.js"
                )

        # Package management validation
        if (
            not config.package_management.enable_flatpak
            and not config.package_management.enable_snap
        ):
            result.add_warning(
                "Both Flatpak and Snap are disabled - some applications may not be available"
            )

    def _validate_security_settings(
        self, config: BootstrapConfiguration, result: ValidationResult
    ) -> None:
        """Validate security-related settings"""

        # Check for secure configurations
        if config.security.ssh_permit_root_login:
            result.add_warning(
                "SSH root login is enabled - consider disabling for security"
            )

        if config.security.ssh_password_authentication:
            result.add_warning(
                "SSH password authentication enabled - consider using key-based auth only"
            )

        if not config.security.enable_firewall:
            result.add_warning("Firewall is disabled - consider enabling for security")

        # Automatic updates security
        if config.updates.enable_automatic_updates and config.updates.automatic_reboot:
            result.add_info(
                "Automatic updates with reboot enabled - ensure this won't disrupt workflows"
            )

        # Development tools security
        if config.development.install_docker and config.security.enable_security:
            result.add_info(
                "Docker with security hardening - review Docker daemon security settings"
            )

    def _validate_compatibility(
        self, config: BootstrapConfiguration, result: ValidationResult
    ) -> None:
        """Validate compatibility between different settings"""

        # Desktop environment compatibility
        de_compat = {
            DesktopEnvironment.GNOME: {
                "themes": [GlobalTheme.DRACULA, GlobalTheme.CATPPUCCIN],
                "shells": [Shell.BASH, Shell.ZSH, Shell.FISH],
            },
            DesktopEnvironment.KDE: {
                "themes": [
                    GlobalTheme.DRACULA,
                    GlobalTheme.NORD,
                    GlobalTheme.CATPPUCCIN,
                ],
                "shells": [Shell.BASH, Shell.ZSH, Shell.FISH],
            },
        }

        de = config.desktop.desktop_environment
        if de in de_compat:
            # Check theme compatibility
            if (
                config.desktop.global_theme not in de_compat[de]["themes"]
                and config.desktop.global_theme != GlobalTheme.NONE
            ):
                result.add_warning(
                    f"Theme {config.desktop.global_theme.value} may not be optimal with {de.value}"
                )

        # Performance settings compatibility
        if config.system.enable_performance_tweaks:
            if config.system.swappiness_value > 20:
                result.add_info(
                    "Performance tweaks enabled but swappiness is high - consider lowering to 1-10"
                )

        # Resource usage validation
        heavy_apps = ["blender", "gimp", "libreoffice", "jetbrains"]
        selected_heavy = [
            app
            for app in config.applications.multimedia_apps
            + config.applications.productivity_apps
            if any(heavy in app.lower() for heavy in heavy_apps)
        ]

        if len(selected_heavy) > 3:
            result.add_info(
                "Many resource-intensive applications selected - ensure adequate system resources"
            )

    def _build_validation_rules(self) -> List[ValidationRule]:
        """Build list of validation rules"""
        return [
            ValidationRule(
                field_path="system.swappiness_value",
                rule_type="range",
                params={"min": 0, "max": 100},
                error_message="Swappiness must be between 0 and 100",
            ),
            ValidationRule(
                field_path="desktop.desktop_icon_size",
                rule_type="range",
                params={"min": 16, "max": 256},
                error_message="Icon size must be between 16 and 256 pixels",
            ),
            ValidationRule(
                field_path="dotfiles.dotfiles_repo",
                rule_type="url",
                params={"schemes": ["http", "https", "git"]},
                error_message="Invalid repository URL format",
            ),
        ]

    # Helper validation methods
    def _is_valid_timezone(self, timezone: str) -> bool:
        """Check if timezone string is valid"""
        try:
            # Try zoneinfo first (Python 3.9+)
            try:
                import zoneinfo

                zoneinfo.ZoneInfo(timezone)
                return True
            except ImportError:
                # Python 3.8 or older - try pytz if available
                try:
                    import pytz

                    return timezone in pytz.all_timezones
                except ImportError:
                    pass
        except Exception:
            pass

        # Fallback for systems without zoneinfo or pytz
        common_timezones = [
            "UTC",
            "America/New_York",
            "America/Chicago",
            "America/Denver",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
        ]
        return timezone in common_timezones or "/" in timezone

    def _is_valid_username(self, username: str) -> bool:
        """Check if username follows Linux conventions"""
        if not username:
            return False

        # Linux username rules: lowercase, start with letter, contain letters/numbers/underscores/hyphens
        pattern = r"^[a-z][a-z0-9_-]*$"
        return bool(re.match(pattern, username)) and len(username) <= 32

    def _is_valid_git_url(self, url: str) -> bool:
        """Check if URL is a valid Git repository URL"""
        if not url:
            return False

        # Common Git URL patterns
        patterns = [
            r"^https://github\.com/[\w\-\.]+/[\w\-\.]+(?:\.git)?/?$",
            r"^https://gitlab\.com/[\w\-\.]+/[\w\-\.]+(?:\.git)?/?$",
            r"^https://bitbucket\.org/[\w\-\.]+/[\w\-\.]+(?:\.git)?/?$",
            r"^git@github\.com:[\w\-\.]+/[\w\-\.]+\.git$",
            r"^git@gitlab\.com:[\w\-\.]+/[\w\-\.]+\.git$",
            r"^https://[\w\-\.]+/.*\.git$",  # Generic Git URL
        ]

        return any(re.match(pattern, url) for pattern in patterns)

    def _is_valid_time_format(self, time_str: str) -> bool:
        """Check if time string is in HH:MM format"""
        pattern = r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
        return bool(re.match(pattern, time_str))


class SchemaValidator:
    """JSON Schema-like validation for configuration"""

    def __init__(self):
        self.logger = get_logger(__name__)

    def validate_against_schema(self, config_dict: Dict[str, Any]) -> ValidationResult:
        """Validate configuration dictionary against expected schema"""
        result = ValidationResult(is_valid=True)
        schema = self._get_configuration_schema()

        self._validate_dict_against_schema(config_dict, schema, "", result)
        return result

    def _validate_dict_against_schema(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        path: str,
        result: ValidationResult,
    ) -> None:
        """Recursively validate dictionary against schema"""

        # Check required fields
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                result.add_error(f"Required field missing: {path}.{field}")

        # Check field types and values
        properties = schema.get("properties", {})
        for field, value in data.items():
            field_path = f"{path}.{field}" if path else field

            if field not in properties:
                result.add_warning(f"Unknown field: {field_path}")
                continue

            field_schema = properties[field]
            self._validate_field_against_schema(value, field_schema, field_path, result)

    def _validate_field_against_schema(
        self, value: Any, schema: Dict[str, Any], path: str, result: ValidationResult
    ) -> None:
        """Validate individual field against its schema"""

        field_type = schema.get("type")

        # Type validation
        if field_type == "string" and not isinstance(value, str):
            result.add_error(f"Field {path} must be a string")
        elif field_type == "integer" and not isinstance(value, int):
            result.add_error(f"Field {path} must be an integer")
        elif field_type == "boolean" and not isinstance(value, bool):
            result.add_error(f"Field {path} must be a boolean")
        elif field_type == "array" and not isinstance(value, list):
            result.add_error(f"Field {path} must be an array")

        # Enum validation
        if "enum" in schema and value not in schema["enum"]:
            result.add_error(
                f"Field {path} must be one of: {', '.join(map(str, schema['enum']))}"
            )

        # Range validation
        if field_type in ["integer", "number"]:
            if "minimum" in schema and value < schema["minimum"]:
                result.add_error(f"Field {path} must be >= {schema['minimum']}")
            if "maximum" in schema and value > schema["maximum"]:
                result.add_error(f"Field {path} must be <= {schema['maximum']}")

        # String validation
        if field_type == "string":
            if "minLength" in schema and len(value) < schema["minLength"]:
                result.add_error(
                    f"Field {path} must be at least {schema['minLength']} characters"
                )
            if "maxLength" in schema and len(value) > schema["maxLength"]:
                result.add_error(
                    f"Field {path} must be no more than {schema['maxLength']} characters"
                )
            if "pattern" in schema and not re.match(schema["pattern"], value):
                result.add_error(f"Field {path} format is invalid")

    def _get_configuration_schema(self) -> Dict[str, Any]:
        """Get the configuration schema definition"""
        return {
            "type": "object",
            "properties": {
                "system_timezone": {
                    "type": "string",
                    "pattern": r"^[A-Za-z]+/[A-Za-z_]+$",
                },
                "system_locale": {
                    "type": "string",
                    "pattern": r"^[a-z]{2}_[A-Z]{2}\..+$",
                },
                "desktop_environment": {
                    "type": "string",
                    "enum": ["gnome", "kde", "xfce", "mate", "cinnamon"],
                },
                "primary_user_shell": {
                    "type": "string",
                    "enum": ["/bin/bash", "/bin/zsh", "/usr/bin/fish"],
                },
                "swappiness_value": {"type": "integer", "minimum": 0, "maximum": 100},
                "desktop_icon_size": {"type": "integer", "minimum": 16, "maximum": 256},
                "development_languages": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "python",
                            "nodejs",
                            "go",
                            "rust",
                            "java",
                            "cpp",
                            "javascript",
                            "typescript",
                        ],
                    },
                },
                "enable_development_tools": {"type": "boolean"},
                "enable_security": {"type": "boolean"},
                "enable_firewall": {"type": "boolean"},
                "install_applications": {"type": "boolean"},
                "configure_dotfiles": {"type": "boolean"},
            },
            "required": [
                "desktop_environment",
                "enable_development_tools",
                "enable_security",
                "install_applications",
            ],
        }


def validate_configuration_file(file_path: str) -> ValidationResult:
    """
    Validate a configuration file

    Args:
        file_path: Path to configuration file

    Returns:
        ValidationResult with validation results
    """
    result = ValidationResult(is_valid=True)

    try:
        # Check file exists
        if not Path(file_path).exists():
            result.add_error(f"Configuration file not found: {file_path}")
            return result

        # Load and validate configuration
        from config_models import load_config

        config = load_config(file_path)

        # Run comprehensive validation
        validator = ConfigurationValidator()
        validation_result = validator.validate(config)

        # Also validate against schema
        schema_validator = SchemaValidator()
        ansible_vars = config.to_ansible_vars()
        schema_result = schema_validator.validate_against_schema(ansible_vars)

        # Merge results
        result.merge(validation_result)
        result.merge(schema_result)

        return result

    except Exception as e:
        result.add_error(f"Failed to validate configuration file: {e}")
        return result


def main():
    """CLI entry point for configuration validation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Ubuntu Bootstrap configuration"
    )
    parser.add_argument("config_file", help="Configuration file to validate")
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    result = validate_configuration_file(args.config_file)

    # Print results
    if result.errors:
        print("❌ Validation Errors:")
        for error in result.errors:
            print(f"  • {error}")
        print()

    if result.warnings:
        print("⚠️  Validation Warnings:")
        for warning in result.warnings:
            print(f"  • {warning}")
        print()

    if result.info:
        print("ℹ️  Information:")
        for info in result.info:
            print(f"  • {info}")
        print()

    if result.is_valid and not (args.strict and result.warnings):
        print("✅ Configuration is valid!")
        return 0
    else:
        if args.strict and result.warnings:
            print("❌ Configuration has warnings (strict mode)")
        else:
            print("❌ Configuration has errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
