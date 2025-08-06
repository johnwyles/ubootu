#!/bin/bash
#
# Ubootu One-Line Installer
# 
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/johnwyles/ubootu/main/install.sh | bash
#   wget -qO- https://raw.githubusercontent.com/johnwyles/ubootu/main/install.sh | bash
#
# Environment Variables:
#   UBOOTU_DIR      - Installation directory (default: $HOME/ubootu)
#   UBOOTU_BRANCH   - Git branch to install (default: main)
#   UBOOTU_CONFIG   - Path to existing config.yml to use
#   NONINTERACTIVE  - Set to 1 for non-interactive installation
#

set -e

# Configuration
REPO_URL="https://github.com/johnwyles/ubootu.git"
INSTALL_DIR="${UBOOTU_DIR:-$HOME/ubootu}"
BRANCH="${UBOOTU_BRANCH:-main}"
MIN_PYTHON_VERSION="3.8"
MIN_ANSIBLE_VERSION="2.9"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Helper functions
print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                        ║"
    echo "║     🚀  ${BOLD}Ubootu${NC}${CYAN} - Ubuntu Configuration Tool  🚀       ║"
    echo "║                                                        ║"
    echo "║     Configure your perfect Ubuntu setup once.         ║"
    echo "║     Deploy it anywhere, anytime.                      ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running on Ubuntu
check_ubuntu() {
    if ! command -v lsb_release &> /dev/null; then
        print_warning "lsb_release not found, attempting to install..."
        sudo apt-get update && sudo apt-get install -y lsb-release
    fi
    
    local os_name=$(lsb_release -si 2>/dev/null)
    local os_version=$(lsb_release -sr 2>/dev/null)
    
    if [[ "$os_name" != "Ubuntu" ]]; then
        print_error "This installer requires Ubuntu. Detected: $os_name"
        exit 1
    fi
    
    case "$os_version" in
        20.04|22.04|24.04|24.10)
            print_success "Ubuntu $os_version detected"
            ;;
        *)
            print_warning "Ubuntu $os_version is not officially tested"
            print_info "Supported versions: 20.04, 22.04, 24.04"
            if [[ "$NONINTERACTIVE" != "1" ]]; then
                read -p "Continue anyway? (y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    exit 1
                fi
            fi
            ;;
    esac
}

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
        if [ $(echo "$python_version >= $MIN_PYTHON_VERSION" | bc -l) -eq 1 ]; then
            print_success "Python $python_version found"
            return 0
        fi
    fi
    
    print_warning "Python 3.8+ not found, installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
}

# Check Ansible
check_ansible() {
    if command -v ansible &> /dev/null; then
        local ansible_version=$(ansible --version | head -1 | grep -oP '\d+\.\d+' | head -1)
        if [ $(echo "$ansible_version >= $MIN_ANSIBLE_VERSION" | bc -l) -eq 1 ]; then
            print_success "Ansible $ansible_version found"
            return 0
        fi
    fi
    
    print_warning "Ansible not found, installing..."
    sudo apt-get update
    sudo apt-get install -y ansible
}

# Check Git
check_git() {
    if command -v git &> /dev/null; then
        print_success "Git found"
        return 0
    fi
    
    print_warning "Git not found, installing..."
    sudo apt-get update
    sudo apt-get install -y git
}

# Install system dependencies
install_dependencies() {
    print_info "Checking system dependencies..."
    
    # Essential packages
    local packages=(
        curl
        wget
        software-properties-common
        apt-transport-https
        ca-certificates
        gnupg
        lsb-release
        bc
    )
    
    local missing_packages=()
    for pkg in "${packages[@]}"; do
        if ! dpkg -l "$pkg" &> /dev/null; then
            missing_packages+=("$pkg")
        fi
    done
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        print_info "Installing missing packages: ${missing_packages[*]}"
        sudo apt-get update
        sudo apt-get install -y "${missing_packages[@]}"
    else
        print_success "All system dependencies installed"
    fi
}

# Clone or update repository
install_ubootu() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        print_info "Ubootu already installed at $INSTALL_DIR"
        if [[ "$NONINTERACTIVE" != "1" ]]; then
            read -p "Update to latest version? (Y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Nn]$ ]]; then
                return 0
            fi
        fi
        
        print_info "Updating Ubootu..."
        cd "$INSTALL_DIR"
        git fetch origin
        git checkout "$BRANCH"
        git pull origin "$BRANCH"
        print_success "Updated to latest version"
    else
        print_info "Installing Ubootu to $INSTALL_DIR..."
        git clone --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
        print_success "Ubootu installed successfully"
    fi
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    cd "$INSTALL_DIR"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    
    # Install requirements
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install pyyaml rich
    
    print_success "Python dependencies installed"
}

# Copy existing configuration if provided
copy_config() {
    if [ -n "$UBOOTU_CONFIG" ] && [ -f "$UBOOTU_CONFIG" ]; then
        print_info "Copying configuration from $UBOOTU_CONFIG"
        cp "$UBOOTU_CONFIG" "$INSTALL_DIR/config.yml"
        print_success "Configuration copied"
    fi
}

# Add to PATH
setup_path() {
    local shell_rc=""
    
    if [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    local path_line="export PATH=\"\$PATH:$INSTALL_DIR\""
    
    if ! grep -q "$INSTALL_DIR" "$shell_rc" 2>/dev/null; then
        print_info "Adding Ubootu to PATH in $shell_rc"
        echo "" >> "$shell_rc"
        echo "# Ubootu" >> "$shell_rc"
        echo "$path_line" >> "$shell_rc"
        print_success "Added to PATH"
        print_warning "Run 'source $shell_rc' or restart your terminal"
    else
        print_success "Ubootu already in PATH"
    fi
}

# Main installation flow
main() {
    print_banner
    
    # Check prerequisites
    print_info "Checking system requirements..."
    check_ubuntu
    install_dependencies
    check_git
    check_python
    check_ansible
    
    # Install Ubootu
    install_ubootu
    install_python_deps
    copy_config
    setup_path
    
    # Success message
    echo
    print_success "🎉 Ubootu installation complete!"
    echo
    echo -e "${BOLD}Next steps:${NC}"
    echo "  1. cd $INSTALL_DIR"
    echo "  2. ./setup.sh           # Configure your system"
    echo
    echo -e "${BOLD}Or restore existing configuration:${NC}"
    echo "  ./setup.sh --restore config.yml"
    echo
    echo -e "${CYAN}Documentation:${NC} https://github.com/johnwyles/ubootu"
    echo
    
    # Launch if not in non-interactive mode
    if [[ "$NONINTERACTIVE" != "1" ]]; then
        read -p "Launch Ubootu now? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            cd "$INSTALL_DIR"
            ./setup.sh
        fi
    fi
}

# Handle errors
trap 'print_error "Installation failed. Check the error messages above."; exit 1' ERR

# Run main installation
main "$@"