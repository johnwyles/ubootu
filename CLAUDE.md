# CLAUDE.md - Complete Claude Code Guide for Ubootu Project

## 🚀 Quick Start for Claude Code

This document provides everything needed for Claude Code to work effectively with the Ubootu project. If you're a new Claude Code instance working on this project, start here!

## Project Overview

**Ubootu** is a professional Ubuntu desktop and server configuration tool created by John Wyles using Claude Code. Born from the frustration of repeatedly setting up new Ubuntu machines, this project automates and streamlines the entire process with an intelligent, menu-driven approach.

### Key Statistics
- **Lines of Code**: 39,000+ (Python & YAML)
- **Tools Available**: 400+ professional tools
- **Ansible Roles**: 10 comprehensive roles
- **Menu Categories**: 15+ major categories
- **Test Coverage**: 90% target (infrastructure ready)
- **Supported Ubuntu**: 20.04, 22.04, 24.04 LTS

### Project Genesis

This project was created entirely through collaboration between John Wyles and Claude using Claude Code. The vision: eliminate the tedious repetition of setting up Ubuntu systems with a professional-grade automation tool.

**Major Achievement**: Successfully refactored a 5,208-line monolithic Python file (`configure_standard_tui.py`) into a clean, modular architecture with no file exceeding 1,200 lines.

## 🏗️ Technical Architecture

### Core Components

1. **TUI System** (`lib/tui/`) - Modular Terminal UI
   ```
   lib/tui/
   ├── __init__.py      # Package initialization
   ├── core.py          # Main orchestrator (255 lines)
   ├── models.py        # Data models - MenuItem (26 lines)
   ├── renderer.py      # Screen rendering (323 lines)
   ├── dialogs.py       # Configuration dialogs (582 lines)
   ├── handlers.py      # Event handling (630 lines)
   ├── config.py        # Config management (208 lines)
   ├── colors.py        # Color definitions (35 lines)
   ├── app.py           # Application class (74 lines)
   └── menus/           # Category-specific builders
       ├── base.py      # Base classes (107 lines)
       ├── development.py   # Dev tools (598 lines)
       ├── desktop.py       # Desktop env (1,192 lines)
       ├── applications.py  # Apps menu (528 lines)
       ├── security.py      # Security (350 lines)
       └── system.py        # System config (350 lines)
   ```

2. **Ansible Automation** (`roles/`)
   - 10 specialized roles for different aspects
   - Idempotent operations throughout
   - Comprehensive error handling
   - Multi-version Ubuntu support

3. **Configuration System**
   - `config.yml` - User selections (git-ignored)
   - `config.example.yml` - Example with defaults
   - YAML-based for portability
   - Ansible variable integration

### Complete Project Structure

```
ubootu/
├── configure_standard_tui.py    # Main entry (26-line wrapper)
├── setup.sh                     # Shell wrapper for setup
├── setup_bootstrap.py           # Python setup orchestrator
├── setup.py                     # Package configuration
├── site.yml                     # Master Ansible playbook
├── bootstrap.yml                # Initial system bootstrap
├── ansible.cfg                  # Ansible configuration
├── requirements.yml             # Ansible dependencies
├── requirements-dev.txt         # Development dependencies
├── pytest.ini                   # Test configuration
├── .coveragerc                  # Coverage settings
├── config.example.yml           # Example configuration
├── 
├── lib/                         # Core Python libraries
│   ├── __init__.py
│   ├── tui/                     # Modular TUI system
│   │   └── [See structure above]
│   ├── ubootu_splash.py         # Animated splash screen
│   ├── show_profile_templates.py # Profile selector
│   ├── menu_ui.py               # Rich-based UI (alternative)
│   ├── tui_dialogs.py           # Curses dialogs (legacy)
│   ├── tui_components.py        # UI components (legacy)
│   └── [Other utility modules]
│
├── roles/                       # Ansible roles
│   ├── common/                  # Base system setup
│   ├── desktop-environment/     # Desktop environments
│   │   ├── tasks/
│   │   │   ├── install-gnome.yml
│   │   │   ├── install-kde.yml
│   │   │   ├── install-hyprland.yml  # Wayland/Hyprland
│   │   │   └── [Other DEs]
│   │   └── templates/           # Config templates
│   ├── development-tools/       # Dev environment
│   ├── applications/            # User applications
│   ├── security/                # Security hardening
│   ├── security-tools/          # Security utilities
│   ├── themes/                  # UI customization
│   ├── app-customization/       # App configs
│   └── dotfiles/                # Dotfile management
│
├── tests/                       # Test suite
│   ├── conftest.py              # Test fixtures
│   ├── lib/                     # Library tests
│   │   └── tui/                 # TUI tests
│   └── [39 test files total]
│
├── group_vars/                  # Global variables
│   └── all/
│       ├── main.yml             # Default settings
│       └── vault.yml            # Secrets template
│
└── inventories/                 # Inventory configs
    └── local/
        └── hosts                # Local inventory
```

## 🎯 Key Files Reference

### Entry Points
- `configure_standard_tui.py` - Main TUI interface
- `setup.sh` - Shell wrapper (runs splash → TUI → Ansible)
- `setup_bootstrap.py` - Python setup orchestrator

### Core TUI Files
- `lib/tui/core.py` - Main TUI application class
- `lib/tui/handlers.py` - Keyboard/event handling
- `lib/tui/renderer.py` - Screen drawing logic
- `lib/tui/config.py` - Configuration state management

### Menu Definitions
- `lib/tui/menus/development.py` - Developer tools menu
- `lib/tui/menus/applications.py` - Applications menu
- `lib/tui/menus/system.py` - System/server configuration

### Configuration
- `config.yml` - User's saved configuration
- `config.example.yml` - Example with all options
- `group_vars/all/main.yml` - Ansible defaults

## 💻 Development Workflow

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/johnwyles/ubootu.git
cd ubootu

# Run the interactive setup
./setup.sh

# Or run TUI directly
./configure_standard_tui.py
```

### Making Changes

1. **Adding New Tools/Applications**:
   ```python
   # Edit appropriate menu file, e.g., lib/tui/menus/development.py
   self.add_selectable("newtool", "New Tool Name", 
       "Description of the tool",
       parent="parent-category")
   ```

2. **Adding Ansible Tasks**:
   ```yaml
   # Create/edit roles/[role-name]/tasks/[task].yml
   - name: Install new tool
     ansible.builtin.apt:
       name: newtool
       state: present
     become: yes
   ```

3. **Testing Changes**:
   ```bash
   # Test TUI compilation
   python3 -m py_compile configure_standard_tui.py
   
   # Run specific tests
   python3 tests/run_tests.py
   
   # Check Ansible syntax
   ansible-playbook site.yml --syntax-check
   ```

## 🔧 Common Tasks & Solutions

### Adding a New Menu Category

1. Create menu builder in `lib/tui/menus/newcategory.py`:
```python
from .base import MenuBuilder

class NewCategoryMenuBuilder(MenuBuilder):
    def build(self):
        self.add_category("newcat", "New Category", 
            "Description", parent="root")
        # Add items...
        return self.items
```

2. Import in `lib/tui/menu_structure.py`:
```python
from .menus.newcategory import NewCategoryMenuBuilder
# Add to build_menu_structure()
```

3. Create corresponding Ansible role in `roles/newcategory/`

### Debugging TUI Issues

```bash
# Enable debug logging
export DEBUG_TUI=1
./configure_standard_tui.py

# Check debug log
tail -f /tmp/debug_tui.log
```

### Working with Configurations

```bash
# Save current config
cp config.yml my-config-backup.yml

# Test with different config
cp config.example.yml config.yml
./setup.sh --restore config.yml

# Validate config
python3 -c "import yaml; yaml.safe_load(open('config.yml'))"
```

## 📊 Testing & Quality

### Test Structure
- **Unit Tests**: `tests/lib/` - Test individual modules
- **Integration Tests**: Test complete workflows
- **Coverage Target**: 90% (currently ~35% actual implementation)

### Running Tests
```bash
# Run all tests
python3 tests/run_tests.py

# Run with coverage (requires pytest)
pytest tests/ -v --cov=lib --cov-report=html

# Check specific module
python3 tests/lib/tui/test_models.py
```

### Code Quality
```bash
# Format code (if black installed)
black lib/ tests/

# Lint code (if flake8 installed)
flake8 lib/ --max-line-length=120

# Type checking (if mypy installed)
mypy lib/
```

## 🚨 Important Patterns & Conventions

### Menu Item IDs
- Use kebab-case: `"docker-ce"`, `"vscode-extensions"`
- Must be unique across entire menu structure
- Used as Ansible variable names

### Ansible Variables
- Menu item selections → `selected_items` list
- Configurable values → Individual variables
- Example: `swappiness` slider → `system_swappiness` variable

### Selection States
- Categories show indicators: ● (all), ◐ (partial), ○ (none)
- Items can be selected/deselected
- Defaults marked with `default=True`

### Error Handling
```python
# Always handle curses errors
try:
    # TUI operations
except curses.error:
    # Graceful fallback
```

## 🎨 UI/UX Guidelines

### Visual Hierarchy
1. **Headers**: Box-drawn with title
2. **Categories**: Bold with selection indicators
3. **Items**: Normal text with [X] selection
4. **Help**: F1 key, bottom bar
5. **Navigation**: Arrow keys + shortcuts

### Color Scheme (Monochrome)
- Currently uses no colors (COLOR_* = 0)
- Relies on text attributes (bold, reverse)
- Works in all terminal environments

### Responsive Design
- Minimum: 80x24 terminal
- Adapts to larger terminals
- Handles resize events

## 🔐 Security Considerations

### Sensitive Data
- Never store passwords in `config.yml`
- Use Ansible vault for secrets
- Git-ignore user configurations

### Privilege Escalation
- Use `become: yes` only when needed
- Validate user input
- Check file permissions

## 🚀 Performance Optimization

### TUI Performance
- Minimal screen redraws
- Efficient menu traversal
- Lazy loading where possible

### Ansible Performance
- Parallel execution where safe
- Fact caching enabled
- Smart package installation

## 📚 Extending the Project

### Adding Wayland/Hyprland Support (Already Done!)
- Full implementation in `roles/desktop-environment/`
- Includes greetd, waybar, wofi configurations
- Ubuntu 24.04+ required
- NVIDIA compatibility warnings

### Future Enhancements
1. **Cloud Deployments**: Terraform integration
2. **Container Support**: Dockerfile generation
3. **Profile Sharing**: Community repository
4. **Web Interface**: Alternative to TUI
5. **macOS/WSL**: Cross-platform support

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure you're in project root
   cd /path/to/ubootu
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **Curses Errors**:
   ```bash
   # Check terminal
   echo $TERM  # Should be xterm-256color or similar
   ```

3. **Ansible Failures**:
   ```bash
   # Run with verbose
   ansible-playbook site.yml -vvv --check
   ```

### Debug Mode
```python
# Add debug prints in TUI
import sys
print("Debug info", file=sys.stderr)
```

## 📈 Project Metrics

### Code Distribution
- **Python**: ~15,000 lines (TUI + utilities)
- **YAML**: ~24,000 lines (Ansible + configs)
- **Tests**: ~3,000 lines (growing)
- **Documentation**: ~2,000 lines

### Complexity Metrics
- **Largest File**: `lib/tui/menus/desktop.py` (1,192 lines)
- **Most Complex**: Event handling and menu navigation
- **Critical Path**: Menu selection → Config generation → Ansible execution

## 🤝 Collaboration Tips for Claude Code

### Effective Prompting
1. **Be Specific**: "Add PostgreSQL 15 to system menu" vs "Add database"
2. **Context**: "Following the existing pattern in development.py..."
3. **Constraints**: "Keep files under 1000 lines"

### Code Generation
- Request modular additions
- Ask for tests with implementation
- Specify Ansible best practices

### Review Patterns
- Check idempotency
- Verify error handling
- Ensure documentation updates

## 🎯 Quick Command Reference

```bash
# Development
./configure_standard_tui.py     # Run TUI
python3 tests/run_tests.py      # Run tests
ansible-playbook site.yml --check  # Dry run

# Configuration
cp config.yml backups/          # Backup config
vi config.yml                   # Edit manually
./setup.sh --restore config.yml # Apply config

# Debugging
export DEBUG_TUI=1              # Enable TUI debug
tail -f /tmp/debug_tui.log      # View debug log
ansible-playbook -vvv           # Verbose Ansible

# Git Operations
git status                      # Check changes
git add -A                      # Stage all
git commit -m "message"         # Commit
git push origin main            # Push changes
```

## 📋 Variable Reference

### Key Variables in config.yml
```yaml
metadata:
  version: "1.0"
  created_at: "timestamp"
  
selected_items:
  - item-id-1
  - item-id-2

configurable_items:
  swappiness:
    id: "swappiness"
    value: 10
    
ansible_variables:
  desktop_environment: "gnome"
  enable_firewall: true
```

## 🏆 Best Practices Summary

1. **Always Test**: Run tests before committing
2. **Document Changes**: Update relevant .md files
3. **Follow Patterns**: Maintain consistency
4. **Consider Ubuntu Versions**: Test compatibility
5. **Security First**: Never commit secrets
6. **User Experience**: Keep it intuitive
7. **Performance**: Optimize for large selections
8. **Error Handling**: Fail gracefully
9. **Modularity**: Keep files focused
10. **Community**: Consider upstream contributions

---

*This document is the primary reference for Claude Code instances working on Ubootu. It represents accumulated knowledge from the project's development and should be updated as the project evolves.*

**Last Updated**: November 2024
**Primary Maintainer**: John Wyles
**AI Assistant**: Claude (Anthropic)
**Built with**: Claude Code