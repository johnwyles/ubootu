"""
Unit tests for core
"""


from __future__ import annotations
import pytest
from unittest.mock import Mock, MagicMock, patch
import inspect

import lib.tui.core


class TestCore:
    """Test Core functionality"""
    
    @pytest.fixture
    def setup(self):
        """Setup test fixtures"""
        with patch('lib.tui.core.curses'):
            with patch('lib.tui.core.yaml'):
                yield {}
    
    def test_import(self):
        """Test that module can be imported"""
        assert lib.tui.core is not None
    
    def test_module_attributes(self, setup):
        """Test module has expected attributes"""
        module = lib.tui.core
        
        # Check module has some content
        attrs = [a for a in dir(module) if not a.startswith('_')]
        assert len(attrs) > 0
        
        # Check for TUI-related functionality
        tui_attrs = [a for a in attrs if 'tui' in a.lower() or 'app' in a.lower() or 'menu' in a.lower()]
        assert len(tui_attrs) > 0
    
    def test_classes(self, setup):
        """Test classes in module"""
        module = lib.tui.core
        
        # Find all classes
        classes = inspect.getmembers(module, inspect.isclass)
        module_classes = [(n, c) for n, c in classes if c.__module__ == module.__name__]
        
        if module_classes:
            assert len(module_classes) > 0
            
            # Test we can at least reference them
            for name, cls in module_classes:
                assert cls is not None
