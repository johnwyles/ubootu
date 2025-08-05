#!/usr/bin/env python3
"""
System Discovery Module for Ubootu
Detects installed packages and system state
"""

import subprocess
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import re


class SystemDiscovery:
    """Discover what's actually installed on the system"""
    
    def __init__(self):
        """Initialize the system discovery module"""
        self.installed_packages = {}
        self.package_to_menu_map = self._build_package_mapping()
        self.state_file = '.ubootu_system_state.yml'
        self.managed_file = '.ubootu_managed.yml'
        
    def _build_package_mapping(self) -> Dict[str, str]:
        """Build mapping from package names to menu item IDs"""
        return {
            # Browsers
            'firefox': 'firefox',
            'google-chrome-stable': 'chrome',
            'chromium-browser': 'chromium',
            'brave-browser': 'brave',
            'vivaldi-stable': 'vivaldi',
            'opera-stable': 'opera',
            'microsoft-edge-stable': 'edge',
            
            # Development tools
            'code': 'vscode',
            'sublime-text': 'sublime',
            'vim': 'vim',
            'neovim': 'neovim',
            'emacs': 'emacs',
            'docker-ce': 'docker',
            'docker.io': 'docker',
            'nodejs': 'nodejs',
            'npm': 'npm',
            'yarn': 'yarn',
            'python3': 'python3',
            'python3-pip': 'pip3',
            'golang-go': 'golang',
            'rustc': 'rust',
            'cargo': 'cargo',
            'git': 'git',
            'gh': 'github-cli',
            
            # Communication
            'slack-desktop': 'slack',
            'discord': 'discord',
            'telegram-desktop': 'telegram',
            'signal-desktop': 'signal',
            'zoom': 'zoom',
            'teams': 'teams',
            'skypeforlinux': 'skype',
            
            # Productivity
            'libreoffice': 'libreoffice',
            'thunderbird': 'thunderbird',
            'obsidian': 'obsidian',
            'notion-snap': 'notion',
            'todoist': 'todoist',
            
            # Multimedia
            'vlc': 'vlc',
            'spotify-client': 'spotify',
            'audacity': 'audacity',
            'gimp': 'gimp',
            'inkscape': 'inkscape',
            'blender': 'blender',
            'obs-studio': 'obs',
            
            # System tools
            'htop': 'htop',
            'neofetch': 'neofetch',
            'tree': 'tree',
            'tmux': 'tmux',
            'zsh': 'zsh',
            'fish': 'fish',
            'kitty': 'kitty',
            'alacritty': 'alacritty',
            'terminator': 'terminator',
            
            # Security tools
            'keepassxc': 'keepassxc',
            'bitwarden': 'bitwarden',
            'rkhunter': 'rkhunter',
            'clamav': 'clamav',
            'ufw': 'ufw',
            'fail2ban': 'fail2ban',
            
            # Container/Cloud tools
            'kubectl': 'kubectl',
            'helm': 'helm',
            'terraform': 'terraform',
            'ansible': 'ansible',
            'vagrant': 'vagrant',
            'virtualbox': 'virtualbox',
            
            # Database tools
            'postgresql': 'postgresql',
            'postgresql-client': 'postgresql-client',
            'mysql-server': 'mysql',
            'mysql-client': 'mysql-client',
            'mongodb': 'mongodb',
            'redis-server': 'redis',
            'sqlite3': 'sqlite',
        }
    
    def get_installed_packages(self) -> Dict[str, Dict]:
        """Get all installed packages with metadata"""
        packages = {}
        
        try:
            # Use dpkg-query to get installed packages
            cmd = ["dpkg-query", "-W", "-f=${binary:Package}|${Version}|${Status}|${Installed-Size}\n"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                parts = line.split('|')
                if len(parts) >= 3:
                    package = parts[0]
                    version = parts[1]
                    status = parts[2]
                    size = parts[3] if len(parts) > 3 else '0'
                    
                    # Only include properly installed packages
                    if 'install ok installed' in status:
                        packages[package] = {
                            'version': version,
                            'status': 'installed',
                            'size': size,
                            'menu_id': self.package_to_menu_map.get(package)
                        }
                        
        except subprocess.CalledProcessError as e:
            print(f"Error getting installed packages: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        self.installed_packages = packages
        return packages
    
    def get_installed_snaps(self) -> Dict[str, Dict]:
        """Get installed snap packages"""
        snaps = {}
        
        try:
            cmd = ["snap", "list", "--format=json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            snap_data = json.loads(result.stdout)
            
            for snap in snap_data:
                name = snap.get('name', '')
                snaps[name] = {
                    'version': snap.get('version', ''),
                    'revision': snap.get('revision', ''),
                    'channel': snap.get('channel', ''),
                    'publisher': snap.get('publisher', ''),
                    'menu_id': self.package_to_menu_map.get(name)
                }
                
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            # Snap might not be installed or available
            pass
        except Exception:
            pass
            
        return snaps
    
    def get_installed_flatpaks(self) -> Dict[str, Dict]:
        """Get installed flatpak packages"""
        flatpaks = {}
        
        try:
            cmd = ["flatpak", "list", "--app", "--columns=application,version,branch"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            for line in result.stdout.strip().split('\n'):
                if not line or line.startswith('Application'):
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 2:
                    app_id = parts[0]
                    version = parts[1] if len(parts) > 1 else ''
                    branch = parts[2] if len(parts) > 2 else ''
                    
                    # Extract simple name from app ID (e.g., org.mozilla.firefox -> firefox)
                    simple_name = app_id.split('.')[-1].lower()
                    
                    flatpaks[app_id] = {
                        'version': version,
                        'branch': branch,
                        'simple_name': simple_name,
                        'menu_id': self.package_to_menu_map.get(simple_name)
                    }
                    
        except subprocess.CalledProcessError:
            # Flatpak might not be installed
            pass
        except Exception:
            pass
            
        return flatpaks
    
    def map_to_menu_items(self, menu_items: List[str]) -> Dict[str, str]:
        """Map installed packages to menu item selections
        
        Returns:
            Dict mapping menu_item_id to installation status:
            'installed' - package is installed
            'not_installed' - package is not installed
            'partial' - some components installed (for groups)
        """
        status_map = {}
        installed = self.get_installed_packages()
        snaps = self.get_installed_snaps()
        flatpaks = self.get_installed_flatpaks()
        
        for item_id in menu_items:
            # Check if this menu item corresponds to any installed package
            installed_as = []
            
            # Check regular packages
            for pkg_name, pkg_info in installed.items():
                if pkg_info.get('menu_id') == item_id:
                    installed_as.append(('apt', pkg_name))
                    
            # Check snaps
            for snap_name, snap_info in snaps.items():
                if snap_info.get('menu_id') == item_id or snap_name == item_id:
                    installed_as.append(('snap', snap_name))
                    
            # Check flatpaks
            for flatpak_id, flatpak_info in flatpaks.items():
                if flatpak_info.get('menu_id') == item_id or flatpak_info.get('simple_name') == item_id:
                    installed_as.append(('flatpak', flatpak_id))
                    
            if installed_as:
                status_map[item_id] = 'installed'
            else:
                status_map[item_id] = 'not_installed'
                
        return status_map
    
    def save_system_state(self) -> None:
        """Save current system state to file"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'packages': self.get_installed_packages(),
            'snaps': self.get_installed_snaps(),
            'flatpaks': self.get_installed_flatpaks()
        }
        
        try:
            with open(self.state_file, 'w') as f:
                yaml.dump(state, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving system state: {e}")
    
    def load_system_state(self) -> Optional[Dict]:
        """Load previously saved system state"""
        if not Path(self.state_file).exists():
            return None
            
        try:
            with open(self.state_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading system state: {e}")
            return None
    
    def get_managed_packages(self) -> Set[str]:
        """Get list of packages that Ubootu explicitly installed"""
        if not Path(self.managed_file).exists():
            return set()
            
        try:
            with open(self.managed_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                return set(data.get('managed_packages', []))
        except Exception:
            return set()
    
    def add_managed_package(self, package: str) -> None:
        """Add a package to the managed list"""
        managed = self.get_managed_packages()
        managed.add(package)
        
        try:
            with open(self.managed_file, 'w') as f:
                yaml.dump({'managed_packages': list(managed)}, f)
        except Exception as e:
            print(f"Error updating managed packages: {e}")
    
    def remove_managed_package(self, package: str) -> None:
        """Remove a package from the managed list"""
        managed = self.get_managed_packages()
        managed.discard(package)
        
        try:
            with open(self.managed_file, 'w') as f:
                yaml.dump({'managed_packages': list(managed)}, f)
        except Exception as e:
            print(f"Error updating managed packages: {e}")
    
    def get_package_dependencies(self, package: str) -> Set[str]:
        """Get dependencies of a package"""
        deps = set()
        
        try:
            cmd = ["apt-cache", "depends", package]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            for line in result.stdout.split('\n'):
                if 'Depends:' in line:
                    dep = line.split('Depends:')[1].strip()
                    # Remove version constraints
                    dep = re.sub(r'[<>=].*', '', dep).strip()
                    deps.add(dep)
                    
        except subprocess.CalledProcessError:
            pass
            
        return deps
    
    def is_safe_to_remove(self, package: str) -> Tuple[bool, str]:
        """Check if a package is safe to remove
        
        Returns:
            Tuple of (is_safe, reason)
        """
        # Never remove essential system packages
        NEVER_REMOVE = {
            'ubuntu-desktop', 'ubuntu-minimal', 'ubuntu-standard',
            'systemd', 'systemd-sysv', 'init', 
            'linux-image-generic', 'linux-headers-generic',
            'grub-pc', 'grub-efi', 'grub2-common',
            'network-manager', 'networkd-dispatcher',
            'apt', 'dpkg', 'bash', 'dash', 'coreutils'
        }
        
        if package in NEVER_REMOVE:
            return (False, f"{package} is an essential system package")
        
        # Check if package has reverse dependencies
        try:
            cmd = ["apt-cache", "rdepends", package]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            rdeps = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('Reverse Depends:') and not line.startswith(package):
                    # Skip virtual packages
                    if not line.startswith('|'):
                        rdeps.append(line.strip())
            
            if rdeps:
                return (False, f"Other packages depend on {package}: {', '.join(rdeps[:3])}")
                
        except subprocess.CalledProcessError:
            pass
        
        # Check if it was manually installed (not by Ubootu)
        if package not in self.get_managed_packages():
            return (False, f"{package} was not installed by Ubootu")
        
        return (True, "Safe to remove")
    
    def get_orphaned_packages(self, config_selections: List[str]) -> Dict[str, Dict]:
        """Find packages installed but not in current config
        
        Args:
            config_selections: List of menu item IDs from current config
            
        Returns:
            Dict of orphaned packages with metadata
        """
        orphaned = {}
        installed = self.get_installed_packages()
        
        # Build set of expected packages from config
        expected = set()
        for item_id in config_selections:
            # Reverse map from menu ID to package names
            for pkg_name, menu_id in self.package_to_menu_map.items():
                if menu_id == item_id:
                    expected.add(pkg_name)
        
        # Find installed packages not in expected
        for pkg_name, pkg_info in installed.items():
            if pkg_name not in expected and pkg_info.get('menu_id'):
                is_safe, reason = self.is_safe_to_remove(pkg_name)
                orphaned[pkg_name] = {
                    'menu_id': pkg_info['menu_id'],
                    'version': pkg_info['version'],
                    'safe_to_remove': is_safe,
                    'reason': reason,
                    'managed_by_ubootu': pkg_name in self.get_managed_packages()
                }
        
        return orphaned


if __name__ == '__main__':
    # Test the discovery module
    discovery = SystemDiscovery()
    
    print("Scanning system packages...")
    packages = discovery.get_installed_packages()
    print(f"Found {len(packages)} installed packages")
    
    # Show packages that map to menu items
    mapped = [p for p, info in packages.items() if info.get('menu_id')]
    print(f"\nPackages with menu mappings: {len(mapped)}")
    for pkg in mapped[:10]:
        info = packages[pkg]
        print(f"  {pkg} -> {info['menu_id']} (v{info['version']})")
    
    # Check snaps
    snaps = discovery.get_installed_snaps()
    if snaps:
        print(f"\nFound {len(snaps)} installed snaps")
        for name, info in list(snaps.items())[:5]:
            print(f"  {name} v{info['version']}")
    
    # Save state
    discovery.save_system_state()
    print("\nSystem state saved to .ubootu_system_state.yml")