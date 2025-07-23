"""
Unit tests for error_handling module
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from enum import Enum

import lib.error_handling
from lib.error_handling import ErrorCode, ValidationError, ConfigurationError, SystemError, PermissionError as CustomPermissionError


class TestErrorHandling:
    """Test error handling functionality"""
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.error_handling is not None
    
    def test_error_codes(self):
        """Test ErrorCode enum"""
        # Verify all expected error codes exist
        assert hasattr(ErrorCode, 'INVALID_CONFIG')
        assert hasattr(ErrorCode, 'MISSING_REQUIRED')
        assert hasattr(ErrorCode, 'CONFLICT')
        assert hasattr(ErrorCode, 'SYSTEM_ERROR')
        assert hasattr(ErrorCode, 'PERMISSION_ERROR')
        
        # Verify they are enum values
        assert isinstance(ErrorCode.INVALID_CONFIG, ErrorCode)
        assert ErrorCode.INVALID_CONFIG.value == "INVALID_CONFIG"
    
    def test_validation_error(self):
        """Test ValidationError exception"""
        # Test with default error code
        error = ValidationError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.code == ErrorCode.INVALID_CONFIG
        
        # Test with specific error code
        error = ValidationError("Missing field", ErrorCode.MISSING_REQUIRED)
        assert error.message == "Missing field"
        assert error.code == ErrorCode.MISSING_REQUIRED
    
    def test_configuration_error(self):
        """Test ConfigurationError exception"""
        error = ConfigurationError("Config error")
        assert str(error) == "Config error"
        assert error.message == "Config error"
        assert error.code == ErrorCode.INVALID_CONFIG
    
    def test_system_error(self):
        """Test SystemError exception"""
        error = SystemError("System error")
        assert str(error) == "System error"
        assert error.message == "System error"
        assert error.code == ErrorCode.SYSTEM_ERROR
    
    def test_permission_error(self):
        """Test PermissionError exception"""
        error = CustomPermissionError("Permission denied")
        assert str(error) == "Permission denied"
        assert error.message == "Permission denied"
        assert error.code == ErrorCode.PERMISSION_ERROR
    
    def test_error_inheritance(self):
        """Test that all errors inherit from ValidationError"""
        # Create instances
        config_error = ConfigurationError("test")
        system_error = SystemError("test")
        perm_error = CustomPermissionError("test")
        
        # Verify inheritance
        assert isinstance(config_error, ValidationError)
        assert isinstance(system_error, ValidationError)
        assert isinstance(perm_error, ValidationError)
        
        # Verify they are also Exceptions
        assert isinstance(config_error, Exception)
        assert isinstance(system_error, Exception)
        assert isinstance(perm_error, Exception)
    
    def test_error_handling_in_context(self):
        """Test error handling in typical usage context"""
        def validate_config(config):
            if not config:
                raise ValidationError("Config cannot be empty", ErrorCode.MISSING_REQUIRED)
            if 'invalid' in config:
                raise ConfigurationError("Invalid configuration")
            return True
        
        # Test empty config
        with pytest.raises(ValidationError) as exc_info:
            validate_config({})
        assert exc_info.value.code == ErrorCode.MISSING_REQUIRED
        
        # Test invalid config
        with pytest.raises(ConfigurationError) as exc_info:
            validate_config({'invalid': True})
        assert exc_info.value.code == ErrorCode.INVALID_CONFIG
        
        # Test valid config
        assert validate_config({'valid': True}) is True


@pytest.mark.parametrize("error_class,expected_code", [
    (ValidationError, ErrorCode.INVALID_CONFIG),
    (ConfigurationError, ErrorCode.INVALID_CONFIG),
    (SystemError, ErrorCode.SYSTEM_ERROR),
    (CustomPermissionError, ErrorCode.PERMISSION_ERROR),
])
def test_error_default_codes(error_class, expected_code):
    """Test that each error class has the correct default error code"""
    error = error_class("Test message")
    assert error.code == expected_code