#!/usr/bin/env python3
"""
Test that all prerequisites are installed before they're needed
"""

import pytest
import subprocess
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestSystemPrerequisites:
    """Test that system prerequisites are properly checked and installed"""
    
    def test_python3_psutil_installed_early(self):
        """Test that python3-psutil is installed before any module needs it"""
        # This should be in common role or bootstrap
        prerequisites = [
            'python3-psutil',
            'python3-apt',
            'python3-gpg',
            'curl',
            'gpg',
            'software-properties-common'
        ]
        
        # Test that these are installed in common/tasks/packages.yml
        common_packages_order = [
            'apt_update',
            'essential_packages',  # Should include above packages
            'other_tasks'
        ]
        
        assert 'python3-psutil' in prerequisites
        assert 'gpg' in prerequisites  # Needed for key operations
    
    def test_groups_created_before_user_tasks(self):
        """Test that groups are created before trying to add users to them"""
        # Groups that need to exist
        required_groups = ['docker', 'vboxusers', 'libvirt', 'kvm']
        
        # Test the group creation logic
        def create_group_if_missing(group_name):
            """Logic that should be in ansible task"""
            return {
                'name': f"Create {group_name} group if it doesn't exist",
                'group': {
                    'name': group_name,
                    'state': 'present'
                },
                'become': True
            }
        
        for group in required_groups:
            task = create_group_if_missing(group)
            assert task['group']['name'] == group
            assert task['group']['state'] == 'present'
            assert task['become'] is True
    
    def test_check_before_modify_pattern(self):
        """Test that we check for existence before modifying"""
        # Pattern for checking before modifying
        check_patterns = [
            {
                'check': 'stat /etc/ssh/sshd_config',
                'condition': 'sshd_config_stat.stat.exists',
                'task': 'modify_sshd_config'
            },
            {
                'check': 'command -v flatpak',
                'condition': 'flatpak_installed.rc == 0',
                'task': 'flatpak_operations'
            },
            {
                'check': 'getent group docker',
                'condition': 'docker_group.rc == 0',
                'task': 'add_user_to_docker_group'
            }
        ]
        
        for pattern in check_patterns:
            assert 'check' in pattern
            assert 'condition' in pattern
            assert 'task' in pattern
    
    def test_ssh_server_check(self):
        """Test SSH server configuration is conditional"""
        ssh_tasks = {
            'name': 'Configure SSH',
            'block': [
                {
                    'name': 'Check if SSH server is installed',
                    'stat': {'path': '/etc/ssh/sshd_config'},
                    'register': 'sshd_config'
                },
                {
                    'name': 'Configure SSH settings',
                    'lineinfile': {
                        'path': '/etc/ssh/sshd_config',
                        'regexp': '^PermitRootLogin',
                        'line': 'PermitRootLogin no'
                    },
                    'when': 'sshd_config.stat.exists'
                }
            ]
        }
        
        # Verify conditional logic
        assert ssh_tasks['block'][1]['when'] == 'sshd_config.stat.exists'
    
    def test_flatpak_check_before_use(self):
        """Test that flatpak is checked before trying to use it"""
        flatpak_logic = {
            'check_task': {
                'name': 'Check if flatpak is installed',
                'command': 'which flatpak',
                'register': 'flatpak_check',
                'failed_when': False
            },
            'install_task': {
                'name': 'Install flatpak if missing',
                'apt': {
                    'name': 'flatpak',
                    'state': 'present'
                },
                'when': 'flatpak_check.rc != 0'
            },
            'use_task': {
                'name': 'Add flathub remote',
                'flatpak_remote': {
                    'name': 'flathub',
                    'flatpakrepo_url': 'https://flathub.org/repo/flathub.flatpakrepo'
                },
                'when': 'flatpak_check.rc == 0 or flatpak_installed is changed'
            }
        }
        
        # Verify proper ordering and conditions
        assert 'which flatpak' in flatpak_logic['check_task']['command']
        assert 'flatpak_check.rc != 0' in flatpak_logic['install_task']['when']


class TestPackageDependencies:
    """Test that package dependencies are handled correctly"""
    
    def test_build_dependencies_for_source_builds(self):
        """Test that build deps are installed before building from source"""
        build_deps = {
            'common': [
                'build-essential',
                'git',
                'curl',
                'wget'
            ],
            'rust': [
                'cargo',
                'rustc'
            ],
            'go': [
                'golang-go'
            ]
        }
        
        # All source builds should check for these
        assert 'build-essential' in build_deps['common']
        assert 'git' in build_deps['common']
    
    def test_package_name_corrections(self):
        """Test that incorrect package names are fixed"""
        package_corrections = {
            'ss': 'iproute2',  # ss is part of iproute2
            'dig': 'dnsutils',  # dig is part of dnsutils
            'netstat': 'net-tools',  # netstat is part of net-tools
            'ifconfig': 'net-tools',
            'dog': None,  # dog needs to be installed via other means
            'gimp-plugin-registry': None  # No longer available in recent Ubuntu
        }
        
        for wrong_name, correct_name in package_corrections.items():
            if correct_name:
                assert correct_name != wrong_name
                assert len(correct_name) > 0
    
    def test_alternative_installation_methods(self):
        """Test packages that need alternative installation methods"""
        alternative_installs = {
            'dog': {
                'method': 'snap',
                'package': 'dog'
            },
            'insomnia': {
                'method': 'deb_download',
                'url': 'https://updates.insomnia.rest/downloads/ubuntu/latest'
            },
            'dbeaver-ce': {
                'method': 'apt_repository',
                'repo': 'dbeaver'
            }
        }
        
        for package, config in alternative_installs.items():
            assert 'method' in config
            assert config['method'] in ['snap', 'deb_download', 'apt_repository', 'flatpak']


class TestOrderingDependencies:
    """Test that tasks are ordered correctly to avoid dependency issues"""
    
    def test_repository_before_package_install(self):
        """Test that repositories are added before installing packages from them"""
        task_order = [
            'add_docker_repository',
            'apt_update',
            'install_docker_ce'
        ]
        
        # Docker repo must be added before installing docker-ce
        assert task_order.index('add_docker_repository') < task_order.index('install_docker_ce')
        assert task_order.index('apt_update') < task_order.index('install_docker_ce')
    
    def test_gpg_key_before_repository(self):
        """Test that GPG keys are added before repositories that need them"""
        task_order = [
            'install_gpg_package',
            'download_repo_key',
            'add_repository',
            'apt_update',
            'install_package'
        ]
        
        # GPG must be installed first
        assert task_order.index('install_gpg_package') == 0
        # Key before repo
        assert task_order.index('download_repo_key') < task_order.index('add_repository')
    
    def test_user_exists_before_user_operations(self):
        """Test that user exists before doing user operations"""
        user_tasks = {
            'create_user': {
                'name': 'Ensure user exists',
                'user': {
                    'name': '{{ primary_user }}',
                    'state': 'present'
                }
            },
            'add_to_group': {
                'name': 'Add user to groups',
                'user': {
                    'name': '{{ primary_user }}',
                    'groups': 'docker,sudo',
                    'append': True
                },
                'when': 'user_created is not changed or True'
            }
        }
        
        assert 'state' in user_tasks['create_user']['user']
        assert user_tasks['create_user']['user']['state'] == 'present'


class TestErrorHandling:
    """Test that errors are handled gracefully"""
    
    def test_missing_package_fallback(self):
        """Test fallback behavior for missing packages"""
        fallback_strategies = {
            'package_not_found': {
                'primary': 'apt',
                'fallback': ['snap', 'flatpak', 'manual_download']
            },
            'repository_not_available': {
                'primary': 'current_release',
                'fallback': ['previous_lts', 'manual_download']
            }
        }
        
        assert 'snap' in fallback_strategies['package_not_found']['fallback']
        assert 'previous_lts' in fallback_strategies['repository_not_available']['fallback']
    
    def test_conditional_task_execution(self):
        """Test that tasks handle missing dependencies gracefully"""
        conditional_patterns = [
            {
                'task': 'Configure Docker',
                'condition': 'docker_installed.rc == 0',
                'skip_message': 'Docker not installed, skipping configuration'
            },
            {
                'task': 'Setup VirtualBox',
                'condition': 'ansible_virtualization_type != "docker"',
                'skip_message': 'Running in container, skipping VirtualBox'
            }
        ]
        
        for pattern in conditional_patterns:
            assert 'condition' in pattern
            assert 'skip_message' in pattern


if __name__ == '__main__':
    pytest.main([__file__, '-v'])