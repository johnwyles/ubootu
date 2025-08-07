#!/usr/bin/env python3
"""
Tests for security tools categories and organization
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

# Mock curses before importing
sys.modules["curses"] = MagicMock()
import curses

# Set up minimal curses constants
curses.A_REVERSE = 262144
curses.error = Exception


class TestSecurityTools(unittest.TestCase):
    """Test security tools categorization"""

    def setUp(self):
        """Set up test fixtures"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

        # Import after mocking
        from lib.tui.menu_items import load_menu_structure
        from lib.tui.unified_menu import UnifiedMenu

        self.UnifiedMenu = UnifiedMenu
        self.load_menu_structure = load_menu_structure

    def test_security_testing_category_exists(self):
        """Test that security testing category exists with proper structure"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        sec_test = next((item for item in menu.items if item["id"] == "security-testing"), None)
        self.assertIsNotNone(sec_test, "Security Testing category not found")
        self.assertEqual(sec_test["parent"], None)  # Root level
        self.assertEqual(sec_test.get("icon"), "🔐")
        self.assertIn("testing", sec_test["description"].lower())

    def test_security_subcategories(self):
        """Test security testing has required subcategories"""
        required_subcats = [
            ("network-security", "Network Security"),
            ("web-security", "Web Security"),
            ("password-tools", "Password Tools"),
            ("wireless-security", "Wireless Security"),
            ("forensics", "Digital Forensics"),
            ("vulnerability-scanners", "Vulnerability Scanners"),
            ("privacy-tools", "Privacy Tools"),
        ]

        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        for subcat_id, expected_label in required_subcats:
            item = next((i for i in menu.items if i["id"] == subcat_id), None)
            self.assertIsNotNone(item, f"Missing security subcategory: {subcat_id}")
            self.assertEqual(item["parent"], "security-testing")
            self.assertIn(expected_label.split()[0].lower(), item["label"].lower())

    def test_security_tools_have_warnings(self):
        """Test that security tools have appropriate warnings"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        # List of tools that should have security warnings
        security_tools = [
            "nmap",
            "wireshark",
            "john",
            "hashcat",
            "aircrack-ng",
            "metasploit",
            "burp-suite",
            "sqlmap",
            "hydra",
        ]

        for tool_id in security_tools:
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            if tool:  # Only check if tool exists
                help_text = tool.get("help", "").lower()
                # Should mention authorization, permission, or legal use
                self.assertTrue(
                    any(word in help_text for word in ["authorized", "permission", "legal", "warning"]),
                    f"Tool {tool_id} missing security warning in help text",
                )

    def test_network_security_tools(self):
        """Test network security tools are properly categorized"""
        expected_tools = {
            "nmap": "Network scanner",
            "wireshark": "Packet analyzer",
            "tcpdump": "Command-line packet analyzer",
            "netcat": "Network utility",
            "masscan": "Port scanner",
        }

        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        for tool_id, expected_desc in expected_tools.items():
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            self.assertIsNotNone(tool, f"Network security tool {tool_id} not found")
            self.assertEqual(tool["parent"], "network-security")
            self.assertIn(expected_desc.split()[0].lower(), tool["description"].lower())

    def test_web_security_tools(self):
        """Test web security tools are properly categorized"""
        expected_tools = {
            "burp-suite": "Web vulnerability scanner",
            "owasp-zap": "Web app security scanner",
            "sqlmap": "SQL injection tool",
            "nikto": "Web server scanner",
            "dirbuster": "Directory/file brute forcer",
        }

        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        for tool_id, expected_desc in expected_tools.items():
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            if tool:  # Only check if tool exists (some may not be implemented yet)
                self.assertEqual(tool["parent"], "web-security")

    def test_password_tools(self):
        """Test password cracking tools are properly categorized"""
        expected_tools = ["john", "hashcat", "hydra", "crackmap-exec"]

        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        for tool_id in expected_tools:
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            if tool:  # Only check if tool exists
                self.assertEqual(tool["parent"], "password-tools")
                # Should have strong security warning
                help_text = tool.get("help", "").lower()
                self.assertTrue(
                    any(word in help_text for word in ["authorization", "authorized", "permission", "warning"]),
                    f"Tool {tool_id} missing security warning",
                )

    def test_privacy_tools_separate_from_security_testing(self):
        """Test that privacy tools for defense are separate from testing tools"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        # Privacy defense tools should be under main security category
        privacy_defense_tools = ["keepassxc", "veracrypt", "tor-browser", "protonvpn"]

        for tool_id in privacy_defense_tools:
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            if tool:
                # Should NOT be under security-testing
                parent = tool["parent"]
                self.assertNotEqual(parent, "security-testing", f"{tool_id} should not be under security-testing")
                # Should be under main security or privacy-tools
                self.assertIn(parent, ["security", "privacy-tools"])

    def test_forensics_tools(self):
        """Test digital forensics tools"""
        expected_tools = ["autopsy", "volatility", "foremost", "binwalk"]

        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        for tool_id in expected_tools:
            tool = next((item for item in menu.items if item["id"] == tool_id), None)
            if tool:
                self.assertEqual(tool["parent"], "forensics")

    def test_security_categories_have_descriptions(self):
        """Test all security categories have helpful descriptions"""
        menu = self.UnifiedMenu(self.stdscr)
        menu.load_menu_structure()

        security_categories = [
            "security-testing",
            "network-security",
            "web-security",
            "password-tools",
            "wireless-security",
            "forensics",
            "vulnerability-scanners",
        ]

        for cat_id in security_categories:
            cat = next((item for item in menu.items if item["id"] == cat_id), None)
            if cat:
                self.assertTrue(len(cat.get("description", "")) > 10, f"Category {cat_id} has insufficient description")


if __name__ == "__main__":
    unittest.main()
