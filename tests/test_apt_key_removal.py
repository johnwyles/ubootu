#!/usr/bin/env python3
"""
Test to ensure all apt-key usage has been removed and replaced with signed-by method.
This test should FAIL initially, then pass after fixes are implemented.
"""

import os
import yaml
import pytest
from pathlib import Path

def find_yaml_files(directory):
    """Find all YAML files in the project"""
    yaml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yml', '.yaml')):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

def scan_file_for_apt_key(file_path):
    """Scan a YAML file for apt-key usage"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check for various forms of apt-key usage
        apt_key_patterns = [
            'apt_key:',
            'ansible.builtin.apt_key:',
            'community.general.apt_key:',
            'apt-key add',
            'apt-key adv',
        ]
        
        found_patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in apt_key_patterns:
                if pattern in line and not line.strip().startswith('#'):
                    found_patterns.append({
                        'file': file_path,
                        'line': i,
                        'content': line.strip(),
                        'pattern': pattern
                    })
                    
        return found_patterns
    except Exception as e:
        # Skip files that can't be read (binary, etc.)
        return []

def test_no_apt_key_usage():
    """Test that no YAML files contain apt-key usage"""
    project_root = Path(__file__).parent.parent
    yaml_files = find_yaml_files(str(project_root))
    
    all_apt_key_usage = []
    
    for yaml_file in yaml_files:
        apt_key_usage = scan_file_for_apt_key(yaml_file)
        all_apt_key_usage.extend(apt_key_usage)
    
    if all_apt_key_usage:
        error_msg = "Found apt-key usage in the following files:\n"
        for usage in all_apt_key_usage:
            error_msg += f"  {usage['file']}:{usage['line']} - {usage['content']}\n"
        error_msg += "\nAll apt-key usage should be replaced with signed-by GPG method."
        
        pytest.fail(error_msg)

def test_signed_by_method_used():
    """Test that signed-by method is used for GPG keys"""
    project_root = Path(__file__).parent.parent
    yaml_files = find_yaml_files(str(project_root))
    
    signed_by_usage = []
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                content = f.read()
                
            if 'signed-by=' in content:
                signed_by_usage.append(yaml_file)
        except:
            continue
    
    # Should have at least some signed-by usage if we're adding repositories
    assert len(signed_by_usage) > 0, "No signed-by GPG method found. Repository setup may be missing proper GPG key handling."

if __name__ == '__main__':
    pytest.main([__file__, '-v'])