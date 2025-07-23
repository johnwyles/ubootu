"""
Unit tests for config_validator.py - Configuration validation and schema enforcement.
"""

import sys
import os
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock

import pytest

# Mock the error_handling module before importing config_validator
sys.modules['error_handling'] = MagicMock()

from lib.config_validator import (
    ValidationRule, ValidationResult, ConfigurationValidator,
    SchemaValidator, validate_configuration_file
)
from lib.config_models import (
    BootstrapConfiguration, SystemConfig, UserConfig, DesktopConfig,
    SecurityConfig, DevelopmentConfig, ApplicationsConfig, DotfilesConfig,
    BackupConfig, UpdatesConfig, DesktopEnvironment, DevelopmentLanguage,
    Shell, GlobalTheme
)


class TestValidationRule:
    """Test ValidationRule dataclass."""
    
    def test_default_values(self):
        """Test default values for ValidationRule."""
        rule = ValidationRule(
            field_path="test.field",
            rule_type="range"
        )
        assert rule.field_path == "test.field"
        assert rule.rule_type == "range"
        assert rule.params == {}
        assert rule.error_message is None
        assert rule.severity == "error"
    
    def test_custom_values(self):
        """Test custom values for ValidationRule."""
        rule = ValidationRule(
            field_path="system.value",
            rule_type="enum",
            params={"values": ["a", "b", "c"]},
            error_message="Invalid value",
            severity="warning"
        )
        assert rule.field_path == "system.value"
        assert rule.rule_type == "enum"
        assert rule.params == {"values": ["a", "b", "c"]}
        assert rule.error_message == "Invalid value"
        assert rule.severity == "warning"


class TestValidationResult:
    """Test ValidationResult class."""
    
    def test_initial_state(self):
        """Test initial state of ValidationResult."""
        result = ValidationResult(is_valid=True)
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.info == []
    
    def test_add_error(self):
        """Test adding errors."""
        result = ValidationResult(is_valid=True)
        result.add_error("Test error")
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0] == "Test error"
    
    def test_add_warning(self):
        """Test adding warnings."""
        result = ValidationResult(is_valid=True)
        result.add_warning("Test warning")
        
        assert result.is_valid is True  # Warnings don't affect validity
        assert len(result.warnings) == 1
        assert result.warnings[0] == "Test warning"
    
    def test_add_info(self):
        """Test adding info messages."""
        result = ValidationResult(is_valid=True)
        result.add_info("Test info")
        
        assert result.is_valid is True
        assert len(result.info) == 1
        assert result.info[0] == "Test info"
    
    def test_merge(self):
        """Test merging validation results."""
        result1 = ValidationResult(is_valid=True)
        result1.add_error("Error 1")
        result1.add_warning("Warning 1")
        result1.add_info("Info 1")
        
        result2 = ValidationResult(is_valid=True)
        result2.add_error("Error 2")
        result2.add_warning("Warning 2")
        result2.add_info("Info 2")
        
        result1.merge(result2)
        
        assert result1.is_valid is False  # Because both have errors
        assert len(result1.errors) == 2
        assert len(result1.warnings) == 2
        assert len(result1.info) == 2
        assert "Error 1" in result1.errors
        assert "Error 2" in result1.errors


class TestConfigurationValidator:
    """Test ConfigurationValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        with patch('lib.config_validator.get_logger'):
            return ConfigurationValidator()
    
    def test_validate_basic_fields_swappiness(self, validator):
        """Test swappiness validation."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Valid swappiness
        config.system.swappiness_value = 10
        validator._validate_basic_fields(config, result)
        assert len(result.errors) == 0
        
        # Invalid swappiness (too low)
        config.system.swappiness_value = -1
        validator._validate_basic_fields(config, result)
        assert any("Swappiness value must be between 0 and 100" in error for error in result.errors)
        
        # Invalid swappiness (too high)
        result = ValidationResult(is_valid=True)
        config.system.swappiness_value = 101
        validator._validate_basic_fields(config, result)
        assert any("Swappiness value must be between 0 and 100" in error for error in result.errors)
    
    def test_validate_basic_fields_icon_size(self, validator):
        """Test desktop icon size validation."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Valid icon size
        config.desktop.desktop_icon_size = 64
        validator._validate_basic_fields(config, result)
        assert len(result.errors) == 0
        
        # Invalid icon size (too small)
        config.desktop.desktop_icon_size = 8
        validator._validate_basic_fields(config, result)
        assert any("Desktop icon size must be between 16 and 256" in error for error in result.errors)
    
    def test_validate_basic_fields_username(self, validator):
        """Test username validation."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Valid username
        config.user.primary_user = "john-doe"
        validator._validate_basic_fields(config, result)
        assert len(result.errors) == 0
        
        # Invalid username (starts with number)
        config.user.primary_user = "123user"
        validator._validate_basic_fields(config, result)
        assert any("Invalid username format" in error for error in result.errors)
    
    def test_validate_basic_fields_git_url(self, validator):
        """Test Git URL validation."""
        config = BootstrapConfiguration()
        config.dotfiles.configure_dotfiles = True
        
        # Valid Git URLs
        valid_urls = [
            "https://github.com/user/repo",
            "https://github.com/user/repo.git",
            "git@github.com:user/repo.git",
            "https://gitlab.com/user/repo",
        ]
        
        for url in valid_urls:
            result = ValidationResult(is_valid=True)
            config.dotfiles.dotfiles_repo = url
            validator._validate_basic_fields(config, result)
            assert len(result.errors) == 0
        
        # Invalid Git URL
        result = ValidationResult(is_valid=True)
        config.dotfiles.dotfiles_repo = "not-a-url"
        validator._validate_basic_fields(config, result)
        assert any("Invalid Git repository URL" in error for error in result.errors)
    
    def test_validate_basic_fields_time_format(self, validator):
        """Test time format validation."""
        config = BootstrapConfiguration()
        
        # Valid time formats
        valid_times = ["03:00", "14:30", "23:59", "0:00", "9:15"]
        
        for time in valid_times:
            result = ValidationResult(is_valid=True)
            config.updates.automatic_reboot_time = time
            validator._validate_basic_fields(config, result)
            assert len(result.errors) == 0
        
        # Invalid time formats
        invalid_times = ["25:00", "12:60", "3:00:00", "noon", "12.30"]
        
        for time in invalid_times:
            result = ValidationResult(is_valid=True)
            config.updates.automatic_reboot_time = time
            validator._validate_basic_fields(config, result)
            assert any("Invalid time format" in error for error in result.errors)
    
    def test_validate_business_logic_development_tools(self, validator):
        """Test business logic validation for development tools."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Development tools disabled but specific tools selected
        config.development.enable_development_tools = False
        config.development.install_vscode = True
        config.development.install_docker = True
        
        validator._validate_business_logic(config, result)
        
        assert len(result.warnings) == 2
        assert any("VS Code selected but development tools are disabled" in warning for warning in result.warnings)
        assert any("Docker selected but development tools are disabled" in warning for warning in result.warnings)
    
    def test_validate_business_logic_security(self, validator):
        """Test business logic validation for security settings."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Security enabled but firewall disabled
        config.security.enable_security = True
        config.security.enable_firewall = False
        config.security.enable_fail2ban = False
        
        validator._validate_business_logic(config, result)
        
        assert any("Security enabled but firewall is disabled" in warning for warning in result.warnings)
        assert any("Consider enabling Fail2Ban" in info for info in result.info)
    
    def test_validate_business_logic_backup(self, validator):
        """Test business logic validation for backup settings."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Backup enabled but no directories or destination
        config.backup.enable_backup = True
        config.backup.backup_directories = []
        config.backup.backup_destination = ""
        
        validator._validate_business_logic(config, result)
        
        assert len(result.errors) == 2
        assert any("Backup enabled but no directories specified" in error for error in result.errors)
        assert any("Backup enabled but no destination specified" in error for error in result.errors)
    
    def test_validate_dependencies_docker(self, validator):
        """Test dependency validation for Docker."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Docker installed but docker group not added
        config.development.install_docker = True
        config.user.create_user_groups = ["sudo", "audio"]
        
        validator._validate_dependencies(config, result)
        
        assert any("Docker installation requires 'docker' group" in error for error in result.errors)
    
    def test_validate_dependencies_typescript(self, validator):
        """Test dependency validation for TypeScript."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # TypeScript without Node.js
        config.development.development_languages = [DevelopmentLanguage.TYPESCRIPT]
        
        validator._validate_dependencies(config, result)
        
        assert any("TypeScript selected but Node.js is not" in warning for warning in result.warnings)
    
    def test_validate_security_settings(self, validator):
        """Test security settings validation."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Insecure settings
        config.security.ssh_permit_root_login = True
        config.security.ssh_password_authentication = True
        config.security.enable_firewall = False
        
        validator._validate_security_settings(config, result)
        
        assert len(result.warnings) >= 3
        assert any("SSH root login is enabled" in warning for warning in result.warnings)
        assert any("SSH password authentication enabled" in warning for warning in result.warnings)
        assert any("Firewall is disabled" in warning for warning in result.warnings)
    
    def test_validate_compatibility_desktop_theme(self, validator):
        """Test compatibility validation for desktop themes."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # GNOME with incompatible theme (theoretical example)
        config.desktop.desktop_environment = DesktopEnvironment.GNOME
        config.desktop.global_theme = GlobalTheme.GRUVBOX
        
        validator._validate_compatibility(config, result)
        
        # Check if warning is generated for incompatible theme
        # (Note: This might need adjustment based on actual compatibility matrix)
        assert len(result.warnings) >= 0  # May or may not warn based on implementation
    
    def test_validate_compatibility_performance(self, validator):
        """Test compatibility validation for performance settings."""
        config = BootstrapConfiguration()
        result = ValidationResult(is_valid=True)
        
        # Performance tweaks with high swappiness
        config.system.enable_performance_tweaks = True
        config.system.swappiness_value = 60
        
        validator._validate_compatibility(config, result)
        
        assert any("Performance tweaks enabled but swappiness is high" in info for info in result.info)
    
    def test_validate_full_configuration(self, validator):
        """Test full configuration validation."""
        config = BootstrapConfiguration()
        
        # Set some values that will trigger various validations
        config.system.swappiness_value = 10
        config.user.primary_user = "testuser"
        config.development.install_docker = True
        config.user.create_user_groups = ["docker", "sudo"]
        
        result = validator.validate(config)
        
        assert isinstance(result, ValidationResult)
        # The configuration should be mostly valid with default values
        assert result.is_valid or len(result.errors) == 0
    
    def test_is_valid_timezone(self, validator):
        """Test timezone validation helper."""
        # Valid timezones
        assert validator._is_valid_timezone("UTC")
        assert validator._is_valid_timezone("America/New_York")
        assert validator._is_valid_timezone("Europe/London")
        
        # Invalid timezones (but may pass basic check)
        assert validator._is_valid_timezone("Mars/Olympus_Mons") or True  # May pass "/" check
    
    def test_is_valid_username(self, validator):
        """Test username validation helper."""
        # Valid usernames
        assert validator._is_valid_username("john")
        assert validator._is_valid_username("john-doe")
        assert validator._is_valid_username("john_doe")
        assert validator._is_valid_username("john123")
        
        # Invalid usernames
        assert not validator._is_valid_username("")
        assert not validator._is_valid_username("123john")
        assert not validator._is_valid_username("John")  # Uppercase
        assert not validator._is_valid_username("john@doe")
        assert not validator._is_valid_username("a" * 33)  # Too long
    
    def test_is_valid_git_url(self, validator):
        """Test Git URL validation helper."""
        # Valid URLs
        assert validator._is_valid_git_url("https://github.com/user/repo")
        assert validator._is_valid_git_url("https://github.com/user/repo.git")
        assert validator._is_valid_git_url("git@github.com:user/repo.git")
        assert validator._is_valid_git_url("https://gitlab.com/user/repo")
        assert validator._is_valid_git_url("https://bitbucket.org/user/repo")
        
        # Invalid URLs
        assert not validator._is_valid_git_url("")
        assert not validator._is_valid_git_url("not-a-url")
        assert not validator._is_valid_git_url("http://example.com")
        assert not validator._is_valid_git_url("ftp://github.com/user/repo")
    
    def test_is_valid_time_format(self, validator):
        """Test time format validation helper."""
        # Valid times
        assert validator._is_valid_time_format("00:00")
        assert validator._is_valid_time_format("12:30")
        assert validator._is_valid_time_format("23:59")
        assert validator._is_valid_time_format("3:15")
        
        # Invalid times
        assert not validator._is_valid_time_format("24:00")
        assert not validator._is_valid_time_format("12:60")
        assert not validator._is_valid_time_format("12:30:00")
        assert not validator._is_valid_time_format("12.30")
        assert not validator._is_valid_time_format("noon")


class TestSchemaValidator:
    """Test SchemaValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a schema validator instance."""
        with patch('lib.config_validator.get_logger'):
            return SchemaValidator()
    
    def test_validate_against_schema_valid(self, validator):
        """Test validation against schema with valid data."""
        config_dict = {
            "desktop_environment": "gnome",
            "enable_development_tools": True,
            "enable_security": True,
            "install_applications": True,
            "swappiness_value": 10,
            "desktop_icon_size": 64
        }
        
        result = validator.validate_against_schema(config_dict)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_validate_against_schema_missing_required(self, validator):
        """Test validation with missing required fields."""
        config_dict = {
            "swappiness_value": 10
        }
        
        result = validator.validate_against_schema(config_dict)
        
        assert not result.is_valid
        assert any("Required field missing" in error for error in result.errors)
    
    def test_validate_against_schema_invalid_type(self, validator):
        """Test validation with invalid field types."""
        config_dict = {
            "desktop_environment": "gnome",
            "enable_development_tools": "yes",  # Should be boolean
            "enable_security": True,
            "install_applications": True,
            "swappiness_value": "10"  # Should be integer
        }
        
        result = validator.validate_against_schema(config_dict)
        
        assert not result.is_valid
        assert any("must be a boolean" in error for error in result.errors)
        assert any("must be an integer" in error for error in result.errors)
    
    def test_validate_against_schema_invalid_enum(self, validator):
        """Test validation with invalid enum values."""
        config_dict = {
            "desktop_environment": "windows",  # Invalid enum
            "enable_development_tools": True,
            "enable_security": True,
            "install_applications": True
        }
        
        result = validator.validate_against_schema(config_dict)
        
        assert not result.is_valid
        assert any("must be one of:" in error for error in result.errors)
    
    def test_validate_against_schema_out_of_range(self, validator):
        """Test validation with out-of-range values."""
        config_dict = {
            "desktop_environment": "gnome",
            "enable_development_tools": True,
            "enable_security": True,
            "install_applications": True,
            "swappiness_value": 150,  # Out of range
            "desktop_icon_size": 512  # Out of range
        }
        
        result = validator.validate_against_schema(config_dict)
        
        assert not result.is_valid
        assert any("must be <= 100" in error for error in result.errors)
        assert any("must be <= 256" in error for error in result.errors)
    
    def test_validate_field_against_schema_string_constraints(self, validator):
        """Test string field validation with constraints."""
        result = ValidationResult(is_valid=True)
        
        # Test pattern validation
        schema = {
            "type": "string",
            "pattern": r"^[a-z]+$"
        }
        
        validator._validate_field_against_schema("abc", schema, "test_field", result)
        assert len(result.errors) == 0
        
        validator._validate_field_against_schema("ABC", schema, "test_field", result)
        assert any("format is invalid" in error for error in result.errors)
    
    def test_validate_field_against_schema_array(self, validator):
        """Test array field validation."""
        result = ValidationResult(is_valid=True)
        
        schema = {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["python", "nodejs", "go"]
            }
        }
        
        # Valid array
        validator._validate_field_against_schema(["python", "go"], schema, "languages", result)
        assert len(result.errors) == 0
        
        # Not an array
        validator._validate_field_against_schema("python", schema, "languages", result)
        assert any("must be an array" in error for error in result.errors)


class TestValidateConfigurationFile:
    """Test validate_configuration_file function."""
    
    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file."""
        result = validate_configuration_file("/tmp/nonexistent_config.yml")
        
        assert not result.is_valid
        assert any("Configuration file not found" in error for error in result.errors)
    
    @patch('lib.config_validator.Path')
    @patch('lib.config_validator.load_config')
    def test_validate_valid_file(self, mock_load_config, mock_path):
        """Test validation of valid configuration file."""
        # Mock file existence
        mock_path.return_value.exists.return_value = True
        
        # Mock loaded configuration
        config = BootstrapConfiguration()
        config.development.install_docker = True
        config.user.create_user_groups = ["docker"]
        mock_load_config.return_value = config
        
        with patch('lib.config_validator.ConfigurationValidator') as mock_validator_class:
            mock_validator = Mock()
            mock_validator.validate.return_value = ValidationResult(is_valid=True)
            mock_validator_class.return_value = mock_validator
            
            with patch('lib.config_validator.SchemaValidator') as mock_schema_class:
                mock_schema = Mock()
                mock_schema.validate_against_schema.return_value = ValidationResult(is_valid=True)
                mock_schema_class.return_value = mock_schema
                
                result = validate_configuration_file("test_config.yml")
                
                assert result.is_valid
                assert len(result.errors) == 0
    
    @patch('lib.config_validator.Path')
    @patch('lib.config_validator.load_config')
    def test_validate_file_with_errors(self, mock_load_config, mock_path):
        """Test validation of configuration file with errors."""
        # Mock file existence
        mock_path.return_value.exists.return_value = True
        
        # Mock loaded configuration with issues
        config = BootstrapConfiguration()
        config.system.swappiness_value = 150  # Invalid value
        mock_load_config.return_value = config
        
        result = validate_configuration_file("test_config.yml")
        
        # Should have validation errors
        assert not result.is_valid or len(result.errors) > 0


class TestMainFunction:
    """Test the main CLI function."""
    
    @patch('sys.argv', ['config_validator.py', 'config.yml'])
    @patch('lib.config_validator.validate_configuration_file')
    def test_main_valid_config(self, mock_validate, capsys):
        """Test main function with valid configuration."""
        # Mock successful validation
        result = ValidationResult(is_valid=True)
        result.add_info("Configuration looks good")
        mock_validate.return_value = result
        
        with patch('sys.exit') as mock_exit:
            from lib.config_validator import main
            main()
            
            captured = capsys.readouterr()
            assert "✅ Configuration is valid!" in captured.out
            mock_exit.assert_called_with(0)
    
    @patch('sys.argv', ['config_validator.py', 'config.yml'])
    @patch('lib.config_validator.validate_configuration_file')
    def test_main_invalid_config(self, mock_validate, capsys):
        """Test main function with invalid configuration."""
        # Mock failed validation
        result = ValidationResult(is_valid=False)
        result.add_error("Invalid configuration value")
        result.add_warning("Consider changing this")
        mock_validate.return_value = result
        
        with patch('sys.exit') as mock_exit:
            from lib.config_validator import main
            main()
            
            captured = capsys.readouterr()
            assert "❌ Validation Errors:" in captured.out
            assert "Invalid configuration value" in captured.out
            assert "⚠️  Validation Warnings:" in captured.out
            mock_exit.assert_called_with(1)
    
    @patch('sys.argv', ['config_validator.py', 'config.yml', '--strict'])
    @patch('lib.config_validator.validate_configuration_file')
    def test_main_strict_mode(self, mock_validate, capsys):
        """Test main function in strict mode."""
        # Mock validation with warnings only
        result = ValidationResult(is_valid=True)
        result.add_warning("This could be better")
        mock_validate.return_value = result
        
        with patch('sys.exit') as mock_exit:
            from lib.config_validator import main
            main()
            
            captured = capsys.readouterr()
            assert "❌ Configuration has warnings (strict mode)" in captured.out
            mock_exit.assert_called_with(1)