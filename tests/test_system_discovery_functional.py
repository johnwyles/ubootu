#!/usr/bin/env python3
"""
Functional tests for system_discovery module
Tests package detection and system state management
"""

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest
import yaml

from lib.system_discovery import SystemDiscovery


class TestSystemDiscoveryFunctional:
    """Test system discovery functionality"""

    def setup_method(self):
        """Setup test instance"""
        self.discovery = SystemDiscovery()

    def test_init_creates_instance(self):
        """Test SystemDiscovery initialization"""
        discovery = SystemDiscovery()
        assert discovery is not None
        assert discovery.installed_packages == {}
        assert discovery.state_file == ".ubootu_system_state.yml"
        assert discovery.managed_file == ".ubootu_managed.yml"

    def test_package_mapping_contains_common_packages(self):
        """Test that package mapping includes common packages"""
        mapping = self.discovery._build_package_mapping()
        
        # Check common packages
        assert "firefox" in mapping
        assert "docker-ce" in mapping
        assert "git" in mapping
        assert "vim" in mapping
        assert "code" in mapping  # VSCode
        
        # Check mapping values
        assert mapping["firefox"] == "firefox"
        assert mapping["docker-ce"] == "docker"
        assert mapping["code"] == "vscode"

    @patch('subprocess.run')
    def test_get_installed_packages_success(self, mock_run):
        """Test getting installed packages from dpkg"""
        # Mock dpkg output
        mock_run.return_value = MagicMock(
            stdout="firefox|2:120.0+build2-0ubuntu0.22.04.1|install ok installed|45678\n"
                   "git|1:2.34.1-1ubuntu1.10|install ok installed|12345\n"
                   "vim|2:8.2.3995-1ubuntu2.15|install ok installed|3456\n",
            returncode=0
        )
        
        packages = self.discovery.get_installed_packages()
        
        assert len(packages) == 3
        assert "firefox" in packages
        assert packages["firefox"]["version"] == "2:120.0+build2-0ubuntu0.22.04.1"
        assert packages["firefox"]["status"] == "installed"
        assert packages["firefox"]["menu_id"] == "firefox"
        
        assert "git" in packages
        assert packages["git"]["menu_id"] == "git"

    @patch('subprocess.run')
    def test_get_installed_packages_handles_error(self, mock_run):
        """Test handling of dpkg query errors"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'dpkg-query')
        
        packages = self.discovery.get_installed_packages()
        
        assert packages == {}

    @patch('subprocess.run')
    def test_get_installed_snaps_success(self, mock_run):
        """Test getting installed snap packages"""
        snap_data = [
            {
                "name": "code",
                "version": "1.85.1",
                "revision": "148",
                "channel": "stable",
                "publisher": "Microsoft"
            },
            {
                "name": "firefox",
                "version": "120.0.1",
                "revision": "3416",
                "channel": "stable",
                "publisher": "Mozilla"
            }
        ]
        
        mock_run.return_value = MagicMock(
            stdout=json.dumps(snap_data),
            returncode=0
        )
        
        snaps = self.discovery.get_installed_snaps()
        
        assert len(snaps) == 2
        assert "code" in snaps
        assert snaps["code"]["version"] == "1.85.1"
        assert snaps["code"]["menu_id"] == "vscode"
        
        assert "firefox" in snaps
        assert snaps["firefox"]["version"] == "120.0.1"

    @patch('subprocess.run')
    def test_get_installed_snaps_not_installed(self, mock_run):
        """Test when snap is not installed"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'snap')
        
        snaps = self.discovery.get_installed_snaps()
        
        assert snaps == {}

    @patch('subprocess.run')
    def test_get_installed_flatpaks_success(self, mock_run):
        """Test getting installed flatpak packages"""
        mock_run.return_value = MagicMock(
            stdout="Application\tVersion\tBranch\n"
                   "org.mozilla.firefox\t120.0\tstable\n"
                   "com.spotify.Client\t1.2.25.1011\tstable\n",
            returncode=0
        )
        
        flatpaks = self.discovery.get_installed_flatpaks()
        
        assert len(flatpaks) == 2
        assert "org.mozilla.firefox" in flatpaks
        assert flatpaks["org.mozilla.firefox"]["version"] == "120.0"
        assert flatpaks["org.mozilla.firefox"]["simple_name"] == "firefox"
        assert flatpaks["org.mozilla.firefox"]["menu_id"] == "firefox"

    @patch('subprocess.run')
    def test_get_installed_flatpaks_not_installed(self, mock_run):
        """Test when flatpak is not installed"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'flatpak')
        
        flatpaks = self.discovery.get_installed_flatpaks()
        
        assert flatpaks == {}

    @patch.object(SystemDiscovery, 'get_installed_flatpaks')
    @patch.object(SystemDiscovery, 'get_installed_snaps')
    @patch.object(SystemDiscovery, 'get_installed_packages')
    def test_map_to_menu_items(self, mock_packages, mock_snaps, mock_flatpaks):
        """Test mapping installed packages to menu items"""
        mock_packages.return_value = {
            "firefox": {"menu_id": "firefox", "version": "120.0"},
            "git": {"menu_id": "git", "version": "2.34.1"},
            "some-lib": {"menu_id": None, "version": "1.0"}
        }
        mock_snaps.return_value = {
            "code": {"menu_id": "vscode", "version": "1.85.1"}
        }
        mock_flatpaks.return_value = {}
        
        menu_items = ["firefox", "git", "vscode", "chrome", "docker"]
        status_map = self.discovery.map_to_menu_items(menu_items)
        
        assert status_map["firefox"] == "installed"
        assert status_map["git"] == "installed"
        assert status_map["vscode"] == "installed"
        assert status_map["chrome"] == "not_installed"
        assert status_map["docker"] == "not_installed"

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(SystemDiscovery, 'get_installed_flatpaks')
    @patch.object(SystemDiscovery, 'get_installed_snaps')
    @patch.object(SystemDiscovery, 'get_installed_packages')
    def test_save_system_state(self, mock_packages, mock_snaps, mock_flatpaks, mock_file):
        """Test saving system state to file"""
        mock_packages.return_value = {"firefox": {"version": "120.0"}}
        mock_snaps.return_value = {"code": {"version": "1.85.1"}}
        mock_flatpaks.return_value = {}
        
        self.discovery.save_system_state()
        
        mock_file.assert_called_once_with(".ubootu_system_state.yml", "w")
        handle = mock_file()
        
        # Verify yaml.dump was called with the handle
        written_content = handle.write.call_args_list
        assert len(written_content) > 0 or handle.__enter__().write.called

    @patch('pathlib.Path.exists')
    def test_load_system_state_file_not_exists(self, mock_exists):
        """Test loading state when file doesn't exist"""
        mock_exists.return_value = False
        
        state = self.discovery.load_system_state()
        
        assert state is None

    @patch('builtins.open', new_callable=mock_open, read_data="timestamp: '2024-01-01T00:00:00'\npackages:\n  firefox:\n    version: '120.0'\n")
    @patch('pathlib.Path.exists')
    def test_load_system_state_success(self, mock_exists, mock_file):
        """Test loading state from file"""
        mock_exists.return_value = True
        
        state = self.discovery.load_system_state()
        
        assert state is not None
        assert "timestamp" in state
        assert "packages" in state
        assert state["packages"]["firefox"]["version"] == "120.0"

    @patch('builtins.open', new_callable=mock_open, read_data="managed_packages:\n- firefox\n- git\n- vim\n")
    @patch('pathlib.Path.exists')
    def test_get_managed_packages(self, mock_exists, mock_file):
        """Test getting list of managed packages"""
        mock_exists.return_value = True
        
        managed = self.discovery.get_managed_packages()
        
        assert len(managed) == 3
        assert "firefox" in managed
        assert "git" in managed
        assert "vim" in managed

    @patch('pathlib.Path.exists')
    def test_get_managed_packages_no_file(self, mock_exists):
        """Test getting managed packages when file doesn't exist"""
        mock_exists.return_value = False
        
        managed = self.discovery.get_managed_packages()
        
        assert managed == set()

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(SystemDiscovery, 'get_managed_packages')
    def test_add_managed_package(self, mock_get_managed, mock_file):
        """Test adding a package to managed list"""
        mock_get_managed.return_value = {"firefox", "git"}
        
        self.discovery.add_managed_package("vim")
        
        mock_file.assert_called_once_with(".ubootu_managed.yml", "w")

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(SystemDiscovery, 'get_managed_packages')
    def test_remove_managed_package(self, mock_get_managed, mock_file):
        """Test removing a package from managed list"""
        mock_get_managed.return_value = {"firefox", "git", "vim"}
        
        self.discovery.remove_managed_package("vim")
        
        mock_file.assert_called_once_with(".ubootu_managed.yml", "w")

    @patch('subprocess.run')
    def test_get_package_dependencies(self, mock_run):
        """Test getting package dependencies"""
        mock_run.return_value = MagicMock(
            stdout="firefox:\n  Depends: libc6 (>= 2.34)\n  Depends: libgtk-3-0\n  Recommends: xdg-utils\n",
            returncode=0
        )
        
        deps = self.discovery.get_package_dependencies("firefox")
        
        assert "libc6" in deps
        assert "libgtk-3-0" in deps
        assert "xdg-utils" not in deps  # Recommends, not Depends

    def test_is_safe_to_remove_essential_package(self):
        """Test that essential packages are not safe to remove"""
        is_safe, reason = self.discovery.is_safe_to_remove("systemd")
        
        assert is_safe is False
        assert "essential system package" in reason

    @patch.object(SystemDiscovery, 'get_managed_packages')
    @patch('subprocess.run')
    def test_is_safe_to_remove_has_dependencies(self, mock_run, mock_managed):
        """Test package with reverse dependencies is not safe to remove"""
        mock_managed.return_value = {"libgtk-3-0"}
        mock_run.return_value = MagicMock(
            stdout="Reverse Depends:\n  firefox\n  thunderbird\n",
            returncode=0
        )
        
        is_safe, reason = self.discovery.is_safe_to_remove("libgtk-3-0")
        
        assert is_safe is False
        assert "depend on" in reason

    @patch.object(SystemDiscovery, 'get_managed_packages')
    @patch('subprocess.run')
    def test_is_safe_to_remove_not_managed(self, mock_run, mock_managed):
        """Test package not managed by Ubootu is not safe to remove"""
        mock_managed.return_value = {"firefox"}
        mock_run.return_value = MagicMock(
            stdout="Reverse Depends:\n",
            returncode=0
        )
        
        is_safe, reason = self.discovery.is_safe_to_remove("vim")
        
        assert is_safe is False
        assert "not installed by Ubootu" in reason

    @patch.object(SystemDiscovery, 'get_managed_packages')
    @patch('subprocess.run')
    def test_is_safe_to_remove_safe(self, mock_run, mock_managed):
        """Test package that is safe to remove"""
        mock_managed.return_value = {"neofetch"}
        mock_run.return_value = MagicMock(
            stdout="Reverse Depends:\n",
            returncode=0
        )
        
        is_safe, reason = self.discovery.is_safe_to_remove("neofetch")
        
        assert is_safe is True
        assert "Safe to remove" in reason

    @patch.object(SystemDiscovery, 'get_managed_packages')
    @patch.object(SystemDiscovery, 'is_safe_to_remove')
    @patch.object(SystemDiscovery, 'get_installed_packages')
    def test_get_orphaned_packages(self, mock_installed, mock_safe, mock_managed):
        """Test finding orphaned packages"""
        mock_installed.return_value = {
            "firefox": {"menu_id": "firefox", "version": "120.0"},
            "opera-stable": {"menu_id": "opera", "version": "105.0"},
            "git": {"menu_id": "git", "version": "2.34.1"}
        }
        mock_managed.return_value = {"firefox", "opera-stable"}
        mock_safe.return_value = (True, "Safe to remove")
        
        # Config only has firefox and git selected
        config_selections = ["firefox", "git"]
        orphaned = self.discovery.get_orphaned_packages(config_selections)
        
        # Opera should be orphaned (installed but not in config)
        assert "opera-stable" in orphaned
        assert orphaned["opera-stable"]["menu_id"] == "opera"
        assert orphaned["opera-stable"]["safe_to_remove"] is True
        assert orphaned["opera-stable"]["managed_by_ubootu"] is True
        
        # Firefox and git should not be orphaned
        assert "firefox" not in orphaned
        assert "git" not in orphaned

    @patch('subprocess.run')
    def test_get_installed_packages_filters_non_installed(self, mock_run):
        """Test that only properly installed packages are included"""
        mock_run.return_value = MagicMock(
            stdout="firefox|120.0|install ok installed|45678\n"
                   "broken-pkg|1.0|deinstall ok config-files|1234\n"
                   "git|2.34.1|install ok installed|12345\n",
            returncode=0
        )
        
        packages = self.discovery.get_installed_packages()
        
        assert len(packages) == 2
        assert "firefox" in packages
        assert "git" in packages
        assert "broken-pkg" not in packages

    @patch('subprocess.run')
    def test_get_installed_snaps_handles_json_error(self, mock_run):
        """Test handling of invalid JSON from snap list"""
        mock_run.return_value = MagicMock(
            stdout="not valid json",
            returncode=0
        )
        
        snaps = self.discovery.get_installed_snaps()
        
        assert snaps == {}

    @patch('subprocess.run')
    def test_get_installed_flatpaks_skips_header(self, mock_run):
        """Test that flatpak list header is skipped"""
        mock_run.return_value = MagicMock(
            stdout="Application\tVersion\tBranch\n"
                   "Application\tVersion\tBranch\n"  # Duplicate header
                   "org.mozilla.firefox\t120.0\tstable\n",
            returncode=0
        )
        
        flatpaks = self.discovery.get_installed_flatpaks()
        
        assert len(flatpaks) == 1
        assert "org.mozilla.firefox" in flatpaks