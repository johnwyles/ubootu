"""
Unit tests for config_validator
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import yaml

import lib.config_validator
from lib.config_validator import ConfigValidator
from lib.error_handling import ValidationError, ErrorCode


class TestConfigValidator:
    """Test ConfigValidator functionality"""
    
    @pytest.fixture
    def validator(self):
        """Create a ConfigValidator instance"""
        return ConfigValidator()
    
    @pytest.fixture
    def valid_config(self):
        """Create a valid config dict"""
        return {
            'version': '1.0',
            'system': {
                'hostname': 'test-host',
                'timezone': 'UTC',
                'locale': 'en_US.UTF-8'
            },
            'user': {
                'username': 'testuser',
                'full_name': 'Test User',
                'email': 'test@example.com'
            },
            'desktop': {
                'environment': 'gnome'
            }
        }
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.config_validator is not None
    
    def test_validator_initialization(self, validator):
        """Test ConfigValidator initialization"""
        assert validator is not None
        assert hasattr(validator, 'validate')
        assert hasattr(validator, 'validate_file')
    
    def test_validate_valid_config(self, validator, valid_config):
        """Test validation of valid config"""
        # Should not raise any exception
        result = validator.validate(valid_config)
        assert result is True
    
    def test_validate_missing_version(self, validator, valid_config):
        """Test validation with missing version"""
        del valid_config['version']
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(valid_config)
        assert exc_info.value.code == ErrorCode.MISSING_REQUIRED
    
    def test_validate_invalid_structure(self, validator):
        """Test validation with invalid structure"""
        invalid_config = {
            'version': '1.0',
            'invalid_key': 'invalid_value'
        }
        
        with pytest.raises(ValidationError):
            validator.validate(invalid_config)
    
    def test_validate_file(self, validator, valid_config, tmp_path):
        """Test file validation"""
        config_file = tmp_path / "config.yml"
        config_file.write_text(yaml.dump(valid_config))
        
        # Should not raise exception
        result = validator.validate_file(str(config_file))
        assert result is True
    
    def test_validate_nonexistent_file(self, validator):
        """Test validation of non-existent file"""
        with pytest.raises(ValidationError):
            validator.validate_file("/path/to/nonexistent/file.yml")
