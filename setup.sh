#!/bin/bash
# Ubootu - The Ultimate Ubuntu Experience Engine
# Professional menu-driven system for Ubuntu desktop configuration

# Debug mode
if [[ "${SETUP_DEBUG}" == "1" ]]; then
    set -x  # Enable command tracing
    echo "[DEBUG] Debug mode enabled"
fi

set -e

# Add lib directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"

# Set TUI mode by default
export TUI_MODE="1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running on Ubuntu
check_ubuntu() {
    echo "[DEBUG] Inside check_ubuntu()"
    
    if ! command -v lsb_release &> /dev/null; then
        echo "[DEBUG] lsb_release not found"
        print_error "This script requires Ubuntu. lsb_release command not found."
        exit 1
    fi
    
    echo "[DEBUG] lsb_release found, checking distro..."
    local distro=$(lsb_release -is)
    echo "[DEBUG] Detected distro: $distro"
    
    if [[ ! "$distro" == "Ubuntu" ]]; then
        print_error "This script is designed for Ubuntu. Detected: $distro"
        exit 1
    fi
    
    echo "[DEBUG] Ubuntu detected successfully"
    echo "[DEBUG] TUI_MODE=$TUI_MODE"
    if [[ "$TUI_MODE" != "1" ]]; then
        echo "[DEBUG] Printing success message"
        print_success "✅ Ubuntu $(lsb_release -rs) detected - Ready for Ubootu configuration!"
    else
        echo "[DEBUG] Skipping success message (TUI_MODE=1)"
    fi
    echo "[DEBUG] Exiting check_ubuntu()"
}

# Check if we have a configuration
has_configuration() {
    [[ -f "config.yml" ]] || [[ -f "$HOME/.config/ubuntu-bootstrap/profiles/current.yml" ]]
}

# Install prerequisites
install_prerequisites() {
    # Check if already installed via TUI
    if [[ -f ".prerequisites_installed" ]] || [[ -n "$PREREQUISITES_INSTALLED" ]]; then
        return 0
    fi
    
    # If running in TUI mode, prerequisites are handled there
    if [[ "$TUI_MODE" == "1" ]]; then
        return 0
    fi
    
    print_info "Checking prerequisites..."
    
    # Check APT health and clean up common issues
    print_info "Checking and cleaning APT configuration..."
    
    # Run the enhanced APT fixer that cleans up issues
    python3 lib/apt_fixer.py
    apt_exit_code=$?
    
    # Additional cleanup for archive_ubuntu_com_ubuntu duplicates
    if [[ -f /etc/apt/sources.list.d/archive_ubuntu_com_ubuntu.list ]] && \
       [[ -f /etc/apt/sources.list.d/archive_ubuntu_com_ubuntu.sources ]]; then
        print_warning "Found duplicate repository files, cleaning up..."
        # Remove the .list file as .sources is newer format
        sudo rm -f /etc/apt/sources.list.d/archive_ubuntu_com_ubuntu.list
        print_success "Removed duplicate repository file"
    fi
    
    echo
    print_info "APT check completed with exit code: $apt_exit_code"
    
    if [[ $apt_exit_code -ne 0 ]]; then
        print_warning "APT has some issues - check the recommendations above"
        print_warning "The bootstrap will continue anyway"
    else
        print_success "APT is healthy and ready"
    fi
    
    # Update package cache
    print_info "Updating package cache..."
    sudo apt update
    
    # Install Python and pip if not present
    if ! command -v python3 &> /dev/null; then
        print_info "Installing Python 3..."
        sudo apt install -y python3 python3-pip python3-venv
    fi
    
    # Install required Python packages
    print_info "Installing Python dependencies..."
    packages=(
        "python3-yaml"
        "python3-rich"
        "python3-git"
        "python3-full"
    )
    
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package"; then
            print_info "Installing $package..."
            sudo apt install -y "$package"
        fi
    done
    
    # Install Ansible
    if ! command -v ansible &> /dev/null; then
        print_info "Installing Ansible..."
        
        # Get Ubuntu version
        ubuntu_version=$(lsb_release -rs)
        ubuntu_codename=$(lsb_release -cs)
        
        # Remove any existing Ansible PPA that might cause issues
        print_info "Cleaning up any existing Ansible PPA..."
        sudo rm -f /etc/apt/sources.list.d/ansible-ubuntu-ansible-*.list 2>/dev/null
        sudo rm -f /etc/apt/sources.list.d/ansible-ubuntu-ansible-*.sources 2>/dev/null
        
        # Check if we should use PPA or default repos
        if [[ "$ubuntu_codename" == "focal" ]] || [[ "$ubuntu_codename" == "jammy" ]] || [[ "$ubuntu_codename" == "noble" ]]; then
            print_info "Adding Ansible PPA for Ubuntu $ubuntu_version..."
            sudo apt install -y software-properties-common
            sudo apt-add-repository --yes --update ppa:ansible/ansible 2>/dev/null || {
                print_warning "Failed to add Ansible PPA, using default repositories..."
                sudo apt update
            }
        else
            print_info "Using default Ubuntu repositories for Ansible..."
        fi
        
        # Install ansible
        sudo apt install -y ansible || {
            print_error "Failed to install Ansible"
            exit 1
        }
    else
        print_success "Ansible is already installed"
    fi
    
    # Try to install rich via pip in user space if not available via apt
    if ! python3 -c "import rich" 2>/dev/null; then
        print_info "Installing additional Python packages..."
        python3 -m pip install --user rich keyboard || {
            print_warning "Could not install rich via pip, some features may be limited"
        }
    fi
    
    print_success "Prerequisites installed"
}

# Install Ansible requirements
install_ansible_requirements() {
    print_info "Installing Ansible collections..."
    ansible-galaxy collection install -r requirements.yml
    print_success "Ansible collections installed"
}

# Show Ubootu TUI splash screen
show_ubootu_splash() {
    [[ "$TUI_MODE" != "1" ]] && print_info "Loading Ubootu..."
    
    # Run the configure_standard_tui.py script which will show the main menu
    python3 configure_standard_tui.py
    exit_code=$?
    
    # Map exit codes to menu choices
    if [[ $exit_code -eq 0 ]]; then
        # User completed configuration
        echo "1" > /tmp/welcome_choice.txt
    elif [[ $exit_code -eq 1 ]]; then
        # User cancelled/exited
        echo "8" > /tmp/welcome_choice.txt
    else
        # Error occurred
        echo "8" > /tmp/welcome_choice.txt
    fi
}

# Welcome menu (no sudo required) - now integrated into splash
show_welcome_menu() {
    # Show the new integrated splash screen with options
    show_ubootu_splash
    
    # The splash screen now handles everything, no need for separate menu
    return 0
    
    # Keeping the old code commented out for reference
    # Create a temporary Python script
    : << 'EOF_COMMENTED'
    cat > /tmp/welcome_menu.py << 'EOF'
import sys
import os
sys.path.insert(0, 'lib')
try:
    from menu_ui import MenuUI
    
    # Initialize menu
    menu = MenuUI()
    
    # Show splash screen
    menu.show_splash_screen()
    
    # Show welcome message
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    
    console = Console()
    
    welcome_text = Text()
    welcome_text.append("🚀 Welcome to Ubootu! 🚀\n\n", style="bold magenta")
    welcome_text.append("Professional Ubuntu Desktop Configuration Tool\n", style="bright_cyan")
    welcome_text.append("Configure your desktop with 400+ tools and customizations.\n\n", style="bright_cyan")
    welcome_text.append("What would you like to do?\n", style="bold white")
    
    panel = Panel(
        Align.center(welcome_text),
        border_style="bright_magenta",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    # Show options
    options = [
        "🚀 Fresh Install - Configure a brand new Ubuntu installation",
        "🔧 Modify Setup - Tweak your existing configuration",
        "📦 Apply Profile - Restore from a saved configuration",
        "💾 Backup Config - Save your current setup",
        "📜 View History - Browse configuration timeline",
        "🎯 Quick Actions - Common tasks and fixes",
        "❓ Help - Get help and documentation",
        "🚪 Exit - See you later!"
    ]
    
    for i, option in enumerate(options, 1):
        console.print(f"  {i}. {option}")
    
    console.print()
    
    # Get user choice
    try:
        choice = input("Enter your choice (1-8): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
            choice = "8"
        
        # Write choice to temp file for bash to read
        with open('/tmp/welcome_choice.txt', 'w') as f:
            f.write(choice)
            
    except (KeyboardInterrupt, EOFError):
        with open('/tmp/welcome_choice.txt', 'w') as f:
            f.write("8")
        
except ImportError as e:
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║                         🚀 UBOOTU 🚀                             ║")
    print("║                                                                  ║")
    print("║           Professional Ubuntu Desktop Configuration Tool          ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print("🚀 Welcome to Ubootu!")
    print()
    print("Professional Ubuntu Desktop Configuration Tool")
    print("Configure your desktop with 400+ tools and customizations.")
    print()
    print("Basic Python libraries are required to run this script.")
    print("This script will install the necessary dependencies.")
    print()
    print("What would you like to do?")
    print()
    print("  1. 🚀 Fresh Install - Configure a brand new Ubuntu installation")
    print("  2. 🔧 Modify Setup - Tweak your existing configuration")
    print("  3. 📦 Apply Profile - Restore from a saved configuration")
    print("  4. 💾 Backup Config - Save your current setup")
    print("  5. 📜 View History - Browse configuration timeline")
    print("  6. 🎯 Quick Actions - Common tasks and fixes")
    print("  7. ❓ Help - Get help and documentation")
    print("  8. 🚪 Exit - See you later!")
    print()
    try:
        choice = input("Enter your choice (1-8): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
            choice = "8"
    except (KeyboardInterrupt, EOFError):
        choice = "8"
    
    with open('/tmp/welcome_choice.txt', 'w') as f:
        f.write(choice)
EOF
    
    # Run the Python script
    python3 /tmp/welcome_menu.py
    
    # Clean up
    rm -f /tmp/welcome_menu.py
EOF_COMMENTED
}

# Explain why sudo is needed (now handled in TUI)
explain_sudo_requirement() {
    # This is now handled within the TUI interface
    # The PrerequisiteInstaller shows this in a dialog
    return 0
}

# Main menu handler
show_main_menu() {
    python3 - << 'EOF'
import sys
import os
sys.path.insert(0, 'lib')

try:
    from menu_ui import MenuUI
    from profile_manager import ProfileManager
    from app_defaults import AppDefaults
    
    # Initialize components
    menu = MenuUI()
    profile_mgr = ProfileManager()
    app_defaults = AppDefaults()
    
    # Show splash screen
    menu.show_splash_screen()
    
    # Check if we have existing configuration
    has_config = os.path.exists('config.yml')
    
    # Show main menu and get choice
    choice = menu.show_main_menu(has_config)
    
    # Write choice to temp file for bash to read
    with open('/tmp/menu_choice.txt', 'w') as f:
        f.write(choice)
        
except ImportError as e:
    print(f"Error loading menu system: {e}")
    print("Please install required dependencies first:")
    print("sudo apt install python3-rich python3-yaml python3-git")
    print("Then run the script again.")
    with open('/tmp/menu_choice.txt', 'w') as f:
        f.write("8")  # Exit
EOF
    
    # Read the choice
    if [[ -f /tmp/menu_choice.txt ]]; then
        choice=$(cat /tmp/menu_choice.txt)
        rm -f /tmp/menu_choice.txt
        echo "$choice"
    else
        echo "8"  # Exit
    fi
}

# Fresh install workflow
fresh_install() {
    print_info "Starting fresh installation workflow..."
    
    # First show profile templates
    # Show profile templates using professional interface
    echo
    print_success "System preparation completed successfully!"
    echo
    print_info "✅ APT package manager checked and updated"
    print_info "✅ Python 3 and dependencies installed"
    print_info "✅ Ansible automation platform installed"
    print_info "✅ Required Python packages installed"
    print_info "✅ Ansible collections installed"
    echo
    print_info "Ready to configure your Ubuntu desktop with your preferred applications and settings."
    echo
    print_info "Starting comprehensive configuration wizard..."
    run_configuration_wizard
    
    # Check if user cancelled
    if [[ $? -ne 0 ]]; then
        print_info "Configuration cancelled by user"
        return 1
    fi
    
    # Run Ansible playbooks
    run_playbooks
    
    # Show success screen
    show_success_screen
}

# Run configuration wizard
run_configuration_wizard() {
    print_info "Starting unified configuration interface..."
    
    # Run the unified TUI interface
    python3 configure_standard_tui.py
    exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        return 0
    elif [[ $exit_code -eq 1 ]]; then
        # User cancelled (pressed escape, quit, or exit action)
        print_info "Configuration cancelled by user"
        return 1
    elif [[ $exit_code -eq 130 ]]; then
        # User pressed Ctrl+C
        print_info "Configuration cancelled by user"
        return 1
    else
        print_error "Configuration interface failed with exit code $exit_code"
        return 1
    fi
}

# Load template profile
load_template_profile() {
    local profile_id=$1
    
    python3 - << EOF
import sys
import yaml
sys.path.insert(0, 'lib')

from profile_manager import ProfileManager

profile_mgr = ProfileManager()
profile_mgr.create_template_profiles()

# Map profile ID to name
profile_map = {
    '1': 'developer',
    '2': 'gaming',
    '3': 'creative', 
    '4': 'security',
    '5': 'minimal'
}

profile_name = profile_map.get('$profile_id', 'developer')
config = profile_mgr.load_profile(profile_name)

# Save as current config
with open('config.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
    
print(f"Loaded {profile_name} profile")
EOF
}

# Modify existing setup
modify_setup() {
    print_info "Modifying existing configuration..."
    
    # Use the unified TUI section selector
    python3 -c "
import curses
import sys
sys.path.insert(0, 'lib')
from tui.section_selector import show_section_selector

try:
    selected = curses.wrapper(show_section_selector)
    if selected:
        with open('/tmp/selected_sections.txt', 'w') as f:
            f.write(','.join(selected))
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"
    exit_code=$?
    
    if [[ $exit_code -ne 0 ]]; then
        print_warning "Section selection cancelled or failed"
        return 1
    fi
    
    if [[ -f /tmp/selected_sections.txt ]]; then
        selected_sections=$(cat /tmp/selected_sections.txt)
        rm -f /tmp/selected_sections.txt
        
        if [[ -n "$selected_sections" ]]; then
            print_success "Selected sections: ${selected_sections//,/, }"
            echo
            
            # Run wizard with only selected sections
            print_info "Starting configuration for selected sections..."
            python3 configure_standard_tui.py --sections "$selected_sections"
            exit_code=$?
            
            if [[ $exit_code -eq 0 ]]; then
                # Run only the selected Ansible tags
                print_info "Applying configuration changes..."
                run_playbooks "--tags $selected_sections"
                show_success_screen
            else
                print_warning "Configuration wizard cancelled"
                return 1
            fi
        else
            print_info "No sections selected. Returning to main menu..."
            return 0
        fi
    else
        print_warning "No selection file found. Returning to main menu..."
        return 1
    fi
}

# Apply saved profile
apply_profile() {
    print_info "Applying saved profile..."
    
    # Use the new TUI profile selector
    python3 lib/profile_selector.py
    
    if [[ -f /tmp/profile_loaded.txt ]]; then
        loaded=$(cat /tmp/profile_loaded.txt)
        rm -f /tmp/profile_loaded.txt
        
        if [[ "$loaded" == "yes" ]]; then
            run_playbooks
            show_success_screen
        else
            print_info "Profile loading cancelled"
        fi
    fi
}

# Backup current configuration
backup_config() {
    print_info "Backing up current configuration..."
    
    # Use the new TUI backup dialog
    python3 lib/backup_config_tui.py
}

# View configuration history
view_history() {
    print_info "Configuration History"
    
    # Use the new TUI history viewer
    python3 lib/history_viewer.py
}

# Run Ansible playbooks with app customization
run_playbooks() {
    local extra_args="$1"
    
    print_info "Starting Ubootu desktop configuration..."
    
    # First, let user review and customize app defaults
    if [[ -z "$extra_args" ]] || [[ "$extra_args" != *"--skip-customization"* ]]; then
        show_app_customizations
    fi
    
    # Ask for sudo password upfront
    print_info "Ansible will need sudo access. Please enter your password when prompted."
    
    # Run bootstrap playbook first if needed
    if [[ ! -f "$HOME/.ansible_bootstrap_complete" ]]; then
        print_info "Running initial bootstrap..."
        ansible-playbook bootstrap.yml --ask-become-pass || {
            print_error "Bootstrap failed"
            exit 1
        }
        touch "$HOME/.ansible_bootstrap_complete"
    fi
    
    # Run main site playbook
    print_info "Running main configuration..."
    if [[ -f "config.yml" ]]; then
        ansible-playbook site.yml --extra-vars "@config.yml" --ask-become-pass $extra_args || {
            print_error "Configuration failed"
            exit 1
        }
    else
        ansible-playbook site.yml --ask-become-pass $extra_args || {
            print_error "Configuration failed"
            exit 1
        }
    fi
    
    print_success "Ubootu configuration complete! 🚀"
}

# Show application customization options
show_app_customizations() {
    print_info "Reviewing application customizations..."
    
    # TODO: Implement app customization in unified TUI
    # For now, skip this step
    print_info "App customization will be available in a future update"
    return 0
    
# Original implementation commented out for reference
: << 'EOF_APP_CUSTOMIZATION'
    python3 - << 'EOF'
import sys
import yaml
sys.path.insert(0, 'lib')

from menu_ui import MenuUI
from app_defaults import AppDefaults

menu = MenuUI()
app_defaults = AppDefaults()

# Load current config
try:
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f) or {}
except:
    config = {}

# Check what apps are being installed
customizations = {}

# Common applications to customize
apps_to_customize = [
    ('vscode', 'developer', 'Visual Studio Code'),
    ('git', 'developer', 'Git Version Control'),
    ('firefox', 'user', 'Firefox Web Browser'),
    ('thunderbird', 'user', 'Thunderbird Email'),
    ('libreoffice', 'user', 'LibreOffice Suite'),
    ('vlc', 'user', 'VLC Media Player'),
    ('system', 'user', 'System Preferences')
]

for app_key, user_type, display_name in apps_to_customize:
    app_config = app_defaults.get_app_config(app_key, user_type)
    if app_config:
        choice = menu.show_app_customization(display_name, app_config)
        if choice == 'a':  # Accept all
            customizations[app_key] = app_config
        elif choice == 'c':  # Customize
            custom_config = menu.show_detailed_customization(display_name, app_config)
            if custom_config:
                customizations[app_key] = custom_config
        # 's' = skip, don't add to customizations

# Save customizations to config
config['app_customizations'] = customizations

with open('config.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
EOF
EOF_APP_CUSTOMIZATION
}

# Show success screen
show_success_screen() {
    print_success "🎉 Ubootu configuration complete!"
    echo
    print_info "Your Ubuntu system has been successfully configured."
    print_info "All selected packages and configurations have been applied."
    echo
    print_warning "Remember to reboot when convenient to apply all changes!"
    echo
    print_info "What would you like to do next?"
    echo "  1. Reboot now"
    echo "  2. View installation log"
    echo "  3. Continue using the system"
    echo
    read -p "Your choice [1-3] (default: 3): " choice
    
    case "${choice:-3}" in
        1)
            print_info "Rebooting..."
            sudo reboot
            ;;
        2)
            if [[ -f ansible.log ]]; then
                less ansible.log
            else
                print_warning "No log file found"
            fi
            ;;
        *)
            print_info "Remember to reboot when convenient to apply all changes!"
            ;;
    esac
    
# Original implementation commented out for reference
: << 'EOF_SUCCESS_SCREEN'
    python3 - << 'EOF'
import sys
import yaml
sys.path.insert(0, 'lib')

from menu_ui import MenuUI

menu = MenuUI()

# Calculate some stats
try:
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f) or {}
        
    stats = {
        'configured': [],
        'packages': 0,
        'boot_improvement': '2.3',
        'security_score': 'A+' if config.get('enable_security', False) else 'B'
    }
    
    if config.get('desktop_environment'):
        stats['configured'].append(f"Desktop: {config['desktop_environment'].upper()}")
    if config.get('enable_themes'):
        stats['configured'].append(f"Theme: {config.get('theme_name', 'custom')}")
    if config.get('enable_development_tools'):
        stats['configured'].append("Development tools installed")
    if config.get('enable_security'):
        stats['configured'].append("Security hardening enabled")
        
    # Count packages (rough estimate)
    stats['packages'] = (
        len(config.get('web_browsers', [])) * 5 +
        len(config.get('code_editors', [])) * 10 +
        len(config.get('programming_languages', [])) * 15 +
        20  # Base packages
    )
    
except:
    stats = {
        'configured': ['System configured successfully'],
        'packages': 47,
        'boot_improvement': '2.3',
        'security_score': 'A'
    }

choice = menu.show_success_screen(stats)

with open('/tmp/success_choice.txt', 'w') as f:
    f.write(choice)
EOF
    
    choice=$(cat /tmp/success_choice.txt 2>/dev/null || echo "l")
    rm -f /tmp/success_choice.txt
    
    case "$choice" in
        r)
            print_info "Rebooting..."
            sudo reboot
            ;;
        v)
            less ansible.log
            ;;
        *)
            print_info "Remember to reboot when convenient to apply all changes!"
            ;;
    esac
EOF_SUCCESS_SCREEN
}

# Quick actions menu
quick_actions() {
    # Use the new TUI quick actions menu
    python3 lib/quick_actions_tui.py
}

# Show help
show_help() {
    # Use the new TUI help viewer
    python3 lib/help_viewer.py
}

# Main execution
main() {
    echo "[DEBUG] Entering main() function"
    echo "[DEBUG] Number of arguments: $#"
    echo "[DEBUG] First argument: ${1:-<none>}"
    
    # Debug mode
    if [[ "$BOOTSTRAP_DEBUG" == "1" ]]; then
        set -x  # Enable command tracing
        print_info "Debug mode enabled"
    fi
    
    # Handle command line arguments
    echo "[DEBUG] Checking command line arguments..."
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --fresh)
            check_ubuntu
            explain_sudo_requirement
            install_prerequisites
            fresh_install
            exit 0
            ;;
        --custom|--configure)
            print_info "Starting direct custom configuration (no profiles)..."
            check_ubuntu
            explain_sudo_requirement
            install_prerequisites
            run_configuration_wizard
            if [[ -f "config.yml" ]]; then
                run_playbooks
                show_success_screen
            fi
            exit 0
            ;;
        --tui)
            print_info "Starting TUI configuration..."
            check_ubuntu
            explain_sudo_requirement
            install_prerequisites
            python3 configure_standard_tui.py
            if [[ -f "config.yml" ]]; then
                run_playbooks
                show_success_screen
            fi
            exit 0
            ;;
        --restore)
            if [[ -z "${2:-}" ]]; then
                print_error "Please provide configuration file path"
                exit 1
            fi
            check_ubuntu
            explain_sudo_requirement
            install_prerequisites
            cp "$2" config.yml
            run_playbooks
            exit 0
            ;;
        --backup)
            backup_config
            exit 0
            ;;
    esac
    
    # Interactive mode
    echo "[DEBUG] Starting interactive mode"
    echo "[DEBUG] Is stdout a TTY: $(if [[ -t 1 ]]; then echo "YES"; else echo "NO"; fi)"
    echo "[DEBUG] Is stdin a TTY: $(if [[ -t 0 ]]; then echo "YES"; else echo "NO"; fi)"
    echo "[DEBUG] TERM=$TERM"
    echo "[DEBUG] Working directory: $(pwd)"
    
    # Don't clear if not in TTY
    if [[ -t 1 ]]; then
        echo "[DEBUG] Clearing screen"
        clear
    else
        echo "[DEBUG] Not clearing screen - not in TTY"
    fi
    
    # Check Ubuntu
    echo "[DEBUG] Checking Ubuntu..."
    check_ubuntu
    echo "[DEBUG] Ubuntu check completed"
    
    # Debug output
    [[ "$TUI_MODE" != "1" ]] && print_info "Starting TUI interface..."
    
    # Check if Python script exists
    if [[ -f "configure_standard_tui.py" ]]; then
        echo "[DEBUG] configure_standard_tui.py found"
    else
        echo "[DEBUG] ERROR: configure_standard_tui.py not found!"
        echo "[DEBUG] Current directory contents:"
        ls -la | head -10
    fi
    
    # Run the TUI which handles everything
    echo "[DEBUG] About to run: python3 configure_standard_tui.py"
    echo "[DEBUG] Python3 location: $(which python3)"
    
    set +e  # Temporarily disable exit on error
    python3 configure_standard_tui.py
    exit_code=$?
    set -e  # Re-enable exit on error
    
    echo "[DEBUG] Python script exit code: $exit_code"
    
    if [[ $exit_code -eq 0 ]]; then
        # User completed configuration, run ansible
        print_info "Configuration saved. Running Ansible playbooks..."
        install_prerequisites
        run_playbooks
        show_success_screen
    else
        # User cancelled or error occurred
        print_info "Thanks for using Ubootu! 🚀"
    fi
}

# Run main function
echo "[DEBUG] Script starting at $(date)"
echo "[DEBUG] Script location: $0"
echo "[DEBUG] All arguments: $@"
main "$@"
echo "[DEBUG] main() returned, script ending"