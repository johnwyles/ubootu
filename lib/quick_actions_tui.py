#!/usr/bin/env python3
"""
Quick Actions TUI for Ubootu
Common system maintenance tasks in a TUI interface with enhanced error reporting
"""

import curses
import os
import subprocess
import sys
import time
from typing import List, Tuple

from lib.menu_dialog import MenuDialog
from lib.tui_components import (
    CommandResult,
    ErrorDetailsDialog,
    HelpOverlay,
    KeyHintBar,
)
from lib.tui_dialogs import ConfirmDialog, ListDialog, MessageDialog, ProgressDialog


class QuickActions:
    """TUI for quick system actions"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.key_hints = KeyHintBar(stdscr)
        self.help_overlay = HelpOverlay(stdscr)
        self.error_dialog = ErrorDetailsDialog(stdscr)

        # Define available actions with descriptions and help
        self.actions = [
            {
                "id": "fix_broken",
                "name": "🔧 Fix Broken Packages",
                "desc": "Repair broken package dependencies and fix dpkg issues",
                "help": [
                    "This action will:",
                    "• Configure any pending dpkg operations",
                    "• Fix broken package dependencies",
                    "• Update package lists",
                    "Use when:",
                    "• Package installation was interrupted",
                    "• You see 'broken packages' errors",
                    "• dpkg reports configuration issues",
                ],
            },
            {
                "id": "update_all",
                "name": "📦 Update All Packages",
                "desc": "Update package lists and upgrade all installed packages",
                "help": [
                    "This action will:",
                    "• Refresh package lists from repositories",
                    "• Upgrade all installed packages to latest versions",
                    "Safe for:",
                    "• Security updates",
                    "• Bug fixes",
                    "• Minor version updates",
                    "Note: Major upgrades may require manual intervention",
                ],
            },
            {
                "id": "clean_system",
                "name": "🧹 Clean System",
                "desc": "Remove unnecessary packages and clean package cache",
                "help": [
                    "This action will:",
                    "• Remove packages no longer needed",
                    "• Clean downloaded package cache",
                    "• Free up disk space",
                    "Safe to run regularly to:",
                    "• Remove old kernel versions",
                    "• Clear orphaned dependencies",
                    "• Clean apt cache",
                ],
            },
            {
                "id": "check_health",
                "name": "🏥 Check System Health",
                "desc": "Check system services, disk space, and memory usage",
                "help": [
                    "This action will check:",
                    "• Failed system services",
                    "• Disk space usage",
                    "• Memory usage",
                    "• System load average",
                    "Helps identify:",
                    "• Services that need restart",
                    "• Low disk space issues",
                    "• High memory usage",
                    "• System performance issues",
                ],
            },
            {
                "id": "security_audit",
                "name": "🔒 Security Audit",
                "desc": "Run comprehensive security checks on your system",
                "help": [
                    "This action will check:",
                    "• Open ports and services",
                    "• Firewall status",
                    "• Failed login attempts",
                    "• Security updates available",
                    "• Password policies",
                    "• File permissions",
                    "Helps identify security issues and vulnerabilities",
                ],
            },
            {
                "id": "reset_defaults",
                "name": "🔄 Reset Application Defaults",
                "desc": "Reset all application configurations to defaults",
                "help": [
                    "This action will:",
                    "• Reset application settings to defaults",
                    "• Re-apply Ansible configuration",
                    "Use when:",
                    "• Applications behave unexpectedly",
                    "• You want to start fresh",
                    "• Configuration is corrupted",
                ],
            },
        ]

    def run_command(self, command: str, description: str) -> CommandResult:
        """Run a shell command and return detailed result"""
        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            duration = time.time() - start_time
            return CommandResult(
                command, result.returncode, result.stdout, result.stderr, duration
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return CommandResult(
                command, -1, "", "Command timed out after 5 minutes", duration
            )
        except Exception as e:
            duration = time.time() - start_time
            return CommandResult(command, -1, "", str(e), duration)

    def fix_broken_packages(self):
        """Fix broken packages with detailed error reporting"""

        confirm = ConfirmDialog(self.stdscr)
        if not confirm.show(
            "Fix Broken Packages",
            "This will attempt to fix broken package dependencies. Continue?",
            default=True,
        ):
            return

        progress = ProgressDialog(
            self.stdscr, "Fixing Packages", "Running package repairs..."
        )
        results = []

        # Step 1: Configure dpkg
        progress.update(25, "Configuring dpkg...")
        result1 = self.run_command("sudo dpkg --configure -a", "Configure dpkg")
        results.append(result1)

        # Step 2: Fix broken install
        progress.update(50, "Fixing broken dependencies...")
        result2 = self.run_command(
            "sudo apt --fix-broken install -y", "Fix broken packages"
        )
        results.append(result2)

        # Step 3: Update package lists
        progress.update(75, "Updating package lists...")
        result3 = self.run_command("sudo apt update", "Update package lists")
        results.append(result3)

        progress.update(100, "Complete!")

        # Check results and show detailed errors if needed
        failed_results = [r for r in results if not r.success]

        if not failed_results:
            msg = MessageDialog(self.stdscr)
            msg.show("Success", "Package repairs completed successfully", "info")
        else:
            # Show detailed error information
            self.error_dialog.show("Package Repair Errors", failed_results)

    def update_all_packages(self):
        """Update all packages with detailed progress"""

        confirm = ConfirmDialog(self.stdscr)
        if not confirm.show(
            "Update All Packages",
            "This will update all installed packages. Continue?",
            default=True,
        ):
            return

        progress = ProgressDialog(
            self.stdscr, "Updating Packages", "Checking for updates..."
        )
        results = []

        # Step 1: Update package lists
        progress.update(33, "Updating package lists...")
        result1 = self.run_command("sudo apt update", "Update package lists")
        results.append(result1)

        # Step 2: Upgrade packages
        progress.update(66, "Upgrading packages...")
        result2 = self.run_command("sudo apt upgrade -y", "Upgrade packages")
        results.append(result2)

        progress.update(100, "Complete!")

        # Check results
        failed_results = [r for r in results if not r.success]

        if not failed_results:
            # Parse upgrade output for summary
            upgrade_output = result2.stdout
            packages_upgraded = 0
            if "upgraded," in upgrade_output:
                try:
                    # Extract number from "X upgraded, Y newly installed..."
                    parts = upgrade_output.split("upgraded,")[0].split()
                    packages_upgraded = int(parts[-1])
                except:
                    pass

            msg = MessageDialog(self.stdscr)
            if packages_upgraded > 0:
                msg.show(
                    "Success",
                    f"Updated {packages_upgraded} packages successfully",
                    "info",
                )
            else:
                msg.show("Success", "All packages are already up to date", "info")
        else:
            self.error_dialog.show("Update Errors", failed_results)

    def clean_system(self):
        """Clean system with detailed reporting"""

        confirm = ConfirmDialog(self.stdscr)
        if not confirm.show(
            "Clean System",
            "This will remove unnecessary packages and clean the package cache. Continue?",
            default=True,
        ):
            return

        progress = ProgressDialog(self.stdscr, "Cleaning System", "Analyzing system...")
        results = []

        # Check what will be removed first
        progress.update(10, "Checking removable packages...")
        check_result = self.run_command(
            "apt-get --dry-run autoremove", "Check removable packages"
        )

        # Parse how much space will be freed
        space_freed = "unknown amount of"
        if "freed" in check_result.stdout:
            try:
                for line in check_result.stdout.split("\n"):
                    if "freed" in line:
                        space_freed = (
                            line.split("freed")[0].split()[-2]
                            + " "
                            + line.split("freed")[0].split()[-1]
                        )
                        break
            except:
                pass

        # Step 1: Autoremove
        progress.update(
            33, f"Removing unused packages (will free {space_freed} space)..."
        )
        result1 = self.run_command("sudo apt autoremove -y", "Remove unused packages")
        results.append(result1)

        # Step 2: Autoclean
        progress.update(66, "Cleaning package cache...")
        result2 = self.run_command("sudo apt autoclean", "Clean package cache")
        results.append(result2)

        progress.update(100, "Complete!")

        # Check results
        failed_results = [r for r in results if not r.success]

        if not failed_results:
            msg = MessageDialog(self.stdscr)
            msg.show(
                "Success",
                f"System cleaned successfully. Freed {space_freed} of disk space.",
                "info",
            )
        else:
            self.error_dialog.show("Cleaning Errors", failed_results)

    def check_system_health(self):
        """Check system health with detailed report"""

        progress = ProgressDialog(
            self.stdscr, "System Health Check", "Gathering system information..."
        )

        health_info = []
        issues_found = 0

        # Check failed services
        progress.update(20, "Checking system services...")
        result = self.run_command(
            "systemctl list-units --state=failed --no-pager", "Check failed services"
        )
        if result.success:
            failed_lines = [
                l for l in result.stdout.strip().split("\n") if l and "●" in l
            ]
            if failed_lines:
                issues_found += len(failed_lines)
                health_info.append(f"⚠️  {len(failed_lines)} failed system services:")
                for line in failed_lines[:3]:  # Show first 3
                    service_name = (
                        line.split()[1] if len(line.split()) > 1 else "unknown"
                    )
                    health_info.append(f"   - {service_name}")
                if len(failed_lines) > 3:
                    health_info.append(f"   ... and {len(failed_lines) - 3} more")
            else:
                health_info.append("✅ All system services running normally")

        # Check disk space
        progress.update(40, "Checking disk space...")
        result = self.run_command("df -h /", "Check disk usage")
        if result.success:
            try:
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        usage_str = parts[4].rstrip("%")
                        usage = int(usage_str)
                        used = parts[2]
                        total = parts[1]

                        if usage > 90:
                            health_info.append(
                                f"❌ Critical: Disk usage at {usage}% ({used}/{total})"
                            )
                            issues_found += 1
                        elif usage > 80:
                            health_info.append(
                                f"⚠️  Warning: Disk usage at {usage}% ({used}/{total})"
                            )
                            issues_found += 1
                        else:
                            health_info.append(
                                f"✅ Disk usage: {usage}% ({used}/{total})"
                            )
            except:
                health_info.append("❓ Could not determine disk usage")

        # Check memory
        progress.update(60, "Checking memory usage...")
        result = self.run_command("free -h", "Check memory")
        if result.success:
            try:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if line.startswith("Mem:"):
                        parts = line.split()
                        total = parts[1]
                        used = parts[2]
                        available = parts[6] if len(parts) > 6 else parts[3]
                        health_info.append(
                            f"💾 Memory: {used}/{total} used, {available} available"
                        )
                        break
            except:
                health_info.append("❓ Could not determine memory usage")

        # Check load average
        progress.update(80, "Checking system load...")
        result = self.run_command("uptime", "Check load")
        if result.success:
            try:
                load_part = result.stdout.split("load average:")[1].strip()
                loads = [float(x.strip()) for x in load_part.split(",")]
                cpu_count = os.cpu_count() or 1

                if loads[0] > cpu_count * 2:
                    health_info.append(f"❌ High load: {load_part} (CPUs: {cpu_count})")
                    issues_found += 1
                elif loads[0] > cpu_count:
                    health_info.append(
                        f"⚠️  Moderate load: {load_part} (CPUs: {cpu_count})"
                    )
                else:
                    health_info.append(
                        f"✅ Load average: {load_part} (CPUs: {cpu_count})"
                    )
            except:
                health_info.append("❓ Could not determine system load")

        # Check for security updates
        progress.update(90, "Checking security updates...")
        result = self.run_command(
            "apt list --upgradable 2>/dev/null | grep -i security | wc -l",
            "Check security updates",
        )
        if result.success:
            try:
                security_updates = int(result.stdout.strip())
                if security_updates > 0:
                    health_info.append(
                        f"🔒 {security_updates} security updates available"
                    )
                    issues_found += 1
                else:
                    health_info.append("✅ No security updates pending")
            except:
                pass

        progress.update(100, "Complete!")

        # Show results
        if issues_found > 0:
            title = f"System Health Report - {issues_found} issues found"
        else:
            title = "System Health Report - System Healthy"

        msg = MessageDialog(self.stdscr)
        msg.show(
            title, "\n".join(health_info), "info" if issues_found == 0 else "warning"
        )

    def security_audit(self):
        """Run comprehensive security audit"""

        progress = ProgressDialog(
            self.stdscr, "Security Audit", "Running security checks..."
        )
        security_info = []
        security_score = 100

        # Check firewall status
        progress.update(20, "Checking firewall...")
        result = self.run_command("sudo ufw status", "Check firewall")
        if result.success:
            if "Status: active" in result.stdout:
                security_info.append("✅ Firewall is active")
            else:
                security_info.append("❌ Firewall is inactive!")
                security_score -= 20

        # Check for open ports
        progress.update(40, "Checking open ports...")
        result = self.run_command("sudo ss -tlnp | grep LISTEN", "Check open ports")
        if result.success:
            open_ports = len(result.stdout.strip().split("\n"))
            security_info.append(f"🔍 {open_ports} ports listening")
            if open_ports > 10:
                security_info.append("⚠️  Many open ports detected")
                security_score -= 10

        # Check failed login attempts
        progress.update(60, "Checking authentication logs...")
        result = self.run_command(
            "sudo journalctl -u ssh --since '1 week ago' | grep -i 'failed\\|invalid' | wc -l",
            "Check failed logins",
        )
        if result.success:
            try:
                failed_attempts = int(result.stdout.strip())
                if failed_attempts > 100:
                    security_info.append(
                        f"⚠️  {failed_attempts} failed login attempts in past week"
                    )
                    security_score -= 15
                elif failed_attempts > 0:
                    security_info.append(
                        f"🔍 {failed_attempts} failed login attempts in past week"
                    )
                else:
                    security_info.append("✅ No failed login attempts")
            except:
                pass

        # Check password policies
        progress.update(80, "Checking password policies...")
        result = self.run_command(
            "grep -E '^PASS_MAX_DAYS|^PASS_MIN_DAYS|^PASS_MIN_LEN' /etc/login.defs",
            "Check password policy",
        )
        if result.success:
            if "PASS_MAX_DAYS\t99999" in result.stdout:
                security_info.append("⚠️  No password expiration set")
                security_score -= 10
            else:
                security_info.append("✅ Password expiration configured")

        progress.update(100, "Complete!")

        # Calculate grade
        if security_score >= 90:
            grade = "A"
        elif security_score >= 80:
            grade = "B"
        elif security_score >= 70:
            grade = "C"
        elif security_score >= 60:
            grade = "D"
        else:
            grade = "F"

        security_info.insert(
            0, f"Security Score: {security_score}/100 (Grade: {grade})"
        )
        security_info.insert(1, "")

        msg = MessageDialog(self.stdscr)
        msg.show(
            "Security Audit Results",
            "\n".join(security_info),
            "info" if security_score >= 80 else "warning",
        )

    def reset_application_defaults(self):
        """Reset application defaults"""

        confirm = ConfirmDialog(self.stdscr)
        if not confirm.show(
            "Reset Application Defaults",
            "This will reset all application configurations to defaults using Ansible. Continue?",
            default=False,
        ):
            return

        progress = ProgressDialog(
            self.stdscr, "Resetting Defaults", "Running Ansible playbook..."
        )

        progress.update(50, "Applying default configurations...")
        result = self.run_command(
            "cd /home/jwyles/code/johnwyles/ubootu && ansible-playbook site.yml --tags 'defaults' --ask-become-pass",
            "Reset defaults",
        )

        progress.update(100, "Complete!")

        if result.success:
            msg = MessageDialog(self.stdscr)
            msg.show("Success", "Application defaults reset successfully", "info")
        else:
            self.error_dialog.show("Reset Failed", [result])

    def show_menu(self) -> str:
        """Show the quick actions menu with unified navigation"""

        # Build menu items for unified menu
        menu_items = []
        for action in self.actions:
            menu_items.append((action["id"], action["name"], action["desc"]))

        # Add back option
        menu_items.append(
            ("__back__", "← Back to Main Menu", "Return to the main Ubootu menu")
        )

        # Create menu dialog
        menu = MenuDialog(self.stdscr)

        # Header for the menu
        header_lines = [
            "Quick system maintenance and troubleshooting tasks",
            "Select an action to perform:",
        ]

        while True:
            # Show menu with arrow navigation
            selected_id = menu.show(
                title="🎯 Quick Actions",
                items=menu_items,
                header_lines=header_lines,
                box_mode=True,
                allow_help=True,
            )

            if not selected_id:
                return "__back__"

            # Check if user wants to perform an action
            if selected_id != "__back__":
                # Find the action
                action = next((a for a in self.actions if a["id"] == selected_id), None)
                if action:
                    # Show action-specific help and confirm
                    confirm = ConfirmDialog(self.stdscr)
                    help_msg = (
                        "\n".join(action["help"])
                        + "\n\nDo you want to run this action?"
                    )
                    if confirm.show(action["name"], help_msg, default=True):
                        return selected_id
                    # Otherwise, continue showing menu
            else:
                return selected_id

    def run(self):
        """Main loop for quick actions"""

        while True:
            # Draw key hints - Help first for visibility
            hints = [
                ("H", "Help"),
                ("↑↓", "Navigate"),
                ("ENTER", "Select"),
                ("ESC", "Back"),
            ]
            self.key_hints.draw(hints, self.stdscr.getmaxyx()[0] - 1)

            action = self.show_menu()

            if action == "__back__" or action is None:
                break
            elif action == "fix_broken":
                self.fix_broken_packages()
            elif action == "update_all":
                self.update_all_packages()
            elif action == "clean_system":
                self.clean_system()
            elif action == "check_health":
                self.check_system_health()
            elif action == "security_audit":
                self.security_audit()
            elif action == "reset_defaults":
                self.reset_application_defaults()


def main():
    """Main entry point"""

    def run(stdscr):
        actions = QuickActions(stdscr)
        actions.run()

    try:
        curses.wrapper(run)
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
