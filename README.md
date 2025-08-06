# 🚀 Ubootu - Ubuntu Configuration Automation

[![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04%20%7C%2022.04%20%7C%2024.04-orange)](https://ubuntu.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Tools](https://img.shields.io/badge/Tools-500+-green)](TOOLS.md)
[![CI](https://github.com/johnwyles/ubootu/actions/workflows/ci.yml/badge.svg)](https://github.com/johnwyles/ubootu/actions/workflows/ci.yml)

**Configure your perfect Ubuntu setup once. Deploy it anywhere, anytime.**

Ubootu is a comprehensive Ubuntu configuration tool that automates the setup of development environments, applications, and system settings through an intuitive TUI (Terminal User Interface) and Ansible automation.

## ✨ Quick Install

```bash
# One-line installer (coming soon)
curl -fsSL https://raw.githubusercontent.com/johnwyles/ubootu/main/install.sh | bash

# Or clone and run
git clone https://github.com/johnwyles/ubootu.git
cd ubootu
./setup.sh
```

## 🎯 Key Features

- **🎨 Intuitive TUI** - Beautiful terminal interface with 500+ tools organized by category
- **💾 Configuration as Code** - Save your setup to `config.yml` and version control it
- **🚀 One Command Deploy** - Apply your saved configuration to any Ubuntu machine
- **🔒 Security First** - Built-in hardening options and security tools
- **📦 Comprehensive Coverage** - Development, desktop, server, security, and more

## 📋 What Can Ubootu Configure?

### Development (50+ categories)
- **Languages**: Python, Go, Rust, Node.js, Java, C/C++, .NET, Ruby, PHP
- **IDEs & Editors**: VS Code, JetBrains Suite, Neovim, Sublime, Zed
- **DevOps**: Docker, Kubernetes, Terraform, Ansible, CI/CD tools
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, DBeaver
- **Cloud Tools**: AWS, Azure, GCP CLIs and SDKs

### Desktop & Applications
- **Desktop Environments**: GNOME, KDE, XFCE, MATE, Cinnamon
- **Browsers**: Firefox, Chrome, Brave, Opera, Vivaldi
- **Communication**: Slack, Discord, Teams, Telegram, Signal
- **Productivity**: LibreOffice, Obsidian, Notion, Todoist
- **Multimedia**: VLC, OBS, GIMP, Kdenlive, Audacity

### System & Security
- **Security Testing**: Nmap, Wireshark, Metasploit, Burp Suite
- **Privacy Tools**: Tor, VPNs, KeePassXC, VeraCrypt
- **System Tools**: htop, glances, ncdu, monitoring tools
- **Networking**: SSH, firewall, network analysis tools
- **Virtualization**: VirtualBox, VMware, QEMU/KVM

### Specialized Categories
- **AI & ML**: TensorFlow, PyTorch, Jupyter, CUDA tools
- **Gaming**: Steam, Lutris, Wine, game development tools
- **Multimedia Production**: DAWs, video editors, 3D tools
- **Graphics & Design**: Blender, Inkscape, Krita, Figma

[📚 **View Complete Tools List**](TOOLS.md)

## 🚀 Usage

### First Time Setup
1. Run `./setup.sh` to launch the TUI
2. Navigate categories and select your tools
3. Press `S` to save your configuration
4. Press `P` to apply and install

### Deploy Saved Configuration
```bash
# Copy your config.yml to a new machine, then:
./setup.sh --restore config.yml
```

### Keyboard Shortcuts
- **↑↓** Navigate | **Space** Select | **Enter** Enter menu | **ESC** Back
- **S** Save config | **P** Apply config | **Q** Quit
- **Ctrl+D** Show diff | **Ctrl+S** Scan system | **Ctrl+M** Toggle mode
- **A/D** Select/Deselect all in category

## 💡 Recommended Workflow

1. **Fork this repository** to maintain your own version
2. **Configure once** using the TUI
3. **Commit your `config.yml`** to your fork
4. **Deploy anywhere** by cloning your fork and running restore

## 📁 Project Structure

```
ubootu/
├── configure_standard_tui.py  # TUI interface
├── setup.sh                   # Main entry point
├── install.sh                 # One-line installer
├── config.yml                 # Your configuration (gitignored)
├── lib/tui/                   # TUI components
├── roles/                     # Ansible roles
└── site.yml                   # Ansible playbook
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Credits

Created by [John Wyles](https://github.com/johnwyles) with [Claude Code](https://claude.ai/code)

---

*Making Ubuntu setup a breeze, one configuration at a time* 🚀