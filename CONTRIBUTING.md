# Contributing to Ubootu

First off, thank you for considering contributing to Ubootu! It's people like you that make Ubootu such a great tool for the Ubuntu community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please be respectful and considerate in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ubootu.git
   cd ubootu
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/johnwyles/ubootu.git
   ```
4. **Keep your fork up to date**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include your system information** (Ubuntu version, Python version, etc.)
- **Include any error messages or logs**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **Consider including mockups or examples**

### Adding New Tools or Features

Ubootu is designed to be extensible. When adding new tools or features:

1. **Check if it fits the project scope** - Ubootu focuses on Ubuntu desktop and server configuration
2. **Discuss major changes first** - Open an issue to discuss before starting work
3. **Follow the existing patterns**:
   - Add new tools to appropriate categories in the menu system
   - Create or update Ansible roles as needed
   - Update documentation

#### Adding a New Tool

1. **Update the menu structure** in `lib/tui/menus/`:
   - Find the appropriate category file (e.g., `development.py`, `applications.py`)
   - Add your tool using the existing patterns

2. **Update the Ansible role**:
   - Add installation tasks in the appropriate role under `roles/`
   - Include any necessary configuration

3. **Test thoroughly**:
   - Test installation on Ubuntu 20.04, 22.04, and 24.04
   - Ensure idempotency (running multiple times doesn't break)

### Pull Requests

1. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, concise commit messages
   - Include tests if applicable
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Test the TUI
   ./setup.sh --tui
   
   # Test specific roles
   ansible-playbook site.yml --tags "your-role" --check
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots for UI changes
   - List the Ubuntu versions you tested on

## Development Setup

### Prerequisites

- Ubuntu 20.04, 22.04, or 24.04
- Python 3.8+
- Ansible 2.15+
- Git

### Setting Up Your Environment

```bash
# Install development dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv ansible git

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements-dev.txt  # If available
```

### Running Tests

```bash
# Run Python syntax checks
python3 -m py_compile lib/tui/*.py

# Test the TUI interface
python3 configure_standard_tui.py

# Test Ansible playbooks
ansible-playbook site.yml --check
```

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length of 100 characters
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Type hints are encouraged

### Ansible Style

- Use YAML syntax, not JSON
- Tasks should have descriptive names
- Use `become: yes` only when necessary
- Make tasks idempotent
- Use variables for repeated values
- Tag tasks appropriately

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add support for VS Code extensions

- Add menu items for popular extensions
- Update VS Code role to install extensions
- Add configuration options for extension settings

Fixes #123
```

## Project Structure

```
ubootu/
├── lib/tui/              # TUI implementation
│   ├── core.py          # Main TUI class
│   ├── menus/           # Menu definitions
│   └── ...
├── roles/               # Ansible roles
│   ├── applications/    # Application installations
│   ├── development-tools/
│   └── ...
├── configure_standard_tui.py  # TUI entry point
├── setup.sh             # Main setup script
└── site.yml            # Ansible playbook
```

### Key Components

- **TUI System**: Modular Python-based interface in `lib/tui/`
- **Menu System**: Hierarchical menus defined in `lib/tui/menus/`
- **Ansible Roles**: Modular installation and configuration tasks
- **Configuration**: YAML-based configuration system

## Testing Your Contributions

Before submitting:

1. **Test on clean Ubuntu installations** (use VMs or containers)
2. **Test all affected menu paths** in the TUI
3. **Verify Ansible tasks are idempotent**
4. **Check for syntax errors and linting issues**
5. **Update documentation** if needed

## Documentation

- Update the README.md if you add new features
- Add comments to complex code sections
- Update CLAUDE.md if you change core functionality
- Include examples in documentation

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Reach out to the maintainers

## Recognition

Contributors will be recognized in:
- The project's contributor list
- Release notes for significant contributions
- Special mentions for major features

Thank you for contributing to Ubootu! Your efforts help make Ubuntu setup easier for everyone.

---

**Remember**: The best contributions are those that benefit the entire Ubuntu community. Whether it's fixing a bug, adding a new tool, improving documentation, or enhancing the user experience - every contribution matters!