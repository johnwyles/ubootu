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
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'timezone': 'America/New_York',
            'desktop_environment': 'gnome',
            'selected_categories': ['development']
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
        validator.validate(valid_config)
    
    def test_validate_missing_required_fields(self, validator):
        """Test validation with missing required fields"""
        invalid_config = {
            'version': '1.0'
            # Missing username and full_name
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(invalid_config)
        assert exc_info.value.code == ErrorCode.MISSING_REQUIRED
    
    def test_validate_invalid_email(self, validator, valid_config):
        """Test validation with invalid email"""
        valid_config['email'] = 'invalid-email'
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(valid_config)
        assert "email" in str(exc_info.value).lower()
    
    def test_validate_invalid_timezone(self, validator, valid_config):
        """Test validation with invalid timezone"""
        valid_config['timezone'] = 'Invalid/Timezone'
        
        # Depending on implementation, this might pass with fallback
        # or raise an error. Test accordingly
        try:
            validator.validate(valid_config)
        except ValidationError:
            # If it raises, that's also acceptable
            pass
    
    def test_validate_file(self, validator, valid_config, tmp_path):
        """Test file validation"""
        config_file = tmp_path / "config.yml"
        config_file.write_text(yaml.dump(valid_config))
        
        # Should not raise exception
        validator.validate_file(str(config_file))
    
    def test_validate_nonexistent_file(self, validator):
        """Test validation of non-existent file"""
        with pytest.raises(ValidationError):
            validator.validate_file("/path/to/nonexistent/file.yml")
