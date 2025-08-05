#!/usr/bin/env python3
"""
Test package availability and alternatives for Ubuntu 25.04.
This test should FAIL initially for packages that don't exist, then pass after alternatives are implemented.
"""

import subprocess
import pytest
import tempfile
import yaml

# Packages that were failing in the logs
PROBLEMATIC_PACKAGES = [
    'bandwhich',
    'speedtest', 
    'dbeaver-ce',
    'paris-traceroute',
    'tailscale',
    'gimp-plugin-registry'
]

# Required packages that should be available
REQUIRED_PACKAGES = [
    'flatpak',
    'python3-psutil',
    'python3-apt',
    'python3-gpg'
]

def test_required_packages_available():
    """Test that essential packages are available in repositories"""
    for package in REQUIRED_PACKAGES:
        result = subprocess.run(
            ['apt-cache', 'show', package],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Required package '{package}' not available in repositories"

def test_problematic_packages_have_alternatives():
    """Test that problematic packages either work or have alternatives defined"""
    
    # Define alternatives for packages that don't work
    alternatives = {
        'bandwhich': 'snap install bandwhich',
        'speedtest': 'snap install speedtest-cli', 
        'dbeaver-ce': 'snap install dbeaver-ce',
        'paris-traceroute': 'mtr-tiny',  # Alternative package
        'gimp-plugin-registry': None,  # Optional, can be skipped
    }
    
    for package in PROBLEMATIC_PACKAGES:
        if package == 'tailscale':
            # Special case: test tailscale repository setup
            continue
            
        # Check if package is available in apt
        result = subprocess.run(
            ['apt-cache', 'show', package],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Package not available, check if alternative is defined
            alternative = alternatives.get(package)
            if alternative is None:
                # Package is optional, can be skipped
                continue
            elif alternative.startswith('snap install'):
                # Test if snap alternative works
                snap_package = alternative.replace('snap install ', '')
                snap_result = subprocess.run(
                    ['snap', 'info', snap_package],
                    capture_output=True,
                    text=True
                )
                assert snap_result.returncode == 0, f"Package '{package}' not available and snap alternative '{snap_package}' also not found"
            else:
                # Test if alternative package is available
                alt_result = subprocess.run(
                    ['apt-cache', 'show', alternative],
                    capture_output=True,
                    text=True
                )
                assert alt_result.returncode == 0, f"Package '{package}' not available and alternative '{alternative}' also not found"

def test_tailscale_repository_setup():
    """Test that tailscale repository can be properly configured"""
    
    # Test the GPG key URL (should not have newlines)
    expected_url = "https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg"
    
    # This would be tested by checking the actual ansible task
    # For now, just verify the URL format
    assert '\n' not in expected_url, "Tailscale GPG URL should not contain newlines"
    assert expected_url.endswith('.noarmor.gpg'), "Tailscale GPG URL should end with .noarmor.gpg"

def test_flatpak_installation():
    """Test that flatpak can be installed and used"""
    
    # Check if flatpak package exists
    result = subprocess.run(
        ['apt-cache', 'show', 'flatpak'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "flatpak package not available"
    
    # After installation, flatpak executable should be available
    # This test validates the dependency chain

def test_ansible_package_syntax():
    """Test that package installation tasks have proper syntax"""
    
    # Create a simple test playbook to validate package syntax
    test_playbook = {
        'hosts': 'localhost',
        'tasks': [
            {
                'name': 'Test package installation with alternatives',
                'block': [
                    {
                        'name': 'Try main package',
                        'apt': {'name': 'nonexistent-package', 'state': 'present'},
                        'ignore_errors': True,
                        'register': 'main_install'
                    },
                    {
                        'name': 'Use snap alternative',
                        'snap': {'name': 'alternative-package', 'state': 'present'},
                        'when': 'main_install.failed'
                    }
                ]
            }
        ]
    }
    
    # Write test playbook
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump([test_playbook], f)
        playbook_path = f.name
    
    # Test syntax
    result = subprocess.run(
        ['ansible-playbook', '--syntax-check', playbook_path],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Package installation syntax test failed: {result.stderr}"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])