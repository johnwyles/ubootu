#!/usr/bin/env python3
"""
Error handling module for Ubootu
Provides error classes and logging utilities
"""

import logging
from enum import Enum


class ErrorCode(Enum):
    """Error codes for validation and bootstrap errors"""
    INVALID_CONFIG = "INVALID_CONFIG"
    MISSING_REQUIRED = "MISSING_REQUIRED"
    CONFLICT = "CONFLICT"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    PERMISSION_ERROR = "PERMISSION_ERROR"


class ValidationError(Exception):
    """Raised when configuration validation fails"""
    def __init__(self, message: str, code: ErrorCode = ErrorCode.INVALID_CONFIG):
        self.message = message
        self.code = code
        super().__init__(message)


class BootstrapError(Exception):
    """Raised when bootstrap process fails"""
    def __init__(self, message: str, code: ErrorCode = ErrorCode.SYSTEM_ERROR):
        self.message = message
        self.code = code
        super().__init__(message)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def raise_config_error(message: str, code: ErrorCode = ErrorCode.INVALID_CONFIG):
    """Raise a configuration error"""
    raise ValidationError(message, code)