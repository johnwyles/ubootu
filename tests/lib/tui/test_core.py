"""
Unit tests for core
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import inspect

import lib.tui.core


class TestCore:
    """Test Core functionality"""
    
    @pytest.fixture
    def mock_menu_registry(self):
        """Mock menu registry"""
        with patch('lib.tui.core.MenuRegistry') as mock_reg:
            instance = MagicMock()
            mock_reg.return_value = instance
            yield instance
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.tui.core is not None
    
    def test_tui_application_exists(self):
        """Test TUIApplication class exists"""
        assert hasattr(lib.tui.core, 'TUIApplication')
        
        # Test instantiation with mocked dependencies
        with patch('lib.tui.core.MenuRegistry'):
            with patch('lib.tui.core.ConfigManager'):
                app = lib.tui.core.TUIApplication()
                assert app is not None
    
    def test_module_initialization(self, mock_menu_registry):
        """Test module initializes correctly"""
        # Check for key components
        module = lib.tui.core
        
        # Look for main classes/functions
        attrs = dir(module)
        # Should have some TUI-related functionality
        tui_attrs = [a for a in attrs if 'tui' in a.lower() or 'menu' in a.lower()]
        assert len(tui_attrs) > 0
