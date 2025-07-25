# 📚 Ubootu Tools Documentation

**Complete catalog of all 500+ tools available in Ubootu with descriptions, links, and installation details**

---

## 📋 Table of Contents

1. [Development Tools](#-development-tools)
   - [IDEs & Editors](#-ides--editors)
   - [Programming Languages](#-programming-languages)
   - [Development Tools](#-development-tools-1)
   - [Containers & DevOps](#-containers--devops)
   - [Modern CLI Tools](#-modern-cli-tools)
   - [Version Managers](#-version-managers)
2. [Desktop Environment](#-desktop-environment)
   - [Desktop Environments](#-desktop-environments)
   - [Themes & Appearance](#-themes--appearance)
   - [Fonts & Typography](#-fonts--typography)
   - [Wayland/Hyprland Tools](#-waylandhyprland-specific-tools)
3. [Applications](#-applications)
   - [Web Browsers](#-web-browsers)
   - [Media & Graphics](#-media--graphics)
   - [Communication](#-communication)
   - [Productivity](#-productivity)
   - [Cloud Storage](#-cloud-storage)
   - [System Utilities](#-system-utilities)
4. [Security & Privacy](#-security--privacy)
   - [Firewall & Network](#-firewall--network-security)
   - [Privacy & Encryption](#-privacy--encryption)
   - [Security Testing Tools](#-security-testing-tools)
5. [System Configuration](#-system-configuration)
   - [Performance](#-performance-optimization)
   - [System Monitoring](#-system-monitoring)

---

## 💻 Development Tools

### 🛠️ IDEs & Editors

#### Visual Studio Code
- **ID**: `vscode`
- **Description**: Microsoft's free, open-source code editor with excellent language support, debugging, Git integration, and a vast extension ecosystem
- **Installation**: Snap package
- **Homepage**: [code.visualstudio.com](https://code.visualstudio.com/)
- **Default**: ✅ Yes

#### IntelliJ IDEA Community
- **ID**: `intellij-idea`
- **Description**: JetBrains' powerful Java IDE with smart code completion, refactoring tools, and built-in version control
- **Installation**: Snap package
- **Homepage**: [jetbrains.com/idea](https://www.jetbrains.com/idea/)
- **Default**: ✅ Yes

#### PyCharm Community
- **ID**: `pycharm`
- **Description**: The best Python IDE with intelligent code completion, debugging, testing, and virtual environment management
- **Installation**: Snap package
- **Homepage**: [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- **Default**: ✅ Yes

#### WebStorm
- **ID**: `webstorm`
- **Description**: JetBrains JavaScript IDE for modern web development with React, Angular, Vue.js support
- **Installation**: Snap package
- **Homepage**: [jetbrains.com/webstorm](https://www.jetbrains.com/webstorm/)
- **Default**: ❌ No

#### Sublime Text
- **ID**: `sublime`
- **Description**: Sophisticated text editor with multiple cursors, command palette, and powerful API
- **Installation**: APT repository
- **Homepage**: [sublimetext.com](https://www.sublimetext.com/)
- **Default**: ❌ No

#### Vim
- **ID**: `vim`
- **Description**: Terminal-based text editor with modal editing, macros, and extensive customization
- **Installation**: APT package
- **Homepage**: [vim.org](https://www.vim.org/)
- **Default**: ❌ No

#### NeoVim
- **ID**: `neovim`
- **Description**: Modern Vim fork with Lua scripting, LSP support, and tree-sitter integration
- **Installation**: APT package
- **Homepage**: [neovim.io](https://neovim.io/)
- **Default**: ❌ No

#### Emacs
- **ID**: `emacs`
- **Description**: Extensible text editor and computing environment with Lisp customization
- **Installation**: APT package
- **Homepage**: [gnu.org/software/emacs](https://www.gnu.org/software/emacs/)
- **Default**: ❌ No

#### Zed
- **ID**: `zed`
- **Description**: High-performance multiplayer code editor built in Rust with AI integration
- **Installation**: Custom installer
- **Homepage**: [zed.dev](https://zed.dev/)
- **Default**: ❌ No

### 🗣️ Programming Languages

#### Python
- **ID**: `python`
- **Description**: Python 3 runtime with pip package manager. The most popular language for scripting, web development, data science, and automation
- **Installation**: APT packages (python3, python3-pip, python3-venv)
- **Homepage**: [python.org](https://www.python.org/)
- **Default**: ✅ Yes

#### Node.js
- **ID**: `nodejs`
- **Description**: JavaScript runtime built on Chrome's V8 engine. Essential for modern web development with npm package manager
- **Installation**: NodeSource repository (LTS version)
- **Homepage**: [nodejs.org](https://nodejs.org/)
- **Default**: ✅ Yes

#### Java
- **ID**: `java`
- **Description**: Java Development Kit (OpenJDK) for Java application development
- **Installation**: APT package (default-jdk)
- **Homepage**: [openjdk.org](https://openjdk.org/)
- **Default**: ✅ Yes

#### Go
- **ID**: `go`
- **Description**: Go programming language for building simple, reliable, and efficient software
- **Installation**: Official Go installer
- **Homepage**: [go.dev](https://go.dev/)
- **Default**: ❌ No

#### Rust
- **ID**: `rust`
- **Description**: Memory-safe systems programming language with cargo package manager
- **Installation**: rustup installer
- **Homepage**: [rust-lang.org](https://www.rust-lang.org/)
- **Default**: ❌ No

#### C/C++
- **ID**: `cpp`
- **Description**: GCC compiler and build tools for C/C++ development
- **Installation**: APT packages (build-essential, gcc, g++, make, cmake)
- **Homepage**: [gcc.gnu.org](https://gcc.gnu.org/)
- **Default**: ❌ No

#### PHP
- **ID**: `php`
- **Description**: PHP interpreter with composer package manager for web development
- **Installation**: APT packages (php, php-cli, composer)
- **Homepage**: [php.net](https://www.php.net/)
- **Default**: ❌ No

#### Ruby
- **ID**: `ruby`
- **Description**: Ruby interpreter with gem package manager for web apps and scripting
- **Installation**: rbenv or APT package
- **Homepage**: [ruby-lang.org](https://www.ruby-lang.org/)
- **Default**: ❌ No

#### .NET
- **ID**: `dotnet`
- **Description**: .NET SDK and runtime for building cross-platform applications
- **Installation**: Microsoft repository
- **Homepage**: [dotnet.microsoft.com](https://dotnet.microsoft.com/)
- **Default**: ❌ No

### 🔧 Development Tools

#### Git
- **ID**: `git`
- **Description**: Distributed version control system for tracking code changes
- **Installation**: APT package
- **Homepage**: [git-scm.com](https://git-scm.com/)
- **Default**: ✅ Yes

#### Docker
- **ID**: `docker`
- **Description**: Platform for building, sharing, and running containerized applications
- **Installation**: Docker CE repository
- **Homepage**: [docker.com](https://www.docker.com/)
- **Default**: ✅ Yes

#### Postman
- **ID**: `postman`
- **Description**: API development platform for building, testing, and documenting APIs
- **Installation**: Snap package
- **Homepage**: [postman.com](https://www.postman.com/)
- **Default**: ❌ No

#### Insomnia
- **ID**: `insomnia`
- **Description**: Open-source API client for REST, GraphQL, and gRPC
- **Installation**: Snap package
- **Homepage**: [insomnia.rest](https://insomnia.rest/)
- **Default**: ❌ No

#### DBeaver
- **ID**: `dbeaver`
- **Description**: Universal database tool supporting all major databases
- **Installation**: Snap package
- **Homepage**: [dbeaver.io](https://dbeaver.io/)
- **Default**: ❌ No

#### MySQL Workbench
- **ID**: `mysql-workbench`
- **Description**: Official MySQL GUI for database design and administration
- **Installation**: APT package
- **Homepage**: [mysql.com/products/workbench](https://www.mysql.com/products/workbench/)
- **Default**: ❌ No

#### pgAdmin
- **ID**: `pgadmin`
- **Description**: Feature-rich PostgreSQL administration and development platform
- **Installation**: APT repository
- **Homepage**: [pgadmin.org](https://www.pgadmin.org/)
- **Default**: ❌ No

#### Redis Desktop Manager
- **ID**: `redis-desktop`
- **Description**: Cross-platform Redis GUI management tool
- **Installation**: Snap package
- **Homepage**: [github.com/RedisInsight/RedisInsight](https://github.com/RedisInsight/RedisInsight)
- **Default**: ❌ No

#### MongoDB Compass
- **ID**: `mongodb-compass`
- **Description**: Official MongoDB GUI for exploring and manipulating data
- **Installation**: DEB package
- **Homepage**: [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
- **Default**: ❌ No

#### GitHub Desktop
- **ID**: `github-desktop`
- **Description**: Official GitHub GUI client for managing repositories
- **Installation**: DEB package
- **Homepage**: [desktop.github.com](https://desktop.github.com/)
- **Default**: ❌ No

#### GitKraken
- **ID**: `gitkraken`
- **Description**: Cross-platform Git GUI with built-in merge conflict editor
- **Installation**: Snap package
- **Homepage**: [gitkraken.com](https://www.gitkraken.com/)
- **Default**: ❌ No

#### SmartGit
- **ID**: `smartgit`
- **Description**: Professional Git GUI with advanced features
- **Installation**: DEB package
- **Homepage**: [syntevo.com/smartgit](https://www.syntevo.com/smartgit/)
- **Default**: ❌ No

#### LazyGit
- **ID**: `lazygit`
- **Description**: Terminal UI for Git commands with intuitive interface
- **Installation**: GitHub release
- **Homepage**: [github.com/jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Default**: ✅ Yes

#### Gittyup
- **ID**: `gittyup`
- **Description**: Clean, fast, and free Git GUI
- **Installation**: AppImage
- **Homepage**: [github.com/Murmele/Gittyup](https://github.com/Murmele/Gittyup)
- **Default**: ❌ No

### 🐳 Containers & DevOps

#### Docker CE
- **ID**: `docker-ce`
- **Description**: Docker Community Edition for container management
- **Installation**: Docker repository
- **Homepage**: [docker.com](https://www.docker.com/)
- **Default**: ✅ Yes

#### Docker Compose
- **ID**: `docker-compose`
- **Description**: Tool for defining and running multi-container Docker applications
- **Installation**: Docker repository (v2)
- **Homepage**: [docs.docker.com/compose](https://docs.docker.com/compose/)
- **Default**: ✅ Yes

#### Podman
- **ID**: `podman`
- **Description**: Daemonless container engine compatible with Docker
- **Installation**: APT package
- **Homepage**: [podman.io](https://podman.io/)
- **Default**: ❌ No

#### Kubernetes
- **ID**: `kubernetes`
- **Description**: kubectl CLI for managing Kubernetes clusters
- **Installation**: Google repository
- **Homepage**: [kubernetes.io](https://kubernetes.io/)
- **Default**: ❌ No

#### Minikube
- **ID**: `minikube`
- **Description**: Local Kubernetes cluster for development
- **Installation**: Binary download
- **Homepage**: [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/)
- **Default**: ❌ No

#### Helm
- **ID**: `helm`
- **Description**: Package manager for Kubernetes applications
- **Installation**: Snap package
- **Homepage**: [helm.sh](https://helm.sh/)
- **Default**: ❌ No

#### Terraform
- **ID**: `terraform`
- **Description**: Infrastructure as Code tool for building and managing cloud resources
- **Installation**: HashiCorp repository
- **Homepage**: [terraform.io](https://www.terraform.io/)
- **Default**: ❌ No

#### Ansible
- **ID**: `ansible`
- **Description**: Automation platform for configuration management
- **Installation**: APT package
- **Homepage**: [ansible.com](https://www.ansible.com/)
- **Default**: ❌ No

#### Vagrant
- **ID**: `vagrant`
- **Description**: Tool for building and managing virtual machine environments
- **Installation**: HashiCorp repository
- **Homepage**: [vagrantup.com](https://www.vagrantup.com/)
- **Default**: ❌ No

### 🚀 Modern CLI Tools

#### bat
- **ID**: `bat`
- **Description**: A cat clone with syntax highlighting, Git integration, and automatic paging
- **Installation**: APT package
- **Homepage**: [github.com/sharkdp/bat](https://github.com/sharkdp/bat)
- **Default**: ✅ Yes

#### exa
- **ID**: `exa`
- **Description**: Modern replacement for ls with colors, Git integration, and tree view
- **Installation**: APT package
- **Homepage**: [github.com/ogham/exa](https://github.com/ogham/exa)
- **Default**: ✅ Yes

#### ripgrep
- **ID**: `ripgrep`
- **Description**: Extremely fast recursive grep that respects .gitignore (rg command)
- **Installation**: APT package
- **Homepage**: [github.com/BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep)
- **Default**: ✅ Yes

#### fd
- **ID**: `fd`
- **Description**: Simple, fast alternative to find with intuitive syntax
- **Installation**: APT package
- **Homepage**: [github.com/sharkdp/fd](https://github.com/sharkdp/fd)
- **Default**: ✅ Yes

#### fzf
- **ID**: `fzf`
- **Description**: Fuzzy finder for terminal - interactive filter for any list
- **Installation**: Git clone + install script
- **Homepage**: [github.com/junegunn/fzf](https://github.com/junegunn/fzf)
- **Default**: ✅ Yes

#### duf
- **ID**: `duf`
- **Description**: Better df alternative with colors and sorting
- **Installation**: GitHub release
- **Homepage**: [github.com/muesli/duf](https://github.com/muesli/duf)
- **Default**: ❌ No

#### dust
- **ID**: `dust`
- **Description**: More intuitive version of du written in Rust
- **Installation**: GitHub release
- **Homepage**: [github.com/bootandy/dust](https://github.com/bootandy/dust)
- **Default**: ❌ No

#### procs
- **ID**: `procs`
- **Description**: Modern replacement for ps with human-readable output
- **Installation**: Snap package
- **Homepage**: [github.com/dalance/procs](https://github.com/dalance/procs)
- **Default**: ❌ No

#### bottom
- **ID**: `bottom`
- **Description**: Yet another cross-platform graphical process/system monitor
- **Installation**: APT package
- **Homepage**: [github.com/ClementTsang/bottom](https://github.com/ClementTsang/bottom)
- **Default**: ❌ No

#### btop++
- **ID**: `btop`
- **Description**: Beautiful resource monitor with mouse support
- **Installation**: APT package
- **Homepage**: [github.com/aristocratos/btop](https://github.com/aristocratos/btop)
- **Default**: ✅ Yes

#### htop
- **ID**: `htop`
- **Description**: Interactive process viewer with colors and mouse support
- **Installation**: APT package
- **Homepage**: [htop.dev](https://htop.dev/)
- **Default**: ✅ Yes

#### glances
- **ID**: `glances`
- **Description**: Cross-platform monitoring tool with web UI
- **Installation**: pip install
- **Homepage**: [github.com/nicolargo/glances](https://github.com/nicolargo/glances)
- **Default**: ✅ Yes

#### delta
- **ID**: `delta`
- **Description**: Syntax-highlighting pager for git, diff, and grep output
- **Installation**: GitHub release
- **Homepage**: [github.com/dandavison/delta](https://github.com/dandavison/delta)
- **Default**: ✅ Yes

#### sd
- **ID**: `sd`
- **Description**: Intuitive find & replace CLI (sed alternative)
- **Installation**: GitHub release
- **Homepage**: [github.com/chmln/sd](https://github.com/chmln/sd)
- **Default**: ❌ No

#### tmux
- **ID**: `tmux`
- **Description**: Terminal multiplexer for managing multiple sessions
- **Installation**: APT package
- **Homepage**: [github.com/tmux/tmux](https://github.com/tmux/tmux)
- **Default**: ✅ Yes

#### zoxide
- **ID**: `zoxide`
- **Description**: Smarter cd command that learns your habits
- **Installation**: GitHub release
- **Homepage**: [github.com/ajeetdsouza/zoxide](https://github.com/ajeetdsouza/zoxide)
- **Default**: ✅ Yes

#### mcfly
- **ID**: `mcfly`
- **Description**: Fly through your shell history with neural networks
- **Installation**: GitHub release
- **Homepage**: [github.com/cantino/mcfly](https://github.com/cantino/mcfly)
- **Default**: ❌ No

#### starship
- **ID**: `starship`
- **Description**: Fast, customizable prompt for any shell
- **Installation**: Shell script installer
- **Homepage**: [starship.rs](https://starship.rs/)
- **Default**: ✅ Yes

#### tldr
- **ID**: `tldr`
- **Description**: Simplified man pages with practical examples
- **Installation**: npm install -g tldr
- **Homepage**: [tldr.sh](https://tldr.sh/)
- **Default**: ✅ Yes

#### navi
- **ID**: `navi`
- **Description**: Interactive cheatsheet tool with fuzzy search
- **Installation**: GitHub release
- **Homepage**: [github.com/denisidoro/navi](https://github.com/denisidoro/navi)
- **Default**: ❌ No

#### zellij
- **ID**: `zellij`
- **Description**: Terminal workspace with layouts and plugins
- **Installation**: GitHub release
- **Homepage**: [zellij.dev](https://zellij.dev/)
- **Default**: ❌ No

#### ncdu
- **ID**: `ncdu`
- **Description**: NCurses disk usage analyzer with delete capability
- **Installation**: APT package
- **Homepage**: [dev.yorhel.nl/ncdu](https://dev.yorhel.nl/ncdu)
- **Default**: ✅ Yes

### 📦 Version Managers

#### nvm
- **Description**: Node Version Manager for installing multiple Node.js versions
- **Installation**: Git clone
- **Homepage**: [github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)

#### pyenv
- **Description**: Python version management tool
- **Installation**: Git clone
- **Homepage**: [github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

#### rbenv
- **Description**: Ruby version manager
- **Installation**: Git clone
- **Homepage**: [github.com/rbenv/rbenv](https://github.com/rbenv/rbenv)

#### rustup
- **Description**: Rust toolchain installer and version manager
- **Installation**: Shell script
- **Homepage**: [rustup.rs](https://rustup.rs/)

#### sdkman
- **Description**: Software Development Kit Manager for JVM languages
- **Installation**: Shell script
- **Homepage**: [sdkman.io](https://sdkman.io/)

#### jenv
- **Description**: Java environment manager
- **Installation**: Git clone
- **Homepage**: [jenv.be](https://www.jenv.be/)

#### gvm
- **Description**: Go Version Manager
- **Installation**: Shell script
- **Homepage**: [github.com/moovweb/gvm](https://github.com/moovweb/gvm)

#### asdf
- **Description**: Universal version manager for multiple languages
- **Installation**: Git clone
- **Homepage**: [asdf-vm.com](https://asdf-vm.com/)

---

## 🖥️ Desktop Environment

### 🏠 Desktop Environments

#### GNOME
- **ID**: `gnome`
- **Description**: Modern desktop with Activities overview and extensions
- **Installation**: ubuntu-desktop meta-package
- **Homepage**: [gnome.org](https://www.gnome.org/)
- **Default**: ✅ Yes

#### KDE Plasma
- **ID**: `kde`
- **Description**: Highly customizable desktop with widgets and effects
- **Installation**: kde-plasma-desktop meta-package
- **Homepage**: [kde.org](https://kde.org/plasma-desktop/)
- **Default**: ❌ No

#### XFCE
- **ID**: `xfce`
- **Description**: Lightweight desktop environment
- **Installation**: xfce4 meta-package
- **Homepage**: [xfce.org](https://xfce.org/)
- **Default**: ❌ No

#### MATE
- **ID**: `mate`
- **Description**: Traditional desktop continuing GNOME 2
- **Installation**: mate-desktop-environment meta-package
- **Homepage**: [mate-desktop.org](https://mate-desktop.org/)
- **Default**: ❌ No

#### Cinnamon
- **ID**: `cinnamon`
- **Description**: Modern desktop with traditional layout
- **Installation**: cinnamon-desktop-environment meta-package
- **Homepage**: [github.com/linuxmint/cinnamon](https://github.com/linuxmint/cinnamon)
- **Default**: ❌ No

#### Budgie
- **ID**: `budgie`
- **Description**: Modern desktop focused on simplicity
- **Installation**: budgie-desktop meta-package
- **Homepage**: [buddiesofbudgie.org](https://buddiesofbudgie.org/)
- **Default**: ❌ No

#### LXQt
- **ID**: `lxqt`
- **Description**: Lightweight Qt-based desktop
- **Installation**: lxqt meta-package
- **Homepage**: [lxqt-project.org](https://lxqt-project.org/)
- **Default**: ❌ No

#### Hyprland
- **Description**: Dynamic tiling Wayland compositor
- **Installation**: PPA or build from source
- **Homepage**: [hyprland.org](https://hyprland.org/)
- **Requirements**: Ubuntu 24.04+ recommended

### 🎨 Themes & Appearance

#### Dark Theme
- **ID**: `theme-dark`
- **Description**: System-wide dark mode for all applications
- **Default**: ✅ Yes

#### Beautiful Icons
- **ID**: `theme-icons`
- **Description**: Papirus icon theme with folder color support
- **Installation**: papirus-icon-theme
- **Homepage**: [github.com/PapirusDevelopmentTeam/papirus-icon-theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)
- **Default**: ✅ Yes

#### Custom Cursors
- **ID**: `theme-cursors`
- **Description**: Better cursor themes (Bibata, Breeze)
- **Default**: ❌ No

#### System Sounds
- **ID**: `theme-sounds`
- **Description**: Pleasant notification and system sounds
- **Default**: ❌ No

### 🔤 Fonts & Typography

#### System Font Packages

##### Ubuntu Font Family
- **ID**: `fonts-ubuntu`
- **Description**: Ubuntu's default font family
- **Installation**: fonts-ubuntu
- **Default**: ✅ Yes

##### Noto Fonts
- **ID**: `fonts-noto`
- **Description**: Google's comprehensive font family supporting all languages
- **Installation**: fonts-noto, fonts-noto-color-emoji
- **Homepage**: [google.com/get/noto](https://www.google.com/get/noto/)
- **Default**: ✅ Yes

##### Liberation Fonts
- **ID**: `fonts-liberation`
- **Description**: Red Hat's metrically compatible fonts
- **Installation**: fonts-liberation
- **Default**: ✅ Yes

##### Roboto
- **ID**: `fonts-roboto`
- **Description**: Android's modern font family
- **Installation**: fonts-roboto
- **Default**: ❌ No

##### Fira Code
- **ID**: `fonts-firacode`
- **Description**: Monospaced font with programming ligatures
- **Installation**: fonts-firacode
- **Homepage**: [github.com/tonsky/FiraCode](https://github.com/tonsky/FiraCode)
- **Default**: ✅ Yes

##### Cascadia Code
- **ID**: `fonts-cascadia`
- **Description**: Microsoft's fun coding font with ligatures
- **Installation**: Manual download
- **Homepage**: [github.com/microsoft/cascadia-code](https://github.com/microsoft/cascadia-code)
- **Default**: ❌ No

##### JetBrains Mono
- **ID**: `fonts-jetbrains`
- **Description**: Font designed for developers
- **Installation**: fonts-jetbrains-mono
- **Homepage**: [jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono/)
- **Default**: ✅ Yes

#### Nerd Fonts (with Icons)

##### JetBrainsMono Nerd Font
- **ID**: `nf-jetbrains`
- **Description**: JetBrains Mono with developer icons
- **Installation**: Nerd Fonts installer
- **Default**: ✅ Yes

##### Hack Nerd Font
- **ID**: `nf-hack`
- **Description**: Clean coding font with icons
- **Installation**: Nerd Fonts installer
- **Default**: ✅ Yes

##### FiraCode Nerd Font
- **ID**: `nf-firacode`
- **Description**: Fira Code with ligatures and icons
- **Installation**: Nerd Fonts installer
- **Default**: ✅ Yes

##### Additional Nerd Fonts
- CascadiaCode Nerd Font
- SourceCodePro Nerd Font
- UbuntuMono Nerd Font
- Inconsolata Nerd Font
- MesloLG Nerd Font

All Nerd Fonts available from: [nerdfonts.com](https://www.nerdfonts.com/)

### 🌊 Wayland/Hyprland Specific Tools

#### wl-clipboard
- **Description**: Command-line copy/paste utilities for Wayland
- **Installation**: APT package
- **Homepage**: [github.com/bugaevc/wl-clipboard](https://github.com/bugaevc/wl-clipboard)

#### wf-recorder
- **Description**: Screen recorder for wlroots-based compositors
- **Installation**: APT package
- **Homepage**: [github.com/ammen99/wf-recorder](https://github.com/ammen99/wf-recorder)

#### wdisplays
- **Description**: GUI display configuration tool for Wayland
- **Installation**: APT package
- **Homepage**: [github.com/artizirk/wdisplays](https://github.com/artizirk/wdisplays)

#### kanshi
- **Description**: Dynamic display configuration
- **Installation**: APT package
- **Homepage**: [github.com/emersion/kanshi](https://github.com/emersion/kanshi)

#### gammastep
- **Description**: Color temperature adjustment (Wayland redshift)
- **Installation**: APT package
- **Homepage**: [gitlab.com/chinstrap/gammastep](https://gitlab.com/chinstrap/gammastep)

#### swayimg
- **Description**: Image viewer for Wayland
- **Installation**: APT package
- **Homepage**: [github.com/artemsen/swayimg](https://github.com/artemsen/swayimg)

#### Additional Wayland Tools
- **wev**: Wayland event viewer
- **waypipe**: Network transparency for Wayland
- **wtype**: xdotool alternative for Wayland
- **wlsunset**: Day/night gamma adjustments
- **clipman**: Clipboard manager
- **wlogout**: Logout menu
- **nwg-launchers**: GTK-based launchers
- **azote**: Wallpaper manager
- **wlr-randr**: xrandr for wlroots
- **swappy**: Screenshot annotation

---

## 📱 Applications

### 🌐 Web Browsers

#### Firefox
- **ID**: `firefox`
- **Description**: Mozilla's privacy-focused web browser
- **Installation**: APT package (pre-installed)
- **Homepage**: [mozilla.org/firefox](https://www.mozilla.org/firefox/)
- **Default**: ✅ Yes

#### Google Chrome
- **ID**: `chrome`
- **Description**: Google's web browser with account sync
- **Installation**: Google repository
- **Homepage**: [google.com/chrome](https://www.google.com/chrome/)
- **Default**: ❌ No

#### Chromium
- **ID**: `chromium`
- **Description**: Open-source base of Chrome
- **Installation**: Snap package
- **Homepage**: [chromium.org](https://www.chromium.org/)
- **Default**: ❌ No

#### Brave
- **ID**: `brave`
- **Description**: Privacy-focused browser with ad blocking
- **Installation**: Brave repository
- **Homepage**: [brave.com](https://brave.com/)
- **Default**: ❌ No

#### Vivaldi
- **ID**: `vivaldi`
- **Description**: Feature-rich customizable browser
- **Installation**: Vivaldi repository
- **Homepage**: [vivaldi.com](https://vivaldi.com/)
- **Default**: ❌ No

#### Opera
- **ID**: `opera`
- **Description**: Browser with free built-in VPN
- **Installation**: Opera repository
- **Homepage**: [opera.com](https://www.opera.com/)
- **Default**: ❌ No

### 🎬 Media & Graphics

#### VLC
- **ID**: `vlc`
- **Description**: Universal media player supporting all formats
- **Installation**: APT package
- **Homepage**: [videolan.org](https://www.videolan.org/)
- **Default**: ✅ Yes

#### mpv
- **ID**: `mpv`
- **Description**: Minimal media player with powerful scripting
- **Installation**: APT package
- **Homepage**: [mpv.io](https://mpv.io/)
- **Default**: ❌ No

#### Spotify
- **ID**: `spotify`
- **Description**: Music streaming service
- **Installation**: Snap package
- **Homepage**: [spotify.com](https://www.spotify.com/)
- **Default**: ❌ No

#### GIMP
- **ID**: `gimp`
- **Description**: GNU Image Manipulation Program
- **Installation**: APT package
- **Homepage**: [gimp.org](https://www.gimp.org/)
- **Default**: ❌ No

#### Inkscape
- **ID**: `inkscape`
- **Description**: Professional vector graphics editor
- **Installation**: APT package
- **Homepage**: [inkscape.org](https://inkscape.org/)
- **Default**: ❌ No

#### Blender
- **ID**: `blender`
- **Description**: 3D creation suite
- **Installation**: Snap package
- **Homepage**: [blender.org](https://www.blender.org/)
- **Default**: ❌ No

#### Kdenlive
- **ID**: `kdenlive`
- **Description**: Non-linear video editor
- **Installation**: APT package
- **Homepage**: [kdenlive.org](https://kdenlive.org/)
- **Default**: ❌ No

#### OBS Studio
- **ID**: `obs`
- **Description**: Open broadcaster for streaming and recording
- **Installation**: PPA repository
- **Homepage**: [obsproject.com](https://obsproject.com/)
- **Default**: ❌ No

### 💬 Communication

#### Slack
- **Description**: Team collaboration platform
- **Installation**: Snap package
- **Homepage**: [slack.com](https://slack.com/)

#### Discord
- **Description**: Voice, video, and text chat
- **Installation**: DEB package
- **Homepage**: [discord.com](https://discord.com/)

#### Microsoft Teams
- **Description**: Business communication platform
- **Installation**: Microsoft repository
- **Homepage**: [microsoft.com/teams](https://www.microsoft.com/teams/)

#### Zoom
- **Description**: Video conferencing
- **Installation**: DEB package
- **Homepage**: [zoom.us](https://zoom.us/)

#### Signal
- **Description**: Privacy-focused messaging
- **Installation**: Signal repository
- **Homepage**: [signal.org](https://signal.org/)

#### Telegram
- **Description**: Cloud-based messaging
- **Installation**: Snap package
- **Homepage**: [telegram.org](https://telegram.org/)

### 📝 Productivity

#### LibreOffice
- **Description**: Complete office suite
- **Installation**: APT package (pre-installed)
- **Homepage**: [libreoffice.org](https://www.libreoffice.org/)

#### Obsidian
- **Description**: Knowledge base with markdown
- **Installation**: AppImage/Snap
- **Homepage**: [obsidian.md](https://obsidian.md/)

#### Notion
- **Description**: All-in-one workspace
- **Installation**: Notion Enhanced (community)
- **Homepage**: [notion.so](https://www.notion.so/)

#### Thunderbird
- **Description**: Email, calendar, and news client
- **Installation**: APT package
- **Homepage**: [thunderbird.net](https://www.thunderbird.net/)

#### Evolution
- **Description**: Email and calendar (GNOME)
- **Installation**: APT package
- **Homepage**: [wiki.gnome.org/Apps/Evolution](https://wiki.gnome.org/Apps/Evolution)

#### Joplin
- **Description**: Open-source note-taking app
- **Installation**: AppImage
- **Homepage**: [joplinapp.org](https://joplinapp.org/)

### ☁️ Cloud Storage

#### Dropbox
- **Description**: Cloud storage with sync
- **Installation**: DEB package
- **Homepage**: [dropbox.com](https://www.dropbox.com/)

#### Insync
- **Description**: Google Drive and OneDrive client
- **Installation**: Insync repository
- **Homepage**: [insynchq.com](https://www.insynchq.com/)

#### OneDrive
- **Description**: Microsoft cloud storage (via rclone)
- **Installation**: rclone + GUI
- **Homepage**: [github.com/abraunegg/onedrive](https://github.com/abraunegg/onedrive)

#### Nextcloud
- **Description**: Self-hosted cloud platform
- **Installation**: Snap package
- **Homepage**: [nextcloud.com](https://nextcloud.com/)

### 🛠️ System Utilities

#### GParted
- **Description**: GNOME partition editor
- **Installation**: APT package
- **Homepage**: [gparted.org](https://gparted.org/)

#### GNOME Disk Utility
- **Description**: Disk management tool
- **Installation**: APT package (gnome-disk-utility)

#### Timeshift
- **Description**: System restore utility
- **Installation**: APT package
- **Homepage**: [github.com/teejee2008/timeshift](https://github.com/teejee2008/timeshift)

#### Deja Dup
- **Description**: Simple backup tool
- **Installation**: APT package
- **Homepage**: [wiki.gnome.org/Apps/DejaDup](https://wiki.gnome.org/Apps/DejaDup)

#### BleachBit
- **Description**: System cleaner
- **Installation**: APT package
- **Homepage**: [bleachbit.org](https://www.bleachbit.org/)

#### Synaptic
- **Description**: Graphical package manager
- **Installation**: APT package

#### GNOME Tweaks
- **Description**: Advanced GNOME settings
- **Installation**: APT package (gnome-tweaks)

#### dconf Editor
- **Description**: Low-level configuration editor
- **Installation**: APT package

---

## 🔒 Security & Privacy

### 🛡️ Firewall & Network Security

#### UFW (Uncomplicated Firewall)
- **ID**: `ufw`
- **Description**: User-friendly netfilter firewall
- **Installation**: APT package (pre-installed)
- **Homepage**: [wiki.ubuntu.com/UncomplicatedFirewall](https://wiki.ubuntu.com/UncomplicatedFirewall)
- **Default**: ✅ Yes

#### Fail2ban
- **ID**: `fail2ban`
- **Description**: Intrusion prevention by monitoring logs
- **Installation**: APT package
- **Homepage**: [fail2ban.org](https://www.fail2ban.org/)
- **Default**: ✅ Yes

#### OpenSnitch
- **ID**: `opensnitch`
- **Description**: Application firewall with GUI
- **Installation**: GitHub release
- **Homepage**: [github.com/evilsocket/opensnitch](https://github.com/evilsocket/opensnitch)
- **Default**: ❌ No

#### Firejail
- **ID**: `firejail`
- **Description**: SUID sandbox program
- **Installation**: APT package
- **Homepage**: [firejail.wordpress.com](https://firejail.wordpress.com/)
- **Default**: ❌ No

### 🕵️ Privacy & Encryption

#### KeePassXC
- **ID**: `keepassxc`
- **Description**: Cross-platform password manager
- **Installation**: APT package
- **Homepage**: [keepassxc.org](https://keepassxc.org/)
- **Default**: ✅ Yes

#### Bitwarden
- **ID**: `bitwarden`
- **Description**: Open-source password manager with sync
- **Installation**: Snap package
- **Homepage**: [bitwarden.com](https://bitwarden.com/)
- **Default**: ❌ No

#### Tor Browser
- **ID**: `tor-browser`
- **Description**: Anonymous web browsing
- **Installation**: Tor Project repository
- **Homepage**: [torproject.org](https://www.torproject.org/)
- **Default**: ❌ No

#### VeraCrypt
- **ID**: `veracrypt`
- **Description**: Disk encryption software
- **Installation**: PPA repository
- **Homepage**: [veracrypt.fr](https://www.veracrypt.fr/)
- **Default**: ❌ No

#### Cryptomator
- **ID**: `cryptomator`
- **Description**: Encrypt cloud storage
- **Installation**: PPA repository
- **Homepage**: [cryptomator.org](https://cryptomator.org/)
- **Default**: ❌ No

### 🔍 Security Testing Tools

#### Network Security

##### Nmap
- **Description**: Network discovery and security auditing
- **Installation**: APT package
- **Homepage**: [nmap.org](https://nmap.org/)

##### Wireshark
- **Description**: Network protocol analyzer
- **Installation**: APT package
- **Homepage**: [wireshark.org](https://www.wireshark.org/)

##### Masscan
- **Description**: Fast TCP port scanner
- **Installation**: APT package
- **Homepage**: [github.com/robertdavidgraham/masscan](https://github.com/robertdavidgraham/masscan)

##### tcpdump
- **Description**: Command-line packet analyzer
- **Installation**: APT package

#### Web Security

##### Burp Suite Community
- **Description**: Web vulnerability scanner
- **Installation**: Shell script
- **Homepage**: [portswigger.net](https://portswigger.net/)

##### OWASP ZAP
- **Description**: Web app security scanner
- **Installation**: Snap package
- **Homepage**: [zaproxy.org](https://www.zaproxy.org/)

##### Nikto
- **Description**: Web server scanner
- **Installation**: APT package
- **Homepage**: [github.com/sullo/nikto](https://github.com/sullo/nikto)

##### sqlmap
- **Description**: SQL injection tool
- **Installation**: APT package
- **Homepage**: [sqlmap.org](https://sqlmap.org/)

#### Vulnerability Assessment

##### Metasploit Framework
- **Description**: Penetration testing platform
- **Installation**: Rapid7 repository
- **Homepage**: [metasploit.com](https://www.metasploit.com/)

##### OpenVAS
- **Description**: Vulnerability scanner
- **Installation**: APT package
- **Homepage**: [openvas.org](https://www.openvas.org/)

##### Lynis
- **Description**: Security auditing tool
- **Installation**: APT package
- **Homepage**: [cisofy.com/lynis](https://cisofy.com/lynis/)

#### Password Cracking

##### John the Ripper
- **Description**: Password security auditing
- **Installation**: APT package
- **Homepage**: [openwall.com/john](https://www.openwall.com/john/)

##### Hashcat
- **Description**: Advanced password recovery
- **Installation**: APT package
- **Homepage**: [hashcat.net](https://hashcat.net/)

##### Hydra
- **Description**: Network login cracker
- **Installation**: APT package
- **Homepage**: [github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra)

#### Wireless Security

##### Aircrack-ng
- **Description**: WiFi security auditing
- **Installation**: APT package
- **Homepage**: [aircrack-ng.org](https://www.aircrack-ng.org/)

##### Kismet
- **Description**: Wireless network detector
- **Installation**: APT package
- **Homepage**: [kismetwireless.net](https://www.kismetwireless.net/)

##### Bettercap
- **Description**: Network attack and monitoring
- **Installation**: APT package
- **Homepage**: [bettercap.org](https://www.bettercap.org/)

#### Container Security

##### Trivy
- **Description**: Container vulnerability scanner
- **Installation**: APT repository
- **Homepage**: [trivy.dev](https://trivy.dev/)

##### Grype
- **Description**: Vulnerability scanner for containers
- **Installation**: GitHub release
- **Homepage**: [github.com/anchore/grype](https://github.com/anchore/grype)

##### Dive
- **Description**: Docker image explorer
- **Installation**: GitHub release
- **Homepage**: [github.com/wagoodman/dive](https://github.com/wagoodman/dive)

---

## ⚙️ System Configuration

### 🚀 Performance Optimization

#### Memory Swappiness
- **ID**: `swappiness`
- **Description**: Controls kernel swap aggressiveness (0-100)
- **Default**: 10 (desktop), 60 (server)
- **Recommendation**: 1-10 for desktop, 60 for servers

#### Preload
- **ID**: `preload`
- **Description**: Adaptive readahead daemon
- **Installation**: APT package
- **Default**: ✅ Yes

#### ZRAM
- **ID**: `zram`
- **Description**: Compressed RAM for swap space
- **Installation**: zram-config package
- **Default**: ❌ No

#### Ananicy CPP
- **ID**: `ananicy`
- **Description**: Auto nice daemon for better responsiveness
- **Installation**: PPA repository
- **Homepage**: [github.com/Nefelim4ag/Ananicy-cpp](https://github.com/Nefelim4ag/Ananicy-cpp)
- **Default**: ❌ No

#### GameMode
- **ID**: `gamemode`
- **Description**: Optimize system for gaming
- **Installation**: APT package
- **Homepage**: [github.com/FeralInteractive/gamemode](https://github.com/FeralInteractive/gamemode)
- **Default**: ❌ No

### 📊 System Monitoring

#### Built-in Tools
- **htop**: Process monitoring (included above)
- **btop++**: Beautiful system monitor (included above)
- **glances**: Cross-platform monitoring (included above)

#### Advanced Monitoring
- **Netdata**: Real-time performance monitoring
- **Prometheus**: Monitoring and alerting toolkit
- **Grafana**: Analytics and monitoring platform
- **Zabbix**: Enterprise monitoring solution

---

## 📝 Installation Methods

### APT Package Manager
Most tools are available through Ubuntu's standard repositories:
```bash
sudo apt update
sudo apt install package-name
```

### Snap Packages
For sandboxed applications:
```bash
sudo snap install package-name
```

### Third-Party Repositories
Some tools require adding PPAs or vendor repositories:
```bash
sudo add-apt-repository ppa:example/ppa
sudo apt update
sudo apt install package-name
```

### Manual Installation
Some tools require downloading from GitHub releases or running install scripts.

### Python pip
For Python-based tools:
```bash
pip install --user package-name
```

### npm Global Packages
For Node.js tools:
```bash
npm install -g package-name
```

---

## 🎯 Default Selections

Ubootu comes with intelligent defaults based on common developer needs:

### Always Included
- Git version control
- Python with pip
- Node.js with npm
- Visual Studio Code
- Docker & Docker Compose
- Essential CLI tools (bat, ripgrep, fzf, etc.)
- Firefox browser
- UFW firewall
- System fonts

### Desktop Defaults
- GNOME desktop environment
- Dark theme enabled
- Papirus icons
- VLC media player

### Performance Defaults
- Swappiness: 10 (optimized for desktop)
- Preload enabled

---

## 🔗 Quick Links

- **Ubootu GitHub**: [github.com/johnwyles/ubootu](https://github.com/johnwyles/ubootu)
- **Issues**: [github.com/johnwyles/ubootu/issues](https://github.com/johnwyles/ubootu/issues)
- **Wiki**: [github.com/johnwyles/ubootu/wiki](https://github.com/johnwyles/ubootu/wiki)

---

*This documentation is maintained as part of the Ubootu project. For corrections or additions, please submit a pull request.*