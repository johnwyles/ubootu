"""
Unit tests for config_models
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from dataclasses import is_dataclass
import inspect

import lib.config_models
from lib.config_models import UbootuConfig, DesktopConfig, DevelopmentConfig, ApplicationsConfig, SecurityConfig


class TestConfigModels:
    """Test ConfigModels functionality"""
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.config_models is not None
    
    def test_ubootu_config_structure(self):
        """Test UbootuConfig dataclass"""
        # Test basic instantiation
        config = UbootuConfig(
            version="1.0",
            username="testuser",
            full_name="Test User"
        )
        assert config.version == "1.0"
        assert config.username == "testuser"
        assert config.full_name == "Test User"
        
        # Test default values
        assert config.email == ""
        assert config.timezone == "UTC"
        assert config.desktop_environment == "gnome"
        assert config.selected_categories == []
    
    def test_desktop_config(self):
        """Test DesktopConfig dataclass"""
        config = DesktopConfig()
        assert config.environment == "gnome"
        assert config.themes == []
        assert config.extensions == []
        assert config.wallpaper == ""
    
    def test_development_config(self):
        """Test DevelopmentConfig dataclass"""
        config = DevelopmentConfig(
            languages=["python", "go"],
            ides=["vscode"],
            tools=["docker", "git"]
        )
        assert config.languages == ["python", "go"]
        assert config.ides == ["vscode"]
        assert config.tools == ["docker", "git"]
        assert config.modern_cli == []
    
    def test_config_serialization(self):
        """Test config can be converted to dict"""
        config = UbootuConfig(
            version="1.0",
            username="test",
            full_name="Test User"
        )
        
        # Use dataclasses.asdict if available
        try:
            from dataclasses import asdict
            config_dict = asdict(config)
            assert config_dict["version"] == "1.0"
            assert config_dict["username"] == "test"
        except ImportError:
            # Fallback to manual dict creation
            assert hasattr(config, "version")
            assert hasattr(config, "username")
