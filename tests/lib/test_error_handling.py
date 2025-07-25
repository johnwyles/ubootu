"""
Unit tests for error_handling module
"""

import logging
from enum import Enum
from unittest.mock import MagicMock, Mock, patch

import pytest

import lib.error_handling
from lib.error_handling import (BootstrapError, ErrorCode, ValidationError,
                                get_logger, raise_config_error)


class TestErrorHandling:
    """Test error handling functionality"""

    def test_import(self):
        """Test that module can be imported"""
        assert lib.error_handling is not None

    def test_error_codes(self):
        """Test ErrorCode enum"""
        # Verify all expected error codes exist
        assert hasattr(ErrorCode, "INVALID_CONFIG")
        assert hasattr(ErrorCode, "MISSING_REQUIRED")
        assert hasattr(ErrorCode, "CONFLICT")
        assert hasattr(ErrorCode, "SYSTEM_ERROR")
        assert hasattr(ErrorCode, "PERMISSION_ERROR")

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

    def test_bootstrap_error(self):
        """Test BootstrapError exception"""
        # Test with default error code
        error = BootstrapError("Bootstrap failed")
        assert str(error) == "Bootstrap failed"
        assert error.message == "Bootstrap failed"
        assert error.code == ErrorCode.SYSTEM_ERROR

        # Test with specific error code
        error = BootstrapError("Permission denied", ErrorCode.PERMISSION_ERROR)
        assert error.message == "Permission denied"
        assert error.code == ErrorCode.PERMISSION_ERROR

    def test_error_inheritance(self):
        """Test that all errors inherit from Exception"""
        # Create instances
        validation_error = ValidationError("test")
        bootstrap_error = BootstrapError("test")

        # Verify they are Exceptions
        assert isinstance(validation_error, Exception)
        assert isinstance(bootstrap_error, Exception)

        # Verify they are NOT related (different base classes)
        assert not isinstance(bootstrap_error, ValidationError)
        assert not isinstance(validation_error, BootstrapError)

    def test_error_handling_in_context(self):
        """Test error handling in typical usage context"""

        def validate_config(config):
            if not config:
                raise ValidationError(
                    "Config cannot be empty", ErrorCode.MISSING_REQUIRED
                )
            if "invalid" in config:
                raise ValidationError("Invalid configuration", ErrorCode.INVALID_CONFIG)
            return True

        # Test empty config
        with pytest.raises(ValidationError) as exc_info:
            validate_config({})
        assert exc_info.value.code == ErrorCode.MISSING_REQUIRED

        # Test invalid config
        with pytest.raises(ValidationError) as exc_info:
            validate_config({"invalid": True})
        assert exc_info.value.code == ErrorCode.INVALID_CONFIG

        # Test valid config
        assert validate_config({"valid": True}) is True

    def test_get_logger(self):
        """Test logger creation"""
        logger = get_logger("test_logger")
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1

        # Test that getting the same logger returns the same instance
        logger2 = get_logger("test_logger")
        assert logger is logger2

    def test_raise_config_error(self):
        """Test raise_config_error helper function"""
        # Test with default error code
        with pytest.raises(ValidationError) as exc_info:
            raise_config_error("Test error")
        assert exc_info.value.message == "Test error"
        assert exc_info.value.code == ErrorCode.INVALID_CONFIG

        # Test with specific error code
        with pytest.raises(ValidationError) as exc_info:
            raise_config_error("Missing value", ErrorCode.MISSING_REQUIRED)
        assert exc_info.value.message == "Missing value"
        assert exc_info.value.code == ErrorCode.MISSING_REQUIRED


@pytest.mark.parametrize(
    "error_class,expected_code",
    [
        (ValidationError, ErrorCode.INVALID_CONFIG),
        (BootstrapError, ErrorCode.SYSTEM_ERROR),
    ],
)
def test_error_default_codes(error_class, expected_code):
    """Test that each error class has the correct default error code"""
    error = error_class("Test message")
    assert error.code == expected_code
