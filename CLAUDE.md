# CLAUDE.md - AI Assistant Context for Ubootu Project

## Project Overview

**Ubootu** is a professional Ubuntu desktop configuration tool - an advanced Ansible-based project for setting up and customizing Ubuntu Desktop environments (20.04, 22.04, 24.04). The project features an intuitive TUI interface, 400+ professional tools, and comprehensive configuration management through an interactive hierarchical menu system.

### Key Features
- 🎨 Intuitive TUI interface with colorful design and radio button indicators
- 🛠️ 400+ professional tools across 15 categories
- 🎯 Smart visual indicators for category selection status
- 💾 Save & continue functionality for iterative configuration
- 🚀 Professional animated splash screen with ASCII art
- 📊 Hierarchical menu system optimized for 80x24 terminals
- ⚡ Support for multiple desktop environments (GNOME, KDE, XFCE, MATE, Cinnamon)
- 🔧 Modular role-based architecture
- 🔒 Comprehensive security hardening options
- 📂 Advanced dotfiles management

## Project Structure

```
unbootu/
├── configure_standard_tui.py    # Sexy hierarchical TUI interface
├── setup.sh                     # Main setup script (splash + TUI + ansible)
├── site.yml             # Master playbook
├── bootstrap.yml        # Initial system bootstrap
├── requirements.yml     # Ansible collection dependencies
├── config.yml          # User configuration (created by wizard, git-ignored)
├── lib/                      # Ubootu core libraries
│   ├── unbootu_splash.py    # Epic splash screen with animations
│   ├── show_profile_templates.py  # Profile selection interface
│   └── menu_ui.py           # TUI components and utilities
├── roles/              # Comprehensive Ansible roles
│   ├── common/         # Base system configuration
│   ├── desktop-environment/  # Desktop environment setup
│   ├── development-tools/    # 100+ development tools
│   ├── applications/        # 200+ applications across categories
│   ├── security/           # Security hardening
│   ├── security-tools/     # Security and privacy tools
│   ├── themes/            # Desktop themes and customization
│   ├── app-customization/ # Application-specific configurations
│   └── dotfiles/          # Advanced dotfiles management
├── group_vars/         # Global default variables
│   └── all/
│       ├── main.yml    # Default settings
│       └── vault.yml   # Encrypted secrets template
└── inventories/        # Environment-specific configs
    ├── local/         # For local machine setup
    └── production/    # For remote machines
```

## Key Files

### Configuration Wizard (`configure_wizard.py`)
- Python 3 script with colored terminal output
- Walks through all configuration options
- Saves preferences to `config.yml`
- Supports single/multiple choice and yes/no questions

### Setup Script (`setup.sh`)
- Checks Ubuntu compatibility
- Installs prerequisites (Ansible, Python)
- Runs the configuration wizard
- Executes Ansible playbooks with user config

### Master Playbook (`site.yml`)
- Orchestrates all roles
- Uses tags for selective execution
- Respects user configuration from `config.yml`

## Variable Precedence

Variables can be overridden at multiple levels (highest to lowest priority):
1. `config.yml` - User preferences from wizard
2. `host_vars/` - Host-specific overrides
3. `inventories/*/group_vars/` - Environment-specific
4. `group_vars/all/` - Global defaults
5. `roles/*/defaults/` - Role defaults

## Development Guidelines

### Adding New Software/Tools
1. Check which role it belongs to (applications, development-tools, etc.)
2. Add to appropriate defaults file
3. Create task file if complex installation
4. Add to wizard options in `configure_wizard.py`

### Ansible Best Practices
- Always make tasks idempotent
- Use `become: yes` only when needed
- Tag tasks appropriately
- Use handlers for service restarts
- Validate configurations before applying

### Testing
- Use `--check` mode for dry runs
- Test with specific tags: `ansible-playbook site.yml --tags "desktop"`
- Molecule tests are planned but not yet implemented

## Common Commands

```bash
# Run the configuration wizard
./configure_wizard.py

# Run complete setup (wizard + ansible)
./setup.sh

# Run ansible with existing config
ansible-playbook site.yml --ask-become-pass

# Run specific role/tag
ansible-playbook site.yml --tags "applications" --ask-become-pass

# Dry run
ansible-playbook site.yml --check --ask-become-pass

# Use different inventory
ansible-playbook -i inventories/production/hosts site.yml
```

## Important Notes

### Security Considerations
- The wizard can configure SSH hardening, firewall, and fail2ban
- Secrets should go in `vault.yml` and be encrypted
- Never commit `config.yml` (it's git-ignored)

### Idempotency
- All playbooks must be safe to run multiple times
- Use `changed_when` and `failed_when` appropriately
- Check for existing configurations before modifying

### Ubuntu Compatibility
- Tested on Ubuntu 20.04, 22.04, 24.04
- Some packages may vary between versions
- Desktop environments may have version-specific features

## TODO/Incomplete Items
1. `development-tools` role - needs implementation
2. `applications` role - needs implementation  
3. `security` role - needs implementation
4. `dotfiles` role - needs implementation
5. Molecule testing framework
6. Comprehensive documentation (README.md)

## Contributing Guidelines
1. Follow existing patterns and conventions
2. Update the wizard when adding new options
3. Test on fresh Ubuntu installation
4. Ensure idempotency
5. Document any new variables in role defaults

## Debugging Tips
- Run with `-vvv` for verbose output
- Check `ansible.log` for detailed logs
- Use `ansible-playbook --list-tasks` to see what will run
- Test individual roles in isolation first