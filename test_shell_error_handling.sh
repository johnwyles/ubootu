#!/bin/bash
# Test script for Ubootu shell error handling improvements

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Ubootu Shell Error Handling Test ==="
echo

# Function to print test results
print_result() {
    local test_name="$1"
    local result="$2"
    local details="$3"
    
    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✓${NC} $test_name"
    else
        echo -e "${RED}✗${NC} $test_name"
        echo -e "  ${YELLOW}Details:${NC} $details"
    fi
}

# Function to test command availability check
test_command_check() {
    echo "Testing command availability checks..."
    
    # Create a temporary shell script with the check_command function
    cat > /tmp/test_check_command.sh << 'EOF'
# Helper function to check if command exists and provide helpful messages
check_command() {
    local cmd="$1"
    local friendly_name="${2:-$cmd}"
    local install_hint="$3"
    
    if command -v "$cmd"; then
        return 0
    else
        if [ -n "$install_hint" ]; then
            echo "[UBOOTU INFO] $friendly_name not found. To install: $install_hint" >&2
        else
            echo "[UBOOTU INFO] $friendly_name not found in PATH" >&2
        fi
        return 1
    fi
}

# Test with existing command
if check_command ls "ls command" 2>/tmp/ls_test.err; then
    echo "ls found"
fi

# Test with non-existing command
if check_command nonexistentcmd "Fake Tool" "sudo apt install fake-tool" 2>/tmp/fake_test.err; then
    echo "fake found"
else
    echo "fake not found"
fi
EOF

    # Run the test
    bash /tmp/test_check_command.sh > /tmp/test_output.txt
    
    # Check results
    if grep -q "ls found" /tmp/test_output.txt && grep -q "fake not found" /tmp/test_output.txt; then
        if grep -q "\[UBOOTU INFO\] Fake Tool not found. To install: sudo apt install fake-tool" /tmp/fake_test.err; then
            print_result "check_command function" "PASS"
        else
            print_result "check_command function" "FAIL" "Error message not formatted correctly"
        fi
    else
        print_result "check_command function" "FAIL" "Function logic error"
    fi
}

# Function to test FZF/FD integration
test_fzf_fd_integration() {
    echo -e "\nTesting FZF/FD integration..."
    
    # Create test script
    cat > /tmp/test_fzf_fd.sh << 'EOF'
# Simulate the FZF configuration
if command -v fzf; then
    # Use fd if available, otherwise fall back to find
    if command -v fd; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
        echo "Using fd for FZF"
    else
        echo "[UBOOTU INFO] fd not found, using find for FZF" >&2
        echo "  For better performance, install fd: sudo apt install fd-find" >&2
        export FZF_DEFAULT_COMMAND='find . -type f -not -path "*/\.git/*"'
        echo "Using find for FZF"
    fi
    echo "FZF_DEFAULT_COMMAND=$FZF_DEFAULT_COMMAND"
fi
EOF

    # Test with fd available
    if command -v fd > /dev/null; then
        output=$(bash /tmp/test_fzf_fd.sh 2>&1)
        if echo "$output" | grep -q "Using fd for FZF"; then
            print_result "FZF with fd available" "PASS"
        else
            print_result "FZF with fd available" "FAIL" "Should use fd when available"
        fi
    fi
    
    # Test without fd (simulate)
    PATH_BACKUP="$PATH"
    export PATH="/usr/bin:/bin"  # Minimal PATH without fd
    output=$(bash /tmp/test_fzf_fd.sh 2>&1)
    export PATH="$PATH_BACKUP"
    
    if echo "$output" | grep -q "\[UBOOTU INFO\] fd not found" && echo "$output" | grep -q "Using find for FZF"; then
        print_result "FZF fallback to find" "PASS"
    else
        print_result "FZF fallback to find" "FAIL" "Should fall back to find with warning"
    fi
}

# Function to test SDKMAN initialization
test_sdkman_init() {
    echo -e "\nTesting SDKMAN initialization..."
    
    # Create test script
    cat > /tmp/test_sdkman.sh << 'EOF'
export SDKMAN_DIR="$HOME/.sdkman"
if [[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]]; then
    # Set SDKMAN to offline mode during shell startup to prevent network calls
    export SDKMAN_OFFLINE_MODE=true
    # Define any missing functions that SDKMAN might expect
    if ! declare -f __sdkman_echo_debug; then
        __sdkman_echo_debug() { :; }
        export -f __sdkman_echo_debug
    fi
    # Source SDKMAN and capture any errors
    if ! source "$SDKMAN_DIR/bin/sdkman-init.sh"; then
        echo "[UBOOTU ERROR] SDKMAN initialization failed. Please check:" >&2
        echo "  - Is SDKMAN properly installed? Run: curl -s 'https://get.sdkman.io' | bash" >&2
        echo "  - Check SDKMAN installation: ls -la $SDKMAN_DIR/bin/" >&2
    fi
    # Re-enable online mode after initialization
    unset SDKMAN_OFFLINE_MODE
else
    echo "[UBOOTU WARNING] SDKMAN directory not found at $SDKMAN_DIR" >&2
    echo "  To install SDKMAN, run: curl -s 'https://get.sdkman.io' | bash" >&2
fi
EOF

    # Test without SDKMAN installed
    SDKMAN_DIR="/tmp/nonexistent_sdkman"
    output=$(export SDKMAN_DIR="$SDKMAN_DIR" && bash /tmp/test_sdkman.sh 2>&1)
    
    if echo "$output" | grep -q "\[UBOOTU WARNING\] SDKMAN directory not found"; then
        print_result "SDKMAN not installed warning" "PASS"
    else
        print_result "SDKMAN not installed warning" "FAIL" "Should show warning when SDKMAN not found"
    fi
}

# Function to test globstar option
test_globstar() {
    echo -e "\nTesting shell option error handling..."
    
    # Create test script
    cat > /tmp/test_globstar.sh << 'EOF'
# Enable globstar (** for recursive matching)
if shopt -s globstar; then
    :  # globstar enabled successfully
else
    echo "[UBOOTU WARNING] globstar option not available in this bash version" >&2
fi
EOF

    # Test (globstar should work in modern bash)
    output=$(bash /tmp/test_globstar.sh 2>&1)
    
    if [ -z "$output" ]; then
        print_result "globstar option (modern bash)" "PASS"
    else
        print_result "globstar option" "FAIL" "Unexpected output: $output"
    fi
}

# Function to test modern CLI aliases
test_modern_cli_aliases() {
    echo -e "\nTesting modern CLI tool aliases..."
    
    # Create test script
    cat > /tmp/test_aliases.sh << 'EOF'
# Modern replacements (if installed)
if command -v eza; then
    alias ls='eza'
else
    echo "[UBOOTU INFO] eza not installed (modern ls replacement)" >&2
fi

if command -v bat; then
    alias cat='bat'
else
    echo "[UBOOTU INFO] bat not installed (syntax-highlighting cat)" >&2
fi
EOF

    # Test without tools (simulate)
    PATH_BACKUP="$PATH"
    export PATH="/usr/bin:/bin"  # Minimal PATH
    output=$(bash /tmp/test_aliases.sh 2>&1)
    export PATH="$PATH_BACKUP"
    
    if echo "$output" | grep -q "\[UBOOTU INFO\] eza not installed" && \
       echo "$output" | grep -q "\[UBOOTU INFO\] bat not installed"; then
        print_result "Modern CLI tool warnings" "PASS"
    else
        print_result "Modern CLI tool warnings" "FAIL" "Should show info messages for missing tools"
    fi
}

# Run all tests
test_command_check
test_fzf_fd_integration
test_sdkman_init
test_globstar
test_modern_cli_aliases

# Cleanup
rm -f /tmp/test_*.sh /tmp/test_output.txt /tmp/*.err

echo -e "\n=== Test Summary ==="
echo "All tests completed. Check results above."

# Manual testing instructions
echo -e "\n${YELLOW}=== Manual Testing Instructions ===${NC}"
echo "To manually test the changes in your shell:"
echo
echo "1. Apply the Ubootu configuration:"
echo "   ansible-playbook site.yml --tags dotfiles,dev"
echo
echo "2. Open a new terminal and observe startup messages"
echo
echo "3. Test specific scenarios:"
echo "   # Test with missing fd"
echo "   sudo mv /usr/bin/fd /usr/bin/fd.bak 2>/dev/null || true"
echo "   bash -l  # Start new login shell"
echo "   # Look for: [UBOOTU INFO] fd not found messages"
echo "   sudo mv /usr/bin/fd.bak /usr/bin/fd 2>/dev/null || true"
echo
echo "4. Test FZF behavior:"
echo "   # In a directory with files"
echo "   fzf  # Should work with find if fd is missing"
echo
echo "5. Check for any error silencing:"
echo "   grep -r '2>/dev/null' roles/*/templates/*.j2 | grep -v UBOOTU"
echo "   # Should show minimal results"