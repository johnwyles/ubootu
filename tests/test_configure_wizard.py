#!/usr/bin/env python3
"""Tests for the configuration wizard"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configure_wizard import ConfigurationWizard, WizardSection


class TestConfigurationWizard:
    """Test the configuration wizard functionality"""
    
    @pytest.fixture
    def wizard(self):
        """Create a wizard instance for testing"""
        return ConfigurationWizard()
    
    def test_wizard_initialization(self, wizard):
        """Test wizard initializes correctly"""
        assert wizard.config == {}
        assert wizard.current_section == 0
        assert len(wizard.sections) == len(WizardSection)
    
    def test_get_yes_no_default_true(self, wizard):
        """Test yes/no prompt with default true"""
        with patch('builtins.input', return_value=''):
            result = wizard.get_yes_no("Test question?", default=True)
            assert result is True
    
    def test_get_yes_no_default_false(self, wizard):
        """Test yes/no prompt with default false"""
        with patch('builtins.input', return_value=''):
            result = wizard.get_yes_no("Test question?", default=False)
            assert result is False
    
    def test_get_yes_no_explicit_yes(self, wizard):
        """Test yes/no prompt with explicit yes"""
        with patch('builtins.input', return_value='y'):
            result = wizard.get_yes_no("Test question?")
            assert result is True
    
    def test_get_yes_no_explicit_no(self, wizard):
        """Test yes/no prompt with explicit no"""
        with patch('builtins.input', return_value='n'):
            result = wizard.get_yes_no("Test question?")
            assert result is False
    
    def test_get_choice_valid(self, wizard):
        """Test single choice selection"""
        options = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value='2'):
            result = wizard.get_choice("Choose one:", options)
            assert result == 1  # 0-indexed
    
    def test_get_choice_with_default(self, wizard):
        """Test single choice with default"""
        options = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value=''):
            result = wizard.get_choice("Choose one:", options, default=2)
            assert result == 1  # 0-indexed
    
    def test_get_multiple_choices(self, wizard):
        """Test multiple choice selection"""
        options = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value='1,3'):
            result = wizard.get_multiple_choices("Choose multiple:", options)
            assert result == [0, 2]  # 0-indexed
    
    def test_get_multiple_choices_with_all(self, wizard):
        """Test multiple choice with 'all' selection"""
        options = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value='all'):
            result = wizard.get_multiple_choices("Choose multiple:", options)
            assert result == [0, 1, 2]
    
    def test_get_multiple_choices_with_none(self, wizard):
        """Test multiple choice with 'none' selection"""
        options = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value='none'):
            result = wizard.get_multiple_choices("Choose multiple:", options)
            assert result == []
    
    def test_configure_desktop_minimal(self, wizard):
        """Test minimal desktop configuration"""
        with patch('builtins.input', side_effect=['n']):
            wizard.configure_desktop()
            assert wizard.config['install_desktop_environment'] is False
    
    def test_configure_desktop_full(self, wizard):
        """Test full desktop configuration"""
        with patch('builtins.input', side_effect=['y', '2', '1', '2', 'n', 'y', 'bottom', 'natural']):
            wizard.configure_desktop()
            assert wizard.config['install_desktop_environment'] is True
            assert wizard.config['desktop_environment'] == 'kde'
            assert wizard.config['default_browser'] == 'firefox'
            assert wizard.config['terminal_emulator'] == 'konsole'
            assert wizard.config['taskbar_position'] == 'bottom'
            assert wizard.config['trackpad_scroll_direction'] == 'natural'
    
    def test_configure_security_minimal(self, wizard):
        """Test minimal security configuration"""
        with patch('builtins.input', side_effect=['n']):
            wizard.configure_security()
            assert wizard.config['enable_security'] is False
    
    def test_configure_security_full(self, wizard):
        """Test full security configuration"""
        with patch('builtins.input', side_effect=[
            'y',  # Enable security
            'y',  # Enable firewall
            'y',  # Enable fail2ban
            'n',  # Install ClamAV
            'y',  # Enable automatic updates
            'y',  # Configure SSH hardening
            'y',  # Generate SSH keys
            '1',  # KeePassXC
            'n',  # Enable super hardening
        ]):
            wizard.configure_security()
            assert wizard.config['enable_security'] is True
            assert wizard.config['enable_firewall'] is True
            assert wizard.config['enable_fail2ban'] is True
            assert wizard.config['install_clamav'] is False
            assert wizard.config['password_managers'] == ['keepassxc']
    
    def test_configure_security_super_hardening(self, wizard):
        """Test security with super hardening enabled"""
        with patch('builtins.input', side_effect=[
            'y',  # Enable security
            'y',  # Enable firewall
            'y',  # Enable fail2ban
            'n',  # Install ClamAV
            'y',  # Enable automatic updates
            'y',  # Configure SSH hardening
            'y',  # Generate SSH keys
            '1',  # KeePassXC
            'y',  # Enable super hardening
            'n',  # Disable IPv6
            'y',  # Enable USBGuard
            'n',  # Disable kernel modules
            'y',  # Enable process accounting
        ]):
            wizard.configure_security()
            assert wizard.config['enable_super_hardening'] is True
            assert wizard.config['disable_ipv6'] is False
            assert wizard.config['enable_usbguard'] is True
            assert wizard.config['disable_kernel_modules'] is False
            assert wizard.config['enable_process_accounting'] is True
    
    def test_save_configuration(self, wizard, tmp_path):
        """Test saving configuration to file"""
        wizard.config = {
            'test_key': 'test_value',
            'test_list': ['item1', 'item2'],
            'test_bool': True
        }
        
        config_file = tmp_path / "test_config.yml"
        with patch('builtins.input', return_value=str(config_file)):
            wizard.save_configuration()
        
        assert config_file.exists()
        content = config_file.read_text()
        assert 'test_key: test_value' in content
        assert 'test_list:' in content
        assert '- item1' in content
        assert 'test_bool: true' in content


class TestWizardHelpers:
    """Test helper methods"""
    
    def test_clear_screen(self):
        """Test screen clearing"""
        wizard = ConfigurationWizard()
        with patch('os.system') as mock_system:
            wizard.clear_screen()
            mock_system.assert_called_once_with('clear')
    
    def test_print_methods(self, capsys):
        """Test print helper methods"""
        wizard = ConfigurationWizard()
        
        wizard.print_header("Test Header")
        wizard.print_section("Test Section")
        wizard.print_question("Test Question")
        wizard.print_success("Test Success")
        wizard.print_error("Test Error")
        wizard.print_info("Test Info")
        
        captured = capsys.readouterr()
        assert "Test Header" in captured.out
        assert "Test Section" in captured.out
        assert "Test Question" in captured.out
        assert "Test Success" in captured.out
        assert "Test Error" in captured.out
        assert "Test Info" in captured.out