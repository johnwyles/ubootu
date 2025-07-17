#!/usr/bin/env python3
"""
Profile management system for Ubuntu Bootstrap
Handles saving, loading, and version control of configurations
"""

import os
import yaml
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class ProfileManager:
    """Manages configuration profiles with Git integration"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or os.path.expanduser("~/.config/ubuntu-bootstrap"))
        self.profiles_dir = self.base_dir / "profiles"
        self.backups_dir = self.base_dir / "backups"
        self.current_config = self.profiles_dir / "current.yml"
        self.templates_dir = self.profiles_dir / "templates"
        self.saved_dir = self.profiles_dir / "saved"
        
        # Ensure directories exist
        self._init_directories()
        
        # Initialize Git if not already done
        self._init_git()
        
    def _init_directories(self):
        """Create required directory structure"""
        dirs = [
            self.base_dir,
            self.profiles_dir,
            self.backups_dir,
            self.templates_dir,
            self.saved_dir
        ]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _init_git(self):
        """Initialize Git repository if not exists"""
        git_dir = self.base_dir / ".git"
        if not git_dir.exists():
            subprocess.run(
                ["git", "init"],
                cwd=self.base_dir,
                capture_output=True
            )
            # Create initial .gitignore
            gitignore = self.base_dir / ".gitignore"
            gitignore.write_text("*.log\n*.tmp\n.DS_Store\n")
            
            # Initial commit
            subprocess.run(["git", "add", "."], cwd=self.base_dir)
            subprocess.run(
                ["git", "commit", "-m", "Initial Ubuntu Bootstrap configuration"],
                cwd=self.base_dir,
                capture_output=True
            )
            
    def save_profile(self, config: Dict[str, Any], name: str = None, 
                    commit_message: str = None) -> str:
        """Save configuration profile with Git tracking"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Backup current config if exists
        if self.current_config.exists():
            backup_path = self.backups_dir / f"backup_{timestamp}.yml"
            shutil.copy2(self.current_config, backup_path)
            
        # Save as current config
        with open(self.current_config, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
        # Save named profile if requested
        if name:
            named_path = self.saved_dir / f"{name}.yml"
            with open(named_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
                
        # Git commit
        subprocess.run(["git", "add", "."], cwd=self.base_dir)
        message = commit_message or f"Update configuration - {timestamp}"
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return str(self.current_config)
        
    def load_profile(self, name: str = None) -> Dict[str, Any]:
        """Load a configuration profile"""
        if name:
            # Load named profile
            profile_path = self.saved_dir / f"{name}.yml"
            if not profile_path.exists():
                # Check templates
                profile_path = self.templates_dir / f"{name}.yml"
                if not profile_path.exists():
                    raise FileNotFoundError(f"Profile '{name}' not found")
        else:
            # Load current profile
            profile_path = self.current_config
            if not profile_path.exists():
                return {}
                
        with open(profile_path, 'r') as f:
            return yaml.safe_load(f) or {}
            
    def list_profiles(self) -> Dict[str, List[str]]:
        """List all available profiles"""
        profiles = {
            "saved": [],
            "templates": [],
            "backups": []
        }
        
        # List saved profiles
        for f in self.saved_dir.glob("*.yml"):
            profiles["saved"].append(f.stem)
            
        # List template profiles
        for f in self.templates_dir.glob("*.yml"):
            profiles["templates"].append(f.stem)
            
        # List backups
        for f in self.backups_dir.glob("*.yml"):
            profiles["backups"].append(f.name)
            
        return profiles
        
    def get_profile_info(self, name: str) -> Dict[str, Any]:
        """Get information about a profile"""
        profile_path = None
        
        # Check saved profiles first
        saved_path = self.saved_dir / f"{name}.yml"
        if saved_path.exists():
            profile_path = saved_path
        else:
            # Check templates
            template_path = self.templates_dir / f"{name}.yml"
            if template_path.exists():
                profile_path = template_path
                
        if not profile_path:
            raise FileNotFoundError(f"Profile '{name}' not found")
            
        # Get file info
        stat = profile_path.stat()
        
        # Load profile to get summary
        with open(profile_path, 'r') as f:
            config = yaml.safe_load(f) or {}
            
        return {
            "name": name,
            "path": str(profile_path),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "size": stat.st_size,
            "summary": self._generate_summary(config)
        }
        
    def _generate_summary(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of configuration"""
        summary = {
            "desktop_environment": config.get("desktop_environment", "Not set"),
            "themes_enabled": config.get("enable_themes", False),
            "development_tools": config.get("enable_development_tools", False),
            "security_hardening": config.get("enable_security", False),
            "applications_count": len(config.get("applications", {}).get("web_browsers", [])) +
                                len(config.get("applications", {}).get("code_editors", [])) +
                                len(config.get("applications", {}).get("media_apps", []))
        }
        return summary
        
    def diff_profiles(self, profile1: str, profile2: str = None) -> str:
        """Show differences between profiles"""
        # Load profiles
        config1 = self.load_profile(profile1)
        config2 = self.load_profile(profile2) if profile2 else self.load_profile()
        
        # Convert to JSON for diff
        json1 = json.dumps(config1, indent=2, sort_keys=True)
        json2 = json.dumps(config2, indent=2, sort_keys=True)
        
        # Create temp files
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write(json1)
            temp1 = f1.name
            
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write(json2)
            temp2 = f2.name
            
        # Run diff
        result = subprocess.run(
            ["diff", "-u", temp1, temp2],
            capture_output=True,
            text=True
        )
        
        # Cleanup
        os.unlink(temp1)
        os.unlink(temp2)
        
        return result.stdout
        
    def get_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get Git commit history"""
        result = subprocess.run(
            ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%ad|%s", "--date=short"],
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )
        
        history = []
        for line in result.stdout.strip().split('\n'):
            if line:
                commit_hash, date, message = line.split('|', 2)
                history.append({
                    "hash": commit_hash[:8],
                    "date": date,
                    "message": message
                })
                
        return history
        
    def restore_from_commit(self, commit_hash: str) -> bool:
        """Restore configuration from a Git commit"""
        # First, backup current state
        self.save_profile(
            self.load_profile(),
            commit_message=f"Backup before restoring to {commit_hash}"
        )
        
        # Checkout the specific file from commit
        result = subprocess.run(
            ["git", "checkout", commit_hash, "profiles/current.yml"],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def create_branch(self, branch_name: str) -> bool:
        """Create a new Git branch for different machine profiles"""
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def switch_branch(self, branch_name: str) -> bool:
        """Switch to a different Git branch"""
        result = subprocess.run(
            ["git", "checkout", branch_name],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def list_branches(self) -> List[str]:
        """List all Git branches"""
        result = subprocess.run(
            ["git", "branch"],
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )
        
        branches = []
        for line in result.stdout.strip().split('\n'):
            branch = line.strip()
            if branch.startswith('* '):
                branches.append(branch[2:] + " (current)")
            else:
                branches.append(branch)
                
        return branches
        
    def add_remote(self, remote_url: str, name: str = "origin") -> bool:
        """Add a Git remote for syncing"""
        result = subprocess.run(
            ["git", "remote", "add", name, remote_url],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def push_to_remote(self, remote: str = "origin", branch: str = None) -> bool:
        """Push configuration to remote repository"""
        if not branch:
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            branch = result.stdout.strip()
            
        result = subprocess.run(
            ["git", "push", remote, branch],
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def pull_from_remote(self, remote: str = "origin", branch: str = None) -> bool:
        """Pull configuration from remote repository"""
        cmd = ["git", "pull", remote]
        if branch:
            cmd.append(branch)
            
        result = subprocess.run(
            cmd,
            cwd=self.base_dir,
            capture_output=True
        )
        
        return result.returncode == 0
        
    def create_template_profiles(self):
        """Create default template profiles"""
        templates = {
            "developer": {
                "desktop_environment": "gnome",
                "enable_themes": True,
                "theme_name": "dracula",
                "enable_development_tools": True,
                "code_editors": ["vscode", "vim"],
                "programming_languages": ["python", "javascript", "go"],
                "development_tools": ["docker", "git", "postman"],
                "enable_security": True,
                "password_managers": ["bitwarden"],
                "terminal_emulator": "gnome-terminal",
                "primary_user_shell": "zsh"
            },
            "minimal": {
                "desktop_environment": "xfce",
                "enable_themes": False,
                "enable_development_tools": False,
                "enable_applications": True,
                "web_browsers": ["firefox"],
                "enable_security": True,
                "enable_automatic_updates": True
            },
            "security": {
                "desktop_environment": "gnome",
                "enable_security": True,
                "enable_super_hardening": True,
                "enable_security_tools": True,
                "password_managers": ["keepassxc", "bitwarden"],
                "security_tools": ["nmap", "wireshark", "metasploit"],
                "enable_firewall": True,
                "enable_fail2ban": True,
                "enable_automatic_updates": True
            },
            "creative": {
                "desktop_environment": "kde",
                "enable_themes": True,
                "enable_applications": True,
                "media_apps": ["gimp", "inkscape", "blender", "kdenlive"],
                "enable_development_tools": False,
                "install_gaming_tools": False
            }
        }
        
        for name, config in templates.items():
            template_path = self.templates_dir / f"{name}.yml"
            if not template_path.exists():
                with open(template_path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)


# Helper function for external use
def get_profile_manager(base_dir: str = None):
    """Factory function to create ProfileManager instance"""
    return ProfileManager(base_dir)