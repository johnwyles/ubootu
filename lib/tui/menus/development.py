#!/usr/bin/env python3
"""
Development tools menu for the Ubootu TUI
"""

from typing import Dict

from lib.tui.menus.base import MenuBuilder, MenuItem


class DevelopmentMenuBuilder(MenuBuilder):
    """Builds the development tools menu section"""

    def build(self) -> Dict[str, MenuItem]:
        """Build development menu structure"""
        self.items.clear()

        # Main development category
        self.add_category(
            "development",
            "Development Tools",
            "Programming languages, IDEs, debugging tools",
            parent="root",
            children=[
                "dev-ides",
                "dev-languages",
                "dev-tools",
                "dev-containers",
                "dev-cli-modern",
            ],
        )

        # Development subcategories
        self._build_ides_menu()
        self._build_languages_menu()
        self._build_tools_menu()
        self._build_containers_menu()
        self._build_modern_cli_menu()

        return self.items

    def _build_ides_menu(self):
        """Build IDEs and editors menu"""
        self.add_category(
            "dev-ides",
            "IDEs & Editors",
            "Integrated development environments",
            parent="development",
            children=[
                "vscode",
                "intellij-idea",
                "pycharm",
                "webstorm",
                "clion",
                "goland",
                "phpstorm",
                "datagrip",
                "rider",
                "android-studio",
                "eclipse",
                "netbeans",
                "sublime",
                "vim",
                "emacs",
                "atom",
                "brackets",
                "zed",
                "helix",
                "lapce",
                "fleet",
            ],
        )

        # Individual IDE items
        self.add_selectable(
            "vscode",
            "Visual Studio Code",
            "Microsoft's popular code editor",
            parent="dev-ides",
            default=True,
        )

        self.add_selectable(
            "intellij-idea",
            "IntelliJ IDEA",
            "JetBrains Java IDE",
            parent="dev-ides",
            default=True,
            ansible_var="dev_ides_intellij",
        )

        self.add_selectable(
            "pycharm",
            "PyCharm",
            "JetBrains Python IDE",
            parent="dev-ides",
            default=True,
        )

        self.add_selectable(
            "webstorm", "WebStorm", "JetBrains JavaScript IDE", parent="dev-ides"
        )

        self.add_selectable(
            "sublime", "Sublime Text", "Sophisticated text editor", parent="dev-ides"
        )

        self.add_selectable(
            "vim", "Vim/NeoVim", "Terminal-based text editor", parent="dev-ides"
        )

        self.add_selectable(
            "emacs", "Emacs", "Extensible text editor", parent="dev-ides"
        )

        self.add_selectable(
            "clion",
            "CLion",
            "C/C++ IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_clion",
        )

        self.add_selectable(
            "goland",
            "GoLand",
            "Go IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_goland",
        )

        self.add_selectable(
            "phpstorm",
            "PhpStorm",
            "PHP IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_phpstorm",
        )

        self.add_selectable(
            "datagrip",
            "DataGrip",
            "Database IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_datagrip",
        )

        self.add_selectable(
            "rider",
            "Rider",
            ".NET IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_rider",
        )

        self.add_selectable(
            "android-studio",
            "Android Studio",
            "Official Android development IDE",
            parent="dev-ides",
            ansible_var="dev_ides_android_studio",
        )

        self.add_selectable(
            "eclipse",
            "Eclipse",
            "Java and multi-language IDE",
            parent="dev-ides",
            ansible_var="dev_ides_eclipse",
        )

        self.add_selectable(
            "netbeans",
            "NetBeans",
            "Java and multi-language IDE",
            parent="dev-ides",
            ansible_var="dev_ides_netbeans",
        )

        self.add_selectable(
            "atom",
            "Atom",
            "Hackable text editor (discontinued)",
            parent="dev-ides",
            ansible_var="dev_ides_atom",
        )

        self.add_selectable(
            "brackets",
            "Brackets",
            "Web-focused editor by Adobe",
            parent="dev-ides",
            ansible_var="dev_ides_brackets",
        )

        self.add_selectable(
            "zed",
            "Zed",
            "High-performance multiplayer editor",
            parent="dev-ides",
            ansible_var="dev_ides_zed",
        )

        self.add_selectable(
            "helix",
            "Helix",
            "Post-modern modal text editor",
            parent="dev-ides",
            ansible_var="dev_ides_helix",
        )

        self.add_selectable(
            "lapce",
            "Lapce",
            "Lightning-fast modern editor",
            parent="dev-ides",
            ansible_var="dev_ides_lapce",
        )

        self.add_selectable(
            "fleet",
            "Fleet",
            "Next-generation IDE by JetBrains",
            parent="dev-ides",
            ansible_var="dev_ides_fleet",
        )

    def _build_languages_menu(self):
        """Build programming languages menu"""
        self.add_category(
            "dev-languages",
            "Programming Languages",
            "Runtimes, compilers, interpreters",
            parent="development",
            children=["python", "nodejs", "java", "go", "rust", "cpp", "php", "ruby"],
        )

        # Language items
        self.add_selectable(
            "python",
            "Python",
            "Python runtime and pip",
            parent="dev-languages",
            default=True,
        )

        self.add_selectable(
            "nodejs",
            "Node.js",
            "JavaScript runtime",
            parent="dev-languages",
            default=True,
        )

        self.add_selectable(
            "java", "Java", "Java Development Kit", parent="dev-languages", default=True
        )

        self.add_selectable(
            "go", "Go", "Go programming language", parent="dev-languages"
        )

        self.add_selectable(
            "rust", "Rust", "Rust programming language", parent="dev-languages"
        )

        self.add_selectable(
            "cpp", "C/C++", "GCC compiler and build tools", parent="dev-languages"
        )

        self.add_selectable("php", "PHP", "PHP interpreter", parent="dev-languages")

        self.add_selectable("ruby", "Ruby", "Ruby interpreter", parent="dev-languages")

    def _build_tools_menu(self):
        """Build development tools menu"""
        self.add_category(
            "dev-tools",
            "Development Tools",
            "Debugging, profiling, testing tools",
            parent="development",
            children=[
                "git",
                "docker",
                "postman",
                "insomnia",
                "mysql-workbench",
                "dbeaver",
                "pgadmin",
                "redis-cli",
                "mongodb-compass",
                "robo3t",
                "curl",
                "httpie",
                "gh-cli",
                "lazygit",
                "gittyup",
                "fork",
                "sourcetree",
                "gitkraken",
                "lens-k8s",
                "k9s",
                "kubectl",
                "helm",
                "terraform",
                "vagrant",
                "ansible-semaphore",
            ],
        )

        # Tool items
        self.add_selectable(
            "git", "Git", "Version control system", parent="dev-tools", default=True
        )

        self.add_selectable(
            "docker", "Docker", "Container platform", parent="dev-tools", default=True
        )

        self.add_selectable(
            "postman", "Postman", "API development tool", parent="dev-tools"
        )

        self.add_selectable(
            "mysql-workbench",
            "MySQL Workbench",
            "Database administration tool",
            parent="dev-tools",
        )

        self.add_selectable(
            "redis-cli", "Redis CLI", "Redis command line interface", parent="dev-tools"
        )

        self.add_selectable(
            "curl", "curl", "HTTP client tool", parent="dev-tools", default=True
        )

        self.add_selectable(
            "insomnia",
            "Insomnia",
            "API client and design tool",
            parent="dev-tools",
            ansible_var="dev_tools_insomnia",
        )

        self.add_selectable(
            "dbeaver",
            "DBeaver",
            "Universal database tool",
            parent="dev-tools",
            ansible_var="dev_tools_dbeaver",
        )

        self.add_selectable(
            "pgadmin",
            "pgAdmin",
            "PostgreSQL administration",
            parent="dev-tools",
            ansible_var="dev_tools_pgadmin",
        )

        self.add_selectable(
            "mongodb-compass",
            "MongoDB Compass",
            "MongoDB GUI",
            parent="dev-tools",
            ansible_var="dev_tools_mongodb_compass",
        )

        self.add_selectable(
            "robo3t",
            "Robo 3T",
            "MongoDB management tool",
            parent="dev-tools",
            ansible_var="dev_tools_robo3t",
        )

        self.add_selectable(
            "httpie",
            "HTTPie",
            "User-friendly HTTP client",
            parent="dev-tools",
            ansible_var="dev_tools_httpie",
        )

        self.add_selectable(
            "gh-cli",
            "GitHub CLI",
            "GitHub command line tool",
            parent="dev-tools",
            ansible_var="dev_tools_gh_cli",
        )

        self.add_selectable(
            "lazygit",
            "LazyGit",
            "Terminal UI for git",
            parent="dev-tools",
            ansible_var="dev_tools_lazygit",
        )

        self.add_selectable(
            "gittyup",
            "Gittyup",
            "Graphical Git client",
            parent="dev-tools",
            ansible_var="dev_tools_gittyup",
        )

        self.add_selectable(
            "fork",
            "Fork",
            "Git client for Mac and Windows",
            parent="dev-tools",
            ansible_var="dev_tools_fork",
        )

        self.add_selectable(
            "sourcetree",
            "Sourcetree",
            "Free Git GUI",
            parent="dev-tools",
            ansible_var="dev_tools_sourcetree",
        )

        self.add_selectable(
            "gitkraken",
            "GitKraken",
            "Cross-platform Git GUI",
            parent="dev-tools",
            ansible_var="dev_tools_gitkraken",
        )

        self.add_selectable(
            "lens-k8s",
            "Lens",
            "Kubernetes IDE",
            parent="dev-tools",
            ansible_var="dev_tools_lens",
        )

        self.add_selectable(
            "k9s",
            "K9s",
            "Terminal UI for Kubernetes",
            parent="dev-tools",
            ansible_var="dev_tools_k9s",
        )

        self.add_selectable(
            "kubectl",
            "kubectl",
            "Kubernetes command-line tool",
            parent="dev-tools",
            ansible_var="dev_tools_kubectl",
        )

        self.add_selectable(
            "helm",
            "Helm",
            "Kubernetes package manager",
            parent="dev-tools",
            ansible_var="dev_tools_helm",
        )

        self.add_selectable(
            "terraform",
            "Terraform",
            "Infrastructure as code",
            parent="dev-tools",
            ansible_var="dev_tools_terraform",
        )

        self.add_selectable(
            "vagrant",
            "Vagrant",
            "Development environments",
            parent="dev-tools",
            ansible_var="dev_tools_vagrant",
        )

        self.add_selectable(
            "ansible-semaphore",
            "Ansible Semaphore",
            "Ansible web UI",
            parent="dev-tools",
            ansible_var="dev_tools_ansible_semaphore",
        )

    def _build_containers_menu(self):
        """Build containers and DevOps menu"""
        self.add_category(
            "dev-containers",
            "Containers & DevOps",
            "Container platforms and orchestration",
            parent="development",
            children=["docker-desktop", "kubernetes", "terraform-iac", "ansible"],
        )

        # Container items
        self.add_selectable(
            "docker-desktop",
            "Docker Desktop",
            "Docker containerization platform with GUI",
            parent="dev-containers",
            default=True,
        )

        self.add_selectable(
            "kubernetes",
            "Kubernetes Tools",
            "Container orchestration tools (kubectl, minikube)",
            parent="dev-containers",
        )

        self.add_selectable(
            "terraform-iac",
            "Terraform",
            "Infrastructure as code tool",
            parent="dev-containers",
        )

        self.add_selectable(
            "ansible",
            "Ansible",
            "Configuration management and automation",
            parent="dev-containers",
        )

    def _build_modern_cli_menu(self):
        """Build modern CLI tools menu"""
        self.add_category(
            "dev-cli-modern",
            "🚀 Modern CLI Tools",
            "Next-gen command line utilities",
            parent="development",
            children=[
                "cli-unix-replacements",
                "cli-file-managers",
                "cli-system-monitoring",
                "cli-network-tools",
                "cli-text-processing",
                "cli-dev-tools",
                "cli-productivity",
            ],
        )

        # CLI subcategories
        self._build_unix_replacements()
        self._build_file_managers()
        self._build_system_monitoring()
        self._build_network_tools()
        self._build_text_processing()
        self._build_dev_cli_tools()
        self._build_productivity_tools()

    def _build_unix_replacements(self):
        """Build Unix command replacements menu"""
        self.add_category(
            "cli-unix-replacements",
            "Unix Command Replacements",
            "Modern alternatives to classic commands",
            parent="dev-cli-modern",
            children=[
                "exa",
                "bat",
                "ripgrep",
                "fd",
                "dust",
                "duf",
                "procs",
                "bottom",
                "sd",
                "delta",
            ],
        )

        self.add_selectable(
            "exa",
            "exa",
            "Modern replacement for ls",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_exa",
        )

        self.add_selectable(
            "bat",
            "bat",
            "Cat clone with syntax highlighting",
            parent="cli-unix-replacements",
            default=True,
            ansible_var="modern_cli_install_bat",
        )

        self.add_selectable(
            "ripgrep",
            "ripgrep (rg)",
            "Extremely fast grep alternative",
            parent="cli-unix-replacements",
            default=True,
            ansible_var="modern_cli_install_ripgrep",
        )

        self.add_selectable(
            "fd",
            "fd",
            "Simple, fast alternative to find",
            parent="cli-unix-replacements",
            default=True,
            ansible_var="modern_cli_install_fd",
        )

        self.add_selectable(
            "dust",
            "dust",
            "More intuitive du",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_dust",
        )

        self.add_selectable(
            "duf",
            "duf",
            "Better df with colors",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_duf",
        )

        self.add_selectable(
            "procs",
            "procs",
            "Modern replacement for ps",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_procs",
        )

        self.add_selectable(
            "bottom",
            "bottom",
            "Graphical process/system monitor",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_bottom",
        )

        self.add_selectable(
            "sd",
            "sd",
            "Intuitive find-and-replace (sed alternative)",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_sd",
        )

        self.add_selectable(
            "delta",
            "delta",
            "Syntax-highlighting pager for git",
            parent="cli-unix-replacements",
            ansible_var="modern_cli_install_delta",
        )

    def _build_file_managers(self):
        """Build terminal file managers menu"""
        self.add_category(
            "cli-file-managers",
            "Terminal File Managers",
            "Navigate files in the terminal",
            parent="dev-cli-modern",
            children=["ranger", "nnn", "mc", "lf", "broot", "fff", "vifm"],
        )

        self.add_selectable(
            "ranger",
            "ranger",
            "Vim-inspired file manager",
            parent="cli-file-managers",
            default=True,
            ansible_var="modern_cli_install_ranger",
        )

        self.add_selectable(
            "nnn",
            "nnn",
            "Blazing fast terminal file manager",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_nnn",
        )

        self.add_selectable(
            "mc",
            "Midnight Commander",
            "Classic dual-pane file manager",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_mc",
        )

        self.add_selectable(
            "lf",
            "lf",
            "Terminal file manager written in Go",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_lf",
        )

        self.add_selectable(
            "broot",
            "broot",
            "New way to navigate directory trees",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_broot",
        )

        self.add_selectable(
            "fff",
            "fff",
            "Fast, simple file manager",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_fff",
        )

        self.add_selectable(
            "vifm",
            "vifm",
            "Vi-like file manager",
            parent="cli-file-managers",
            ansible_var="modern_cli_install_vifm",
        )

    def _build_system_monitoring(self):
        """Build system monitoring tools menu"""
        self.add_category(
            "cli-system-monitoring",
            "System Monitoring",
            "Monitor system resources",
            parent="dev-cli-modern",
            children=["htop", "glances", "btop", "gotop", "zenith", "ytop", "bashtop"],
        )

        self.add_selectable(
            "htop",
            "htop",
            "Interactive process viewer",
            parent="cli-system-monitoring",
            default=True,
            ansible_var="modern_cli_install_htop",
        )

        self.add_selectable(
            "glances",
            "glances",
            "Cross-platform monitoring tool",
            parent="cli-system-monitoring",
            ansible_var="modern_cli_install_glances",
        )

        self.add_selectable(
            "btop",
            "btop++",
            "Resource monitor with game-like UI",
            parent="cli-system-monitoring",
            default=True,
            ansible_var="modern_cli_install_btop",
        )

        self.add_selectable(
            "gotop",
            "gotop",
            "Terminal based graphical activity monitor",
            parent="cli-system-monitoring",
            ansible_var="modern_cli_install_gotop",
        )

        self.add_selectable(
            "zenith",
            "zenith",
            "Charts for system metrics",
            parent="cli-system-monitoring",
            ansible_var="modern_cli_install_zenith",
        )

        self.add_selectable(
            "ytop",
            "ytop",
            "TUI system monitor written in Rust",
            parent="cli-system-monitoring",
            ansible_var="modern_cli_install_ytop",
        )

        self.add_selectable(
            "bashtop",
            "bashtop",
            "Resource monitor written in Bash",
            parent="cli-system-monitoring",
            ansible_var="modern_cli_install_bashtop",
        )

    def _build_network_tools(self):
        """Build network utilities menu"""
        self.add_category(
            "cli-network-tools",
            "Network Utilities",
            "Modern network analysis tools",
            parent="dev-cli-modern",
            children=[
                "httpie-cli",
                "bandwhich",
                "gping",
                "trippy",
                "dog",
                "curlie",
                "xh",
            ],
        )

        self.add_selectable(
            "httpie-cli",
            "HTTPie",
            "User-friendly curl replacement",
            parent="cli-network-tools",
            default=True,
            ansible_var="modern_cli_install_httpie",
        )

        self.add_selectable(
            "bandwhich",
            "bandwhich",
            "Terminal bandwidth utilization tool",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_bandwhich",
        )

        self.add_selectable(
            "gping",
            "gping",
            "Ping with a graph",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_gping",
        )

        self.add_selectable(
            "trippy",
            "trippy",
            "Network diagnostic tool",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_trippy",
        )

        self.add_selectable(
            "dog",
            "dog",
            "Command-line DNS client",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_dog",
        )

        self.add_selectable(
            "curlie",
            "curlie",
            "Curl with colors and formatting",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_curlie",
        )

        self.add_selectable(
            "xh",
            "xh",
            "Friendly and fast HTTP client",
            parent="cli-network-tools",
            ansible_var="modern_cli_install_xh",
        )

    def _build_text_processing(self):
        """Build text and data processing tools menu"""
        self.add_category(
            "cli-text-processing",
            "Text & Data Processing",
            "Process text and structured data",
            parent="dev-cli-modern",
            children=["jq", "yq", "miller", "xsv", "dasel", "jless", "gron"],
        )

        self.add_selectable(
            "jq",
            "jq",
            "Command-line JSON processor",
            parent="cli-text-processing",
            default=True,
            ansible_var="modern_cli_install_jq",
        )

        self.add_selectable(
            "yq",
            "yq",
            "YAML processor like jq",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_yq",
        )

        self.add_selectable(
            "miller",
            "Miller",
            "Like awk/sed/cut for CSV/TSV/JSON",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_miller",
        )

        self.add_selectable(
            "xsv",
            "xsv",
            "Fast CSV command line toolkit",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_xsv",
        )

        self.add_selectable(
            "dasel",
            "dasel",
            "Query and modify data structures",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_dasel",
        )

        self.add_selectable(
            "jless",
            "jless",
            "Command-line JSON viewer",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_jless",
        )

        self.add_selectable(
            "gron",
            "gron",
            "Make JSON greppable",
            parent="cli-text-processing",
            ansible_var="modern_cli_install_gron",
        )

    def _build_dev_cli_tools(self):
        """Build development CLI tools menu"""
        self.add_category(
            "cli-dev-tools",
            "Development CLI",
            "Git and development utilities",
            parent="dev-cli-modern",
            children=[
                "gh",
                "lazygit-cli",
                "tig",
                "gitui",
                "delta-git",
                "forgit",
                "git-extras",
            ],
        )

        self.add_selectable(
            "gh",
            "GitHub CLI",
            "GitHub's official command line tool",
            parent="cli-dev-tools",
            default=True,
            ansible_var="modern_cli_install_gh",
        )

        self.add_selectable(
            "lazygit-cli",
            "lazygit",
            "Simple terminal UI for git",
            parent="cli-dev-tools",
            default=True,
            ansible_var="modern_cli_install_lazygit",
        )

        self.add_selectable(
            "tig",
            "tig",
            "Text-mode interface for git",
            parent="cli-dev-tools",
            ansible_var="modern_cli_install_tig",
        )

        self.add_selectable(
            "gitui",
            "gitui",
            "Blazing fast terminal git UI",
            parent="cli-dev-tools",
            ansible_var="modern_cli_install_gitui",
        )

        self.add_selectable(
            "delta-git",
            "git-delta",
            "Syntax-highlighting pager for git",
            parent="cli-dev-tools",
            ansible_var="modern_cli_install_git_delta",
        )

        self.add_selectable(
            "forgit",
            "forgit",
            "Interactive git with fzf",
            parent="cli-dev-tools",
            ansible_var="modern_cli_install_forgit",
        )

        self.add_selectable(
            "git-extras",
            "git-extras",
            "Extra git commands",
            parent="cli-dev-tools",
            ansible_var="modern_cli_install_git_extras",
        )

    def _build_productivity_tools(self):
        """Build productivity tools menu"""
        self.add_category(
            "cli-productivity",
            "Productivity Tools",
            "Terminal productivity enhancers",
            parent="dev-cli-modern",
            children=["tmux", "zsh", "fzf", "z", "autojump", "direnv", "asdf"],
        )

        self.add_selectable(
            "tmux",
            "tmux",
            "Terminal multiplexer",
            parent="cli-productivity",
            default=True,
            ansible_var="modern_cli_install_tmux",
        )

        self.add_selectable(
            "zsh",
            "Zsh + Oh My Zsh",
            "Advanced shell with framework",
            parent="cli-productivity",
            default=True,
            ansible_var="modern_cli_install_zsh",
        )

        self.add_selectable(
            "fzf",
            "fzf",
            "Fuzzy finder for terminal",
            parent="cli-productivity",
            default=True,
            ansible_var="modern_cli_install_fzf",
        )

        self.add_selectable(
            "z",
            "z",
            "Jump to frecent directories",
            parent="cli-productivity",
            ansible_var="modern_cli_install_z",
        )

        self.add_selectable(
            "autojump",
            "autojump",
            "Fast directory navigation",
            parent="cli-productivity",
            ansible_var="modern_cli_install_autojump",
        )

        self.add_selectable(
            "direnv",
            "direnv",
            "Directory-specific environments",
            parent="cli-productivity",
            ansible_var="modern_cli_install_direnv",
        )

        self.add_selectable(
            "asdf",
            "asdf",
            "Version manager for multiple languages",
            parent="cli-productivity",
            ansible_var="modern_cli_install_asdf",
        )
