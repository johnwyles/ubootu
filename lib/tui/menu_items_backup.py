#!/usr/bin/env python3
"""
Menu item definitions for the unified TUI
All menu structure and items are defined here
"""

from typing import Dict, List


def load_menu_structure() -> List[Dict]:
    """Load and return the complete menu structure"""
    items = []
    
    # Root level categories
    categories = [
        {
            'id': 'development',
            'label': 'Development Tools',
            'description': 'Programming languages, IDEs, tools',
            'icon': '💻',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'ai-ml',
            'label': 'AI & Machine Learning',
            'description': 'AI tools, ML frameworks, LLMs',
            'icon': '🤖',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'desktop',
            'label': 'Desktop Environment',
            'description': 'Desktop environments and themes',
            'icon': '🖥️',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'applications',
            'label': 'Applications',
            'description': 'Browsers, productivity, multimedia',
            'icon': '📦',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'security',
            'label': 'Security & Privacy',
            'description': 'Firewall, VPN, encryption tools',
            'icon': '🔒',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'system',
            'label': 'System Configuration',
            'description': 'Performance, services, hardware',
            'icon': '⚙️',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'customization',
            'label': 'Application Customization',
            'description': 'Customize appearance and behavior of apps',
            'icon': '🎨',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'gaming',
            'label': 'Gaming',
            'description': 'Gaming platforms and tools',
            'icon': '🎮',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'multimedia',
            'label': 'Multimedia Production',
            'description': 'Audio, video, and graphics creation',
            'icon': '🎬',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'networking',
            'label': 'Networking',
            'description': 'Network tools and configuration',
            'icon': '🌐',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'virtualization',
            'label': 'Virtualization',
            'description': 'Virtual machines and containers',
            'icon': '📦',
            'is_category': True,
            'parent': None,
            'children': []
        },
        {
            'id': 'cloud-tools',
            'label': 'Cloud Tools',
            'description': 'Cloud platforms and infrastructure',
            'icon': '☁️',
            'is_category': True,
            'parent': None,
            'children': []
        },
    ]
    
    # Development Tools
    dev_tools = [
        # IDEs and Editors
        {
            'id': 'vscode',
            'label': 'Visual Studio Code',
            'description': 'Modern code editor',
            'parent': 'development',
            'default': True,
            'help': 'Visual Studio Code is Microsoft\'s free, open-source code editor with excellent language support, debugging, Git integration, and a vast extension ecosystem.'
        },
        {
            'id': 'pycharm',
            'label': 'PyCharm Community',
            'description': 'Python IDE',
            'parent': 'development',
            'help': 'PyCharm Community Edition is the best Python IDE with intelligent code completion, debugging, testing, and virtual environment management.'
        },
        {
            'id': 'intellij-idea',
            'label': 'IntelliJ IDEA Community',
            'description': 'Java/Kotlin IDE',
            'parent': 'development',
            'help': 'IntelliJ IDEA Community Edition is JetBrains\' powerful Java IDE with smart code completion, refactoring tools, and built-in version control.'
        },
        {
            'id': 'webstorm',
            'label': 'WebStorm',
            'description': 'JavaScript IDE',
            'parent': 'development',
            'help': 'WebStorm is JetBrains\' powerful IDE for JavaScript and related technologies.'
        },
        {
            'id': 'goland',
            'label': 'GoLand',
            'description': 'Go IDE',
            'parent': 'development',
            'help': 'GoLand is JetBrains\' IDE for Go development with advanced code analysis.'
        },
        {
            'id': 'clion',
            'label': 'CLion',
            'description': 'C/C++ IDE',
            'parent': 'development',
            'help': 'CLion is JetBrains\' cross-platform IDE for C and C++ development.'
        },
        {
            'id': 'rider',
            'label': 'Rider',
            'description': '.NET IDE',
            'parent': 'development',
            'help': 'Rider is JetBrains\' cross-platform .NET IDE based on IntelliJ and ReSharper.'
        },
        {
            'id': 'datagrip',
            'label': 'DataGrip',
            'description': 'Database IDE',
            'parent': 'development',
            'help': 'DataGrip is JetBrains\' IDE for databases and SQL with smart query console.'
        },
        {
            'id': 'android-studio',
            'label': 'Android Studio',
            'description': 'Android development',
            'parent': 'development',
            'help': 'Android Studio is the official IDE for Android app development based on IntelliJ IDEA.'
        },
        {
            'id': 'sublime-text',
            'label': 'Sublime Text',
            'description': 'Fast text editor',
            'parent': 'development',
            'help': 'Sublime Text is a sophisticated text editor for code, markup and prose with a slick user interface and extraordinary features.'
        },
        {
            'id': 'vim',
            'label': 'Vim',
            'description': 'Terminal editor',
            'parent': 'development',
            'help': 'Vim is a highly configurable text editor built to enable efficient text editing. It\'s an improved version of the vi editor.'
        },
        {
            'id': 'neovim',
            'label': 'Neovim',
            'description': 'Modern Vim fork',
            'parent': 'development',
            'help': 'Neovim is a refactor of Vim aiming to improve extensibility and maintainability with better plugin architecture.'
        },
        # Languages
        {
            'id': 'python',
            'label': 'Python 3',
            'description': 'Python runtime and pip',
            'parent': 'development',
            'default': True,
            'help': 'Python 3 runtime with pip package manager. The most popular language for scripting, web development, data science, and automation.'
        },
        {
            'id': 'nodejs',
            'label': 'Node.js',
            'description': 'JavaScript runtime',
            'parent': 'development',
            'default': True,
            'help': 'Node.js JavaScript runtime built on Chrome\'s V8 engine. Essential for modern web development, React, Angular, Vue.js, and server-side JavaScript.'
        },
        {
            'id': 'rust',
            'label': 'Rust',
            'description': 'Systems programming language',
            'parent': 'development',
            'help': 'Rust is a language empowering everyone to build reliable and efficient software with memory safety and zero-cost abstractions.'
        },
        {
            'id': 'go',
            'label': 'Go',
            'description': 'Google\'s programming language',
            'parent': 'development',
            'help': 'Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.'
        },
        # Tools
        {
            'id': 'git',
            'label': 'Git',
            'description': 'Version control',
            'parent': 'development',
            'default': True,
            'help': 'Git is a free and open source distributed version control system designed to handle everything from small to very large projects.'
        },
        {
            'id': 'docker',
            'label': 'Docker',
            'description': 'Container platform',
            'parent': 'development',
            'default': True,
            'help': 'Docker is a platform for developers to develop, deploy, and run applications with containers.'
        },
        {
            'id': 'docker-compose',
            'label': 'Docker Compose',
            'description': 'Multi-container orchestration',
            'parent': 'development',
            'help': 'Docker Compose is a tool for defining and running multi-container Docker applications with YAML configuration.'
        },
        # Additional IDEs
        {
            'id': 'cursor',
            'label': 'Cursor',
            'description': 'AI-powered code editor',
            'parent': 'development',
            'help': 'Cursor is an AI-first code editor that helps you code faster with AI assistance.'
        },
        {
            'id': 'zed',
            'label': 'Zed',
            'description': 'High-performance code editor',
            'parent': 'development',
            'help': 'Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.'
        },
        {
            'id': 'neovim',
            'label': 'Neovim',
            'description': 'Hyperextensible Vim-based editor',
            'parent': 'development',
            'help': 'Neovim is a refactor of Vim with better plugin architecture and modern features.'
        },
        {
            'id': 'emacs',
            'label': 'Emacs',
            'description': 'Extensible text editor',
            'parent': 'development',
            'help': 'GNU Emacs is an extensible, customizable, self-documenting text editor.'
        },
        # Database Tools
        {
            'id': 'dbeaver',
            'label': 'DBeaver',
            'description': 'Universal database tool',
            'parent': 'development',
            'help': 'DBeaver is a free multi-platform database tool for developers, SQL programmers, and DBAs.'
        },
        {
            'id': 'pgadmin',
            'label': 'pgAdmin',
            'description': 'PostgreSQL management',
            'parent': 'development',
            'help': 'pgAdmin is the most popular and feature-rich Open Source administration platform for PostgreSQL.'
        },
        {
            'id': 'mysql-workbench',
            'label': 'MySQL Workbench',
            'description': 'MySQL database design',
            'parent': 'development',
            'help': 'MySQL Workbench is a unified visual tool for database architects, developers, and DBAs.'
        },
        # API Tools
        {
            'id': 'postman',
            'label': 'Postman',
            'description': 'API development platform',
            'parent': 'development',
            'help': 'Postman is an API platform for building and using APIs with testing and documentation.'
        },
        {
            'id': 'insomnia',
            'label': 'Insomnia',
            'description': 'REST and GraphQL client',
            'parent': 'development',
            'help': 'Insomnia is a powerful REST and GraphQL client with a beautiful interface.'
        },
        {
            'id': 'httpie',
            'label': 'HTTPie',
            'description': 'CLI HTTP client',
            'parent': 'development',
            'help': 'HTTPie is a command-line HTTP client with an intuitive UI and JSON support.'
        },
        # Cloud CLIs
        {
            'id': 'aws-cli',
            'label': 'AWS CLI',
            'description': 'Amazon Web Services CLI',
            'parent': 'development',
            'help': 'AWS CLI is a unified tool to manage your AWS services from the command line.'
        },
        {
            'id': 'gcloud',
            'label': 'Google Cloud SDK',
            'description': 'Google Cloud Platform CLI',
            'parent': 'development',
            'help': 'Google Cloud SDK is a set of tools for Google Cloud Platform including gcloud, gsutil, and bq.'
        },
        {
            'id': 'azure-cli',
            'label': 'Azure CLI',
            'description': 'Microsoft Azure CLI',
            'parent': 'development',
            'help': 'Azure CLI is a cross-platform command-line tool to manage Azure resources.'
        },
        {
            'id': 'terraform',
            'label': 'Terraform',
            'description': 'Infrastructure as Code',
            'parent': 'development',
            'help': 'Terraform is an infrastructure as code tool for building, changing, and versioning infrastructure.'
        },
        {
            'id': 'pulumi',
            'label': 'Pulumi',
            'description': 'Modern Infrastructure as Code',
            'parent': 'development',
            'help': 'Pulumi is an infrastructure as code platform that allows you to use familiar programming languages.'
        },
        # Terminal Customization
        {
            'id': 'terminal-transparency',
            'label': 'Terminal Transparency',
            'description': 'Background transparency (0-100%)',
            'parent': 'development',
            'is_configurable': True,
            'default_value': 85,
            'help': 'Set the transparency level of your terminal background. 0% is opaque, 100% is fully transparent.'
        },
        {
            'id': 'terminal-font-size',
            'label': 'Terminal Font Size',
            'description': 'Font size in points',
            'parent': 'development',
            'is_configurable': True,
            'default_value': 12,
            'help': 'Set the font size for your terminal in points.'
        },
        {
            'id': 'terminal-cursor-blink',
            'label': 'Terminal Cursor Blink',
            'description': 'Enable cursor blinking',
            'parent': 'development',
            'default': True,
            'help': 'Enable or disable cursor blinking in the terminal.'
        },
        # Editor Settings
        {
            'id': 'vscode-vim-mode',
            'label': 'VS Code Vim Mode',
            'description': 'Enable Vim keybindings',
            'parent': 'development',
            'help': 'Enable Vim keybindings in Visual Studio Code for efficient text editing.'
        },
        {
            'id': 'vscode-theme-sync',
            'label': 'VS Code Theme Sync',
            'description': 'Sync with system theme',
            'parent': 'development',
            'help': 'Automatically switch VS Code theme to match your system theme.'
        },
        {
            'id': 'editor-minimap',
            'label': 'Editor Minimap',
            'description': 'Show code minimap',
            'parent': 'development',
            'default': True,
            'help': 'Show a minimap overview of your code on the side of the editor.'
        },
        {
            'id': 'editor-ligatures',
            'label': 'Editor Ligatures',
            'description': 'Enable font ligatures',
            'parent': 'development',
            'default': True,
            'help': 'Enable programming ligatures if using a font that supports them (like Fira Code).'
        },
        # VS Code Specific Settings
        {
            'id': 'vscode-font-size',
            'label': 'VS Code Font Size',
            'description': 'Editor font size (10-24)',
            'parent': 'development',
            'is_configurable': True,
            'default_value': 14,
            'help': 'Set the font size for the VS Code editor (pixels).'
        },
        {
            'id': 'vscode-tab-size',
            'label': 'VS Code Tab Size',
            'description': 'Spaces per tab (2-8)',
            'parent': 'development',
            'is_configurable': True,
            'default_value': 4,
            'help': 'Number of spaces to use for each tab in VS Code.'
        },
        {
            'id': 'vscode-word-wrap',
            'label': 'VS Code Word Wrap',
            'description': 'Wrap long lines',
            'parent': 'development',
            'help': 'Automatically wrap long lines in the VS Code editor.'
        },
        {
            'id': 'vscode-bracket-colorization',
            'label': 'Bracket Pair Colorization',
            'description': 'Color matching brackets',
            'parent': 'development',
            'default': True,
            'help': 'Use colors to help identify matching bracket pairs in VS Code.'
        },
        {
            'id': 'vscode-sticky-scroll',
            'label': 'VS Code Sticky Scroll',
            'description': 'Show current scope',
            'parent': 'development',
            'default': True,
            'help': 'Show the current function/class scope at the top of the editor while scrolling.'
        },
        {
            'id': 'vscode-inlay-hints',
            'label': 'VS Code Inlay Hints',
            'description': 'Show inline type hints',
            'parent': 'development',
            'help': 'Display inline parameter names and type information in the editor.'
        },
        # Application Integration
        {
            'id': 'app-theme-integration',
            'label': 'Application Theme Integration',
            'description': 'Apply system theme to apps',
            'parent': 'development',
            'default': True,
            'help': 'Automatically apply your selected system theme to supported applications.'
        },
        {
            'id': 'git-config-global',
            'label': 'Git Global Configuration',
            'description': 'Set up Git user info',
            'parent': 'development',
            'help': 'Configure Git with your name and email for all repositories.'
        },
        {
            'id': 'ssh-key-github',
            'label': 'SSH Key for GitHub',
            'description': 'Generate GitHub SSH key',
            'parent': 'development',
            'help': 'Generate an SSH key and add it to your GitHub account for secure access.'
        },
        # Databases
        {
            'id': 'postgresql',
            'label': 'PostgreSQL',
            'description': 'Advanced SQL database',
            'parent': 'development',
            'help': 'PostgreSQL is a powerful, open source object-relational database system.'
        },
        {
            'id': 'mysql',
            'label': 'MySQL',
            'description': 'Popular SQL database',
            'parent': 'development',
            'help': 'MySQL is the world\'s most popular open source database.'
        },
        {
            'id': 'mariadb',
            'label': 'MariaDB',
            'description': 'MySQL fork',
            'parent': 'development',
            'help': 'MariaDB is a community-developed fork of MySQL with enhanced features.'
        },
        {
            'id': 'mongodb',
            'label': 'MongoDB',
            'description': 'NoSQL database',
            'parent': 'development',
            'help': 'MongoDB is a document-oriented NoSQL database used for high volume data storage.'
        },
        {
            'id': 'redis',
            'label': 'Redis',
            'description': 'In-memory data store',
            'parent': 'development',
            'help': 'Redis is an in-memory data structure store used as a database, cache, and message broker.'
        },
        {
            'id': 'elasticsearch',
            'label': 'Elasticsearch',
            'description': 'Search engine',
            'parent': 'development',
            'help': 'Elasticsearch is a distributed, RESTful search and analytics engine.'
        },
        {
            'id': 'cassandra',
            'label': 'Cassandra',
            'description': 'Wide column store',
            'parent': 'development',
            'help': 'Apache Cassandra is a distributed NoSQL database management system.'
        },
        {
            'id': 'couchdb',
            'label': 'CouchDB',
            'description': 'Document database',
            'parent': 'development',
            'help': 'Apache CouchDB is a document-oriented NoSQL database.'
        },
        {
            'id': 'influxdb',
            'label': 'InfluxDB',
            'description': 'Time series database',
            'parent': 'development',
            'help': 'InfluxDB is a time series database designed for high-write and high-query loads.'
        },
        # Shell and Prompts
        {
            'id': 'bash',
            'label': 'Bash',
            'description': 'Bourne Again Shell',
            'parent': 'development',
            'default': True,
            'help': 'Bash is the GNU Project\'s shell and the default shell on most Linux systems.'
        },
        {
            'id': 'zsh',
            'label': 'Zsh',
            'description': 'Z Shell',
            'parent': 'development',
            'help': 'Zsh is a shell designed for interactive use with many features from bash, ksh, and tcsh.'
        },
        {
            'id': 'fish',
            'label': 'Fish',
            'description': 'Friendly shell',
            'parent': 'development',
            'help': 'Fish is a smart and user-friendly command line shell with autosuggestions.'
        },
        {
            'id': 'nushell',
            'label': 'Nushell',
            'description': 'Modern shell',
            'parent': 'development',
            'help': 'Nushell is a modern shell that understands data structures.'
        },
        {
            'id': 'elvish',
            'label': 'Elvish',
            'description': 'Expressive shell',
            'parent': 'development',
            'help': 'Elvish is an expressive programming language and a versatile interactive shell.'
        },
        {
            'id': 'prompt-starship',
            'label': 'Starship Prompt',
            'description': 'Fast cross-shell prompt',
            'parent': 'development',
            'help': 'Starship is a minimal, blazing-fast, and customizable prompt for any shell.'
        },
        {
            'id': 'prompt-ohmyposh',
            'label': 'Oh My Posh',
            'description': 'Prompt theme engine',
            'parent': 'development',
            'help': 'Oh My Posh is a prompt theme engine for any shell with many built-in themes.'
        },
        {
            'id': 'prompt-pure',
            'label': 'Pure Prompt',
            'description': 'Minimal Zsh prompt',
            'parent': 'development',
            'help': 'Pure is a pretty, minimal and fast ZSH prompt.'
        },
        {
            'id': 'prompt-spaceship',
            'label': 'Spaceship Prompt',
            'description': 'Minimalistic Zsh prompt',
            'parent': 'development',
            'help': 'Spaceship is a minimalistic, powerful and customizable Zsh prompt.'
        },
        {
            'id': 'prompt-powerlevel10k',
            'label': 'Powerlevel10k',
            'description': 'Feature-rich Zsh theme',
            'parent': 'development',
            'help': 'Powerlevel10k is a theme for Zsh that emphasizes speed, flexibility and out-of-the-box experience.'
        },
        # Additional Programming Languages
        {
            'id': 'java',
            'label': 'Java (OpenJDK)',
            'description': 'Java development kit',
            'parent': 'development',
            'help': 'OpenJDK is a free and open-source implementation of the Java Platform, Standard Edition.'
        },
        {
            'id': 'dotnet',
            'label': '.NET SDK',
            'description': 'Microsoft .NET development',
            'parent': 'development',
            'help': '.NET is a free, cross-platform, open source developer platform for building many different types of applications.'
        },
        {
            'id': 'ruby',
            'label': 'Ruby',
            'description': 'Ruby programming language',
            'parent': 'development',
            'help': 'Ruby is a dynamic, open source programming language with a focus on simplicity and productivity.'
        },
        {
            'id': 'php',
            'label': 'PHP',
            'description': 'PHP scripting language',
            'parent': 'development',
            'help': 'PHP is a popular general-purpose scripting language that is especially suited to web development.'
        },
        {
            'id': 'kotlin',
            'label': 'Kotlin',
            'description': 'Modern JVM language',
            'parent': 'development',
            'help': 'Kotlin is a modern programming language that makes developers happier.'
        },
        {
            'id': 'scala',
            'label': 'Scala',
            'description': 'Functional JVM language',
            'parent': 'development',
            'help': 'Scala combines object-oriented and functional programming in one concise, high-level language.'
        },
        {
            'id': 'swift',
            'label': 'Swift',
            'description': 'Apple\'s programming language',
            'parent': 'development',
            'help': 'Swift is a powerful and intuitive programming language for macOS, iOS, watchOS, tvOS and beyond.'
        },
        {
            'id': 'dart',
            'label': 'Dart',
            'description': 'Flutter language',
            'parent': 'development',
            'help': 'Dart is a client-optimized language for fast apps on any platform.'
        },
        {
            'id': 'flutter',
            'label': 'Flutter SDK',
            'description': 'Cross-platform UI toolkit',
            'parent': 'development',
            'help': 'Flutter is Google\'s UI toolkit for building beautiful, natively compiled applications.'
        },
        {
            'id': 'julia',
            'label': 'Julia',
            'description': 'Scientific computing',
            'parent': 'development',
            'help': 'Julia is a high-level, high-performance, dynamic programming language for numerical computing.'
        },
        {
            'id': 'r-lang',
            'label': 'R Language',
            'description': 'Statistical computing',
            'parent': 'development',
            'help': 'R is a programming language and free software environment for statistical computing and graphics.'
        },
        {
            'id': 'haskell',
            'label': 'Haskell',
            'description': 'Functional programming',
            'parent': 'development',
            'help': 'Haskell is an advanced, purely functional programming language.'
        },
        {
            'id': 'elixir',
            'label': 'Elixir',
            'description': 'Dynamic functional language',
            'parent': 'development',
            'help': 'Elixir is a dynamic, functional language designed for building maintainable and scalable applications.'
        },
        {
            'id': 'clojure',
            'label': 'Clojure',
            'description': 'Lisp on JVM',
            'parent': 'development',
            'help': 'Clojure is a dynamic, general-purpose programming language, combining Lisp with Java.'
        },
        {
            'id': 'ocaml',
            'label': 'OCaml',
            'description': 'Functional language',
            'parent': 'development',
            'help': 'OCaml is an industrial strength programming language supporting functional, imperative and object-oriented styles.'
        },
        {
            'id': 'zig',
            'label': 'Zig',
            'description': 'Systems programming',
            'parent': 'development',
            'help': 'Zig is a general-purpose programming language and toolchain for maintaining robust, optimal, and reusable software.'
        },
        {
            'id': 'nim',
            'label': 'Nim',
            'description': 'Efficient expressive language',
            'parent': 'development',
            'help': 'Nim is a statically typed compiled systems programming language.'
        },
        {
            'id': 'crystal',
            'label': 'Crystal',
            'description': 'Ruby-like compiled language',
            'parent': 'development',
            'help': 'Crystal is a programming language with Ruby-like syntax but statically type-checked.'
        },
        {
            'id': 'lua',
            'label': 'Lua',
            'description': 'Lightweight scripting',
            'parent': 'development',
            'help': 'Lua is a powerful, efficient, lightweight, embeddable scripting language.'
        },
        {
            'id': 'perl',
            'label': 'Perl',
            'description': 'Practical extraction language',
            'parent': 'development',
            'help': 'Perl is a highly capable, feature-rich programming language with over 30 years of development.'
        },
        # Build Tools
        {
            'id': 'maven',
            'label': 'Maven',
            'description': 'Java build tool',
            'parent': 'development',
            'help': 'Apache Maven is a software project management and comprehension tool for Java projects.'
        },
        {
            'id': 'gradle',
            'label': 'Gradle',
            'description': 'Build automation',
            'parent': 'development',
            'help': 'Gradle is a build automation tool for multi-language software development.'
        },
        {
            'id': 'cmake',
            'label': 'CMake',
            'description': 'Cross-platform build',
            'parent': 'development',
            'help': 'CMake is an open-source, cross-platform family of tools designed to build, test and package software.'
        },
        {
            'id': 'meson',
            'label': 'Meson',
            'description': 'Fast build system',
            'parent': 'development',
            'help': 'Meson is an open source build system meant to be both extremely fast and user friendly.'
        },
        {
            'id': 'bazel',
            'label': 'Bazel',
            'description': 'Google build tool',
            'parent': 'development',
            'help': 'Bazel is a fast, scalable, multi-language and extensible build system.'
        },
        {
            'id': 'ninja',
            'label': 'Ninja',
            'description': 'Small build system',
            'parent': 'development',
            'help': 'Ninja is a small build system with a focus on speed.'
        },
        # Version Managers
        {
            'id': 'nvm',
            'label': 'NVM',
            'description': 'Node version manager',
            'parent': 'development',
            'help': 'NVM (Node Version Manager) allows you to install and manage multiple Node.js versions.'
        },
        {
            'id': 'pyenv',
            'label': 'pyenv',
            'description': 'Python version manager',
            'parent': 'development',
            'help': 'pyenv lets you easily switch between multiple versions of Python.'
        },
        {
            'id': 'rbenv',
            'label': 'rbenv',
            'description': 'Ruby version manager',
            'parent': 'development',
            'help': 'rbenv provides support for specifying application-specific Ruby versions.'
        },
        {
            'id': 'rustup',
            'label': 'rustup',
            'description': 'Rust toolchain installer',
            'parent': 'development',
            'help': 'rustup is an installer for the systems programming language Rust.'
        },
        {
            'id': 'sdkman',
            'label': 'SDKMAN!',
            'description': 'SDK version manager',
            'parent': 'development',
            'help': 'SDKMAN! is a tool for managing parallel versions of multiple Software Development Kits.'
        },
        # Code Quality Tools
        {
            'id': 'eslint',
            'label': 'ESLint',
            'description': 'JavaScript linter',
            'parent': 'development',
            'help': 'ESLint is a tool for identifying and reporting on patterns found in ECMAScript/JavaScript code.'
        },
        {
            'id': 'prettier',
            'label': 'Prettier',
            'description': 'Code formatter',
            'parent': 'development',
            'help': 'Prettier is an opinionated code formatter with support for many languages.'
        },
        {
            'id': 'black',
            'label': 'Black',
            'description': 'Python formatter',
            'parent': 'development',
            'help': 'Black is the uncompromising Python code formatter.'
        },
        {
            'id': 'ruff',
            'label': 'Ruff',
            'description': 'Fast Python linter',
            'parent': 'development',
            'help': 'Ruff is an extremely fast Python linter, written in Rust.'
        },
        {
            'id': 'rustfmt',
            'label': 'rustfmt',
            'description': 'Rust formatter',
            'parent': 'development',
            'help': 'rustfmt is a tool for formatting Rust code according to style guidelines.'
        },
        {
            'id': 'gofmt',
            'label': 'gofmt',
            'description': 'Go formatter',
            'parent': 'development',
            'help': 'gofmt is a tool that automatically formats Go source code.'
        },
        # Documentation Tools
        {
            'id': 'sphinx',
            'label': 'Sphinx',
            'description': 'Documentation generator',
            'parent': 'development',
            'help': 'Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.'
        },
        {
            'id': 'mkdocs',
            'label': 'MkDocs',
            'description': 'Project documentation',
            'parent': 'development',
            'help': 'MkDocs is a fast, simple and downright gorgeous static site generator for documentation.'
        },
        {
            'id': 'doxygen',
            'label': 'Doxygen',
            'description': 'Source code documentation',
            'parent': 'development',
            'help': 'Doxygen is the de facto standard tool for generating documentation from annotated source code.'
        },
        {
            'id': 'swagger',
            'label': 'Swagger Tools',
            'description': 'API documentation',
            'parent': 'development',
            'help': 'Swagger tools for designing, building, documenting, and consuming RESTful APIs.'
        },
        # Testing Frameworks
        {
            'id': 'jest',
            'label': 'Jest',
            'description': 'JavaScript testing',
            'parent': 'development',
            'help': 'Jest is a delightful JavaScript Testing Framework with a focus on simplicity.'
        },
        {
            'id': 'pytest',
            'label': 'pytest',
            'description': 'Python testing',
            'parent': 'development',
            'help': 'pytest is a mature full-featured Python testing tool.'
        },
        {
            'id': 'junit',
            'label': 'JUnit',
            'description': 'Java testing',
            'parent': 'development',
            'help': 'JUnit is a simple framework to write repeatable tests for Java.'
        },
        {
            'id': 'mocha',
            'label': 'Mocha',
            'description': 'JavaScript test framework',
            'parent': 'development',
            'help': 'Mocha is a feature-rich JavaScript test framework running on Node.js.'
        },
        {
            'id': 'cypress',
            'label': 'Cypress',
            'description': 'End-to-end testing',
            'parent': 'development',
            'help': 'Cypress is a next generation front end testing tool built for the modern web.'
        },
        {
            'id': 'selenium',
            'label': 'Selenium',
            'description': 'Web browser automation',
            'parent': 'development',
            'help': 'Selenium is a suite of tools for automating web browsers.'
        },
        # DevOps Tools
        {
            'id': 'jenkins',
            'label': 'Jenkins',
            'description': 'CI/CD server',
            'parent': 'development',
            'help': 'Jenkins is an open source automation server for building, deploying and automating projects.'
        },
        {
            'id': 'gitlab-runner',
            'label': 'GitLab Runner',
            'description': 'CI/CD runner',
            'parent': 'development',
            'help': 'GitLab Runner is an application that works with GitLab CI/CD to run jobs in a pipeline.'
        },
        {
            'id': 'github-cli',
            'label': 'GitHub CLI',
            'description': 'GitHub from terminal',
            'parent': 'development',
            'help': 'GitHub CLI brings GitHub to your terminal for seamless workflow.'
        },
        {
            'id': 'gitlab-cli',
            'label': 'GitLab CLI',
            'description': 'GitLab from terminal',
            'parent': 'development',
            'help': 'GitLab CLI (glab) is an open source GitLab command line tool.'
        },
        {
            'id': 'circleci-cli',
            'label': 'CircleCI CLI',
            'description': 'CircleCI from terminal',
            'parent': 'development',
            'help': 'CircleCI CLI is a command line interface for CircleCI.'
        },
        # Package Managers
        {
            'id': 'yarn',
            'label': 'Yarn',
            'description': 'Fast npm alternative',
            'parent': 'development',
            'help': 'Yarn is a package manager that doubles down as project manager.'
        },
        {
            'id': 'pnpm',
            'label': 'pnpm',
            'description': 'Efficient package manager',
            'parent': 'development',
            'help': 'pnpm is a fast, disk space efficient package manager.'
        },
        {
            'id': 'poetry',
            'label': 'Poetry',
            'description': 'Python dependency management',
            'parent': 'development',
            'help': 'Poetry is a tool for dependency management and packaging in Python.'
        },
        {
            'id': 'pipenv',
            'label': 'Pipenv',
            'description': 'Python dev workflow',
            'parent': 'development',
            'help': 'Pipenv is a tool that aims to bring the best of all packaging worlds to Python.'
        },
        {
            'id': 'cargo',
            'label': 'Cargo',
            'description': 'Rust package manager',
            'parent': 'development',
            'help': 'Cargo is the Rust package manager that downloads dependencies and compiles packages.'
        },
        {
            'id': 'composer',
            'label': 'Composer',
            'description': 'PHP dependency manager',
            'parent': 'development',
            'help': 'Composer is a tool for dependency management in PHP.'
        },
        {
            'id': 'bundler',
            'label': 'Bundler',
            'description': 'Ruby dependency manager',
            'parent': 'development',
            'help': 'Bundler provides a consistent environment for Ruby projects by tracking gems.'
        },
        # Terminal Tools
        {
            'id': 'tmux',
            'label': 'tmux',
            'description': 'Terminal multiplexer',
            'parent': 'development',
            'help': 'tmux is a terminal multiplexer that lets you switch between several programs in one terminal.'
        },
        {
            'id': 'screen',
            'label': 'GNU Screen',
            'description': 'Terminal multiplexer',
            'parent': 'development',
            'help': 'GNU Screen is a full-screen window manager that multiplexes physical terminals.'
        },
        {
            'id': 'alacritty',
            'label': 'Alacritty',
            'description': 'GPU-accelerated terminal',
            'parent': 'development',
            'help': 'Alacritty is a modern terminal emulator with sensible defaults and GPU acceleration.'
        },
        {
            'id': 'kitty',
            'label': 'Kitty',
            'description': 'Fast feature-rich terminal',
            'parent': 'development',
            'help': 'Kitty is a fast, feature-rich, GPU based terminal emulator.'
        },
        {
            'id': 'wezterm',
            'label': 'WezTerm',
            'description': 'GPU-accelerated terminal',
            'parent': 'development',
            'help': 'WezTerm is a powerful cross-platform terminal emulator and multiplexer.'
        },
        {
            'id': 'terminator',
            'label': 'Terminator',
            'description': 'Multiple terminals in one',
            'parent': 'development',
            'help': 'Terminator is a terminal emulator which supports tabs and multiple resizable terminal panels.'
        },
        {
            'id': 'tilix',
            'label': 'Tilix',
            'description': 'Tiling terminal emulator',
            'parent': 'development',
            'help': 'Tilix is an advanced GTK3 tiling terminal emulator.'
        },
        # CLI Utilities
        {
            'id': 'fzf',
            'label': 'fzf',
            'description': 'Fuzzy finder',
            'parent': 'development',
            'help': 'fzf is a general-purpose command-line fuzzy finder.'
        },
        {
            'id': 'ripgrep',
            'label': 'ripgrep',
            'description': 'Fast grep alternative',
            'parent': 'development',
            'help': 'ripgrep recursively searches directories for a regex pattern while respecting gitignore.'
        },
        {
            'id': 'fd',
            'label': 'fd',
            'description': 'Fast find alternative',
            'parent': 'development',
            'help': 'fd is a simple, fast and user-friendly alternative to find.'
        },
        {
            'id': 'bat',
            'label': 'bat',
            'description': 'Cat with syntax highlighting',
            'parent': 'development',
            'help': 'bat is a cat clone with syntax highlighting and Git integration.'
        },
        {
            'id': 'exa',
            'label': 'exa',
            'description': 'Modern ls replacement',
            'parent': 'development',
            'help': 'exa is a modern replacement for ls with more features and better defaults.'
        },
        {
            'id': 'lsd',
            'label': 'lsd',
            'description': 'LSDeluxe',
            'parent': 'development',
            'help': 'lsd is a rewrite of GNU ls with lots of added features like colors and icons.'
        },
        {
            'id': 'delta',
            'label': 'delta',
            'description': 'Better git diff',
            'parent': 'development',
            'help': 'delta provides language syntax highlighting for git and diff output.'
        },
        {
            'id': 'lazygit',
            'label': 'lazygit',
            'description': 'Terminal UI for git',
            'parent': 'development',
            'help': 'lazygit is a simple terminal UI for git commands.'
        },
        {
            'id': 'tig',
            'label': 'tig',
            'description': 'Text-mode git interface',
            'parent': 'development',
            'help': 'tig is an ncurses-based text-mode interface for git.'
        },
        {
            'id': 'gh',
            'label': 'GitHub CLI',
            'description': 'GitHub in terminal',
            'parent': 'development',
            'help': 'GitHub CLI brings pull requests, issues, and other GitHub concepts to the terminal.'
        },
        {
            'id': 'jq',
            'label': 'jq',
            'description': 'JSON processor',
            'parent': 'development',
            'help': 'jq is a lightweight and flexible command-line JSON processor.'
        },
        {
            'id': 'yq',
            'label': 'yq',
            'description': 'YAML processor',
            'parent': 'development',
            'help': 'yq is a portable command-line YAML processor.'
        },
        {
            'id': 'tree',
            'label': 'tree',
            'description': 'Directory listing',
            'parent': 'development',
            'help': 'tree is a recursive directory listing command with tree-like format.'
        },
        {
            'id': 'ncdu',
            'label': 'ncdu',
            'description': 'Disk usage analyzer',
            'parent': 'development',
            'help': 'ncdu is a disk usage analyzer with an ncurses interface.'
        },
        {
            'id': 'duf',
            'label': 'duf',
            'description': 'Disk usage/free utility',
            'parent': 'development',
            'help': 'duf is a better df alternative with a more user-friendly output.'
        },
        {
            'id': 'tldr',
            'label': 'tldr',
            'description': 'Simplified man pages',
            'parent': 'development',
            'help': 'tldr provides simplified and community-driven man pages.'
        },
        {
            'id': 'asciinema',
            'label': 'asciinema',
            'description': 'Terminal recorder',
            'parent': 'development',
            'help': 'asciinema lets you record and share terminal sessions.'
        },
    ]
    
    # AI/ML Tools
    ai_tools = [
        {
            'id': 'ollama',
            'label': 'Ollama',
            'description': 'Local LLM runner',
            'parent': 'ai-ml',
            'default': True,
            'help': 'Ollama makes running large language models locally simple and efficient. Supports models like Llama 3, Mistral, Gemma, and many more.'
        },
        {
            'id': 'pytorch',
            'label': 'PyTorch',
            'description': 'Deep learning framework',
            'parent': 'ai-ml',
            'help': 'PyTorch is the most popular deep learning framework for research with dynamic computation graphs and excellent GPU support.'
        },
        {
            'id': 'tensorflow',
            'label': 'TensorFlow',
            'description': 'ML framework by Google',
            'parent': 'ai-ml',
            'help': 'TensorFlow is an end-to-end open source platform for machine learning with comprehensive tools and libraries.'
        },
        {
            'id': 'jupyter-lab',
            'label': 'JupyterLab',
            'description': 'Interactive notebooks',
            'parent': 'ai-ml',
            'default': True,
            'help': 'JupyterLab is the next-gen interface for Jupyter notebooks, perfect for data science and machine learning experiments.'
        },
        {
            'id': 'stable-diffusion-webui',
            'label': 'Stable Diffusion WebUI',
            'description': 'AI image generation',
            'parent': 'ai-ml',
            'help': 'AUTOMATIC1111\'s WebUI is the most popular Stable Diffusion interface for generating images from text prompts.'
        },
        {
            'id': 'text-generation-webui',
            'label': 'Text Generation WebUI',
            'description': 'LLM chat interface',
            'parent': 'ai-ml',
            'help': 'Oobabooga\'s interface for running LLMs locally with many features including character roleplay and extensions.'
        },
        # Additional AI/ML Tools
        {
            'id': 'langchain',
            'label': 'LangChain',
            'description': 'LLM framework',
            'parent': 'ai-ml',
            'help': 'LangChain is a framework for developing applications powered by language models.'
        },
        {
            'id': 'huggingface-cli',
            'label': 'Hugging Face CLI',
            'description': 'Model hub access',
            'parent': 'ai-ml',
            'help': 'Hugging Face CLI for downloading and managing models from the Hugging Face Hub.'
        },
        {
            'id': 'transformers',
            'label': 'Transformers',
            'description': 'NLP library',
            'parent': 'ai-ml',
            'help': 'State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX.'
        },
        {
            'id': 'scikit-learn',
            'label': 'scikit-learn',
            'description': 'ML library',
            'parent': 'ai-ml',
            'help': 'Simple and efficient tools for predictive data analysis.'
        },
        {
            'id': 'pandas',
            'label': 'pandas',
            'description': 'Data analysis',
            'parent': 'ai-ml',
            'help': 'Fast, powerful, flexible and easy to use open source data analysis tool.'
        },
        {
            'id': 'numpy',
            'label': 'NumPy',
            'description': 'Numerical computing',
            'parent': 'ai-ml',
            'help': 'The fundamental package for scientific computing with Python.'
        },
        {
            'id': 'matplotlib',
            'label': 'Matplotlib',
            'description': 'Plotting library',
            'parent': 'ai-ml',
            'help': 'Comprehensive library for creating static, animated, and interactive visualizations.'
        },
        {
            'id': 'seaborn',
            'label': 'Seaborn',
            'description': 'Statistical plotting',
            'parent': 'ai-ml',
            'help': 'Python data visualization library based on matplotlib for statistical graphics.'
        },
        {
            'id': 'plotly',
            'label': 'Plotly',
            'description': 'Interactive plots',
            'parent': 'ai-ml',
            'help': 'Interactive, open-source, and browser-based graphing library.'
        },
        {
            'id': 'mlflow',
            'label': 'MLflow',
            'description': 'ML lifecycle',
            'parent': 'ai-ml',
            'help': 'Open source platform for the machine learning lifecycle.'
        },
        {
            'id': 'wandb',
            'label': 'Weights & Biases',
            'description': 'ML experiment tracking',
            'parent': 'ai-ml',
            'help': 'Developer tools for machine learning experiment tracking.'
        },
        {
            'id': 'tensorboard',
            'label': 'TensorBoard',
            'description': 'TensorFlow visualization',
            'parent': 'ai-ml',
            'help': 'TensorFlow\'s visualization toolkit for machine learning experimentation.'
        },
        {
            'id': 'keras',
            'label': 'Keras',
            'description': 'Deep learning API',
            'parent': 'ai-ml',
            'help': 'Deep learning API written in Python, running on top of TensorFlow.'
        },
        {
            'id': 'xgboost',
            'label': 'XGBoost',
            'description': 'Gradient boosting',
            'parent': 'ai-ml',
            'help': 'Optimized distributed gradient boosting library.'
        },
        {
            'id': 'lightgbm',
            'label': 'LightGBM',
            'description': 'Gradient boosting',
            'parent': 'ai-ml',
            'help': 'Fast, distributed, high performance gradient boosting framework.'
        },
        {
            'id': 'spacy',
            'label': 'spaCy',
            'description': 'NLP library',
            'parent': 'ai-ml',
            'help': 'Industrial-strength Natural Language Processing in Python.'
        },
        {
            'id': 'nltk',
            'label': 'NLTK',
            'description': 'Natural language toolkit',
            'parent': 'ai-ml',
            'help': 'Natural Language Toolkit for building Python programs to work with human language data.'
        },
        {
            'id': 'opencv',
            'label': 'OpenCV',
            'description': 'Computer vision',
            'parent': 'ai-ml',
            'help': 'Open Source Computer Vision Library for image and video processing.'
        },
        {
            'id': 'fastai',
            'label': 'fast.ai',
            'description': 'Deep learning library',
            'parent': 'ai-ml',
            'help': 'Deep learning library that provides practitioners with high-level components.'
        },
        {
            'id': 'ray',
            'label': 'Ray',
            'description': 'Distributed AI',
            'parent': 'ai-ml',
            'help': 'Open source framework for building distributed applications.'
        },
        {
            'id': 'dask',
            'label': 'Dask',
            'description': 'Parallel computing',
            'parent': 'ai-ml',
            'help': 'Flexible library for parallel computing in Python.'
        },
        {
            'id': 'airflow',
            'label': 'Apache Airflow',
            'description': 'Workflow automation',
            'parent': 'ai-ml',
            'help': 'Platform to programmatically author, schedule and monitor workflows.'
        },
        {
            'id': 'prefect',
            'label': 'Prefect',
            'description': 'Dataflow automation',
            'parent': 'ai-ml',
            'help': 'The easiest way to automate your data.'
        },
        {
            'id': 'dagster',
            'label': 'Dagster',
            'description': 'Data orchestration',
            'parent': 'ai-ml',
            'help': 'Cloud-native data pipeline orchestrator for the whole development lifecycle.'
        },
        {
            'id': 'kedro',
            'label': 'Kedro',
            'description': 'Data pipelines',
            'parent': 'ai-ml',
            'help': 'Python framework for creating reproducible, maintainable and modular data science code.'
        },
        {
            'id': 'great-expectations',
            'label': 'Great Expectations',
            'description': 'Data validation',
            'parent': 'ai-ml',
            'help': 'Tool for validating, documenting, and profiling your data.'
        },
        {
            'id': 'labelimg',
            'label': 'LabelImg',
            'description': 'Image annotation',
            'parent': 'ai-ml',
            'help': 'Graphical image annotation tool for object detection.'
        },
        {
            'id': 'label-studio',
            'label': 'Label Studio',
            'description': 'Data labeling',
            'parent': 'ai-ml',
            'help': 'Open source data labeling tool for multiple data types.'
        },
        {
            'id': 'streamlit',
            'label': 'Streamlit',
            'description': 'ML app framework',
            'parent': 'ai-ml',
            'help': 'The fastest way to build and share data apps.'
        },
        {
            'id': 'gradio',
            'label': 'Gradio',
            'description': 'ML demos',
            'parent': 'ai-ml',
            'help': 'Build and share delightful machine learning apps.'
        },
        {
            'id': 'dash',
            'label': 'Dash',
            'description': 'Analytical web apps',
            'parent': 'ai-ml',
            'help': 'Python framework for building analytical web applications.'
        },
        {
            'id': 'bokeh',
            'label': 'Bokeh',
            'description': 'Interactive visualization',
            'parent': 'ai-ml',
            'help': 'Interactive visualization library for modern web browsers.'
        },
        {
            'id': 'altair',
            'label': 'Altair',
            'description': 'Declarative visualization',
            'parent': 'ai-ml',
            'help': 'Declarative statistical visualization library for Python.'
        },
        {
            'id': 'holoviews',
            'label': 'HoloViews',
            'description': 'Data visualization',
            'parent': 'ai-ml',
            'help': 'Data visualization library that makes data analysis and visualization seamless.'
        },
        {
            'id': 'panel',
            'label': 'Panel',
            'description': 'Dashboards',
            'parent': 'ai-ml',
            'help': 'High-level app and dashboarding solution for Python.'
        },
        {
            'id': 'voila',
            'label': 'Voilà',
            'description': 'Jupyter dashboards',
            'parent': 'ai-ml',
            'help': 'Turn Jupyter notebooks into standalone web applications.'
        },
        {
            'id': 'nbconvert',
            'label': 'nbconvert',
            'description': 'Notebook converter',
            'parent': 'ai-ml',
            'help': 'Convert Jupyter notebooks to various formats.'
        },
        {
            'id': 'papermill',
            'label': 'Papermill',
            'description': 'Parameterize notebooks',
            'parent': 'ai-ml',
            'help': 'Tool for parameterizing and executing Jupyter Notebooks.'
        },
        {
            'id': 'nbdime',
            'label': 'nbdime',
            'description': 'Notebook diff/merge',
            'parent': 'ai-ml',
            'help': 'Tools for diffing and merging of Jupyter notebooks.'
        },
        {
            'id': 'jupytext',
            'label': 'Jupytext',
            'description': 'Notebooks as text',
            'parent': 'ai-ml',
            'help': 'Jupyter notebooks as Markdown documents, Julia, Python or R scripts.'
        },
        {
            'id': 'dvc',
            'label': 'DVC',
            'description': 'Data version control',
            'parent': 'ai-ml',
            'help': 'Data Version Control - Git for data and ML models.'
        },
        {
            'id': 'cml',
            'label': 'CML',
            'description': 'CI/CD for ML',
            'parent': 'ai-ml',
            'help': 'Continuous Machine Learning - CI/CD for ML projects.'
        },
        {
            'id': 'bentoml',
            'label': 'BentoML',
            'description': 'ML model serving',
            'parent': 'ai-ml',
            'help': 'The easiest way to serve AI/ML models in production.'
        },
        {
            'id': 'seldon-core',
            'label': 'Seldon Core',
            'description': 'ML deployment',
            'parent': 'ai-ml',
            'help': 'Open source platform for deploying machine learning models on Kubernetes.'
        },
        {
            'id': 'kubeflow',
            'label': 'Kubeflow',
            'description': 'ML on Kubernetes',
            'parent': 'ai-ml',
            'help': 'Machine Learning toolkit for Kubernetes.'
        },
        {
            'id': 'polyaxon',
            'label': 'Polyaxon',
            'description': 'ML platform',
            'parent': 'ai-ml',
            'help': 'Platform for building, training, and monitoring large scale deep learning applications.'
        },
    ]
    
    # Desktop Environments
    desktop_envs = [
        {
            'id': 'gnome',
            'label': 'GNOME',
            'description': 'Modern, clean desktop',
            'parent': 'desktop',
            'default': True,
            'help': 'GNOME is a modern desktop environment focusing on simplicity and ease of use with a clean interface.',
            'ansible_var': 'desktop_environment'
        },
        {
            'id': 'kde',
            'label': 'KDE Plasma',
            'description': 'Customizable desktop',
            'parent': 'desktop',
            'help': 'KDE Plasma is a highly customizable desktop environment with powerful features and beautiful visuals.',
            'ansible_var': 'desktop_environment'
        },
        {
            'id': 'xfce',
            'label': 'XFCE',
            'description': 'Lightweight desktop',
            'parent': 'desktop',
            'help': 'XFCE is a lightweight desktop environment that\'s fast and low on system resources while being visually appealing.',
            'ansible_var': 'desktop_environment'
        },
        {
            'id': 'cinnamon',
            'label': 'Cinnamon',
            'description': 'Traditional desktop',
            'parent': 'desktop',
            'help': 'Cinnamon provides a traditional desktop experience with a Windows-like layout and modern features.',
            'ansible_var': 'desktop_environment'
        },
        {
            'id': 'mate',
            'label': 'MATE',
            'description': 'Classic GNOME 2 continuation',
            'parent': 'desktop',
            'help': 'MATE is a fork of GNOME 2 providing a traditional desktop experience with modern technology.',
            'ansible_var': 'desktop_environment'
        },
        {
            'id': 'budgie',
            'label': 'Budgie',
            'description': 'Modern desktop by Solus',
            'parent': 'desktop',
            'help': 'Budgie is a desktop environment designed with the modern user in mind, focusing on simplicity and elegance.'
        },
        {
            'id': 'lxde',
            'label': 'LXDE',
            'description': 'Lightweight X11 desktop',
            'parent': 'desktop',
            'help': 'LXDE is an extremely fast-performing and energy-saving desktop environment.'
        },
        {
            'id': 'lxqt',
            'label': 'LXQt',
            'description': 'Lightweight Qt desktop',
            'parent': 'desktop',
            'help': 'LXQt is a lightweight Qt desktop environment that is fast and maintains a traditional desktop interface.'
        },
        {
            'id': 'enlightenment',
            'label': 'Enlightenment',
            'description': 'Compositing window manager',
            'parent': 'desktop',
            'help': 'Enlightenment is a compositing window manager and desktop shell that is highly configurable and visually appealing.'
        },
        {
            'id': 'deepin',
            'label': 'Deepin',
            'description': 'Beautiful Chinese desktop',
            'parent': 'desktop',
            'help': 'Deepin Desktop Environment is an elegant desktop environment originally created for Deepin Linux distribution.'
        },
        {
            'id': 'hyprland',
            'label': 'Hyprland',
            'description': 'Wayland compositor',
            'parent': 'desktop',
            'help': 'Hyprland is a dynamic tiling Wayland compositor that\'s highly customizable with smooth animations.'
        },
        # Window Managers
        {
            'id': 'i3',
            'label': 'i3',
            'description': 'Tiling window manager',
            'parent': 'desktop',
            'help': 'i3 is a tiling window manager designed for X11, targeting experienced users and developers.'
        },
        {
            'id': 'sway',
            'label': 'Sway',
            'description': 'i3-compatible Wayland WM',
            'parent': 'desktop',
            'help': 'Sway is a tiling Wayland compositor and a drop-in replacement for the i3 window manager.'
        },
        {
            'id': 'awesome',
            'label': 'Awesome WM',
            'description': 'Configurable framework WM',
            'parent': 'desktop',
            'help': 'Awesome is a highly configurable, framework window manager for X, configured in Lua.'
        },
        {
            'id': 'bspwm',
            'label': 'bspwm',
            'description': 'Binary space partitioning WM',
            'parent': 'desktop',
            'help': 'bspwm is a tiling window manager that represents windows as the leaves of a full binary tree.'
        },
        {
            'id': 'dwm',
            'label': 'dwm',
            'description': 'Dynamic window manager',
            'parent': 'desktop',
            'help': 'dwm is an extremely fast, small, and dynamic window manager for X written by suckless.'
        },
        {
            'id': 'openbox',
            'label': 'Openbox',
            'description': 'Lightweight stacking WM',
            'parent': 'desktop',
            'help': 'Openbox is a highly configurable, lightweight window manager with extensive standards support.'
        },
        {
            'id': 'qtile',
            'label': 'Qtile',
            'description': 'Python-based tiling WM',
            'parent': 'desktop',
            'help': 'Qtile is a full-featured, hackable tiling window manager written and configured in Python.'
        },
        {
            'id': 'river',
            'label': 'River',
            'description': 'Dynamic Wayland compositor',
            'parent': 'desktop',
            'help': 'River is a dynamic tiling Wayland compositor with flexible runtime configuration.'
        },
        {
            'id': 'wayfire',
            'label': 'Wayfire',
            'description': '3D Wayland compositor',
            'parent': 'desktop',
            'help': 'Wayfire is a 3D Wayland compositor inspired by Compiz with a focus on customizability.'
        },
        {
            'id': 'herbstluftwm',
            'label': 'herbstluftwm',
            'description': 'Manual tiling WM',
            'parent': 'desktop',
            'help': 'herbstluftwm is a manual tiling window manager for X11 using Xlib and Glib.'
        },
        {
            'id': 'spectrwm',
            'label': 'spectrwm',
            'description': 'Small dynamic tiling WM',
            'parent': 'desktop',
            'help': 'spectrwm is a small dynamic tiling window manager for X11, largely inspired by xmonad and dwm.'
        },
        {
            'id': 'xmonad',
            'label': 'XMonad',
            'description': 'Haskell tiling WM',
            'parent': 'desktop',
            'help': 'XMonad is a dynamically tiling X11 window manager that is written and configured in Haskell.'
        },
        {
            'id': 'leftwm',
            'label': 'LeftWM',
            'description': 'Theming tiling WM',
            'parent': 'desktop',
            'help': 'LeftWM is a tiling window manager written in Rust that aims to be stable and performant.'
        },
    ]
    
    # Themes and Appearance
    themes = [
        # Global Theme Selector
        {
            'id': 'global-theme',
            'label': 'Global Theme',
            'description': 'Apply theme system-wide',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'dracula',
            'config_options': [
                ('dracula', 'Dracula - Dark elegant theme'),
                ('catppuccin-mocha', 'Catppuccin Mocha - Soothing pastel dark'),
                ('catppuccin-latte', 'Catppuccin Latte - Soothing pastel light'),
                ('nord', 'Nord - Arctic blue palette'),
                ('gruvbox-dark', 'Gruvbox Dark - Retro warm colors'),
                ('gruvbox-light', 'Gruvbox Light - Retro warm light'),
                ('solarized-dark', 'Solarized Dark - Precision colors'),
                ('solarized-light', 'Solarized Light - Precision light'),
                ('tokyo-night', 'Tokyo Night - Modern dark theme'),
                ('one-dark', 'One Dark - Atom-inspired dark'),
                ('material', 'Material - Google Material Design'),
                ('monokai-pro', 'Monokai Pro - Vibrant colors'),
                ('ayu-dark', 'Ayu Dark - Simple and bright'),
                ('ayu-light', 'Ayu Light - Light and peaceful'),
                ('everforest', 'Everforest - Green forest theme'),
                ('rose-pine', 'Rose Pine - All natural pine theme'),
                ('default', 'System Default'),
            ],
            'ansible_var': 'themes_global_theme',
            'help': 'Select a theme to apply across all supported applications including terminals, editors, browsers, and system UI.'
        },
        # Desktop Themes
        {
            'id': 'theme-dracula',
            'label': 'Dracula Theme',
            'description': 'Dark elegant theme',
            'parent': 'desktop',
            'help': 'Dracula is a dark theme with carefully chosen colors for comfortable viewing.'
        },
        {
            'id': 'theme-catppuccin-mocha',
            'label': 'Catppuccin Mocha',
            'description': 'Soothing pastel dark',
            'parent': 'desktop',
            'help': 'Catppuccin Mocha is a soothing pastel theme with dark background and warm colors.'
        },
        {
            'id': 'theme-catppuccin-latte',
            'label': 'Catppuccin Latte',
            'description': 'Soothing pastel light',
            'parent': 'desktop',
            'help': 'Catppuccin Latte is a soothing pastel theme with light background and soft colors.'
        },
        {
            'id': 'theme-catppuccin-frappe',
            'label': 'Catppuccin Frappé',
            'description': 'Soothing pastel mid-tone',
            'parent': 'desktop',
            'help': 'Catppuccin Frappé is a soothing pastel theme with mid-tone background.'
        },
        {
            'id': 'theme-catppuccin-macchiato',
            'label': 'Catppuccin Macchiato',
            'description': 'Soothing pastel darker',
            'parent': 'desktop',
            'help': 'Catppuccin Macchiato is a soothing pastel theme with darker background.'
        },
        {
            'id': 'theme-tokyo-night',
            'label': 'Tokyo Night',
            'description': 'Modern dark theme',
            'parent': 'desktop',
            'help': 'Tokyo Night is a clean, dark theme inspired by Tokyo\'s night lights.'
        },
        {
            'id': 'theme-nord',
            'label': 'Nord',
            'description': 'Arctic blue palette',
            'parent': 'desktop',
            'help': 'Nord is an arctic, north-bluish color palette with clean and elegant colors.'
        },
        {
            'id': 'theme-gruvbox',
            'label': 'Gruvbox',
            'description': 'Retro groove colors',
            'parent': 'desktop',
            'help': 'Gruvbox is a retro groove color scheme with warm colors and vintage feel.'
        },
        {
            'id': 'theme-solarized-dark',
            'label': 'Solarized Dark',
            'description': 'Precision colors dark',
            'parent': 'desktop',
            'help': 'Solarized Dark is a precision color scheme for accurate color representation.'
        },
        {
            'id': 'theme-solarized-light',
            'label': 'Solarized Light',
            'description': 'Precision colors light',
            'parent': 'desktop',
            'help': 'Solarized Light is a precision color scheme with light background.'
        },
        {
            'id': 'theme-one-dark',
            'label': 'One Dark',
            'description': 'Atom-inspired dark',
            'parent': 'desktop',
            'help': 'One Dark is inspired by Atom\'s default dark theme with vibrant colors.'
        },
        {
            'id': 'theme-arc',
            'label': 'Arc Theme',
            'description': 'Flat theme with transparent elements',
            'parent': 'desktop',
            'help': 'Arc is a flat theme with transparent elements for GTK3, GTK2 and GNOME Shell.'
        },
        {
            'id': 'theme-materia',
            'label': 'Materia',
            'description': 'Material Design theme',
            'parent': 'desktop',
            'help': 'Materia is a Material Design theme for GNOME/GTK based desktop environments.'
        },
        # Font Management
        {
            'id': 'font-interface',
            'label': 'Interface Font',
            'description': 'System UI font',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'Ubuntu 11',
            'config_options': [
                ('Ubuntu 11', 'Ubuntu 11pt'),
                ('Ubuntu 10', 'Ubuntu 10pt'),
                ('Ubuntu 12', 'Ubuntu 12pt'),
                ('Noto Sans 11', 'Noto Sans 11pt'),
                ('DejaVu Sans 11', 'DejaVu Sans 11pt'),
                ('Liberation Sans 11', 'Liberation Sans 11pt'),
                ('Roboto 11', 'Roboto 11pt'),
                ('Cantarell 11', 'Cantarell 11pt'),
                ('Sans 11', 'System Sans 11pt'),
            ],
            'ansible_var': 'de_font_interface',
            'help': 'Font used for system interface elements like menus and buttons.'
        },
        {
            'id': 'font-document',
            'label': 'Document Font',
            'description': 'Default document font',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'Sans 11',
            'config_options': [
                ('Sans 11', 'Sans Serif 11pt'),
                ('Serif 11', 'Serif 11pt'),
                ('Ubuntu 11', 'Ubuntu 11pt'),
                ('Liberation Sans 11', 'Liberation Sans 11pt'),
                ('Liberation Serif 11', 'Liberation Serif 11pt'),
                ('DejaVu Sans 11', 'DejaVu Sans 11pt'),
                ('DejaVu Serif 11', 'DejaVu Serif 11pt'),
                ('Noto Sans 11', 'Noto Sans 11pt'),
                ('Noto Serif 11', 'Noto Serif 11pt'),
            ],
            'ansible_var': 'de_font_document',
            'help': 'Default font for documents and text editors.'
        },
        {
            'id': 'font-monospace',
            'label': 'Monospace Font',
            'description': 'Terminal and code font',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'Ubuntu Mono 13',
            'config_options': [
                ('Ubuntu Mono 13', 'Ubuntu Mono 13pt'),
                ('Ubuntu Mono 12', 'Ubuntu Mono 12pt'),
                ('Ubuntu Mono 14', 'Ubuntu Mono 14pt'),
                ('JetBrains Mono 12', 'JetBrains Mono 12pt'),
                ('Hack 12', 'Hack 12pt'),
                ('Fira Code 12', 'Fira Code 12pt'),
                ('Source Code Pro 12', 'Source Code Pro 12pt'),
                ('Inconsolata 13', 'Inconsolata 13pt'),
                ('Cascadia Code 12', 'Cascadia Code 12pt'),
                ('DejaVu Sans Mono 12', 'DejaVu Sans Mono 12pt'),
                ('Liberation Mono 12', 'Liberation Mono 12pt'),
            ],
            'ansible_var': 'de_font_monospace',
            'help': 'Font used for terminals, code editors, and monospace text.'
        },
        {
            'id': 'font-title',
            'label': 'Window Title Font',
            'description': 'Window titlebar font',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'Ubuntu Bold 11',
            'config_options': [
                ('Ubuntu Bold 11', 'Ubuntu Bold 11pt'),
                ('Ubuntu Bold 10', 'Ubuntu Bold 10pt'),
                ('Ubuntu Bold 12', 'Ubuntu Bold 12pt'),
                ('Ubuntu Medium 11', 'Ubuntu Medium 11pt'),
                ('Noto Sans Bold 11', 'Noto Sans Bold 11pt'),
                ('DejaVu Sans Bold 11', 'DejaVu Sans Bold 11pt'),
                ('Liberation Sans Bold 11', 'Liberation Sans Bold 11pt'),
                ('Roboto Bold 11', 'Roboto Bold 11pt'),
                ('Cantarell Bold 11', 'Cantarell Bold 11pt'),
            ],
            'ansible_var': 'de_font_title',
            'help': 'Font used for window title bars.'
        },
        {
            'id': 'font-antialiasing',
            'label': 'Font Antialiasing',
            'description': 'Smooth font edges',
            'parent': 'desktop',
            'config_type': 'toggle',
            'config_value': True,
            'ansible_var': 'de_font_antialiasing',
            'help': 'Enable antialiasing for smoother font rendering.'
        },
        {
            'id': 'font-hinting',
            'label': 'Font Hinting',
            'description': 'Optimize font clarity',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'slight',
            'config_options': [
                ('none', 'No hinting'),
                ('slight', 'Slight hinting'),
                ('medium', 'Medium hinting'),
                ('full', 'Full hinting'),
            ],
            'ansible_var': 'de_font_hinting',
            'help': 'Font hinting improves the clarity of fonts at small sizes.'
        },
        {
            'id': 'font-size-scaling',
            'label': 'Font Size Scaling',
            'description': 'Global font size adjustment',
            'parent': 'desktop',
            'config_type': 'slider',
            'config_range': (80, 150),
            'config_value': 100,
            'config_unit': '%',
            'ansible_var': 'fonts_global_scaling',
            'help': 'Scale all fonts by this percentage. 100% is normal size.'
        },
        {
            'id': 'nerd-fonts-pack',
            'label': 'Nerd Fonts Collection',
            'description': 'Programming fonts with icons',
            'parent': 'desktop',
            'config_type': 'dropdown',
            'config_value': 'jetbrains-mono',
            'config_options': [
                ('jetbrains-mono', 'JetBrains Mono - Modern coding font'),
                ('hack', 'Hack - Source code font'),
                ('fira-code', 'Fira Code - Font with ligatures'),
                ('cascadia-code', 'Cascadia Code - Microsoft font'),
                ('source-code-pro', 'Source Code Pro - Adobe font'),
                ('ubuntu-mono', 'Ubuntu Mono - Ubuntu default'),
                ('inconsolata', 'Inconsolata - Monospace font'),
                ('meslo', 'Meslo LG - Customized Menlo'),
                ('iosevka', 'Iosevka - Slender typeface'),
                ('victor-mono', 'Victor Mono - Programming font'),
            ],
            'ansible_var': 'fonts_nerd_font_selection',
            'help': 'Nerd Fonts are programming fonts patched with additional icons for terminals and editors.'
        },
        # Icon Themes
        {
            'id': 'icons-papirus',
            'label': 'Papirus Icons',
            'description': 'Modern icon theme',
            'parent': 'desktop',
            'help': 'Papirus is a free and open source SVG icon theme with material-like design.'
        },
        {
            'id': 'icons-numix',
            'label': 'Numix Icons',
            'description': 'Circle icon theme',
            'parent': 'desktop',
            'help': 'Numix is a modern flat icon theme with circular application icons.'
        },
        {
            'id': 'icons-tela',
            'label': 'Tela Icons',
            'description': 'Colorful icon theme',
            'parent': 'desktop',
            'help': 'Tela is a flat colorful icon theme with rounded square icons.'
        },
        {
            'id': 'icons-qogir',
            'label': 'Qogir Icons',
            'description': 'Colorful design icons',
            'parent': 'desktop',
            'help': 'Qogir is a flat colorful design icon theme for linux desktops.'
        },
        # Fonts
        {
            'id': 'font-jetbrains-mono',
            'label': 'JetBrains Mono',
            'description': 'Developer font with ligatures',
            'parent': 'desktop',
            'help': 'JetBrains Mono is a free and open source typeface for developers with ligatures.'
        },
        {
            'id': 'font-fira-code',
            'label': 'Fira Code',
            'description': 'Monospaced font with ligatures',
            'parent': 'desktop',
            'help': 'Fira Code is a monospaced font with programming ligatures.'
        },
        {
            'id': 'font-source-code-pro',
            'label': 'Source Code Pro',
            'description': 'Adobe\'s coding font',
            'parent': 'desktop',
            'help': 'Source Code Pro is a monospaced font designed for coding by Adobe.'
        },
        {
            'id': 'font-cascadia-code',
            'label': 'Cascadia Code',
            'description': 'Microsoft\'s coding font',
            'parent': 'desktop',
            'help': 'Cascadia Code is a monospaced font by Microsoft with programming ligatures.'
        },
        {
            'id': 'font-nerd-fonts',
            'label': 'Nerd Fonts',
            'description': 'Fonts with icons',
            'parent': 'desktop',
            'help': 'Nerd Fonts patches developer targeted fonts with icons and glyphs.'
        },
        # Terminal Themes
        {
            'id': 'term-theme-dracula',
            'label': 'Dracula Terminal',
            'description': 'Dark terminal theme',
            'parent': 'desktop',
            'help': 'Dracula theme for your terminal with carefully selected colors.'
        },
        {
            'id': 'term-theme-catppuccin',
            'label': 'Catppuccin Terminal',
            'description': 'Pastel terminal colors',
            'parent': 'desktop',
            'help': 'Catppuccin terminal theme with soothing pastel colors.'
        },
        {
            'id': 'term-theme-tokyo-night',
            'label': 'Tokyo Night Terminal',
            'description': 'Clean dark terminal',
            'parent': 'desktop',
            'help': 'Tokyo Night theme for terminal with modern color scheme.'
        },
    ]
    
    # Applications
    applications = [
        # Browsers
        {
            'id': 'firefox',
            'label': 'Firefox',
            'description': 'Open source browser',
            'parent': 'applications',
            'default': True,
            'help': 'Firefox is a free and open source web browser developed by Mozilla with strong privacy features.'
        },
        {
            'id': 'chrome',
            'label': 'Google Chrome',
            'description': 'Popular web browser',
            'parent': 'applications',
            'help': 'Google Chrome is a fast, secure, and free web browser built for the modern web.'
        },
        {
            'id': 'brave',
            'label': 'Brave',
            'description': 'Privacy-focused browser',
            'parent': 'applications',
            'help': 'Brave is a privacy-focused browser that blocks ads and trackers by default.'
        },
        {
            'id': 'librewolf',
            'label': 'LibreWolf',
            'description': 'Privacy-hardened Firefox',
            'parent': 'applications',
            'help': 'LibreWolf is a custom version of Firefox focused on privacy, security, and freedom.'
        },
        {
            'id': 'vivaldi',
            'label': 'Vivaldi',
            'description': 'Feature-rich customizable browser',
            'parent': 'applications',
            'help': 'Vivaldi is a freeware, cross-platform web browser with a built-in email client, extensive customization options, and power user features.'
        },
        {
            'id': 'waterfox',
            'label': 'Waterfox',
            'description': 'Privacy-focused Firefox fork',
            'parent': 'applications',
            'help': 'Waterfox is a Firefox-based browser that maintains support for legacy extensions and focuses on privacy.'
        },
        {
            'id': 'min-browser',
            'label': 'Min Browser',
            'description': 'Minimalist web browser',
            'parent': 'applications',
            'help': 'Min is a fast, minimal browser that protects your privacy with built-in ad blocking and minimal data collection.'
        },
        {
            'id': 'qutebrowser',
            'label': 'qutebrowser',
            'description': 'Keyboard-driven browser',
            'parent': 'applications',
            'help': 'qutebrowser is a keyboard-focused browser with a minimal GUI using Python and Qt.'
        },
        {
            'id': 'tor-browser',
            'label': 'Tor Browser',
            'description': 'Anonymous browsing',
            'parent': 'applications',
            'help': 'Tor Browser prevents anyone from learning your location or browsing habits through onion routing.'
        },
        {
            'id': 'opera',
            'label': 'Opera',
            'description': 'Feature-rich browser with free VPN',
            'parent': 'applications',
            'help': 'Opera is a multi-platform web browser with built-in VPN, ad blocker, and various productivity features.'
        },
        {
            'id': 'microsoft-edge',
            'label': 'Microsoft Edge',
            'description': 'Microsoft\'s Chromium browser',
            'parent': 'applications',
            'help': 'Microsoft Edge is a cross-platform browser based on Chromium with Microsoft integrations.'
        },
        # Productivity
        {
            'id': 'libreoffice',
            'label': 'LibreOffice',
            'description': 'Office suite',
            'parent': 'applications',
            'default': True,
            'help': 'LibreOffice is a powerful open source office suite with word processing, spreadsheets, presentations, and more.'
        },
        {
            'id': 'thunderbird',
            'label': 'Thunderbird',
            'description': 'Email client',
            'parent': 'applications',
            'help': 'Thunderbird is a free email application that\'s easy to set up and customize with many features.'
        },
        {
            'id': 'obsidian',
            'label': 'Obsidian',
            'description': 'Knowledge base and note-taking',
            'parent': 'applications',
            'help': 'Obsidian is a powerful knowledge base that works on top of a local folder of plain text Markdown files.'
        },
        {
            'id': 'notion',
            'label': 'Notion',
            'description': 'All-in-one workspace',
            'parent': 'applications',
            'help': 'Notion is an all-in-one workspace for notes, tasks, wikis, and databases.'
        },
        {
            'id': 'zettlr',
            'label': 'Zettlr',
            'description': 'Markdown editor for researchers',
            'parent': 'applications',
            'help': 'Zettlr is a Markdown editor for the 21st century, designed for academic writing and note-taking.'
        },
        {
            'id': 'joplin',
            'label': 'Joplin',
            'description': 'Open source note-taking',
            'parent': 'applications',
            'help': 'Joplin is an open source note-taking app with synchronization capabilities for Windows, macOS, Linux, Android and iOS.'
        },
        {
            'id': 'standardnotes',
            'label': 'Standard Notes',
            'description': 'Encrypted notes app',
            'parent': 'applications',
            'help': 'Standard Notes is a free, open-source, and completely encrypted notes app.'
        },
        # Communication
        {
            'id': 'discord',
            'label': 'Discord',
            'description': 'Voice, video, and text chat',
            'parent': 'applications',
            'help': 'Discord is a proprietary freeware VoIP application designed for creating communities.'
        },
        {
            'id': 'slack',
            'label': 'Slack',
            'description': 'Team collaboration',
            'parent': 'applications',
            'help': 'Slack is a messaging app for business that connects people to the information they need.'
        },
        {
            'id': 'teams',
            'label': 'Microsoft Teams',
            'description': 'Business communication platform',
            'parent': 'applications',
            'help': 'Microsoft Teams is a proprietary business communication platform developed by Microsoft.'
        },
        {
            'id': 'element',
            'label': 'Element',
            'description': 'Secure decentralized chat',
            'parent': 'applications',
            'help': 'Element is a free and open-source software instant messaging client based on the Matrix protocol.'
        },
        {
            'id': 'signal',
            'label': 'Signal',
            'description': 'Private messaging',
            'parent': 'applications',
            'help': 'Signal is a cross-platform encrypted messaging service with a focus on privacy.'
        },
        {
            'id': 'telegram',
            'label': 'Telegram',
            'description': 'Cloud-based messaging',
            'parent': 'applications',
            'help': 'Telegram is a cloud-based instant messaging and voice over IP service.'
        },
        {
            'id': 'wire',
            'label': 'Wire',
            'description': 'Secure collaboration platform',
            'parent': 'applications',
            'help': 'Wire is an encrypted communication and collaboration app with messaging, voice, and video calls.'
        },
        # Media
        {
            'id': 'vlc',
            'label': 'VLC Media Player',
            'description': 'Universal media player',
            'parent': 'applications',
            'default': True,
            'help': 'VLC is a free and open source cross-platform multimedia player that plays most multimedia files.'
        },
        {
            'id': 'spotify',
            'label': 'Spotify',
            'description': 'Music streaming',
            'parent': 'applications',
            'help': 'Spotify is a digital music service that gives you access to millions of songs.'
        },
        {
            'id': 'gimp',
            'label': 'GIMP',
            'description': 'Image editor',
            'parent': 'applications',
            'help': 'GIMP is a free and open-source raster graphics editor used for image manipulation and editing.'
        },
        {
            'id': 'inkscape',
            'label': 'Inkscape',
            'description': 'Vector graphics editor',
            'parent': 'applications',
            'help': 'Inkscape is a free and open-source vector graphics editor used to create vector images.'
        },
        {
            'id': 'blender',
            'label': 'Blender',
            'description': '3D creation suite',
            'parent': 'applications',
            'help': 'Blender is a free and open-source 3D computer graphics software toolset for creating animated films, visual effects, and 3D games.'
        },
        {
            'id': 'kdenlive',
            'label': 'Kdenlive',
            'description': 'Video editor',
            'parent': 'applications',
            'help': 'Kdenlive is a free and open-source video editing software based on the MLT Framework, KDE and Qt.'
        },
        {
            'id': 'obs-studio',
            'label': 'OBS Studio',
            'description': 'Streaming and recording',
            'parent': 'applications',
            'help': 'OBS Studio is a free and open-source software for video recording and live streaming.'
        },
        {
            'id': 'audacity',
            'label': 'Audacity',
            'description': 'Audio editor',
            'parent': 'applications',
            'help': 'Audacity is a free and open-source digital audio editor and recording application software.'
        },
        {
            'id': 'handbrake',
            'label': 'HandBrake',
            'description': 'Video transcoder',
            'parent': 'applications',
            'help': 'HandBrake is a free and open-source transcoder for digital video files.'
        },
        # Office and Productivity
        {
            'id': 'libreoffice',
            'label': 'LibreOffice',
            'description': 'Office suite',
            'parent': 'applications',
            'default': True,
            'help': 'LibreOffice is a free and open source office suite compatible with Microsoft Office.',
            'ansible_var': 'productivity_apps'
        },
        {
            'id': 'onlyoffice',
            'label': 'OnlyOffice',
            'description': 'Office suite with cloud',
            'parent': 'applications',
            'help': 'ONLYOFFICE is an office suite that combines text, spreadsheet and presentation editors.'
        },
        {
            'id': 'wps-office',
            'label': 'WPS Office',
            'description': 'MS Office alternative',
            'parent': 'applications',
            'help': 'WPS Office is an office suite with high compatibility with Microsoft Office formats.'
        },
        {
            'id': 'calligra',
            'label': 'Calligra Suite',
            'description': 'KDE office suite',
            'parent': 'applications',
            'help': 'Calligra Suite is a graphic art and office suite by KDE.'
        },
        {
            'id': 'freeoffice',
            'label': 'FreeOffice',
            'description': 'SoftMaker office suite',
            'parent': 'applications',
            'help': 'FreeOffice is a full-featured office suite with high compatibility.'
        },
        # Document Viewers
        {
            'id': 'okular',
            'label': 'Okular',
            'description': 'Universal document viewer',
            'parent': 'applications',
            'help': 'Okular is a universal document viewer with support for PDF, ePub, and many other formats.'
        },
        {
            'id': 'evince',
            'label': 'Evince',
            'description': 'GNOME document viewer',
            'parent': 'applications',
            'help': 'Evince is a document viewer for multiple document formats like PDF and PostScript.'
        },
        {
            'id': 'calibre',
            'label': 'Calibre',
            'description': 'E-book manager',
            'parent': 'applications',
            'help': 'Calibre is a powerful e-book manager that can view, convert, and catalog e-books.'
        },
        {
            'id': 'sigil',
            'label': 'Sigil',
            'description': 'ePub editor',
            'parent': 'applications',
            'help': 'Sigil is a multi-platform EPUB ebook editor.'
        },
        # Note Taking
        {
            'id': 'joplin',
            'label': 'Joplin',
            'description': 'Note-taking with sync',
            'parent': 'applications',
            'help': 'Joplin is an open source note-taking app with synchronization capabilities.'
        },
        {
            'id': 'logseq',
            'label': 'Logseq',
            'description': 'Knowledge management',
            'parent': 'applications',
            'help': 'Logseq is a privacy-first, open-source knowledge base.'
        },
        {
            'id': 'zettlr',
            'label': 'Zettlr',
            'description': 'Markdown editor',
            'parent': 'applications',
            'help': 'Zettlr is a Markdown editor for the 21st century.'
        },
        {
            'id': 'trilium',
            'label': 'Trilium Notes',
            'description': 'Hierarchical note taking',
            'parent': 'applications',
            'help': 'Trilium Notes is a hierarchical note taking application with focus on building personal knowledge bases.'
        },
        {
            'id': 'cherrytree',
            'label': 'CherryTree',
            'description': 'Hierarchical note taking',
            'parent': 'applications',
            'help': 'CherryTree is a hierarchical note taking application, featuring rich text and syntax highlighting.'
        },
        # Email Clients
        {
            'id': 'thunderbird',
            'label': 'Thunderbird',
            'description': 'Email client',
            'parent': 'applications',
            'default': True,
            'help': 'Mozilla Thunderbird is a free and open source email, news, RSS, and chat client.',
            'ansible_var': 'productivity_apps'
        },
        {
            'id': 'evolution',
            'label': 'Evolution',
            'description': 'GNOME email client',
            'parent': 'applications',
            'help': 'Evolution is a personal information management application that provides email, calendar, and address book.'
        },
        {
            'id': 'kmail',
            'label': 'KMail',
            'description': 'KDE email client',
            'parent': 'applications',
            'help': 'KMail is the email component of Kontact, the integrated personal information manager from KDE.'
        },
        {
            'id': 'geary',
            'label': 'Geary',
            'description': 'Simple email client',
            'parent': 'applications',
            'help': 'Geary is an email client built for the GNOME desktop environment.'
        },
        {
            'id': 'claws-mail',
            'label': 'Claws Mail',
            'description': 'Lightweight email',
            'parent': 'applications',
            'help': 'Claws Mail is a GTK+ based, lightweight, and fast email client.'
        },
        # Calendar and Tasks
        {
            'id': 'gnome-calendar',
            'label': 'GNOME Calendar',
            'description': 'Simple calendar',
            'parent': 'applications',
            'help': 'GNOME Calendar is a simple and beautiful calendar application for GNOME.'
        },
        {
            'id': 'kalendar',
            'label': 'Kalendar',
            'description': 'KDE calendar',
            'parent': 'applications',
            'help': 'Kalendar is a calendar application that allows you to manage your tasks and events.'
        },
        {
            'id': 'planner',
            'label': 'Planner',
            'description': 'Task manager',
            'parent': 'applications',
            'help': 'Planner is a task manager with Todoist support designed for GNU/Linux.'
        },
        {
            'id': 'getting-things-gnome',
            'label': 'Getting Things GNOME',
            'description': 'GTD task manager',
            'parent': 'applications',
            'help': 'Getting Things GNOME is a personal tasks and TODO-list items organizer for GNOME.'
        },
        # Finance
        {
            'id': 'gnucash',
            'label': 'GnuCash',
            'description': 'Accounting software',
            'parent': 'applications',
            'help': 'GnuCash is personal and small-business financial-accounting software.'
        },
        {
            'id': 'kmymoney',
            'label': 'KMyMoney',
            'description': 'Personal finance manager',
            'parent': 'applications',
            'help': 'KMyMoney is a personal finance manager for KDE.'
        },
        {
            'id': 'skrooge',
            'label': 'Skrooge',
            'description': 'Personal finances manager',
            'parent': 'applications',
            'help': 'Skrooge is a personal finances manager for KDE, aiming to be simple and intuitive.'
        },
        {
            'id': 'homebank',
            'label': 'HomeBank',
            'description': 'Free personal finance',
            'parent': 'applications',
            'help': 'HomeBank is free software to manage your personal accounts.'
        },
        # Download Managers
        {
            'id': 'uget',
            'label': 'uGet',
            'description': 'Download manager',
            'parent': 'applications',
            'help': 'uGet is a lightweight yet powerful download manager.'
        },
        {
            'id': 'persepolis',
            'label': 'Persepolis',
            'description': 'Download manager GUI',
            'parent': 'applications',
            'help': 'Persepolis is a download manager & GUI for aria2 with lots of features.'
        },
        {
            'id': 'kget',
            'label': 'KGet',
            'description': 'KDE download manager',
            'parent': 'applications',
            'help': 'KGet is a versatile and user-friendly download manager.'
        },
        {
            'id': 'xtreme-download-manager',
            'label': 'Xtreme Download Manager',
            'description': 'Powerful downloader',
            'parent': 'applications',
            'help': 'Xtreme Download Manager is a powerful tool to increase download speed.'
        },
        # File Managers
        {
            'id': 'nautilus',
            'label': 'Nautilus',
            'description': 'GNOME file manager',
            'parent': 'applications',
            'help': 'Nautilus is the official file manager for the GNOME desktop.'
        },
        {
            'id': 'dolphin',
            'label': 'Dolphin',
            'description': 'KDE file manager',
            'parent': 'applications',
            'help': 'Dolphin is KDE\'s file manager that lets you navigate and browse the contents of your hard drives.'
        },
        {
            'id': 'thunar',
            'label': 'Thunar',
            'description': 'XFCE file manager',
            'parent': 'applications',
            'help': 'Thunar is a modern file manager for the Xfce Desktop Environment.'
        },
        {
            'id': 'pcmanfm',
            'label': 'PCManFM',
            'description': 'Lightweight file manager',
            'parent': 'applications',
            'help': 'PCManFM is an extremely fast, lightweight, yet feature-rich file manager.'
        },
        {
            'id': 'ranger',
            'label': 'Ranger',
            'description': 'Terminal file manager',
            'parent': 'applications',
            'help': 'Ranger is a console file manager with VI key bindings.'
        },
        {
            'id': 'mc',
            'label': 'Midnight Commander',
            'description': 'Terminal file manager',
            'parent': 'applications',
            'help': 'GNU Midnight Commander is a visual file manager with a text user interface.'
        },
        {
            'id': 'nemo',
            'label': 'Nemo',
            'description': 'Cinnamon file manager',
            'parent': 'applications',
            'help': 'Nemo is the official file manager for the Cinnamon desktop.'
        },
        {
            'id': 'krusader',
            'label': 'Krusader',
            'description': 'Twin panel file manager',
            'parent': 'applications',
            'help': 'Krusader is an advanced twin panel file manager for KDE.'
        },
        # Archive Managers
        {
            'id': 'file-roller',
            'label': 'File Roller',
            'description': 'GNOME archive manager',
            'parent': 'applications',
            'help': 'File Roller is an archive manager for the GNOME desktop environment.'
        },
        {
            'id': 'ark',
            'label': 'Ark',
            'description': 'KDE archive manager',
            'parent': 'applications',
            'help': 'Ark is a graphical file compression/decompression utility for KDE.'
        },
        {
            'id': 'peazip',
            'label': 'PeaZip',
            'description': 'Archive manager',
            'parent': 'applications',
            'help': 'PeaZip is a free file archiver utility and extractor.'
        },
        {
            'id': 'xarchiver',
            'label': 'Xarchiver',
            'description': 'GTK archive manager',
            'parent': 'applications',
            'help': 'Xarchiver is a GTK front-end for various command line archiving tools.'
        },
        # Remote Desktop
        {
            'id': 'remmina',
            'label': 'Remmina',
            'description': 'Remote desktop client',
            'parent': 'applications',
            'help': 'Remmina is a remote desktop client with support for RDP, VNC, SPICE, NX, XDMCP, SSH and more.'
        },
        {
            'id': 'vinagre',
            'label': 'Vinagre',
            'description': 'VNC client',
            'parent': 'applications',
            'help': 'Vinagre is a VNC, SSH, RDP and SPICE client for the GNOME desktop.'
        },
        {
            'id': 'krdc',
            'label': 'KRDC',
            'description': 'KDE remote desktop',
            'parent': 'applications',
            'help': 'KRDC is a client application that allows you to view or control desktop sessions on other machines.'
        },
        {
            'id': 'anydesk',
            'label': 'AnyDesk',
            'description': 'Remote access',
            'parent': 'applications',
            'help': 'AnyDesk is a remote desktop application distributed by AnyDesk Software GmbH.'
        },
        {
            'id': 'rustdesk',
            'label': 'RustDesk',
            'description': 'Open source remote desktop',
            'parent': 'applications',
            'help': 'RustDesk is an open source remote desktop client software written in Rust.'
        },
        # Screenshot Tools
        {
            'id': 'flameshot',
            'label': 'Flameshot',
            'description': 'Screenshot tool',
            'parent': 'applications',
            'help': 'Flameshot is a powerful yet simple to use screenshot software.'
        },
        {
            'id': 'spectacle',
            'label': 'Spectacle',
            'description': 'KDE screenshot',
            'parent': 'applications',
            'help': 'Spectacle is a screenshot taking utility for the KDE desktop.'
        },
        {
            'id': 'gnome-screenshot',
            'label': 'GNOME Screenshot',
            'description': 'GNOME screenshot tool',
            'parent': 'applications',
            'help': 'GNOME Screenshot is a utility for taking screenshots in GNOME.'
        },
        {
            'id': 'shutter',
            'label': 'Shutter',
            'description': 'Feature-rich screenshot',
            'parent': 'applications',
            'help': 'Shutter is a feature-rich screenshot program with editing capabilities.'
        },
        {
            'id': 'ksnip',
            'label': 'ksnip',
            'description': 'Cross-platform screenshot',
            'parent': 'applications',
            'help': 'ksnip is a Qt-based cross-platform screenshot tool with annotation features.'
        },
        # System Monitors
        {
            'id': 'htop',
            'label': 'htop',
            'description': 'Interactive process viewer',
            'parent': 'applications',
            'help': 'htop is an interactive process viewer for Unix systems.'
        },
        {
            'id': 'btop',
            'label': 'btop++',
            'description': 'Resource monitor',
            'parent': 'applications',
            'help': 'btop++ is a resource monitor that shows usage and stats for processor, memory, disks, network and processes.'
        },
        {
            'id': 'glances',
            'label': 'Glances',
            'description': 'System monitoring tool',
            'parent': 'applications',
            'help': 'Glances is a cross-platform monitoring tool written in Python.'
        },
        {
            'id': 'gnome-system-monitor',
            'label': 'GNOME System Monitor',
            'description': 'GNOME system monitor',
            'parent': 'applications',
            'help': 'GNOME System Monitor is a tool to manage running processes and monitor system resources.'
        },
        {
            'id': 'ksysguard',
            'label': 'KSysGuard',
            'description': 'KDE system monitor',
            'parent': 'applications',
            'help': 'KSysGuard is a system monitor for KDE.'
        },
        # Backup Tools
        {
            'id': 'timeshift',
            'label': 'Timeshift',
            'description': 'System restore utility',
            'parent': 'applications',
            'help': 'Timeshift is a system restore utility which takes snapshots of the system.'
        },
        {
            'id': 'deja-dup',
            'label': 'Déjà Dup',
            'description': 'Simple backup tool',
            'parent': 'applications',
            'help': 'Déjà Dup is a simple backup tool that hides the complexity of backing up.'
        },
        {
            'id': 'kbackup',
            'label': 'KBackup',
            'description': 'KDE backup program',
            'parent': 'applications',
            'help': 'KBackup is a program that lets you back up any directories or files.'
        },
        {
            'id': 'backintime',
            'label': 'Back In Time',
            'description': 'Snapshot backup',
            'parent': 'applications',
            'help': 'Back In Time is a simple backup tool inspired by the Flyback project and TimeVault.'
        },
        {
            'id': 'duplicati',
            'label': 'Duplicati',
            'description': 'Cloud backup',
            'parent': 'applications',
            'help': 'Duplicati is a backup client that securely stores encrypted backups on cloud storage services.'
        },
    ]
    
    # Security Tools
    security_tools = [
        {
            'id': 'ufw',
            'label': 'UFW Firewall',
            'description': 'Simple firewall',
            'parent': 'security',
            'default': True,
            'help': 'Uncomplicated Firewall (UFW) provides an easy to use interface for managing iptables firewall rules.'
        },
        {
            'id': 'fail2ban',
            'label': 'Fail2ban',
            'description': 'Intrusion prevention',
            'parent': 'security',
            'help': 'Fail2ban scans log files and bans IPs that show malicious signs like too many password failures.'
        },
        {
            'id': 'keepassxc',
            'label': 'KeePassXC',
            'description': 'Password manager',
            'parent': 'security',
            'default': True,
            'help': 'KeePassXC is a cross-platform password manager that stores passwords securely in an encrypted database.'
        },
        {
            'id': 'veracrypt',
            'label': 'VeraCrypt',
            'description': 'Disk encryption',
            'parent': 'security',
            'help': 'VeraCrypt is a free open source disk encryption software for Windows, Mac OS X and Linux.'
        },
        # Security Testing Tools
        {
            'id': 'nmap',
            'label': 'Nmap',
            'description': 'Network scanner',
            'parent': 'security',
            'help': 'Nmap is a free and open source utility for network discovery and security auditing.'
        },
        {
            'id': 'wireshark',
            'label': 'Wireshark',
            'description': 'Packet analyzer',
            'parent': 'security',
            'help': 'Wireshark is the world\'s foremost network protocol analyzer.'
        },
        {
            'id': 'metasploit',
            'label': 'Metasploit Framework',
            'description': 'Penetration testing',
            'parent': 'security',
            'help': 'Metasploit is a penetration testing framework that makes hacking simple.'
        },
        {
            'id': 'burpsuite',
            'label': 'Burp Suite',
            'description': 'Web security testing',
            'parent': 'security',
            'help': 'Burp Suite is an integrated platform for performing security testing of web applications.'
        },
        {
            'id': 'john',
            'label': 'John the Ripper',
            'description': 'Password cracker',
            'parent': 'security',
            'help': 'John the Ripper is a fast password cracker for many operating systems.'
        },
        {
            'id': 'hashcat',
            'label': 'Hashcat',
            'description': 'Advanced password recovery',
            'parent': 'security',
            'help': 'Hashcat is the world\'s fastest and most advanced password recovery utility.'
        },
        {
            'id': 'aircrack-ng',
            'label': 'Aircrack-ng',
            'description': 'WiFi security testing',
            'parent': 'security',
            'help': 'Aircrack-ng is a complete suite of tools to assess WiFi network security.'
        },
        {
            'id': 'hydra',
            'label': 'THC Hydra',
            'description': 'Network logon cracker',
            'parent': 'security',
            'help': 'Hydra is a parallelized login cracker which supports numerous protocols.'
        },
        {
            'id': 'sqlmap',
            'label': 'SQLMap',
            'description': 'SQL injection tool',
            'parent': 'security',
            'help': 'SQLMap is an open source penetration testing tool that automates SQL injection.'
        },
        {
            'id': 'nikto',
            'label': 'Nikto',
            'description': 'Web server scanner',
            'parent': 'security',
            'help': 'Nikto is an open source web server scanner which performs comprehensive tests.'
        },
        {
            'id': 'dirb',
            'label': 'DIRB',
            'description': 'Web content scanner',
            'parent': 'security',
            'help': 'DIRB is a web content scanner that looks for existing and hidden web objects.'
        },
        {
            'id': 'gobuster',
            'label': 'Gobuster',
            'description': 'Directory/file brute-forcer',
            'parent': 'security',
            'help': 'Gobuster is a tool used to brute-force URIs, DNS subdomains, and virtual host names.'
        },
        {
            'id': 'ffuf',
            'label': 'ffuf',
            'description': 'Web fuzzer',
            'parent': 'security',
            'help': 'ffuf is a fast web fuzzer written in Go.'
        },
        {
            'id': 'zaproxy',
            'label': 'OWASP ZAP',
            'description': 'Web app scanner',
            'parent': 'security',
            'help': 'OWASP ZAP is an open-source web application security scanner.'
        },
        {
            'id': 'beef',
            'label': 'BeEF',
            'description': 'Browser exploitation',
            'parent': 'security',
            'help': 'BeEF is a penetration testing tool that focuses on web browsers.'
        },
        # Privacy Tools
        {
            'id': 'tor-browser',
            'label': 'Tor Browser',
            'description': 'Anonymous browsing',
            'parent': 'security',
            'help': 'Tor Browser prevents anyone from learning your location or browsing habits.'
        },
        {
            'id': 'bitwarden',
            'label': 'Bitwarden',
            'description': 'Password manager',
            'parent': 'security',
            'help': 'Bitwarden is an open source password manager for individuals, teams, and businesses.'
        },
        {
            'id': 'protonvpn',
            'label': 'ProtonVPN',
            'description': 'Secure VPN service',
            'parent': 'security',
            'help': 'ProtonVPN is a security focused VPN service developed by CERN and MIT scientists.'
        },
        {
            'id': 'mullvad-vpn',
            'label': 'Mullvad VPN',
            'description': 'Privacy-focused VPN',
            'parent': 'security',
            'help': 'Mullvad is a VPN service that helps keep your online activity private.'
        },
        {
            'id': 'signal',
            'label': 'Signal Desktop',
            'description': 'Encrypted messaging',
            'parent': 'security',
            'help': 'Signal is a cross-platform encrypted messaging service.'
        },
        {
            'id': 'mat2',
            'label': 'MAT2',
            'description': 'Metadata removal',
            'parent': 'security',
            'help': 'MAT2 is a metadata removal tool, supporting a wide range of commonly used file formats.'
        },
        {
            'id': 'bleachbit',
            'label': 'BleachBit',
            'description': 'System cleaner',
            'parent': 'security',
            'help': 'BleachBit cleans files to free disk space and maintain privacy.'
        },
    ]
    
    # System Configuration
    system_config = [
        {
            'id': 'swappiness',
            'label': 'Swappiness',
            'description': 'Memory management (0-100)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 10,
            'help': 'Controls how aggressively the kernel swaps memory to disk. Lower values (1-10) keep more in RAM.'
        },
        {
            'id': 'enable-flatpak',
            'label': 'Enable Flatpak',
            'description': 'Universal app packages',
            'parent': 'system',
            'help': 'Flatpak is a framework for distributing desktop applications across various Linux distributions.'
        },
        {
            'id': 'enable-snap',
            'label': 'Enable Snap',
            'description': 'Snap package support',
            'parent': 'system',
            'default': True,
            'help': 'Snap is a software packaging and deployment system for Linux operating systems.'
        },
        # Display Settings
        {
            'id': 'display-scaling',
            'label': 'Display Scaling',
            'description': 'UI scaling factor (100-200%)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 100,
            'help': 'Adjust the scaling of UI elements for high-DPI displays. 100% is default, 200% doubles the size.'
        },
        {
            'id': 'night-light',
            'label': 'Night Light',
            'description': 'Blue light filter',
            'parent': 'system',
            'help': 'Reduces blue light emission for better sleep by warming the display colors at night.'
        },
        {
            'id': 'display-arrangement',
            'label': 'Display Arrangement',
            'description': 'Multi-monitor setup',
            'parent': 'system',
            'help': 'Configure the arrangement and position of multiple monitors.'
        },
        {
            'id': 'refresh-rate',
            'label': 'Display Refresh Rate',
            'description': 'Monitor refresh rate',
            'parent': 'system',
            'config_type': 'dropdown',
            'config_value': '60',
            'config_options': [
                ('60', '60 Hz'),
                ('75', '75 Hz'),
                ('120', '120 Hz'),
                ('144', '144 Hz'),
                ('165', '165 Hz'),
                ('240', '240 Hz'),
            ],
            'ansible_var': 'display_refresh_rate',
            'help': 'Set the refresh rate for your display (if supported).'
        },
        {
            'id': 'color-profile',
            'label': 'Color Profile',
            'description': 'Display color calibration',
            'parent': 'system',
            'help': 'Select or create a color profile for accurate color reproduction.'
        },
        # Mouse and Trackpad Settings
        {
            'id': 'mouse-speed',
            'label': 'Mouse Speed',
            'description': 'Pointer speed (1-10)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 5,
            'help': 'Adjust how fast the mouse pointer moves. 1 is slowest, 10 is fastest.'
        },
        {
            'id': 'mouse-acceleration',
            'label': 'Mouse Acceleration',
            'description': 'Adaptive pointer speed',
            'parent': 'system',
            'help': 'Enable mouse acceleration to make the pointer move faster when you move the mouse quickly.'
        },
        {
            'id': 'natural-scrolling',
            'label': 'Natural Scrolling',
            'description': 'Reverse scroll direction',
            'parent': 'system',
            'help': 'Scroll content in the same direction as finger movement (like touchscreens).'
        },
        {
            'id': 'natural-scroll',
            'label': 'Natural Scroll',
            'description': 'Reverse scroll direction',
            'parent': 'system',
            'help': 'Enable natural scrolling (reverse direction) for mouse and touchpad.'
        },
        {
            'id': 'scroll-speed',
            'label': 'Scroll Speed',
            'description': 'Mouse wheel speed',
            'parent': 'system',
            'config_type': 'slider',
            'config_range': (1, 20),
            'config_value': 10,
            'ansible_var': 'de_scroll_speed',
            'help': 'Adjust the speed of mouse wheel scrolling.'
        },
        {
            'id': 'tap-to-click',
            'label': 'Tap to Click',
            'description': 'Trackpad tap clicking',
            'parent': 'system',
            'help': 'Enable clicking by tapping the trackpad instead of pressing it.'
        },
        {
            'id': 'touchpad-tap-click',
            'label': 'Touchpad Tap to Click',
            'description': 'Enable tap clicking',
            'parent': 'system',
            'help': 'Enable clicking by tapping the touchpad.'
        },
        {
            'id': 'touchpad-gestures',
            'label': 'Touchpad Gestures',
            'description': 'Multi-finger gestures',
            'parent': 'system',
            'help': 'Enable multi-finger gestures for touchpad (swipe, pinch, etc.).'
        },
        # Keyboard Settings
        {
            'id': 'keyboard-repeat-rate',
            'label': 'Key Repeat Rate',
            'description': 'Speed of key repeats',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 30,
            'help': 'How fast keys repeat when held down (characters per second).'
        },
        {
            'id': 'keyboard-repeat-delay',
            'label': 'Key Repeat Delay',
            'description': 'Delay before repeat (ms)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 250,
            'help': 'How long to wait before a held key starts repeating (milliseconds).'
        },
        # Window Effects
        {
            'id': 'window-transparency',
            'label': 'Window Transparency',
            'description': 'Enable transparency effects',
            'parent': 'system',
            'help': 'Enable transparency and blur effects for windows and panels.'
        },
        {
            'id': 'animations',
            'label': 'Animations',
            'description': 'Enable UI animations',
            'parent': 'system',
            'default': True,
            'help': 'Enable smooth animations for window transitions and desktop effects.'
        },
        {
            'id': 'animation-speed',
            'label': 'Animation Speed',
            'description': 'Speed of animations (0.1-2.0)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 1.0,
            'help': 'Adjust the speed of desktop animations. Lower is faster, higher is slower.'
        },
        # Power Management
        {
            'id': 'power-profile',
            'label': 'Power Profile',
            'description': 'Performance vs battery',
            'parent': 'system',
            'help': 'Select between balanced, power saver, or performance power profiles.'
        },
        {
            'id': 'cpu-governor',
            'label': 'CPU Governor',
            'description': 'CPU frequency scaling',
            'parent': 'system',
            'config_type': 'dropdown',
            'config_value': 'powersave',
            'config_options': [
                ('performance', 'Performance - Maximum speed'),
                ('powersave', 'Powersave - Energy efficient'),
                ('ondemand', 'On Demand - Dynamic scaling'),
                ('conservative', 'Conservative - Gradual scaling'),
                ('schedutil', 'Schedutil - Scheduler based'),
            ],
            'ansible_var': 'system_cpu_governor',
            'help': 'Control how the CPU frequency scales based on system load.'
        },
        {
            'id': 'tlp-config',
            'label': 'TLP Power Management',
            'description': 'Advanced power saving',
            'parent': 'system',
            'help': 'TLP provides advanced power management for Linux with many optimizations.'
        },
        {
            'id': 'suspend-on-lid-close',
            'label': 'Suspend on Lid Close',
            'description': 'Laptop lid behavior',
            'parent': 'system',
            'default': True,
            'help': 'Suspend the system when the laptop lid is closed.'
        },
        {
            'id': 'battery-percentage',
            'label': 'Show Battery Percentage',
            'description': 'Display battery % in panel',
            'parent': 'system',
            'default': True,
            'help': 'Show battery percentage in the system panel instead of just an icon.'
        },
        # Sound Settings
        {
            'id': 'startup-sound',
            'label': 'Startup Sound',
            'description': 'Play sound on boot',
            'parent': 'system',
            'help': 'Play a sound when the system starts up.'
        },
        {
            'id': 'system-sounds',
            'label': 'System Sounds',
            'description': 'UI feedback sounds',
            'parent': 'system',
            'help': 'Enable sounds for system events like notifications and alerts.'
        },
    ]
    
    # Application Customization
    customization_items = [
        # Terminal Emulator Themes
        {
            'id': 'terminal-theme-dracula',
            'label': 'Terminal Dracula Theme',
            'description': 'Apply Dracula to terminal',
            'parent': 'customization',
            'help': 'Apply the Dracula color scheme to your terminal emulator (gnome-terminal, konsole, etc.).'
        },
        {
            'id': 'terminal-theme-catppuccin',
            'label': 'Terminal Catppuccin Theme',
            'description': 'Apply Catppuccin to terminal',
            'parent': 'customization',
            'help': 'Apply the Catppuccin color scheme to your terminal emulator.'
        },
        {
            'id': 'terminal-theme-tokyo-night',
            'label': 'Terminal Tokyo Night Theme',
            'description': 'Apply Tokyo Night to terminal',
            'parent': 'customization',
            'help': 'Apply the Tokyo Night color scheme to your terminal emulator.'
        },
        # VS Code Theme Integration
        {
            'id': 'vscode-theme-dracula',
            'label': 'VS Code Dracula Theme',
            'description': 'Install Dracula for VS Code',
            'parent': 'customization',
            'help': 'Install and activate the official Dracula theme for Visual Studio Code.'
        },
        {
            'id': 'vscode-theme-catppuccin',
            'label': 'VS Code Catppuccin Theme',
            'description': 'Install Catppuccin for VS Code',
            'parent': 'customization',
            'help': 'Install and activate the Catppuccin theme for Visual Studio Code.'
        },
        {
            'id': 'vscode-theme-tokyo-night',
            'label': 'VS Code Tokyo Night Theme',
            'description': 'Install Tokyo Night for VS Code',
            'parent': 'customization',
            'help': 'Install and activate the Tokyo Night theme for Visual Studio Code.'
        },
        # Browser Theme Integration
        {
            'id': 'firefox-theme-integration',
            'label': 'Firefox Theme Integration',
            'description': 'Match Firefox to system theme',
            'parent': 'customization',
            'default': True,
            'help': 'Configure Firefox to automatically match your system theme.'
        },
        {
            'id': 'chrome-theme-integration',
            'label': 'Chrome Theme Integration',
            'description': 'Match Chrome to system theme',
            'parent': 'customization',
            'help': 'Configure Chrome/Chromium to automatically match your system theme.'
        },
        # Application Font Settings
        {
            'id': 'app-font-antialiasing',
            'label': 'Font Antialiasing',
            'description': 'Smooth font rendering',
            'parent': 'customization',
            'default': True,
            'help': 'Enable font antialiasing for smoother text rendering across all applications.'
        },
        {
            'id': 'app-font-hinting',
            'label': 'Font Hinting',
            'description': 'Improve font clarity',
            'parent': 'customization',
            'default': True,
            'help': 'Enable font hinting to improve text clarity at small sizes.'
        },
        # Terminal Specific Customization
        {
            'id': 'terminal-bell-visual',
            'label': 'Visual Terminal Bell',
            'description': 'Flash instead of beep',
            'parent': 'customization',
            'help': 'Use a visual flash instead of an audible beep for terminal alerts.'
        },
        {
            'id': 'terminal-scrollback-lines',
            'label': 'Terminal Scrollback',
            'description': 'Lines of history (1000-50000)',
            'parent': 'customization',
            'is_configurable': True,
            'default_value': 10000,
            'help': 'Number of lines to keep in terminal scrollback history.'
        },
        {
            'id': 'terminal-confirm-close',
            'label': 'Confirm Terminal Close',
            'description': 'Warn before closing',
            'parent': 'customization',
            'default': True,
            'help': 'Show a confirmation dialog when closing a terminal with running processes.'
        },
        # Text Editor Customization
        {
            'id': 'editor-line-numbers',
            'label': 'Editor Line Numbers',
            'description': 'Show line numbers',
            'parent': 'customization',
            'default': True,
            'help': 'Display line numbers in text editors.'
        },
        {
            'id': 'editor-highlight-current-line',
            'label': 'Highlight Current Line',
            'description': 'Highlight active line',
            'parent': 'customization',
            'default': True,
            'help': 'Highlight the line where the cursor is positioned.'
        },
        {
            'id': 'editor-show-whitespace',
            'label': 'Show Whitespace',
            'description': 'Display spaces and tabs',
            'parent': 'customization',
            'help': 'Show visual indicators for spaces, tabs, and line endings.'
        },
        {
            'id': 'editor-auto-save',
            'label': 'Editor Auto Save',
            'description': 'Save files automatically',
            'parent': 'customization',
            'help': 'Automatically save files after changes with a delay.'
        },
        # Application Behavior
        {
            'id': 'app-single-click-activate',
            'label': 'Single Click Activation',
            'description': 'Open with single click',
            'parent': 'customization',
            'help': 'Open files and folders with a single click instead of double click.'
        },
        {
            'id': 'app-remember-window-position',
            'label': 'Remember Window Positions',
            'description': 'Restore window locations',
            'parent': 'customization',
            'default': True,
            'help': 'Remember and restore application window positions and sizes.'
        },
        {
            'id': 'app-global-menu',
            'label': 'Global Menu Bar',
            'description': 'Mac-style menu bar',
            'parent': 'customization',
            'help': 'Use a global menu bar at the top of the screen for all applications.'
        },
        # Development Tool Customization
        {
            'id': 'git-credential-helper',
            'label': 'Git Credential Helper',
            'description': 'Remember Git passwords',
            'parent': 'customization',
            'default': True,
            'help': 'Configure Git to securely remember your credentials.'
        },
        {
            'id': 'docker-desktop-integration',
            'label': 'Docker Desktop Integration',
            'description': 'Docker system tray icon',
            'parent': 'customization',
            'help': 'Enable Docker Desktop integration with system tray and notifications.'
        },
    ]
    
    # Gaming
    gaming_tools = [
        {
            'id': 'steam',
            'label': 'Steam',
            'description': 'Gaming platform',
            'parent': 'gaming',
            'help': 'Steam is the ultimate destination for playing, discussing, and creating games.'
        },
        {
            'id': 'lutris',
            'label': 'Lutris',
            'description': 'Gaming manager',
            'parent': 'gaming',
            'help': 'Lutris is an open gaming platform for Linux that helps you install and manage games.'
        },
        {
            'id': 'heroic',
            'label': 'Heroic Games Launcher',
            'description': 'Epic/GOG launcher',
            'parent': 'gaming',
            'help': 'Heroic is an open source game launcher for Epic Games and GOG.'
        },
        {
            'id': 'bottles',
            'label': 'Bottles',
            'description': 'Windows app runner',
            'parent': 'gaming',
            'help': 'Bottles helps you run Windows software and games on Linux.'
        },
        {
            'id': 'playonlinux',
            'label': 'PlayOnLinux',
            'description': 'Wine frontend',
            'parent': 'gaming',
            'help': 'PlayOnLinux is a graphical frontend for Wine compatibility layer.'
        },
        {
            'id': 'gamemode',
            'label': 'GameMode',
            'description': 'Gaming optimizer',
            'parent': 'gaming',
            'help': 'GameMode optimizes Linux system performance on demand for games.'
        },
        {
            'id': 'mangohud',
            'label': 'MangoHud',
            'description': 'Gaming overlay',
            'parent': 'gaming',
            'help': 'MangoHud is a Vulkan and OpenGL overlay for monitoring FPS, temperatures, CPU/GPU load.'
        },
        {
            'id': 'goverlay',
            'label': 'GOverlay',
            'description': 'MangoHud GUI',
            'parent': 'gaming',
            'help': 'GOverlay is a graphical UI to manage MangoHud, vkBasalt and ReplaySorcery.'
        },
        {
            'id': 'protontricks',
            'label': 'Protontricks',
            'description': 'Proton helper',
            'parent': 'gaming',
            'help': 'Protontricks helps you run Winetricks commands for Steam Play/Proton games.'
        },
    ]
    
    # Multimedia Production
    multimedia_tools = [
        {
            'id': 'obs-studio',
            'label': 'OBS Studio',
            'description': 'Streaming software',
            'parent': 'multimedia',
            'help': 'OBS Studio is free and open source software for video recording and live streaming.'
        },
        {
            'id': 'kdenlive',
            'label': 'Kdenlive',
            'description': 'Video editor',
            'parent': 'multimedia',
            'help': 'Kdenlive is a powerful free and open source video editor.'
        },
        {
            'id': 'shotcut',
            'label': 'Shotcut',
            'description': 'Cross-platform editor',
            'parent': 'multimedia',
            'help': 'Shotcut is a free, open source, cross-platform video editor.'
        },
        {
            'id': 'openshot',
            'label': 'OpenShot',
            'description': 'Simple video editor',
            'parent': 'multimedia',
            'help': 'OpenShot is an easy-to-use, powerful video editor.'
        },
        {
            'id': 'davinci-resolve',
            'label': 'DaVinci Resolve',
            'description': 'Professional editor',
            'parent': 'multimedia',
            'help': 'DaVinci Resolve is a professional video editing and color grading software.'
        },
        {
            'id': 'audacity',
            'label': 'Audacity',
            'description': 'Audio editor',
            'parent': 'multimedia',
            'help': 'Audacity is a free, open source, cross-platform audio software.'
        },
        {
            'id': 'ardour',
            'label': 'Ardour',
            'description': 'Digital audio workstation',
            'parent': 'multimedia',
            'help': 'Ardour is a professional digital audio workstation.'
        },
        {
            'id': 'lmms',
            'label': 'LMMS',
            'description': 'Music production',
            'parent': 'multimedia',
            'help': 'LMMS is a free cross-platform software for making music.'
        },
        {
            'id': 'hydrogen',
            'label': 'Hydrogen',
            'description': 'Drum machine',
            'parent': 'multimedia',
            'help': 'Hydrogen is an advanced drum machine for Linux.'
        },
        {
            'id': 'bitwig-studio',
            'label': 'Bitwig Studio',
            'description': 'Music production suite',
            'parent': 'multimedia',
            'help': 'Bitwig Studio is a multi-platform music-creation system.'
        },
        {
            'id': 'blender',
            'label': 'Blender',
            'description': '3D creation suite',
            'parent': 'multimedia',
            'help': 'Blender is a free and open source 3D creation suite.'
        },
        {
            'id': 'freecad',
            'label': 'FreeCAD',
            'description': 'Parametric 3D CAD',
            'parent': 'multimedia',
            'help': 'FreeCAD is an open-source parametric 3D modeler.'
        },
        {
            'id': 'openscad',
            'label': 'OpenSCAD',
            'description': 'Script-based CAD',
            'parent': 'multimedia',
            'help': 'OpenSCAD is a software for creating solid 3D CAD models.'
        },
        {
            'id': 'openshot',
            'label': 'OpenShot',
            'description': 'Video editor',
            'parent': 'multimedia',
            'help': 'OpenShot Video Editor is a free and open-source video editor for Linux, macOS, and Windows.'
        },
        {
            'id': 'davinci-resolve',
            'label': 'DaVinci Resolve',
            'description': 'Professional video editor',
            'parent': 'multimedia',
            'help': 'DaVinci Resolve is a professional video editing and color grading application.'
        },
        {
            'id': 'audacity',
            'label': 'Audacity',
            'description': 'Audio editor',
            'parent': 'multimedia',
            'help': 'Audacity is a free and open-source digital audio editor and recording application.'
        },
        {
            'id': 'ardour',
            'label': 'Ardour',
            'description': 'Digital audio workstation',
            'parent': 'multimedia',
            'help': 'Ardour is a hard disk recorder and digital audio workstation application.'
        },
        {
            'id': 'lmms',
            'label': 'LMMS',
            'description': 'Music production',
            'parent': 'multimedia',
            'help': 'LMMS is a free cross-platform alternative to commercial programs like FL Studio.'
        },
        {
            'id': 'hydrogen',
            'label': 'Hydrogen',
            'description': 'Drum machine',
            'parent': 'multimedia',
            'help': 'Hydrogen is an advanced drum machine for GNU/Linux, Windows and Mac OS X.'
        },
        {
            'id': 'bitwig-studio',
            'label': 'Bitwig Studio',
            'description': 'Music production suite',
            'parent': 'multimedia',
            'help': 'Bitwig Studio is a digital audio workstation for music production, remixing and live performance.'
        },
        {
            'id': 'krita',
            'label': 'Krita',
            'description': 'Digital painting',
            'parent': 'multimedia',
            'help': 'Krita is a professional free and open source painting program made by artists.'
        },
        {
            'id': 'inkscape',
            'label': 'Inkscape',
            'description': 'Vector graphics',
            'parent': 'multimedia',
            'help': 'Inkscape is a free and open-source vector graphics editor.'
        },
    ]
    
    # Networking Tools
    networking_tools = [
        {
            'id': 'wireshark',
            'label': 'Wireshark',
            'description': 'Network analyzer',
            'parent': 'networking',
            'help': 'Wireshark is the world\'s foremost network protocol analyzer.'
        },
        {
            'id': 'nmap',
            'label': 'Nmap',
            'description': 'Network scanner',
            'parent': 'networking',
            'help': 'Nmap is a free and open source utility for network discovery and security auditing.'
        },
        {
            'id': 'netcat',
            'label': 'Netcat',
            'description': 'Network utility',
            'parent': 'networking',
            'help': 'Netcat is a versatile networking utility for reading/writing network connections.'
        },
        {
            'id': 'tcpdump',
            'label': 'tcpdump',
            'description': 'Packet analyzer',
            'parent': 'networking',
            'help': 'tcpdump is a powerful command-line packet analyzer.'
        },
        {
            'id': 'iftop',
            'label': 'iftop',
            'description': 'Bandwidth monitor',
            'parent': 'networking',
            'help': 'iftop displays bandwidth usage on an interface in real-time.'
        },
        {
            'id': 'network-manager-hostname',
            'label': 'Hostname',
            'description': 'System hostname',
            'parent': 'networking',
            'config_type': 'text',
            'config_value': 'ubuntu',
            'ansible_var': 'system_hostname',
            'help': 'Set the system hostname for network identification.'
        },
    ]
    
    # Virtualization
    virtualization_tools = [
        {
            'id': 'virtualbox',
            'label': 'VirtualBox',
            'description': 'VM software',
            'parent': 'virtualization',
            'help': 'VirtualBox is a powerful x86 and AMD64/Intel64 virtualization product.'
        },
        {
            'id': 'vmware-workstation',
            'label': 'VMware Workstation',
            'description': 'Professional VM',
            'parent': 'virtualization',
            'help': 'VMware Workstation Pro is a hosted hypervisor for 64-bit computers.'
        },
        {
            'id': 'qemu-kvm',
            'label': 'QEMU/KVM',
            'description': 'Linux virtualization',
            'parent': 'virtualization',
            'help': 'QEMU with KVM provides near-native performance virtualization.'
        },
        {
            'id': 'virt-manager',
            'label': 'Virt-Manager',
            'description': 'VM management GUI',
            'parent': 'virtualization',
            'help': 'Virtual Machine Manager is a desktop tool for managing VMs via libvirt.'
        },
        {
            'id': 'gnome-boxes',
            'label': 'GNOME Boxes',
            'description': 'Simple VM tool',
            'parent': 'virtualization',
            'help': 'GNOME Boxes is a simple GNOME application to access virtual machines.'
        },
        {
            'id': 'podman',
            'label': 'Podman',
            'description': 'Daemonless containers',
            'parent': 'virtualization',
            'help': 'Podman is a daemonless container engine for developing and running containers.'
        },
        {
            'id': 'kubernetes',
            'label': 'Kubernetes Tools',
            'description': 'K8s orchestration',
            'parent': 'virtualization',
            'help': 'Kubernetes tools including kubectl, minikube, and kind.'
        },
        {
            'id': 'minikube',
            'label': 'Minikube',
            'description': 'Local Kubernetes',
            'parent': 'virtualization',
            'help': 'Minikube runs a single-node Kubernetes cluster locally.'
        },
        {
            'id': 'k9s',
            'label': 'K9s',
            'description': 'K8s terminal UI',
            'parent': 'virtualization',
            'help': 'K9s provides a terminal UI to interact with Kubernetes clusters.'
        },
        {
            'id': 'lens',
            'label': 'Lens',
            'description': 'Kubernetes IDE',
            'parent': 'virtualization',
            'help': 'Lens is the most powerful IDE for Kubernetes clusters.'
        },
        {
            'id': 'helm',
            'label': 'Helm',
            'description': 'K8s package manager',
            'parent': 'virtualization',
            'help': 'Helm is the package manager for Kubernetes.'
        },
        {
            'id': 'kubectl',
            'label': 'kubectl',
            'description': 'K8s CLI',
            'parent': 'virtualization',
            'help': 'kubectl is the Kubernetes command-line tool.'
        },
    ]
    
    # Cloud Tools
    cloud_tools = [
        {
            'id': 'aws-cli',
            'label': 'AWS CLI',
            'description': 'Amazon Web Services CLI',
            'parent': 'cloud-tools',
            'help': 'AWS CLI is a unified tool to manage your AWS services.'
        },
        {
            'id': 'gcloud',
            'label': 'Google Cloud SDK',
            'description': 'Google Cloud CLI',
            'parent': 'cloud-tools',
            'help': 'Google Cloud SDK is a set of tools for Google Cloud Platform.'
        },
        {
            'id': 'azure-cli',
            'label': 'Azure CLI',
            'description': 'Microsoft Azure CLI',
            'parent': 'cloud-tools',
            'help': 'Azure CLI is a cross-platform command-line tool for Azure.'
        },
        {
            'id': 'terraform',
            'label': 'Terraform',
            'description': 'Infrastructure as Code',
            'parent': 'cloud-tools',
            'help': 'Terraform enables you to create, change, and improve infrastructure.'
        },
        {
            'id': 'pulumi',
            'label': 'Pulumi',
            'description': 'Modern IaC',
            'parent': 'cloud-tools',
            'help': 'Pulumi is infrastructure as code using programming languages.'
        },
        {
            'id': 'ansible',
            'label': 'Ansible',
            'description': 'Automation tool',
            'parent': 'cloud-tools',
            'help': 'Ansible is an open-source automation tool for configuration management.'
        },
        {
            'id': 'vagrant',
            'label': 'Vagrant',
            'description': 'VM automation',
            'parent': 'cloud-tools',
            'help': 'Vagrant provides easy-to-configure, reproducible development environments.'
        },
        {
            'id': 'packer',
            'label': 'Packer',
            'description': 'Image builder',
            'parent': 'cloud-tools',
            'help': 'Packer automates the creation of machine images.'
        },
        {
            'id': 'vault',
            'label': 'HashiCorp Vault',
            'description': 'Secrets management',
            'parent': 'cloud-tools',
            'help': 'Vault secures, stores, and tightly controls access to secrets.'
        },
        {
            'id': 'consul',
            'label': 'Consul',
            'description': 'Service mesh',
            'parent': 'cloud-tools',
            'help': 'Consul is a service mesh solution providing service discovery and configuration.'
        },
    ]
    
    # Build complete item list
    items.extend(categories)
    items.extend(dev_tools)
    items.extend(ai_tools)
    items.extend(desktop_envs)
    items.extend(themes)
    items.extend(applications)
    items.extend(security_tools)
    items.extend(system_config)
    items.extend(customization_items)
    items.extend(gaming_tools)
    items.extend(multimedia_tools)
    items.extend(networking_tools)
    items.extend(virtualization_tools)
    items.extend(cloud_tools)
    
    # Update category children lists
    for item in items:
        if item.get('parent'):
            for category in categories:
                if category['id'] == item['parent']:
                    category['children'].append(item['id'])
                    break
                    
    return items