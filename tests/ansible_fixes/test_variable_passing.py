#!/usr/bin/env python3
"""
Test that variables from config.yml are properly passed to Ansible playbook
"""

import pytest
import yaml
import json
import subprocess
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestVariablePassing:
    """Test that all config variables are passed to Ansible"""
    
    @pytest.fixture
    def sample_config(self):
        """Create a sample config.yml structure"""
        return {
            'selected_items': [
                'dev-code-editors',
                'cursor', 
                'vscode',
                'git',
                'docker-ce',
                'helm'
            ],
            'configurable_items': {
                'swappiness': {'id': 'swappiness', 'value': 10},
                'terminal-font-size': {'id': 'terminal-font-size', 'value': 12}
            },
            'ansible_variables': {
                'desktop_environment': 'gnome',
                'de_environment': 'gnome',
                'de_autologin': False,
                'primary_user': 'testuser'
            }
        }
    
    @pytest.fixture
    def temp_config_file(self, sample_config):
        """Write sample config to temporary file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(sample_config, f)
            temp_path = f.name
        yield temp_path
        os.unlink(temp_path)
    
    def test_selected_items_passed_to_ansible(self, sample_config):
        """Test that selected_items from config are available in Ansible"""
        # This test verifies the unified_menu.py passes selected_items
        from lib.tui.unified_menu import UnifiedMenu
        
        # Mock the necessary parts
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        # Get the extra vars that would be passed to ansible
        extra_vars = menu._prepare_ansible_variables()
        
        # Verify selected_items is in extra_vars
        assert 'selected_items' in extra_vars
        assert extra_vars['selected_items'] == sample_config['selected_items']
        assert 'helm' in extra_vars['selected_items']
        assert 'docker-ce' in extra_vars['selected_items']
    
    def test_ansible_variables_passed(self, sample_config):
        """Test that ansible_variables from config are passed"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        extra_vars = menu._prepare_ansible_variables()
        
        # All ansible_variables should be in extra_vars
        assert 'desktop_environment' in extra_vars
        assert extra_vars['desktop_environment'] == 'gnome'
        assert 'de_environment' in extra_vars
        assert extra_vars['de_environment'] == 'gnome'
        assert 'primary_user' in extra_vars
    
    def test_configurable_items_converted(self, sample_config):
        """Test that configurable_items are converted to ansible variables"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        extra_vars = menu._prepare_ansible_variables()
        
        # Configurable items should be converted to simple key-value
        assert 'system_swappiness' in extra_vars
        assert extra_vars['system_swappiness'] == 10
    
    def test_extra_vars_file_created(self, sample_config, tmp_path):
        """Test that extra vars are written to file for ansible"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        # Create extra vars file
        extra_vars_file = menu._create_extra_vars_file(tmp_path)
        
        assert extra_vars_file.exists()
        
        # Load and verify contents
        with open(extra_vars_file) as f:
            vars_data = yaml.safe_load(f)
        
        assert 'selected_items' in vars_data
        assert 'desktop_environment' in vars_data
        assert 'system_swappiness' in vars_data
    
    @patch('subprocess.run')
    def test_ansible_command_includes_extra_vars(self, mock_run, sample_config):
        """Test that ansible-playbook command includes extra-vars file"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        # Mock the ansible run
        mock_run.return_value = Mock(returncode=0)
        
        # Get the command that would be run
        cmd = menu._build_ansible_command()
        
        # Verify extra-vars is in command
        assert '--extra-vars' in cmd or '-e' in cmd
        # Should reference a file with @ prefix
        extra_vars_args = [arg for arg in cmd if arg.startswith('@') and 'extra-vars' in arg]
        assert len(extra_vars_args) > 0
    
    def test_display_manager_variables_included(self, sample_config):
        """Test that desktop environment display manager vars are included"""
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        extra_vars = menu._prepare_ansible_variables()
        
        # Should include display manager mapping
        assert 'de_display_manager' in extra_vars
        assert isinstance(extra_vars['de_display_manager'], dict)
        assert 'gnome' in extra_vars['de_display_manager']
        assert extra_vars['de_display_manager']['gnome'] == 'gdm3'
    
    def test_no_undefined_variables_error(self, sample_config):
        """Integration test: verify no 'undefined variable' errors occur"""
        # This would be run against actual ansible with --syntax-check
        from lib.tui.unified_menu import UnifiedMenu
        
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        
        menu = UnifiedMenu(mock_stdscr)
        menu.config = sample_config
        
        # Create extra vars
        extra_vars = menu._prepare_ansible_variables()
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(extra_vars, f)
            vars_file = f.name
        
        try:
            # Run ansible syntax check
            result = subprocess.run([
                'ansible-playbook',
                'site.yml',
                '--syntax-check',
                '-e', f'@{vars_file}',
                '-i', 'localhost,'
            ], capture_output=True, text=True, cwd='/home/jwyles/code/ubootu')
            
            # Should not have undefined variable errors
            assert 'undefined variable' not in result.stderr
            assert 'is undefined' not in result.stderr
            
        finally:
            os.unlink(vars_file)


class TestVariableMapping:
    """Test the mapping of config values to ansible variable names"""
    
    def test_configurable_item_name_mapping(self):
        """Test that configurable items map to correct ansible var names"""
        mappings = {
            'swappiness': 'system_swappiness',
            'terminal-font-size': 'terminal_font_size',
            'terminal-font-family': 'terminal_font_family',
            'custom-accent': 'theme_custom_accent',
            'custom-background': 'theme_custom_background'
        }
        
        from lib.tui.unified_menu import UnifiedMenu
        
        # Verify the mapping exists
        assert hasattr(UnifiedMenu, '_get_ansible_var_name')
        
        menu = UnifiedMenu(Mock())
        for config_name, ansible_name in mappings.items():
            assert menu._get_ansible_var_name(config_name) == ansible_name


if __name__ == '__main__':
    pytest.main([__file__, '-v'])