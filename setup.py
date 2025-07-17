#!/usr/bin/env python3
"""
Ubuntu Bootstrap Setup - Main Entry Point

This is the new Python-based setup script that replaces setup.sh
with better error handling, modularity, and maintainability.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List

# Add lib directory to Python path
lib_path = Path(__file__).parent / 'lib'
sys.path.insert(0, str(lib_path))

try:
    from setup_manager import SetupManager, SetupError
    from config_interface import ConfigurationInterface
    from config_models import BootstrapConfiguration, load_config, create_default_config
    from menu_schema import MenuSchema
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure you're running this script from the project root directory.")
    sys.exit(1)


class WelcomeMenu:
    """Professional welcome menu for setup options"""
    
    def __init__(self):
        self.setup_manager = SetupManager()
    
    def show_welcome(self) -> None:
        """Display welcome message"""
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║                    🐧 Ubuntu Desktop Bootstrap 🐧                ║")
        print("║                                                                  ║")
        print("║                    Transform Your Ubuntu Experience              ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print()
        print("🐧 Welcome to Ubuntu Desktop Bootstrap!")
        print()
        print("This tool will help you set up a personalized Ubuntu desktop")
        print("with your preferred applications and customizations.")
        print()
    
    def show_menu(self) -> int:
        """Show main menu and get user choice"""
        options = [
            "🚀 Fresh Install - Configure a brand new Ubuntu installation",
            "🔧 Modify Setup - Tweak your existing configuration", 
            "📦 Apply Profile - Restore from a saved configuration",
            "💾 Backup Config - Save your current setup",
            "🎯 Quick Setup - Install prerequisites only",
            "🔍 System Check - Verify system compatibility",
            "❓ Help - Get help and documentation",
            "🚪 Exit - See you later!"
        ]
        
        print("What would you like to do?")
        print()
        
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        print()
        
        while True:
            try:
                choice = input("Enter your choice (1-8): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 8:
                    return int(choice)
                else:
                    print("Please enter a number between 1 and 8.")
            except (KeyboardInterrupt, EOFError):
                return 8  # Exit
    
    def handle_choice(self, choice: int) -> bool:
        """Handle user menu choice"""
        try:
            if choice == 1:
                return self._fresh_install()
            elif choice == 2:
                return self._modify_setup()
            elif choice == 3:
                return self._apply_profile()
            elif choice == 4:
                return self._backup_config()
            elif choice == 5:
                return self._quick_setup()
            elif choice == 6:
                return self._system_check()
            elif choice == 7:
                return self._show_help()
            elif choice == 8:
                print("\n👋 Thanks for using Ubuntu Desktop Bootstrap!")
                return False
            else:
                print("Invalid choice")
                return True
        except Exception as e:
            print(f"Error: {e}")
            return True
    
    def _fresh_install(self) -> bool:
        """Handle fresh installation"""
        print("\n🚀 Starting fresh installation...")
        
        # Run system checks and prerequisites first
        if not self.setup_manager.quick_setup():
            print("❌ Prerequisites installation failed")
            return True
        
        # Launch configuration wizard
        print("\n📝 Launching configuration wizard...")
        try:
            # Try to import and run the wizard
            from configure_wizard import ConfigurationWizard
            wizard = ConfigurationWizard()
            if wizard.run():
                print("\n✅ Configuration completed!")
                
                # Ask if user wants to apply the configuration
                apply = input("\nWould you like to apply the configuration now? (y/N): ").strip().lower()
                if apply in ['y', 'yes']:
                    return self._run_ansible()
            else:
                print("\n❌ Configuration cancelled")
        except ImportError:
            print("❌ Configuration wizard not available")
            print("Please run one of the alternative configuration interfaces:")
            print("  - ./configure_interactive.py")
            print("  - ./configure_compact_tui.py")
            print("  - ./configure_hierarchical_tui.py")
        
        return True
    
    def _modify_setup(self) -> bool:
        """Handle setup modification"""
        print("\n🔧 Modifying existing setup...")
        
        # Check if configuration exists
        if not self.setup_manager.config_manager.has_configuration():
            print("❌ No existing configuration found")
            print("Please run 'Fresh Install' first to create a configuration")
            return True
        
        # Load existing configuration
        config = self.setup_manager.config_manager.load_configuration()
        if not config:
            print("❌ Failed to load existing configuration")
            return True
        
        print(f"✅ Loaded existing configuration")
        
        # Show configuration options
        print("\nAvailable modification options:")
        print("  1. Re-run configuration wizard")
        print("  2. Apply existing configuration")
        print("  3. Run specific Ansible tags")
        print("  4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Re-run wizard with existing config
            try:
                from configure_wizard import ConfigurationWizard
                wizard = ConfigurationWizard()
                if wizard.run():
                    apply = input("\nApply updated configuration? (y/N): ").strip().lower()
                    if apply in ['y', 'yes']:
                        return self._run_ansible()
            except ImportError:
                print("❌ Configuration wizard not available")
        elif choice == '2':
            return self._run_ansible()
        elif choice == '3':
            return self._run_ansible_tags()
        
        return True
    
    def _apply_profile(self) -> bool:
        """Handle profile application"""
        print("\n📦 Applying saved profile...")
        
        profiles_dir = self.setup_manager.config_manager.profiles_dir
        if not profiles_dir.exists():
            print("❌ No profiles directory found")
            return True
        
        # List available profiles
        profiles = list(profiles_dir.glob("*.yml"))
        if not profiles:
            print("❌ No saved profiles found")
            return True
        
        print("\nAvailable profiles:")
        for i, profile in enumerate(profiles, 1):
            print(f"  {i}. {profile.stem}")
        
        try:
            choice = input(f"\nEnter profile number (1-{len(profiles)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(profiles):
                selected_profile = profiles[int(choice) - 1]
                
                # Copy profile to config.yml
                import shutil
                shutil.copy2(selected_profile, "config.yml")
                print(f"✅ Applied profile: {selected_profile.stem}")
                
                # Ask if user wants to run Ansible
                apply = input("\nRun Ansible with this profile? (y/N): ").strip().lower()
                if apply in ['y', 'yes']:
                    return self._run_ansible()
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")
        
        return True
    
    def _backup_config(self) -> bool:
        """Handle configuration backup"""
        print("\n💾 Backing up configuration...")
        
        name = input("Enter backup name (leave empty for timestamp): ").strip()
        if self.setup_manager.config_manager.backup_configuration(name or None):
            print("✅ Configuration backed up successfully")
        else:
            print("❌ Backup failed")
        
        return True
    
    def _quick_setup(self) -> bool:
        """Handle quick setup"""
        print("\n🎯 Running quick setup...")
        
        if self.setup_manager.quick_setup():
            print("✅ Quick setup completed successfully")
        else:
            print("❌ Quick setup failed")
        
        return True
    
    def _system_check(self) -> bool:
        """Handle system check"""
        print("\n🔍 Running system checks...")
        
        if self.setup_manager.run_system_checks():
            print("✅ System checks passed")
            print(f"System: {self.setup_manager.system_info.os_name} {self.setup_manager.system_info.os_version}")
            print(f"Python: {self.setup_manager.system_info.python_version}")
            print(f"Architecture: {self.setup_manager.system_info.architecture}")
        else:
            print("❌ System checks failed")
        
        return True
    
    def _show_help(self) -> bool:
        """Show help information"""
        print("\n❓ Ubuntu Desktop Bootstrap Help")
        print("=" * 50)
        print()
        print("This tool helps you configure and customize your Ubuntu desktop.")
        print()
        print("Available interfaces:")
        print("  - configure_wizard.py         - Original command-line wizard")
        print("  - configure_interactive.py    - Full-screen TUI interface")
        print("  - configure_compact_tui.py    - Compact TUI interface")
        print("  - configure_hierarchical_tui.py - Hierarchical navigation")
        print()
        print("Configuration files:")
        print("  - config.yml                  - Main configuration file")
        print("  - group_vars/all/main.yml     - Default settings")
        print("  - ~/.config/ubuntu-bootstrap/ - User configuration directory")
        print()
        print("Ansible playbooks:")
        print("  - bootstrap.yml               - Initial system setup")
        print("  - site.yml                    - Complete configuration")
        print()
        print("For more information, see:")
        print("  - README.md")
        print("  - QUICK_START.md")
        print("  - CLAUDE.md")
        print()
        
        input("Press Enter to continue...")
        return True
    
    def _run_ansible(self) -> bool:
        """Run Ansible playbook"""
        print("\n🤖 Running Ansible playbook...")
        
        if not Path("config.yml").exists():
            print("❌ No configuration file found")
            return True
        
        # Ask for confirmation
        print("This will apply your configuration to the system.")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Cancelled")
            return True
        
        success = self.setup_manager.run_bootstrap()
        if success:
            print("✅ Ansible playbook completed successfully")
        else:
            print("❌ Ansible playbook failed")
        
        return True
    
    def _run_ansible_tags(self) -> bool:
        """Run Ansible with specific tags"""
        print("\n🏷️  Running Ansible with specific tags...")
        
        available_tags = [
            "desktop", "applications", "development", "security", 
            "system", "dotfiles", "performance"
        ]
        
        print("\nAvailable tags:")
        for i, tag in enumerate(available_tags, 1):
            print(f"  {i}. {tag}")
        
        tag_input = input("\nEnter tag numbers (comma-separated) or tag names: ").strip()
        
        tags = []
        if tag_input:
            for item in tag_input.split(','):
                item = item.strip()
                if item.isdigit():
                    idx = int(item) - 1
                    if 0 <= idx < len(available_tags):
                        tags.append(available_tags[idx])
                else:
                    tags.append(item)
        
        if not tags:
            print("❌ No valid tags specified")
            return True
        
        print(f"Running with tags: {', '.join(tags)}")
        success = self.setup_manager.run_bootstrap(tags=tags)
        
        if success:
            print("✅ Ansible playbook completed successfully")
        else:
            print("❌ Ansible playbook failed")
        
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Ubuntu Desktop Bootstrap Setup")
    parser.add_argument('--check', action='store_true', 
                       help="Run system checks only")
    parser.add_argument('--quick', action='store_true',
                       help="Run quick setup (prerequisites only)")
    parser.add_argument('--config', type=str, default="config.yml",
                       help="Configuration file path")
    parser.add_argument('--tags', type=str,
                       help="Ansible tags to run (comma-separated)")
    parser.add_argument('--dry-run', action='store_true',
                       help="Run Ansible in check mode")
    parser.add_argument('--interface', type=str, 
                       choices=['wizard', 'interactive', 'compact', 'hierarchical'],
                       help="Launch specific configuration interface")
    
    args = parser.parse_args()
    
    setup_manager = SetupManager()
    
    try:
        # Handle command-line arguments
        if args.check:
            success = setup_manager.run_system_checks()
            sys.exit(0 if success else 1)
        
        if args.quick:
            success = setup_manager.quick_setup()
            sys.exit(0 if success else 1)
        
        if args.interface:
            # Launch specific interface
            interfaces = {
                'wizard': 'configure_wizard.py',
                'interactive': 'configure_interactive.py', 
                'compact': 'configure_compact_tui.py',
                'hierarchical': 'configure_hierarchical_tui.py'
            }
            
            script = interfaces.get(args.interface)
            if script and Path(script).exists():
                os.system(f'python3 {script}')
            else:
                print(f"Interface '{args.interface}' not available")
            sys.exit(0)
        
        if args.tags:
            # Run Ansible with specific tags
            tags = [tag.strip() for tag in args.tags.split(',')]
            success = setup_manager.run_bootstrap(args.config, tags, args.dry_run)
            sys.exit(0 if success else 1)
        
        # If no arguments, show interactive menu
        welcome = WelcomeMenu()
        welcome.show_welcome()
        
        while True:
            choice = welcome.show_menu()
            if not welcome.handle_choice(choice):
                break
    
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()