"""
Unit tests for config_validator
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import yaml

import lib.config_validator
from lib.config_validator import ConfigurationValidator, ValidationResult
from lib.error_handling import ValidationError, ErrorCode
from lib.config_models import BootstrapConfiguration


class TestConfigurationValidator:
    """Test ConfigurationValidator functionality"""
    
    @pytest.fixture
    def validator(self):
        """Create a ConfigurationValidator instance"""
        return ConfigurationValidator()
    
    @pytest.fixture
    def valid_config(self):
        """Create a valid BootstrapConfiguration"""
        return BootstrapConfiguration()
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.config_validator is not None
    
    def test_validator_initialization(self, validator):
        """Test ConfigurationValidator initialization"""
        assert validator is not None
        assert hasattr(validator, 'validate')
        assert hasattr(validator, 'logger')
    
    def test_validate_valid_config(self, validator, valid_config):
        """Test validation of valid config"""
        # Should not raise any exception
        result = validator.validate(valid_config)
        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
    
    def test_validate_invalid_swappiness(self, validator, valid_config):
        """Test validation with invalid swappiness value"""
        valid_config.system.swappiness_value = 150  # > 100
        
        result = validator.validate(valid_config)
        assert result.is_valid is False
        assert any("Swappiness" in error for error in result.errors)
    
    def test_validate_invalid_icon_size(self, validator, valid_config):
        """Test validation with invalid icon size"""
        valid_config.desktop.desktop_icon_size = 512  # > 256
        
        result = validator.validate(valid_config)
        assert result.is_valid is False
        assert any("icon size" in error for error in result.errors)
    
    def test_validate_backup_without_directories(self, validator, valid_config):
        """Test validation with backup enabled but no directories"""
        valid_config.backup.enable_backup = True
        valid_config.backup.backup_directories = []
        
        result = validator.validate(valid_config)
        assert result.is_valid is False
        assert any("no directories specified" in error for error in result.errors)
    
    def test_validate_docker_without_group(self, validator, valid_config):
        """Test validation with docker enabled but no docker group"""
        valid_config.development.install_docker = True
        valid_config.user.create_user_groups = ["sudo", "adm"]
        
        result = validator.validate(valid_config)
        assert result.is_valid is False
        assert any("docker" in error and "group" in error for error in result.errors)