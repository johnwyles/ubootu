"""
Shared pytest fixtures for the test suite
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import tempfile
import yaml
import curses
import os
from pathlib import Path


@pytest.fixture
def mock_curses():
    """Mock curses module for TUI tests"""
    with patch('curses.initscr') as mock_initscr:
        with patch('curses.start_color'):
            with patch('curses.use_default_colors'):
                with patch('curses.curs_set'):
                    with patch('curses.noecho'):
                        with patch('curses.cbreak'):
                            mock_screen = MagicMock()
                            mock_screen.getmaxyx.return_value = (24, 80)
                            mock_screen.getch.return_value = ord('q')
                            mock_initscr.return_value = mock_screen
                            yield mock_screen


@pytest.fixture
def temp_config():
    """Create a temporary config file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        config = {
            'version': '1.0',
            'username': 'testuser',
            'full_name': 'Test User',
            'timezone': 'UTC',
            'desktop_environment': 'gnome',
            'selected_categories': ['development', 'applications']
        }
        yaml.dump(config, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def mock_yaml_config():
    """Mock YAML configuration for tests"""
    return {
        'version': '1.0',
        'username': 'testuser',
        'full_name': 'Test User',
        'email': 'test@example.com',
        'timezone': 'America/New_York',
        'desktop_environment': 'gnome',
        'selected_categories': ['development', 'applications', 'security'],
        'development': {
            'languages': ['python', 'nodejs', 'go'],
            'ides': ['vscode', 'pycharm'],
            'tools': ['docker', 'git']
        },
        'applications': {
            'browsers': ['firefox', 'chrome'],
            'media': ['vlc', 'spotify']
        },
        'security': {
            'firewall': True,
            'antivirus': False
        }
    }


@pytest.fixture
def mock_menu_registry():
    """Mock menu registry for TUI tests"""
    registry = MagicMock()
    registry.get_all_builders.return_value = []
    registry.register = MagicMock()
    return registry


@pytest.fixture(autouse=True)
def mock_terminal_check():
    """Auto-mock terminal checks for all tests"""
    with patch('lib.terminal_check.can_run_tui', return_value=True):
        with patch('lib.terminal_check.check_terminal_capabilities', return_value={'colors': True, 'unicode': True, 'size': (80, 24)}):
            yield


@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ''
        mock_run.return_value.stderr = ''
        yield mock_run
