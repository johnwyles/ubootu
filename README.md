# 🚀 Ubootu - Professional Ubuntu Desktop & Server Configuration Tool

[![Ubuntu Support](https://img.shields.io/badge/Ubuntu-20.04%20%7C%2022.04%20%7C%2024.04-orange)](https://ubuntu.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ansible](https://img.shields.io/badge/Ansible-2.15+-red)](https://www.ansible.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Test Suite](https://github.com/johnwyles/ubootu/actions/workflows/test.yml/badge.svg)](https://github.com/johnwyles/ubootu/actions/workflows/test.yml)
[![CI](https://github.com/johnwyles/ubootu/actions/workflows/ci.yml/badge.svg)](https://github.com/johnwyles/ubootu/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/johnwyles/ubootu/branch/main/graph/badge.svg)](https://codecov.io/gh/johnwyles/ubootu)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-purple)](https://claude.ai/code)

[![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-41K+-brightgreen)](https://github.com/johnwyles/ubootu)
[![Tools Available](https://img.shields.io/badge/Tools-500+-blue)](https://github.com/johnwyles/ubootu)
[![Ansible Roles](https://img.shields.io/badge/Ansible%20Roles-10-red)](https://github.com/johnwyles/ubootu/tree/main/roles)
[![Languages](https://img.shields.io/github/languages/count/johnwyles/ubootu)](https://github.com/johnwyles/ubootu)
[![Top Language](https://img.shields.io/github/languages/top/johnwyles/ubootu)](https://github.com/johnwyles/ubootu)
[![Contributors](https://img.shields.io/github/contributors/johnwyles/ubootu)](https://github.com/johnwyles/ubootu/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/johnwyles/ubootu)](https://github.com/johnwyles/ubootu/commits/main)

**Ubootu** is a professional Ubuntu configuration tool created by John Wyles using Claude Code. Born from the frustration of repeatedly setting up new Ubuntu machines, this project provides a comprehensive, menu-driven solution for configuring both desktop workstations and servers with 500+ curated tools and applications.

📚 **[View Complete Tools Documentation](TOOLS.md)** - Detailed list of all available tools with descriptions and links

## ✨ Why Ubootu?

Setting up a new Ubuntu machine is a time-consuming process. Whether you're a developer, system administrator, or power user, you've likely spent hours:
- Installing the same tools and applications
- Configuring system settings
- Setting up development environments
- Hardening security
- Customizing the desktop

**Ubootu solves this problem once and for all.** Configure your system once, save your configuration, and apply it to any number of machines. It's that simple.

## 🎯 Key Features

- **🎨 Beautiful Rich TUI**: Enhanced interface with emojis, better indicators (◉=all, ◎=partial, ○=none)
- **💾 Configuration Persistence**: Save your setup as `config.yml` and reuse it forever
- **🛠️ 500+ Professional Tools**: Curated selection across development, security, productivity
- **🚀 Desktop & Server Support**: Configure workstations, servers, or both
- **📚 Help System**: Press H for detailed help on any item
- **🔤 Smart Font Configuration**: Dynamic font selection based on installed packages
- **⚡ Community Defaults**: Pre-selected popular tools based on developer surveys
- **🔧 Modular Architecture**: Clean Ansible roles, easy to extend and customize
- **🔒 Security First**: Built-in security hardening options
- **🎯 Linux-Only Tools**: All tools verified to work on Ubuntu/Linux

## 📋 System Requirements

- **OS**: Ubuntu 20.04 LTS, 22.04 LTS, or 24.04 LTS
- **Memory**: 4GB RAM minimum (8GB+ recommended)
- **Storage**: 10GB free space minimum
- **Terminal**: Modern terminal emulator with UTF-8 support
- **Privileges**: sudo access required

## 🚀 Quick Start

### First Time Setup

```bash
# Clone the repository
git clone https://github.com/johnwyles/ubootu.git
cd ubootu

# Run the interactive setup
./setup.sh
```

The TUI will guide you through selecting and configuring your tools. Your selections are saved to `config.yml`.

### Reusing Your Configuration

Once you have a `config.yml` you like:

```bash
# On a new machine, clone the repo
git clone https://github.com/johnwyles/ubootu.git
cd ubootu

# Copy your config.yml to the new machine
# Then apply it with one command:
./setup.sh --restore config.yml
```

That's it! Your new machine will be configured exactly like your previous one.

## 💡 Recommended Workflow: Fork and Personalize

We strongly recommend forking this repository to maintain your own version:

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ubootu.git
   cd ubootu
   ```
3. **Configure your system** using the TUI
4. **Commit your `config.yml`** to your fork:
   ```bash
   git add config.yml
   git commit -m "Add my personal configuration"
   git push origin main
   ```
5. **On new machines**, clone your fork and run:
   ```bash
   ./setup.sh --restore config.yml
   ```

This way, you always have your configuration backed up and versioned!

## 📚 What Can Ubootu Configure?

### 🖥️ Desktop Environments
- GNOME, KDE Plasma, XFCE, MATE, Cinnamon
- Themes, icons, fonts, and appearance settings
- Display scaling, font sizes, cursor themes
- Keyboard shortcuts and input methods

### 👨‍💻 Development Tools
- **Editors/IDEs**: VS Code, PyCharm, IntelliJ IDEA, Neovim, Sublime Text, Zed
- **Languages**: Python, Node.js, Go, Rust, Java, .NET, Ruby, PHP, C/C++
- **Containers**: Docker CE, Docker Compose, Kubernetes, Podman, Helm
- **Version Control**: Git, LazyGit, GitKraken, SmartGit, GitHub Desktop
- **Modern CLI**: bat, ripgrep, fd, exa, fzf, starship, glances, and 50+ more
- **Database Tools**: DBeaver, pgAdmin, MySQL Workbench, MongoDB Compass

### 🌐 Server Configuration
- **Web Servers**: Nginx, Apache, Caddy, HAProxy, Traefik
- **Databases**: PostgreSQL, MySQL/MariaDB, MongoDB, Redis
- **Services**: SSH server, FTP, NFS, Samba, rsync
- **Monitoring**: Prometheus, Grafana, Netdata, Zabbix
- **Security**: Fail2ban, UFW, certificate management

### 🔒 Security & Privacy
- Firewall configuration (UFW)
- SSH hardening and key generation
- VPN servers (WireGuard, OpenVPN)
- Password managers (KeePassXC, Bitwarden)
- Encryption tools (VeraCrypt, GnuPG)
- Privacy tools (Tor Browser, secure messengers)

### 📱 Applications
- Web browsers, email clients, office suites
- Media players, image/video editors
- Communication tools (Slack, Discord, Teams)
- Productivity apps and utilities

## 📖 Configuration Examples

### Minimal Developer Setup
```yaml
selected_items:
  - git
  - vscode
  - python
  - docker
  - ripgrep
  - fzf
```

### Full Stack Developer
```yaml
selected_items:
  - vscode
  - git
  - nodejs
  - python
  - postgresql
  - redis
  - docker
  - nginx
  - postman
```

### Security Professional
```yaml
selected_items:
  - wireshark
  - nmap
  - burpsuite
  - metasploit
  - john
  - hashcat
  - tor-browser
  - veracrypt
```

### Home Server
```yaml
selected_items:
  - ssh-server
  - nginx
  - docker
  - portainer
  - nextcloud
  - jellyfin
  - samba
  - fail2ban
```

See `config.example.yml` for a complete example with sensible defaults.

## ⌨️ TUI Navigation

- **↑↓ Arrow Keys**: Navigate menu items
- **→ Enter**: Enter submenu or configure item
- **← Backspace/ESC**: Go back
- **Space**: Toggle selection
- **A**: Select all in category
- **N**: Deselect all in category
- **F1**: Actions menu (install, save, reset)
- **H**: Detailed help for current item (NEW!)
- **S**: Save configuration
- **R**: Run installation
- **Q**: Quit

## 🏗️ Architecture

```
ubootu/
├── configure_standard_tui.py  # TUI entry point
├── setup.sh                   # Main setup script
├── config.yml                 # Your configuration (git-ignored)
├── config.example.yml         # Example configuration
├── TOOLS.md                   # Complete tools documentation (NEW!)
├── lib/
│   ├── enhanced_menu_ui.py    # Beautiful Rich-based TUI
│   └── ...
├── roles/                     # Ansible roles
│   ├── applications/
│   ├── development-tools/
│   ├── desktop-environment/
│   ├── security/
│   └── ...
└── site.yml                   # Master Ansible playbook
```

## 🤝 Contributing

We welcome contributions! Whether it's adding new tools, improving documentation, or fixing bugs, your help makes Ubootu better for everyone. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on Ubuntu 20.04/22.04/24.04
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Created by**: [John Wyles](https://github.com/johnwyles)
- **Built with**: [Claude Code](https://claude.ai/code) (Anthropic's AI assistant)
- **Powered by**: [Ansible](https://www.ansible.com/) and Python
- **Inspired by**: Years of repetitive Ubuntu setups

## 💬 Support & Community

- **Issues**: [GitHub Issues](https://github.com/johnwyles/ubootu/issues)
- **Discussions**: [GitHub Discussions](https://github.com/johnwyles/ubootu/discussions)
- **Wiki**: [Documentation Wiki](https://github.com/johnwyles/ubootu/wiki)

## 🎉 Why This Project Exists

Like many developers and system administrators, I found myself repeatedly setting up Ubuntu machines with the same tools, configurations, and customizations. Each new machine meant hours of manual work, trying to remember all the tools I needed and their configurations.

Ubootu was born from this frustration. With the help of Claude Code, I created a tool that captures my entire Ubuntu setup in a single configuration file. Now, setting up a new machine takes minutes instead of hours.

The best part? Once you've configured Ubootu to your liking, you'll never have to manually set up an Ubuntu machine again. Your perfect configuration travels with you, ready to deploy whenever you need it.

## 🚀 Get Started Now

Don't waste another minute manually configuring Ubuntu. Clone Ubootu, run the setup, and create your perfect configuration today. Your future self will thank you!

```bash
git clone https://github.com/johnwyles/ubootu.git
cd ubootu
./setup.sh
```

---

*Built with ❤️ by John Wyles and Claude | Making Ubuntu setup a breeze, one configuration at a time*