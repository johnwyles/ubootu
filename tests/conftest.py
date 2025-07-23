"""
Global pytest fixtures and configuration for Ubootu tests.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import yaml

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_terminal():
    """Mock terminal for TUI testing."""
    terminal = Mock()
    terminal.width = 80
    terminal.height = 24
    terminal.is_a_tty = True
    terminal.does_styling = True
    terminal.number_of_colors = 256
    
    # Mock color attributes
    colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for color in colors:
        setattr(terminal, color, lambda x: f'[{color}]{x}[/{color}]')
        setattr(terminal, f'on_{color}', lambda x: f'[on_{color}]{x}[/on_{color}]')
        setattr(terminal, f'bright_{color}', lambda x: f'[bright_{color}]{x}[/bright_{color}]')
    
    # Mock style attributes
    styles = ['bold', 'italic', 'underline', 'blink', 'reverse', 'normal']
    for style in styles:
        setattr(terminal, style, lambda x: f'[{style}]{x}[/{style}]')
    
    # Mock positioning
    terminal.move = Mock(side_effect=lambda y, x: f'\033[{y};{x}H')
    terminal.move_up = Mock(side_effect=lambda n=1: f'\033[{n}A')
    terminal.move_down = Mock(side_effect=lambda n=1: f'\033[{n}B')
    terminal.clear = Mock(return_value='\033[2J\033[H')
    terminal.clear_eol = Mock(return_value='\033[K')
    
    return terminal


@pytest.fixture
def sample_config():
    """Sample configuration dictionary for testing."""
    return {
        'system': {
            'hostname': 'test-ubuntu',
            'timezone': 'UTC',
            'locale': 'en_US.UTF-8',
            'enable_updates': True,
            'enable_unattended_upgrades': False
        },
        'desktop_environment': {
            'install': True,
            'environment': 'gnome',
            'display_manager': 'gdm3',
            'install_themes': True
        },
        'development_tools': {
            'editors': ['vim', 'emacs', 'nano'],
            'ides': ['vscode'],
            'languages': {
                'python': {
                    'install': True,
                    'versions': ['3.8', '3.9', '3.10', '3.11'],
                    'pip_packages': ['pytest', 'black', 'flake8']
                },
                'nodejs': {
                    'install': True,
                    'version': '18',
                    'npm_packages': ['yarn', 'typescript']
                }
            },
            'containers': {
                'docker': True,
                'podman': False
            }
        },
        'applications': {
            'browsers': ['firefox', 'chromium'],
            'communication': ['slack', 'discord'],
            'multimedia': ['vlc', 'spotify'],
            'productivity': ['libreoffice']
        },
        'security': {
            'enable_firewall': True,
            'enable_fail2ban': True,
            'ssh_hardening': True,
            'install_antivirus': False
        }
    }


@pytest.fixture
def sample_config_file(temp_dir, sample_config):
    """Create a temporary config file with sample data."""
    config_file = temp_dir / 'config.yml'
    with open(config_file, 'w') as f:
        yaml.dump(sample_config, f)
    return config_file


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for command execution tests."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'Success'
        mock_run.return_value.stderr = ''
        yield mock_run


@pytest.fixture
def mock_ansible_runner():
    """Mock ansible runner for playbook execution tests."""
    with patch('ansible_runner.run') as mock_run:
        mock_result = Mock()
        mock_result.rc = 0
        mock_result.status = 'successful'
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_curses():
    """Mock curses module for TUI testing."""
    mock_curses = Mock()
    mock_stdscr = Mock()
    
    # Mock screen dimensions
    mock_stdscr.getmaxyx.return_value = (24, 80)
    mock_stdscr.getyx.return_value = (0, 0)
    
    # Mock color support
    mock_curses.has_colors.return_value = True
    mock_curses.can_change_color.return_value = True
    mock_curses.COLORS = 256
    mock_curses.COLOR_PAIRS = 256
    
    # Mock color constants
    for i, color in enumerate(['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']):
        setattr(mock_curses, f'COLOR_{color}', i)
    
    # Mock attributes
    mock_curses.A_NORMAL = 0
    mock_curses.A_BOLD = 1
    mock_curses.A_UNDERLINE = 2
    mock_curses.A_REVERSE = 4
    
    # Mock key constants
    mock_curses.KEY_UP = 259
    mock_curses.KEY_DOWN = 258
    mock_curses.KEY_LEFT = 260
    mock_curses.KEY_RIGHT = 261
    mock_curses.KEY_ENTER = 10
    mock_curses.KEY_BACKSPACE = 263
    
    with patch('curses.initscr', return_value=mock_stdscr):
        with patch.dict('sys.modules', {'curses': mock_curses}):
            yield mock_curses, mock_stdscr


@pytest.fixture
def capture_output():
    """Capture stdout and stderr for testing."""
    from io import StringIO
    import sys
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    
    yield sys.stdout, sys.stderr
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr


# Markers for test categorization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require external dependencies"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that may require external dependencies"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )
    config.addinivalue_line(
        "markers", "tui: Tests specific to the TUI interface"
    )
    config.addinivalue_line(
        "markers", "requires_terminal: Tests that require terminal functionality"
    )


# Skip tests that require a real terminal in CI environments
def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    if not sys.stdout.isatty():
        skip_terminal = pytest.mark.skip(reason="requires terminal")
        for item in items:
            if "requires_terminal" in item.keywords:
                item.add_marker(skip_terminal)