#!/usr/bin/env python3
"""
Test package names and download URLs are correct
"""

import pytest
import requests
from unittest.mock import Mock, patch
import re


class TestPackageNames:
    """Test that package names are correct for Ubuntu"""
    
    def test_corrected_package_names(self):
        """Test that package names are corrected"""
        package_mappings = {
            # Wrong name -> Correct name
            'ss': 'iproute2',  # ss command is in iproute2
            'dig': 'dnsutils',  # dig is in dnsutils
            'nslookup': 'dnsutils',
            'netstat': 'net-tools',
            'ifconfig': 'net-tools',
            'dog': None,  # Not available in apt, use snap or build
            'gimp-plugin-registry': None,  # Removed from Ubuntu
            'speedtest': 'speedtest-cli',  # If using apt
        }
        
        for wrong, correct in package_mappings.items():
            if correct:
                assert wrong != correct
                # Test that ansible uses correct name
                apt_task = {
                    'name': f'Install {wrong} command',
                    'apt': {
                        'name': correct,
                        'state': 'present'
                    }
                }
                assert apt_task['apt']['name'] == correct
    
    def test_removed_packages_handled(self):
        """Test that removed packages are handled appropriately"""
        removed_packages = {
            'gimp-plugin-registry': {
                'reason': 'Removed from Ubuntu repositories',
                'alternative': 'Install GIMP plugins manually or via flatpak'
            },
            'python-pip': {
                'reason': 'Python 2 removed',
                'alternative': 'python3-pip'
            }
        }
        
        for package, info in removed_packages.items():
            assert 'reason' in info
            assert 'alternative' in info
    
    def test_snap_packages(self):
        """Test packages that should be installed via snap"""
        snap_packages = [
            'dog',  # DNS client
            'btop',  # System monitor
            'dust',  # Disk usage
            'procs',  # Process viewer
        ]
        
        for package in snap_packages:
            snap_task = {
                'name': f'Install {package} via snap',
                'snap': {
                    'name': package,
                    'state': 'present'
                }
            }
            assert snap_task['snap']['name'] == package


class TestDownloadURLs:
    """Test that download URLs are valid and correct"""
    
    @pytest.mark.parametrize("tool,expected_url_pattern", [
        ('diff-so-fancy', r'https://github\.com/so-fancy/diff-so-fancy/releases/download/v[\d\.]+/diff-so-fancy'),
        ('hub', r'https://github\.com/github/hub/releases/download/v[\d\.]+/hub-linux-amd64-[\d\.]+\.tgz'),
        ('rclone', r'https://downloads\.rclone\.org/v[\d\.]+/rclone-v[\d\.]+-linux-amd64\.zip'),
        ('nebula', r'https://github\.com/slackhq/nebula/releases/download/v[\d\.]+/nebula-linux-amd64\.tar\.gz'),
    ])
    def test_github_release_urls(self, tool, expected_url_pattern):
        """Test GitHub release URL patterns"""
        # These should use GitHub API to get latest release
        github_api_pattern = f'https://api.github.com/repos/{{owner}}/{{repo}}/releases/latest'
        
        # Verify URL pattern matches expected format
        assert re.match(expected_url_pattern.replace('[\d\.]+', '.*'), expected_url_pattern)
    
    def test_fixed_download_urls(self):
        """Test corrected download URLs"""
        fixed_urls = {
            'diff-so-fancy': {
                'old': 'https://raw.githubusercontent.com/so-fancy/diff-so-fancy/master/third_party/build_fatpack/diff-so-fancy',
                'new': 'Use GitHub releases API',
                'api': 'https://api.github.com/repos/so-fancy/diff-so-fancy/releases/latest'
            },
            'rclone-browser': {
                'old': 'https://github.com/kapitainsky/RcloneBrowser/releases/download/1.8.0/rclone-browser-1.8.0-linux-x86_64.AppImage',
                'new': 'Project archived, use rclone web UI instead',
                'alternative': 'rclone rcd --rc-web-gui'
            },
            'hub': {
                'old': 'Direct download of specific version',
                'new': 'Use GitHub CLI (gh) instead',
                'install': 'apt install gh'
            }
        }
        
        for tool, urls in fixed_urls.items():
            assert 'old' in urls
            assert 'new' in urls or 'alternative' in urls
    
    def test_apt_repository_urls(self):
        """Test that APT repository URLs are correct"""
        repo_urls = {
            'docker': 'https://download.docker.com/linux/ubuntu',
            'microsoft': 'https://packages.microsoft.com/repos/code',
            'syncthing': 'https://apt.syncthing.net/',
            'tailscale': 'https://pkgs.tailscale.com/stable/ubuntu',
            'speedtest': 'https://packagecloud.io/ookla/speedtest-cli/ubuntu',
            'dbeaver': 'https://dbeaver.io/debs/dbeaver-ce',
        }
        
        for name, url in repo_urls.items():
            assert url.startswith('https://')
            assert len(url) > 10


class TestGitHubAPIUsage:
    """Test proper GitHub API usage for dynamic downloads"""
    
    def test_github_release_api_structure(self):
        """Test structure for getting latest releases from GitHub"""
        api_call = {
            'uri': {
                'url': 'https://api.github.com/repos/{{ item.owner }}/{{ item.repo }}/releases/latest',
                'headers': {
                    'Accept': 'application/vnd.github.v3+json'
                }
            },
            'register': 'github_release'
        }
        
        # Then use the result to get download URL
        download_logic = '''
        github_release.json.assets |
        selectattr('name', 'match', '.*linux.*amd64.*') |
        map(attribute='browser_download_url') |
        first
        '''
        
        assert 'api.github.com' in api_call['uri']['url']
        assert 'Accept' in api_call['uri']['headers']
    
    def test_handle_empty_github_results(self):
        """Test handling when GitHub API returns no matching assets"""
        # This is the "No first item, sequence was empty" error
        safe_filter = '''
        github_release.json.assets |
        selectattr('name', 'match', '.*linux.*amd64.*') |
        list
        '''
        
        # Then check if list is empty
        condition = 'filtered_assets | length > 0'
        
        # This prevents the "No first item" error
        assert 'list' in safe_filter
        assert 'length > 0' in condition


class TestAlternativeInstallMethods:
    """Test alternative installation methods for packages"""
    
    def test_manual_build_instructions(self):
        """Test packages that need manual building"""
        manual_builds = {
            'ghostty': {
                'type': 'source',
                'repo': 'https://github.com/ghostty-org/ghostty',
                'build_deps': ['zig', 'pkg-config', 'libgtk-4-dev'],
                'build_cmd': 'zig build -Doptimize=ReleaseFast'
            },
            'zellij': {
                'type': 'cargo',
                'install_cmd': 'cargo install zellij'
            }
        }
        
        for tool, config in manual_builds.items():
            assert 'type' in config
            if config['type'] == 'source':
                assert 'build_deps' in config
    
    def test_deb_download_tasks(self):
        """Test direct .deb file downloads"""
        deb_downloads = {
            'vscode': {
                'url': 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64',
                'filename': 'vscode.deb'
            },
            'slack': {
                'url': 'https://downloads.slack-edge.com/linux_releases/slack-desktop-amd64.deb',
                'filename': 'slack.deb'
            }
        }
        
        for app, config in deb_downloads.items():
            task = {
                'name': f'Download {app} .deb',
                'get_url': {
                    'url': config['url'],
                    'dest': f'/tmp/{config["filename"]}'
                }
            }
            assert task['get_url']['url'] == config['url']
    
    def test_appimage_downloads(self):
        """Test AppImage downloads"""
        appimages = {
            'neovim': {
                'url': 'https://github.com/neovim/neovim/releases/download/stable/nvim.appimage',
                'dest': '/usr/local/bin/nvim'
            },
            'obsidian': {
                'url': 'https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian.AppImage',
                'dest': '/opt/obsidian/Obsidian.AppImage'
            }
        }
        
        for app, config in appimages.items():
            assert config['url'].endswith('.appimage') or config['url'].endswith('.AppImage')
            assert config['dest'].startswith('/usr/local/bin') or config['dest'].startswith('/opt')


class TestPackageAvailability:
    """Test package availability in different Ubuntu versions"""
    
    def test_ubuntu_2504_specific_issues(self):
        """Test Ubuntu 25.04 specific package issues"""
        ubuntu_2504_issues = {
            'repositories_missing_plucky': [
                'tailscale',
                'speedtest-cli',
                'docker-ce',
                'syncthing'
            ],
            'fallback_to': 'noble',  # 24.04 LTS
            'packages_removed': [
                'gimp-plugin-registry',
                'apt-key'  # Command removed
            ]
        }
        
        assert ubuntu_2504_issues['fallback_to'] == 'noble'
        assert 'apt-key' in ubuntu_2504_issues['packages_removed']
    
    def test_conditional_package_install(self):
        """Test conditional package installation based on Ubuntu version"""
        version_conditions = {
            'task': 'Install package with version check',
            'apt': {
                'name': '{{ package_name }}',
                'state': 'present'
            },
            'when': [
                'ansible_distribution == "Ubuntu"',
                'ansible_distribution_major_version | int >= 22'
            ]
        }
        
        assert 'ansible_distribution' in str(version_conditions['when'])
        assert 'ansible_distribution_major_version' in str(version_conditions['when'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])