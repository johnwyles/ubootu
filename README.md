# 🚀 Ubootu - Professional Ubuntu Desktop Configuration Tool

[![Ubuntu Support](https://img.shields.io/badge/Ubuntu-20.04%20%7C%2022.04%20%7C%2024.04-orange)](https://ubuntu.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ansible](https://img.shields.io/badge/Ansible-2.15+-red)](https://www.ansible.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)

**Ubootu** is a professional Ubuntu desktop configuration tool for setting up and customizing Ubuntu Desktop environments with 400+ curated tools, intuitive TUI interface, and comprehensive configuration management.

## ✨ Features

- **🎨 Intuitive TUI Interface**: Beautiful, colorful terminal UI with hierarchical menus and radio button indicators
- **🛠️ 400+ Professional Tools**: Development environments, AI/ML tools, security utilities, productivity applications
- **🎯 Smart Categories**: Visual indicators show selection status (full/partial/empty) at a glance
- **💾 Save & Continue**: Save configurations without installing, then continue customizing
- **🚀 Professional Splash Screen**: Animated startup with colorful ASCII art and clean branding
- **⚡ Enterprise-Ready**: Industry-standard practices, idempotent operations, secure handling
- **📊 Profile Management**: Save, restore, and share configurations with version control
- **🔧 Modular Architecture**: Clean separation of concerns with comprehensive Ansible roles

## 📋 System Requirements

- **OS**: Ubuntu 20.04 LTS, 22.04 LTS, or 24.04 LTS
- **Memory**: 4GB RAM minimum (8GB+ recommended)
- **Storage**: 10GB free space minimum
- **Terminal**: Modern terminal emulator with UTF-8 support
- **Privileges**: sudo access required for system configuration

## 🛠️ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/bootstrap-ubuntu.git
cd bootstrap-ubuntu

# Run the setup
./setup.sh
```

The professional TUI will guide you through:
1. Profile selection (Developer, Security, Creative, Gaming, Minimal)
2. Detailed customization of selected profile
3. Application of configuration via Ansible

## 📚 Categories & Tools

### Development Tools
- **Code Editors**: VS Code, Cursor AI, JetBrains, Neovim, Sublime Text
- **Version Control**: Git, GitKraken, lazygit, GitHub CLI, git-delta
- **Containers**: Docker, Podman, Kubernetes tools (kubectl, k9s, Lens)
- **Languages**: Python, Node.js, Go, Rust, Java, .NET, Ruby, PHP, C/C++

### Modern CLI Tools
- **Core Utils**: ripgrep, fd, bat, eza, dust, procs, sd, bottom
- **Productivity**: fzf, zoxide, McFly, Atuin, tmux, Starship
- **Data Processing**: jq, yq, xsv, Miller, VisiData

### AI & Machine Learning
- **Coding Assistants**: GitHub Copilot, Codeium, Aider, Continue
- **ML Frameworks**: PyTorch, TensorFlow, JAX, scikit-learn
- **LLM Tools**: Ollama, llama.cpp, LangChain, Hugging Face

### Security Tools
- **Defensive**: UFW, Fail2Ban, ClamAV, OpenSnitch, Firejail
- **Privacy**: Bitwarden, KeePassXC, VeraCrypt, Tor Browser
- **Network**: Nmap, Wireshark, tcpdump, Netcat
- **Web Security**: Burp Suite, OWASP ZAP, sqlmap

### Self-Hosted Services
- Nextcloud, Jellyfin, Vaultwarden, Pi-hole, WireGuard Server
- Gitea, Portainer, Uptime Kuma, AdGuard Home

And many more across 17 specialized categories!

## 🎯 Usage

### Interactive Mode (Recommended)
```bash
./setup.sh
```

### Direct TUI Mode
```bash
./setup.sh --tui
```

### Apply Saved Configuration
```bash
./setup.sh --restore config.yml
```

### Custom Configuration
```bash
./setup.sh --custom
```

## ⌨️ TUI Navigation

- **Arrow Keys**: Navigate options
- **Space**: Toggle selection
- **Enter**: Confirm/Enter submenu
- **c**: Change category
- **s**: Search
- **sa**: Select all in category
- **da**: Deselect all in category
- **save**: Save configuration
- **q**: Quit

## 🏗️ Architecture

```
bootstrap-ubuntu/
├── configure_rich_tui.py    # Professional TUI interface
├── setup.sh                 # Main entry point
├── site.yml                 # Ansible orchestration
├── roles/                   # Modular Ansible roles
│   ├── common/
│   ├── desktop-environment/
│   ├── development-tools/
│   └── ...
├── lib/                     # Python modules
│   ├── menu_hierarchy.py    # Hierarchical menu system
│   ├── config_models.py     # Configuration data models
│   └── ...
└── group_vars/             # Default configurations
```

## 🔧 Configuration

Configuration is stored in `config.yml` with the following structure:

```yaml
dev:
  vscode: true
  git: true
lang:
  python: true
  nodejs: true
cli:
  ripgrep: true
  fd: true
  bat: true
# ... etc
```

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bootstrap-ubuntu/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/bootstrap-ubuntu/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bootstrap-ubuntu/discussions)

## 🙏 Acknowledgments

Built with:
- [Ansible](https://www.ansible.com/) - Infrastructure automation
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal UI
- [Python](https://python.org/) - Core programming language

---

**Note**: This tool requires administrative privileges to install software and configure system settings. Always review configurations before applying them to production systems.