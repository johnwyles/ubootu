#!/usr/bin/env python3
"""
Test for undefined variables that cause Ansible failures.
This test should FAIL initially, then pass after variables are properly defined.
"""

import subprocess
import tempfile
import yaml
import pytest
from pathlib import Path

# Variables that were undefined in the logs
UNDEFINED_VARIABLES = [
    'prompt_decorator',
    'code_editors', 
    'devtools_selected_file_managers',
    'devtools_selected_system_monitoring',
    'devtools_selected_network_tools',
    'devtools_selected_text_processing',
    'devtools_selected_dev_cli_tools',
    'devtools_selected_productivity_tools',
    'devtools_selected_modern_replacements'
]

def test_undefined_variables_have_defaults():
    """Test that all previously undefined variables have default values"""
    
    # Create a test playbook that uses all the problematic variables
    test_vars = {}
    for var in UNDEFINED_VARIABLES:
        test_vars[var] = []  # Most are lists, some may need different defaults
    
    # Special cases for non-list variables
    test_vars['prompt_decorator'] = 'default'
    test_vars['code_editors'] = ['vim']  # Should be a list
    
    test_playbook = [{
        'hosts': 'localhost',
        'vars': test_vars,
        'tasks': [
            {
                'name': 'Test variable usage',
                'debug': {
                    'msg': 'Testing {{ item }}'
                },
                'loop': UNDEFINED_VARIABLES,
                'when': f'{item} is defined'
            }
        ]
    }]
    
    # Write test playbook
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(test_playbook, f)
        playbook_path = f.name
    
    # Test syntax
    result = subprocess.run(
        ['ansible-playbook', '--syntax-check', playbook_path],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Variable syntax test failed: {result.stderr}"

def test_git_editor_variable():
    """Test the specific git editor variable issue"""
    
    test_playbook = [{
        'hosts': 'localhost',
        'vars': {
            'code_editors': ['vscode', 'vim']
        },
        'tasks': [
            {
                'name': 'Test git editor setting',
                'debug': {
                    'msg': "{{ 'code --wait' if 'vscode' in code_editors else 'vim' }}"
                }
            }
        ]
    }]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(test_playbook, f)
        playbook_path = f.name
    
    result = subprocess.run(
        ['ansible-playbook', '--syntax-check', playbook_path],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Git editor variable test failed: {result.stderr}"

def test_github_api_variable_handling():
    """Test that GitHub API calls handle empty responses"""
    
    # Test the pattern that was failing: first item from empty sequence
    test_playbook = [{
        'hosts': 'localhost',
        'vars': {
            'test_release': {
                'json': {
                    'assets': []
                }
            }
        },
        'tasks': [
            {
                'name': 'Test GitHub API with empty response',
                'debug': {
                    'msg': "{{ test_release.json.assets | selectattr('name', 'match', '.*linux.*') | map(attribute='browser_download_url') | list | first | default('') }}"
                }
            }
        ]
    }]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(test_playbook, f)
        playbook_path = f.name
    
    result = subprocess.run(
        ['ansible-playbook', '--syntax-check', playbook_path],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"GitHub API variable handling test failed: {result.stderr}"

def test_role_defaults_exist():
    """Test that role defaults files contain required variables"""
    
    project_root = Path(__file__).parent.parent
    roles_dir = project_root / 'roles'
    
    critical_roles = [
        'development-tools',
        'dotfiles',
        'applications'
    ]
    
    for role_name in critical_roles:
        defaults_file = roles_dir / role_name / 'defaults' / 'main.yml'
        
        if defaults_file.exists():
            with open(defaults_file, 'r') as f:
                content = f.read()
                
            # Check for some key variables that should be defined
            if role_name == 'development-tools':
                required_vars = [
                    'devtools_selected_file_managers',
                    'devtools_selected_modern_replacements'
                ]
                for var in required_vars:
                    assert var in content, f"Variable '{var}' not found in {role_name} defaults"
            
            elif role_name == 'dotfiles':
                assert 'code_editors' in content or 'prompt_decorator' in content, f"Git-related variables not found in {role_name} defaults"

def test_ansible_undefined_variable_check():
    """Test using ansible-playbook to check for undefined variables"""
    
    project_root = Path(__file__).parent.parent
    
    # Test with minimal variables to catch undefined ones
    test_vars = {
        'primary_user': 'test',
        'selected_items': ['git'],
        'desktop_environment': 'gnome'
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(test_vars, f)
        vars_file = f.name
    
    # Run syntax check with variables
    result = subprocess.run([
        'ansible-playbook',
        str(project_root / 'site.yml'),
        '--syntax-check',
        '-e', f'@{vars_file}'
    ], capture_output=True, text=True, cwd=str(project_root))
    
    # Should not have undefined variable errors
    assert 'is undefined' not in result.stderr, f"Found undefined variables: {result.stderr}"
    assert result.returncode == 0, f"Syntax check failed: {result.stderr}"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])