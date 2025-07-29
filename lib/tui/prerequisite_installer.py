#!/usr/bin/env python3
"""
TUI-based prerequisite installer
Handles all setup tasks within the curses interface
"""

import curses
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional

from .sudo_dialog import SudoDialog
from .progress_dialog import ProgressDialog
from .dialogs import MessageDialog, ConfirmDialog
from .utils import draw_box, draw_centered_text


class PrerequisiteInstaller:
    """Install prerequisites within TUI interface"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.sudo_dialog = SudoDialog(stdscr)
        self.progress_dialog = ProgressDialog(stdscr)
        self.message_dialog = MessageDialog(stdscr)
        self.confirm_dialog = ConfirmDialog(stdscr)
        self.tasks_completed = []
        
    def check_and_install(self) -> bool:
        """Check and install all prerequisites"""
        # First show explanation dialog
        if not self._show_sudo_explanation():
            return False
            
        # Run prerequisite tasks
        tasks = [
            ("Checking Ubuntu version", self._check_ubuntu),
            ("Checking APT health", self._check_apt_health),
            ("Updating package cache", self._update_apt_cache),
            ("Installing Python 3", self._install_python),
            ("Installing Ansible", self._install_ansible),
            ("Installing Python packages", self._install_python_packages),
            ("Installing Ansible collections", self._install_ansible_collections),
        ]
        
        # Show task list
        self._show_task_list(tasks)
        
        # Run each task
        for i, (task_name, task_func) in enumerate(tasks):
            if not self._run_task(i, task_name, task_func):
                self.message_dialog.show(
                    "Installation Failed",
                    f"Failed to complete task: {task_name}\n\n"
                    "Please check the error messages and try again.",
                    "error"
                )
                return False
                
        # Show success message
        self.message_dialog.show(
            "Prerequisites Installed",
            "All prerequisites have been successfully installed!\n\n"
            "Your system is now ready for configuration.",
            "success"
        )
        
        return True
        
    def _show_sudo_explanation(self) -> bool:
        """Show explanation for why sudo is needed"""
        explanation = """Ubootu needs administrator privileges to:

• Install software packages and updates
• Configure system settings and preferences  
• Set up development tools and environments
• Apply security configurations
• Manage system services and permissions

Your password is only used for these system-level changes.
We never store or transmit your password anywhere.

Continue with installation?"""
        
        return self.confirm_dialog.show(
            "Administrator Access Required",
            explanation
        )
        
    def _show_task_list(self, tasks: List[Tuple[str, callable]]):
        """Show list of tasks to be completed"""
        self.stdscr.clear()
        
        # Draw header
        draw_box(self.stdscr, 0, 0, 4, self.width, "🚀 Installing Prerequisites")
        draw_centered_text(self.stdscr, 2, "Preparing your system for Ubootu configuration")
        
        # Draw task list
        list_y = 6
        list_height = min(len(tasks) + 4, self.height - 10)
        list_width = min(60, self.width - 10)
        list_x = (self.width - list_width) // 2
        
        draw_box(self.stdscr, list_y, list_x, list_height, list_width, "Tasks")
        
        for i, (task_name, _) in enumerate(tasks):
            task_y = list_y + 2 + i
            if task_y < list_y + list_height - 2:
                status = "[ ]"  # Will be updated as tasks complete
                self.stdscr.addstr(task_y, list_x + 3, f"{status} {task_name}")
                
        self.stdscr.refresh()
        
    def _run_task(self, index: int, task_name: str, task_func: callable) -> bool:
        """Run a single task and update display"""
        # Update task status to running
        self._update_task_status(index, "running")
        
        # Run the task
        try:
            result = task_func()
            if result:
                self._update_task_status(index, "completed")
                self.tasks_completed.append(task_name)
                return True
            else:
                self._update_task_status(index, "failed")
                return False
        except Exception as e:
            self._update_task_status(index, "failed")
            self.message_dialog.show(
                "Task Failed",
                f"Error in {task_name}:\n{str(e)}",
                "error"
            )
            return False
            
    def _update_task_status(self, index: int, status: str):
        """Update task status in the display"""
        # Calculate position
        list_y = 6
        list_width = min(60, self.width - 10)
        list_x = (self.width - list_width) // 2
        task_y = list_y + 2 + index
        
        # Status symbols
        symbols = {
            "pending": "[ ]",
            "running": "[►]",
            "completed": "[✓]",
            "failed": "[✗]"
        }
        
        # Update display
        if task_y < self.height - 4:
            self.stdscr.addstr(task_y, list_x + 3, symbols.get(status, "[ ]"))
            self.stdscr.refresh()
            
    def _check_ubuntu(self) -> bool:
        """Check Ubuntu version"""
        try:
            result = subprocess.run(
                ['lsb_release', '-rs'],
                capture_output=True,
                text=True
            )
            version = result.stdout.strip()
            
            # Check if supported version
            supported = ["20.04", "22.04", "24.04", "24.10", "25.04"]
            if version in supported:
                return True
            else:
                self.message_dialog.show(
                    "Unsupported Version",
                    f"Ubuntu {version} is not fully supported.\n"
                    "Supported versions: " + ", ".join(supported),
                    "warning"
                )
                return True  # Continue anyway
        except:
            return False
            
    def _check_apt_health(self) -> bool:
        """Check and fix APT configuration"""
        # Run APT fixer
        apt_fixer_path = Path(__file__).parent.parent / "apt_fixer.py"
        
        if apt_fixer_path.exists():
            exit_code = self.progress_dialog.run_command(
                [sys.executable, str(apt_fixer_path)],
                "Checking APT Health",
                show_output=True
            )
            return exit_code == 0
        else:
            # Fallback to basic check
            return self._run_apt_check()
            
    def _run_apt_check(self) -> bool:
        """Basic APT health check"""
        exit_code = self.progress_dialog.run_command(
            ['apt', '--version'],
            "Checking APT",
            show_output=False
        )
        return exit_code == 0
        
    def _update_apt_cache(self) -> bool:
        """Update APT package cache"""
        exit_code = self.progress_dialog.run_command(
            ['sudo', 'apt', 'update'],
            "Updating Package Cache",
            show_output=True,
            sudo_dialog=self.sudo_dialog
        )
        return exit_code == 0
        
    def _install_python(self) -> bool:
        """Install Python 3 if not present"""
        # Check if already installed
        check_result = subprocess.run(
            ['which', 'python3'],
            capture_output=True
        )
        
        if check_result.returncode == 0:
            return True  # Already installed
            
        # Install Python
        exit_code = self.progress_dialog.run_command(
            ['sudo', 'apt', 'install', '-y', 'python3', 'python3-pip', 'python3-venv'],
            "Installing Python 3",
            show_output=True,
            sudo_dialog=self.sudo_dialog
        )
        return exit_code == 0
        
    def _install_ansible(self) -> bool:
        """Install Ansible"""
        # Check if already installed
        check_result = subprocess.run(
            ['which', 'ansible'],
            capture_output=True
        )
        
        if check_result.returncode == 0:
            return True  # Already installed
            
        # Get Ubuntu codename
        codename_result = subprocess.run(
            ['lsb_release', '-cs'],
            capture_output=True,
            text=True
        )
        codename = codename_result.stdout.strip()
        
        # Install based on Ubuntu version
        if codename in ['focal', 'jammy', 'noble']:
            # Add Ansible PPA first
            self.progress_dialog.show_message(
                "Installing Ansible",
                "Adding Ansible PPA repository...",
                wait_for_key=False
            )
            
            exit_code = self.progress_dialog.run_command(
                ['sudo', 'apt', 'install', '-y', 'software-properties-common'],
                "Installing Dependencies",
                show_output=True,
                sudo_dialog=self.sudo_dialog
            )
            
            if exit_code == 0:
                exit_code = self.progress_dialog.run_command(
                    ['sudo', 'apt-add-repository', '--yes', '--update', 'ppa:ansible/ansible'],
                    "Adding Ansible PPA",
                    show_output=True,
                    sudo_dialog=self.sudo_dialog
                )
        
        # Install Ansible
        exit_code = self.progress_dialog.run_command(
            ['sudo', 'apt', 'install', '-y', 'ansible'],
            "Installing Ansible",
            show_output=True,
            sudo_dialog=self.sudo_dialog
        )
        return exit_code == 0
        
    def _install_python_packages(self) -> bool:
        """Install required Python packages"""
        packages = ['pyyaml', 'jinja2', 'rich', 'questionary']
        
        # Try pip3 first, fall back to pip
        pip_cmd = 'pip3' if subprocess.run(['which', 'pip3'], capture_output=True).returncode == 0 else 'pip'
        
        exit_code = self.progress_dialog.run_command(
            [pip_cmd, 'install', '--user'] + packages,
            "Installing Python Packages",
            show_output=True
        )
        return exit_code == 0
        
    def _install_ansible_collections(self) -> bool:
        """Install Ansible collections"""
        requirements_file = Path("requirements.yml")
        
        if not requirements_file.exists():
            return True  # Skip if no requirements file
            
        exit_code = self.progress_dialog.run_command(
            ['ansible-galaxy', 'install', '-r', 'requirements.yml'],
            "Installing Ansible Collections",
            show_output=True
        )
        return exit_code == 0