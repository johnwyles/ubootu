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
            'description': 'Cloud platform CLIs and tools',
            'icon': '☁️',
            'is_category': True,
            'parent': None,
            'children': []
        },
    ]
    
    # Add root categories first
    items.extend(categories)
    
    # Development subcategories
    dev_subcategories = [
        # Programming Languages
        {
            'id': 'dev-languages',
            'label': 'Programming Languages',
            'description': 'Compilers, interpreters, and runtimes',
            'icon': '🔤',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        {
            'id': 'dev-go',
            'label': 'Go',
            'description': 'Go language and tools',
            'icon': '🐹',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-python',
            'label': 'Python',
            'description': 'Python language and tools',
            'icon': '🐍',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-javascript',
            'label': 'JavaScript/TypeScript',
            'description': 'JS/TS runtimes and tools',
            'icon': '📜',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-rust',
            'label': 'Rust',
            'description': 'Rust language and tools',
            'icon': '🦀',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-java',
            'label': 'Java/Kotlin',
            'description': 'JVM languages and tools',
            'icon': '☕',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-cpp',
            'label': 'C/C++',
            'description': 'C/C++ compilers and tools',
            'icon': '🏗️',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-dotnet',
            'label': '.NET/C#',
            'description': '.NET SDK and tools',
            'icon': '🟦',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        {
            'id': 'dev-other-langs',
            'label': 'Other Languages',
            'description': 'Additional programming languages',
            'icon': '📚',
            'is_category': True,
            'parent': 'dev-languages',
            'children': []
        },
        
        # IDEs and Editors
        {
            'id': 'dev-ides',
            'label': 'IDEs & Editors',
            'description': 'Integrated development environments',
            'icon': '📝',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        {
            'id': 'dev-jetbrains',
            'label': 'JetBrains IDEs',
            'description': 'Professional IDEs by JetBrains',
            'icon': '🧠',
            'is_category': True,
            'parent': 'dev-ides',
            'children': []
        },
        {
            'id': 'dev-code-editors',
            'label': 'Code Editors',
            'description': 'Modern code editors',
            'icon': '✏️',
            'is_category': True,
            'parent': 'dev-ides',
            'children': []
        },
        {
            'id': 'dev-text-editors',
            'label': 'Text Editors',
            'description': 'Terminal and GUI text editors',
            'icon': '📄',
            'is_category': True,
            'parent': 'dev-ides',
            'children': []
        },
        
        # Version Control
        {
            'id': 'dev-vcs',
            'label': 'Version Control',
            'description': 'Source control systems',
            'icon': '🌿',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Containers & Orchestration
        {
            'id': 'dev-containers',
            'label': 'Containers & Orchestration',
            'description': 'Container platforms and tools',
            'icon': '📦',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Databases
        {
            'id': 'dev-databases',
            'label': 'Databases',
            'description': 'Database servers and tools',
            'icon': '🗄️',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        {
            'id': 'dev-sql-databases',
            'label': 'SQL Databases',
            'description': 'Relational databases',
            'icon': '🔍',
            'is_category': True,
            'parent': 'dev-databases',
            'children': []
        },
        {
            'id': 'dev-nosql-databases',
            'label': 'NoSQL Databases',
            'description': 'Non-relational databases',
            'icon': '📊',
            'is_category': True,
            'parent': 'dev-databases',
            'children': []
        },
        {
            'id': 'dev-db-tools',
            'label': 'Database Tools',
            'description': 'Database management tools',
            'icon': '🛠️',
            'is_category': True,
            'parent': 'dev-databases',
            'children': []
        },
        
        # API & Web Tools
        {
            'id': 'dev-api-tools',
            'label': 'API & Web Tools',
            'description': 'API testing and web development',
            'icon': '🌐',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Terminal & Shell
        {
            'id': 'dev-terminal',
            'label': 'Terminal & Shell',
            'description': 'Shells and terminal tools',
            'icon': '💻',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        {
            'id': 'dev-shells',
            'label': 'Shells',
            'description': 'Command line shells',
            'icon': '🐚',
            'is_category': True,
            'parent': 'dev-terminal',
            'children': []
        },
        {
            'id': 'dev-terminal-emulators',
            'label': 'Terminal Emulators',
            'description': 'Terminal applications',
            'icon': '🖥️',
            'is_category': True,
            'parent': 'dev-terminal',
            'children': []
        },
        {
            'id': 'dev-shell-enhancements',
            'label': 'Shell Enhancements',
            'description': 'Prompts and utilities',
            'icon': '✨',
            'is_category': True,
            'parent': 'dev-terminal',
            'children': []
        },
        
        # Cloud & Infrastructure
        {
            'id': 'dev-cloud',
            'label': 'Cloud & Infrastructure',
            'description': 'Cloud CLIs and IaC tools',
            'icon': '☁️',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Build & Development Tools
        {
            'id': 'dev-build-tools',
            'label': 'Build & Package Tools',
            'description': 'Build systems and package managers',
            'icon': '🔨',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Testing & Quality
        {
            'id': 'dev-testing',
            'label': 'Testing & Quality',
            'description': 'Testing frameworks and tools',
            'icon': '🧪',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Documentation
        {
            'id': 'dev-documentation',
            'label': 'Documentation',
            'description': 'Documentation generators',
            'icon': '📚',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Development Utilities
        {
            'id': 'dev-utilities',
            'label': 'Development Utilities',
            'description': 'Miscellaneous dev tools',
            'icon': '🔧',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        
        # Settings
        {
            'id': 'dev-editor-settings',
            'label': 'Editor Settings',
            'description': 'Configure editor preferences',
            'icon': '⚙️',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
        {
            'id': 'dev-terminal-settings',
            'label': 'Terminal Settings',
            'description': 'Configure terminal preferences',
            'icon': '⚙️',
            'is_category': True,
            'parent': 'development',
            'children': []
        },
    ]
    
    items.extend(dev_subcategories)
    
    # Update children for development category
    development_cat = next(cat for cat in categories if cat['id'] == 'development')
    development_cat['children'] = [
        'dev-languages', 'dev-ides', 'dev-vcs', 'dev-containers', 
        'dev-databases', 'dev-api-tools', 'dev-terminal', 'dev-cloud',
        'dev-build-tools', 'dev-testing', 'dev-documentation', 
        'dev-utilities', 'dev-editor-settings', 'dev-terminal-settings'
    ]
    
    # Update children for subcategories
    dev_languages = next(cat for cat in dev_subcategories if cat['id'] == 'dev-languages')
    dev_languages['children'] = [
        'dev-go', 'dev-python', 'dev-javascript', 'dev-rust', 
        'dev-java', 'dev-cpp', 'dev-dotnet', 'dev-other-langs'
    ]
    
    dev_ides = next(cat for cat in dev_subcategories if cat['id'] == 'dev-ides')
    dev_ides['children'] = ['dev-jetbrains', 'dev-code-editors', 'dev-text-editors']
    
    dev_databases = next(cat for cat in dev_subcategories if cat['id'] == 'dev-databases')
    dev_databases['children'] = ['dev-sql-databases', 'dev-nosql-databases', 'dev-db-tools']
    
    dev_terminal = next(cat for cat in dev_subcategories if cat['id'] == 'dev-terminal')
    dev_terminal['children'] = ['dev-shells', 'dev-terminal-emulators', 'dev-shell-enhancements']
    
    # Development items organized by category
    
    # Go tools
    go_items = [
        {
            'id': 'go',
            'label': 'Go',
            'description': 'Google\'s programming language',
            'parent': 'dev-go',
            'default': False,
            'help': 'Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.'
        },
        {
            'id': 'goland',
            'label': 'GoLand',
            'description': 'Go IDE by JetBrains',
            'parent': 'dev-go',
            'help': 'GoLand is JetBrains\' IDE for Go development with advanced code analysis.'
        },
        {
            'id': 'gofmt',
            'label': 'gofmt',
            'description': 'Go formatter',
            'parent': 'dev-go',
            'help': 'gofmt is a tool that automatically formats Go source code.'
        },
    ]
    
    # Python tools
    python_items = [
        {
            'id': 'python',
            'label': 'Python 3',
            'description': 'Python runtime and pip',
            'parent': 'dev-python',
            'default': True,
            'help': 'Python 3 runtime with pip package manager. The most popular language for scripting, web development, data science, and automation.'
        },
        {
            'id': 'pycharm',
            'label': 'PyCharm Community',
            'description': 'Python IDE by JetBrains',
            'parent': 'dev-python',
            'help': 'PyCharm Community Edition is the best Python IDE with intelligent code completion, debugging, testing, and virtual environment management.'
        },
        {
            'id': 'poetry',
            'label': 'Poetry',
            'description': 'Python dependency management',
            'parent': 'dev-python',
            'help': 'Poetry is a modern dependency management and packaging tool for Python.'
        },
        {
            'id': 'pipenv',
            'label': 'Pipenv',
            'description': 'Python dev workflow tool',
            'parent': 'dev-python',
            'help': 'Pipenv automatically creates and manages a virtualenv for your projects.'
        },
        {
            'id': 'pyenv',
            'label': 'pyenv',
            'description': 'Python version management',
            'parent': 'dev-python',
            'help': 'pyenv lets you easily switch between multiple versions of Python.'
        },
        {
            'id': 'black',
            'label': 'Black',
            'description': 'Python code formatter',
            'parent': 'dev-python',
            'help': 'Black is the uncompromising Python code formatter.'
        },
        {
            'id': 'pytest',
            'label': 'pytest',
            'description': 'Python testing framework',
            'parent': 'dev-python',
            'help': 'pytest is a mature full-featured Python testing tool.'
        },
    ]
    
    # JavaScript/TypeScript tools
    javascript_items = [
        {
            'id': 'nodejs',
            'label': 'Node.js',
            'description': 'JavaScript runtime',
            'parent': 'dev-javascript',
            'default': True,
            'help': 'Node.js JavaScript runtime built on Chrome\'s V8 engine. Essential for modern web development, React, Angular, Vue.js, and server-side JavaScript.'
        },
        {
            'id': 'webstorm',
            'label': 'WebStorm',
            'description': 'JavaScript IDE by JetBrains',
            'parent': 'dev-javascript',
            'help': 'WebStorm is JetBrains\' powerful IDE for JavaScript and related technologies.'
        },
        {
            'id': 'yarn',
            'label': 'Yarn',
            'description': 'Fast package manager',
            'parent': 'dev-javascript',
            'help': 'Yarn is a fast, reliable, and secure dependency management tool.'
        },
        {
            'id': 'pnpm',
            'label': 'pnpm',
            'description': 'Efficient package manager',
            'parent': 'dev-javascript',
            'help': 'pnpm is a fast, disk space efficient package manager.'
        },
        {
            'id': 'nvm',
            'label': 'NVM',
            'description': 'Node version manager',
            'parent': 'dev-javascript',
            'help': 'NVM allows you to quickly install and use different versions of Node.'
        },
        {
            'id': 'prettier',
            'label': 'Prettier',
            'description': 'Code formatter',
            'parent': 'dev-javascript',
            'help': 'Prettier is an opinionated code formatter for JavaScript, TypeScript, and more.'
        },
        {
            'id': 'eslint',
            'label': 'ESLint',
            'description': 'JavaScript linter',
            'parent': 'dev-javascript',
            'help': 'ESLint is a tool for identifying and reporting on patterns in JavaScript.'
        },
        {
            'id': 'jest',
            'label': 'Jest',
            'description': 'JavaScript testing',
            'parent': 'dev-javascript',
            'help': 'Jest is a delightful JavaScript testing framework with a focus on simplicity.'
        },
        {
            'id': 'mocha',
            'label': 'Mocha',
            'description': 'Test framework',
            'parent': 'dev-javascript',
            'help': 'Mocha is a feature-rich JavaScript test framework running on Node.js.'
        },
        {
            'id': 'bundler',
            'label': 'Bundler',
            'description': 'Module bundler',
            'parent': 'dev-javascript',
            'help': 'Modern JavaScript module bundler for building applications.'
        },
    ]
    
    # Rust tools
    rust_items = [
        {
            'id': 'rust',
            'label': 'Rust',
            'description': 'Systems programming language',
            'parent': 'dev-rust',
            'help': 'Rust is a language empowering everyone to build reliable and efficient software with memory safety and zero-cost abstractions.'
        },
        {
            'id': 'cargo',
            'label': 'Cargo',
            'description': 'Rust package manager',
            'parent': 'dev-rust',
            'help': 'Cargo is the Rust package manager that downloads dependencies and compiles packages.'
        },
        {
            'id': 'rustup',
            'label': 'rustup',
            'description': 'Rust toolchain installer',
            'parent': 'dev-rust',
            'help': 'rustup is the Rust toolchain installer and version management tool.'
        },
        {
            'id': 'rustfmt',
            'label': 'rustfmt',
            'description': 'Rust code formatter',
            'parent': 'dev-rust',
            'help': 'rustfmt is a tool for formatting Rust code according to style guidelines.'
        },
    ]
    
    # Java/Kotlin tools
    java_items = [
        {
            'id': 'java',
            'label': 'Java (OpenJDK)',
            'description': 'Java Development Kit',
            'parent': 'dev-java',
            'help': 'OpenJDK is the open-source implementation of the Java Platform.'
        },
        {
            'id': 'kotlin',
            'label': 'Kotlin',
            'description': 'Modern JVM language',
            'parent': 'dev-java',
            'help': 'Kotlin is a modern programming language that makes developers happier.'
        },
        {
            'id': 'intellij-idea',
            'label': 'IntelliJ IDEA Community',
            'description': 'Java/Kotlin IDE',
            'parent': 'dev-java',
            'help': 'IntelliJ IDEA Community Edition is JetBrains\' powerful Java IDE with smart code completion, refactoring tools, and built-in version control.'
        },
        {
            'id': 'android-studio',
            'label': 'Android Studio',
            'description': 'Android development',
            'parent': 'dev-java',
            'help': 'Android Studio is the official IDE for Android app development based on IntelliJ IDEA.'
        },
        {
            'id': 'gradle',
            'label': 'Gradle',
            'description': 'Build automation tool',
            'parent': 'dev-java',
            'help': 'Gradle is a build automation tool for multi-language software development.'
        },
        {
            'id': 'maven',
            'label': 'Maven',
            'description': 'Project management tool',
            'parent': 'dev-java',
            'help': 'Apache Maven is a software project management and comprehension tool.'
        },
    ]
    
    # C/C++ tools
    cpp_items = [
        {
            'id': 'clion',
            'label': 'CLion',
            'description': 'C/C++ IDE by JetBrains',
            'parent': 'dev-cpp',
            'help': 'CLion is JetBrains\' cross-platform IDE for C and C++ development.'
        },
        {
            'id': 'cmake',
            'label': 'CMake',
            'description': 'Build system generator',
            'parent': 'dev-cpp',
            'help': 'CMake is a cross-platform build system generator.'
        },
    ]
    
    # .NET/C# tools
    dotnet_items = [
        {
            'id': 'dotnet',
            'label': '.NET SDK',
            'description': '.NET development platform',
            'parent': 'dev-dotnet',
            'help': '.NET is a free, cross-platform, open source developer platform.'
        },
        {
            'id': 'rider',
            'label': 'Rider',
            'description': '.NET IDE by JetBrains',
            'parent': 'dev-dotnet',
            'help': 'Rider is JetBrains\' cross-platform .NET IDE based on IntelliJ and ReSharper.'
        },
    ]
    
    # Other languages
    other_lang_items = [
        {
            'id': 'php',
            'label': 'PHP',
            'description': 'PHP scripting language',
            'parent': 'dev-other-langs',
            'help': 'PHP is a popular general-purpose scripting language for web development.'
        },
        {
            'id': 'ruby',
            'label': 'Ruby',
            'description': 'Ruby programming language',
            'parent': 'dev-other-langs',
            'help': 'Ruby is a dynamic, interpreted programming language focused on simplicity.'
        },
        {
            'id': 'perl',
            'label': 'Perl',
            'description': 'Perl programming language',
            'parent': 'dev-other-langs',
            'help': 'Perl is a highly capable, feature-rich programming language.'
        },
        {
            'id': 'lua',
            'label': 'Lua',
            'description': 'Lightweight scripting',
            'parent': 'dev-other-langs',
            'help': 'Lua is a powerful, efficient, lightweight, embeddable scripting language.'
        },
        {
            'id': 'clojure',
            'label': 'Clojure',
            'description': 'Lisp on the JVM',
            'parent': 'dev-other-langs',
            'help': 'Clojure is a dynamic, functional programming language on the JVM.'
        },
        {
            'id': 'elixir',
            'label': 'Elixir',
            'description': 'Functional language',
            'parent': 'dev-other-langs',
            'help': 'Elixir is a dynamic, functional language designed for building scalable applications.'
        },
        {
            'id': 'haskell',
            'label': 'Haskell',
            'description': 'Pure functional language',
            'parent': 'dev-other-langs',
            'help': 'Haskell is an advanced, purely functional programming language.'
        },
        {
            'id': 'scala',
            'label': 'Scala',
            'description': 'JVM language',
            'parent': 'dev-other-langs',
            'help': 'Scala combines object-oriented and functional programming in one language.'
        },
        {
            'id': 'swift',
            'label': 'Swift',
            'description': 'Apple\'s language',
            'parent': 'dev-other-langs',
            'help': 'Swift is a powerful and intuitive programming language for Apple platforms.'
        },
        {
            'id': 'dart',
            'label': 'Dart',
            'description': 'Flutter language',
            'parent': 'dev-other-langs',
            'help': 'Dart is a client-optimized language for fast apps on any platform.'
        },
        {
            'id': 'julia',
            'label': 'Julia',
            'description': 'Scientific computing',
            'parent': 'dev-other-langs',
            'help': 'Julia is a high-level, high-performance language for technical computing.'
        },
        {
            'id': 'nim',
            'label': 'Nim',
            'description': 'Systems language',
            'parent': 'dev-other-langs',
            'help': 'Nim is a statically typed compiled systems programming language.'
        },
        {
            'id': 'zig',
            'label': 'Zig',
            'description': 'Systems language',
            'parent': 'dev-other-langs',
            'help': 'Zig is a general-purpose programming language and toolchain.'
        },
    ]
    
    # JetBrains IDEs
    jetbrains_items = [
        {
            'id': 'datagrip',
            'label': 'DataGrip',
            'description': 'Database IDE',
            'parent': 'dev-jetbrains',
            'help': 'DataGrip is JetBrains\' IDE for databases and SQL with smart query console.'
        },
    ]
    
    # Code Editors
    code_editor_items = [
        {
            'id': 'vscode',
            'label': 'Visual Studio Code',
            'description': 'Modern code editor',
            'parent': 'dev-code-editors',
            'default': True,
            'help': '''Visual Studio Code is Microsoft's free, open-source code editor with excellent language support, debugging, Git integration, and a vast extension ecosystem.

This will install:
- Visual Studio Code (latest stable version)
- code command-line tool for opening files/folders

Extensions automatically installed:
- Python (ms-python.python) - IntelliSense, linting, debugging, code formatting
- Docker (ms-azuretools.vscode-docker) - Build, manage, and deploy containerized applications
- GitLens (eamodio.gitlens) - Supercharge Git within VS Code
- Prettier (esbenp.prettier-vscode) - Code formatter for JavaScript, TypeScript, CSS
- ESLint (dbaeumer.vscode-eslint) - JavaScript linting
- Live Server (ritwickdey.liveserver) - Launch a local development server
- Remote Development Pack - Work with remote machines, containers, and WSL

Settings configured:
- Auto-save enabled after delay
- Format on save enabled
- Terminal integrated with system shell
- Git integration enabled
- Telemetry disabled for privacy
- Theme synced with system preference (if selected)

Keybindings added:
- Ctrl+` - Toggle integrated terminal
- Ctrl+Shift+P - Command palette
- Ctrl+P - Quick file open
- F5 - Start debugging

System integration:
- Adds VS Code repository for automatic updates
- Creates desktop shortcut
- Registers as default editor for common file types
- Integrates with system file manager context menu'''
        },
        {
            'id': 'cursor',
            'label': 'Cursor',
            'description': 'AI-powered code editor',
            'parent': 'dev-code-editors',
            'help': 'Cursor is an AI-first code editor that helps you code faster with AI assistance.'
        },
        {
            'id': 'zed',
            'label': 'Zed',
            'description': 'High-performance code editor',
            'parent': 'dev-code-editors',
            'help': 'Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.'
        },
        {
            'id': 'sublime-text',
            'label': 'Sublime Text',
            'description': 'Fast text editor',
            'parent': 'dev-code-editors',
            'help': 'Sublime Text is a sophisticated text editor for code, markup and prose with a slick user interface and extraordinary features.'
        },
    ]
    
    # Text Editors
    text_editor_items = [
        {
            'id': 'vim',
            'label': 'Vim',
            'description': 'Terminal editor',
            'parent': 'dev-text-editors',
            'help': 'Vim is a highly configurable text editor built to enable efficient text editing. It\'s an improved version of the vi editor.'
        },
        {
            'id': 'neovim',
            'label': 'Neovim',
            'description': 'Modern Vim fork',
            'parent': 'dev-text-editors',
            'help': 'Neovim is a refactor of Vim aiming to improve extensibility and maintainability with better plugin architecture.'
        },
        {
            'id': 'emacs',
            'label': 'Emacs',
            'description': 'Extensible text editor',
            'parent': 'dev-text-editors',
            'help': 'GNU Emacs is an extensible, customizable, self-documenting text editor.'
        },
    ]
    
    # Version Control
    vcs_items = [
        {
            'id': 'git',
            'label': 'Git',
            'description': 'Version control',
            'parent': 'dev-vcs',
            'default': True,
            'help': 'Git is a free and open source distributed version control system designed to handle everything from small to very large projects.'
        },
        {
            'id': 'git-config-global',
            'label': 'Git Global Configuration',
            'description': 'Set up Git user info',
            'parent': 'dev-vcs',
            'help': 'Configure Git with your name and email for all repositories.'
        },
        {
            'id': 'ssh-key-github',
            'label': 'SSH Key for GitHub',
            'description': 'Generate GitHub SSH key',
            'parent': 'dev-vcs',
            'help': 'Generate an SSH key and add it to your GitHub account for secure access.'
        },
    ]
    
    # Containers & Orchestration
    container_items = [
        {
            'id': 'docker',
            'label': 'Docker',
            'description': 'Container platform',
            'parent': 'dev-containers',
            'default': True,
            'help': '''Docker is a platform for developers to develop, deploy, and run applications with containers.

This will install:
- docker-ce - Docker Community Edition engine
- docker-ce-cli - Docker command-line interface
- containerd.io - Container runtime
- docker-compose-plugin - Docker Compose v2 as Docker plugin
- docker-buildx-plugin - Docker Buildx for advanced image building

Additional configurations:
- Adds your user to the docker group (no sudo needed for docker commands)
- Enables Docker service to start on boot
- Configures Docker daemon with production-ready settings
- Sets up log rotation to prevent disk space issues

Requirements:
- 64-bit Ubuntu system
- Kernel 3.10 or higher
- iptables 1.4 or higher
- git 1.7 or higher
- A ps executable (procps or similar)
- XZ Utils 4.9 or higher

Storage drivers supported:
- overlay2 (recommended)
- aufs
- btrfs
- zfs
- devicemapper

Common use cases:
- Application containerization
- Microservices architecture
- Development environment isolation
- CI/CD pipelines
- Testing and staging environments'''
        },
        {
            'id': 'docker-compose',
            'label': 'Docker Compose',
            'description': 'Multi-container orchestration',
            'parent': 'dev-containers',
            'help': 'Docker Compose is a tool for defining and running multi-container Docker applications with YAML configuration.'
        },
        {
            'id': 'kubernetes',
            'label': 'Kubernetes',
            'description': 'Container orchestration',
            'parent': 'dev-containers',
            'help': '''Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.

This will install:
- kubectl - The Kubernetes command-line tool for managing clusters
- kubeadm - Tool to bootstrap Kubernetes clusters
- kubelet - The primary node agent that runs on each node
- kubernetes-cni - Container Network Interface plugins for pod networking

Additional tools included:
- helm - The Kubernetes package manager for deploying applications
- k9s - Terminal UI for Kubernetes cluster management
- kubectx/kubens - Fast switching between clusters and namespaces
- stern - Multi-pod and container log tailing

Requirements:
- Docker or another container runtime (containerd, CRI-O)
- Minimum 2GB RAM (4GB recommended for comfortable operation)
- 2 CPU cores minimum
- Network connectivity for pulling container images
- Swap must be disabled for kubelet to work properly

Common use cases:
- Local development with minikube or kind
- Production container orchestration
- Microservices deployment and management
- CI/CD pipeline integration'''
        },
    ]
    
    # SQL Databases
    sql_db_items = [
        {
            'id': 'postgresql',
            'label': 'PostgreSQL',
            'description': 'Advanced SQL database',
            'parent': 'dev-sql-databases',
            'help': 'PostgreSQL is a powerful, open source object-relational database system.'
        },
        {
            'id': 'mysql',
            'label': 'MySQL',
            'description': 'Popular SQL database',
            'parent': 'dev-sql-databases',
            'help': 'MySQL is the world\'s most popular open source database.'
        },
        {
            'id': 'mariadb',
            'label': 'MariaDB',
            'description': 'MySQL fork',
            'parent': 'dev-sql-databases',
            'help': 'MariaDB is a community-developed fork of MySQL with enhanced features.'
        },
    ]
    
    # NoSQL Databases
    nosql_db_items = [
        {
            'id': 'mongodb',
            'label': 'MongoDB',
            'description': 'Document database',
            'parent': 'dev-nosql-databases',
            'help': 'MongoDB is a document-oriented NoSQL database used for high volume data storage.'
        },
        {
            'id': 'redis',
            'label': 'Redis',
            'description': 'In-memory data store',
            'parent': 'dev-nosql-databases',
            'help': 'Redis is an in-memory data structure store used as a database, cache, and message broker.'
        },
        {
            'id': 'elasticsearch',
            'label': 'Elasticsearch',
            'description': 'Search engine',
            'parent': 'dev-nosql-databases',
            'help': 'Elasticsearch is a distributed, RESTful search and analytics engine.'
        },
        {
            'id': 'cassandra',
            'label': 'Cassandra',
            'description': 'Wide column store',
            'parent': 'dev-nosql-databases',
            'help': 'Apache Cassandra is a distributed NoSQL database management system.'
        },
        {
            'id': 'couchdb',
            'label': 'CouchDB',
            'description': 'Document database',
            'parent': 'dev-nosql-databases',
            'help': 'Apache CouchDB is a document-oriented NoSQL database.'
        },
        {
            'id': 'influxdb',
            'label': 'InfluxDB',
            'description': 'Time series database',
            'parent': 'dev-nosql-databases',
            'help': 'InfluxDB is a time series database designed for high-write and high-query loads.'
        },
    ]
    
    # Database Tools
    db_tool_items = [
        {
            'id': 'dbeaver',
            'label': 'DBeaver',
            'description': 'Universal database tool',
            'parent': 'dev-db-tools',
            'help': 'DBeaver is a free multi-platform database tool for developers, SQL programmers, and DBAs.'
        },
        {
            'id': 'pgadmin',
            'label': 'pgAdmin',
            'description': 'PostgreSQL management',
            'parent': 'dev-db-tools',
            'help': 'pgAdmin is the most popular and feature-rich Open Source administration platform for PostgreSQL.'
        },
        {
            'id': 'mysql-workbench',
            'label': 'MySQL Workbench',
            'description': 'MySQL database design',
            'parent': 'dev-db-tools',
            'help': 'MySQL Workbench is a unified visual tool for database architects, developers, and DBAs.'
        },
    ]
    
    # API & Web Tools
    api_tool_items = [
        {
            'id': 'postman',
            'label': 'Postman',
            'description': 'API development platform',
            'parent': 'dev-api-tools',
            'help': 'Postman is an API platform for building and using APIs with testing and documentation.'
        },
        {
            'id': 'insomnia',
            'label': 'Insomnia',
            'description': 'REST and GraphQL client',
            'parent': 'dev-api-tools',
            'help': 'Insomnia is a powerful REST and GraphQL client with a beautiful interface.'
        },
        {
            'id': 'httpie',
            'label': 'HTTPie',
            'description': 'CLI HTTP client',
            'parent': 'dev-api-tools',
            'help': 'HTTPie is a command-line HTTP client with an intuitive UI and JSON support.'
        },
    ]
    
    # Shells
    shell_items = [
        {
            'id': 'bash',
            'label': 'Bash',
            'description': 'Bourne Again Shell',
            'parent': 'dev-shells',
            'default': True,
            'help': 'Bash is the GNU Project\'s shell and the default shell on most Linux systems.'
        },
        {
            'id': 'zsh',
            'label': 'Zsh',
            'description': 'Z Shell',
            'parent': 'dev-shells',
            'help': 'Zsh is a shell designed for interactive use with many features from bash, ksh, and tcsh.'
        },
        {
            'id': 'fish',
            'label': 'Fish',
            'description': 'Friendly shell',
            'parent': 'dev-shells',
            'help': 'Fish is a smart and user-friendly command line shell with autosuggestions.'
        },
        {
            'id': 'nushell',
            'label': 'Nushell',
            'description': 'Modern shell',
            'parent': 'dev-shells',
            'help': 'Nushell is a modern shell that understands data structures.'
        },
        {
            'id': 'elvish',
            'label': 'Elvish',
            'description': 'Expressive shell',
            'parent': 'dev-shells',
            'help': 'Elvish is an expressive programming language and a versatile interactive shell.'
        },
    ]
    
    # Terminal Emulators
    terminal_emulator_items = [
        {
            'id': 'kitty',
            'label': 'Kitty',
            'description': 'GPU-accelerated terminal',
            'parent': 'dev-terminal-emulators',
            'help': 'Kitty is a fast, feature-rich, GPU based terminal emulator.'
        },
        {
            'id': 'alacritty',
            'label': 'Alacritty',
            'description': 'GPU-accelerated terminal',
            'parent': 'dev-terminal-emulators',
            'help': 'Alacritty is a modern terminal emulator with sensible defaults and extensive configuration.'
        },
        {
            'id': 'wezterm',
            'label': 'WezTerm',
            'description': 'GPU-accelerated terminal',
            'parent': 'dev-terminal-emulators',
            'help': 'WezTerm is a GPU-accelerated cross-platform terminal emulator and multiplexer.'
        },
    ]
    
    # Shell Enhancements
    shell_enhancement_items = [
        {
            'id': 'prompt-starship',
            'label': 'Starship Prompt',
            'description': 'Fast cross-shell prompt',
            'parent': 'dev-shell-enhancements',
            'help': 'Starship is a minimal, blazing-fast, and customizable prompt for any shell.'
        },
        {
            'id': 'prompt-ohmyposh',
            'label': 'Oh My Posh',
            'description': 'Prompt theme engine',
            'parent': 'dev-shell-enhancements',
            'help': 'Oh My Posh is a prompt theme engine for any shell with many built-in themes.'
        },
        {
            'id': 'prompt-pure',
            'label': 'Pure Prompt',
            'description': 'Minimal Zsh prompt',
            'parent': 'dev-shell-enhancements',
            'help': 'Pure is a pretty, minimal and fast ZSH prompt.'
        },
        {
            'id': 'prompt-spaceship',
            'label': 'Spaceship Prompt',
            'description': 'Minimalistic Zsh prompt',
            'parent': 'dev-shell-enhancements',
            'help': 'Spaceship is a minimalistic, powerful and customizable Zsh prompt.'
        },
        {
            'id': 'tmux',
            'label': 'tmux',
            'description': 'Terminal multiplexer',
            'parent': 'dev-shell-enhancements',
            'help': 'tmux is a terminal multiplexer that lets you switch between several programs in one terminal.'
        },
        {
            'id': 'screen',
            'label': 'GNU Screen',
            'description': 'Terminal multiplexer',
            'parent': 'dev-shell-enhancements',
            'help': 'GNU Screen is a full-screen window manager that multiplexes a physical terminal.'
        },
    ]
    
    # Cloud & Infrastructure
    cloud_items = [
        {
            'id': 'aws-cli',
            'label': 'AWS CLI',
            'description': 'Amazon Web Services CLI',
            'parent': 'dev-cloud',
            'help': 'AWS CLI is a unified tool to manage your AWS services from the command line.'
        },
        {
            'id': 'gcloud',
            'label': 'Google Cloud SDK',
            'description': 'Google Cloud Platform CLI',
            'parent': 'dev-cloud',
            'help': 'Google Cloud SDK is a set of tools for Google Cloud Platform including gcloud, gsutil, and bq.'
        },
        {
            'id': 'azure-cli',
            'label': 'Azure CLI',
            'description': 'Microsoft Azure CLI',
            'parent': 'dev-cloud',
            'help': 'Azure CLI is a cross-platform command-line tool to manage Azure resources.'
        },
        {
            'id': 'terraform',
            'label': 'Terraform',
            'description': 'Infrastructure as Code',
            'parent': 'dev-cloud',
            'help': 'Terraform is an infrastructure as code tool for building, changing, and versioning infrastructure.'
        },
        {
            'id': 'pulumi',
            'label': 'Pulumi',
            'description': 'Modern Infrastructure as Code',
            'parent': 'dev-cloud',
            'help': 'Pulumi is an infrastructure as code platform that allows you to use familiar programming languages.'
        },
    ]
    
    # Build Tools
    build_tool_items = [
        {
            'id': 'make',
            'label': 'GNU Make',
            'description': 'Build automation',
            'parent': 'dev-build-tools',
            'help': 'GNU Make is a tool which controls the generation of executables from source code.'
        },
        {
            'id': 'bazel',
            'label': 'Bazel',
            'description': 'Build and test tool',
            'parent': 'dev-build-tools',
            'help': 'Bazel is Google\'s build tool for building and testing software at any scale.'
        },
        {
            'id': 'ninja',
            'label': 'Ninja',
            'description': 'Small build system',
            'parent': 'dev-build-tools',
            'help': 'Ninja is a small build system with a focus on speed.'
        },
    ]
    
    # Testing Tools
    testing_items = [
        {
            'id': 'selenium',
            'label': 'Selenium',
            'description': 'Web testing framework',
            'parent': 'dev-testing',
            'help': 'Selenium is a suite of tools for automating web browsers.'
        },
        {
            'id': 'cypress',
            'label': 'Cypress',
            'description': 'E2E testing framework',
            'parent': 'dev-testing',
            'help': 'Cypress is a JavaScript end-to-end testing framework.'
        },
        {
            'id': 'playwright',
            'label': 'Playwright',
            'description': 'Browser automation',
            'parent': 'dev-testing',
            'help': 'Playwright enables reliable end-to-end testing for modern web apps.'
        },
    ]
    
    # Documentation Tools
    doc_items = [
        {
            'id': 'sphinx',
            'label': 'Sphinx',
            'description': 'Python documentation',
            'parent': 'dev-documentation',
            'help': 'Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.'
        },
        {
            'id': 'mkdocs',
            'label': 'MkDocs',
            'description': 'Project documentation',
            'parent': 'dev-documentation',
            'help': 'MkDocs is a fast, simple and downright gorgeous static site generator for documentation.'
        },
        {
            'id': 'doxygen',
            'label': 'Doxygen',
            'description': 'Source code documentation',
            'parent': 'dev-documentation',
            'help': 'Doxygen is the de facto standard tool for generating documentation from annotated source code.'
        },
    ]
    
    # Development Utilities
    dev_util_items = [
        {
            'id': 'ctags',
            'label': 'ctags',
            'description': 'Code indexing',
            'parent': 'dev-utilities',
            'help': 'ctags generates an index file of language objects found in source files.'
        },
        {
            'id': 'gnu-global',
            'label': 'GNU Global',
            'description': 'Source code tagging',
            'parent': 'dev-utilities',
            'help': 'GNU Global is a source code tagging system that works with many languages.'
        },
        {
            'id': 'binutils',
            'label': 'GNU Binutils',
            'description': 'Binary utilities',
            'parent': 'dev-utilities',
            'help': 'GNU Binutils is a collection of binary tools including assembler, linker, and others.'
        },
        {
            'id': 'gdb',
            'label': 'GDB',
            'description': 'GNU debugger',
            'parent': 'dev-utilities',
            'help': 'GDB, the GNU Project debugger, allows you to see what is going on inside programs.'
        },
        {
            'id': 'valgrind',
            'label': 'Valgrind',
            'description': 'Memory debugger',
            'parent': 'dev-utilities',
            'help': 'Valgrind is an instrumentation framework for building dynamic analysis tools.'
        },
        {
            'id': 'strace',
            'label': 'strace',
            'description': 'System call tracer',
            'parent': 'dev-utilities',
            'help': 'strace is a diagnostic, debugging and instructional userspace utility for Linux.'
        },
        {
            'id': 'ltrace',
            'label': 'ltrace',
            'description': 'Library call tracer',
            'parent': 'dev-utilities',
            'help': 'ltrace is a program that intercepts and records dynamic library calls.'
        },
        {
            'id': 'perf',
            'label': 'perf',
            'description': 'Performance analysis',
            'parent': 'dev-utilities',
            'help': 'perf is a performance analyzing tool in Linux for profiling applications.'
        },
        {
            'id': 'heaptrack',
            'label': 'Heaptrack',
            'description': 'Heap memory profiler',
            'parent': 'dev-utilities',
            'help': 'Heaptrack is a heap memory profiler that tracks allocations.'
        },
        {
            'id': 'jq',
            'label': 'jq',
            'description': 'JSON processor',
            'parent': 'dev-utilities',
            'help': 'jq is a lightweight and flexible command-line JSON processor.'
        },
        {
            'id': 'yq',
            'label': 'yq',
            'description': 'YAML processor',
            'parent': 'dev-utilities',
            'help': 'yq is a portable command-line YAML processor.'
        },
    ]
    
    # Editor Settings
    editor_setting_items = [
        {
            'id': 'vscode-vim-mode',
            'label': 'VS Code Vim Mode',
            'description': 'Enable Vim keybindings',
            'parent': 'dev-editor-settings',
            'help': 'Enable Vim keybindings in Visual Studio Code for efficient text editing.'
        },
        {
            'id': 'vscode-theme-sync',
            'label': 'VS Code Theme Sync',
            'description': 'Sync with system theme',
            'parent': 'dev-editor-settings',
            'help': 'Automatically switch VS Code theme to match your system theme.'
        },
        {
            'id': 'editor-minimap',
            'label': 'Editor Minimap',
            'description': 'Show code minimap',
            'parent': 'dev-editor-settings',
            'default': True,
            'help': 'Show a minimap overview of your code on the side of the editor.'
        },
        {
            'id': 'editor-ligatures',
            'label': 'Editor Ligatures',
            'description': 'Enable font ligatures',
            'parent': 'dev-editor-settings',
            'default': True,
            'help': 'Enable programming ligatures if using a font that supports them (like Fira Code).'
        },
        {
            'id': 'vscode-font-size',
            'label': 'VS Code Font Size',
            'description': 'Editor font size (10-24)',
            'parent': 'dev-editor-settings',
            'is_configurable': True,
            'default_value': 14,
            'help': 'Set the font size for the VS Code editor (pixels).'
        },
        {
            'id': 'vscode-tab-size',
            'label': 'VS Code Tab Size',
            'description': 'Spaces per tab (2-8)',
            'parent': 'dev-editor-settings',
            'is_configurable': True,
            'default_value': 4,
            'help': 'Number of spaces to use for each tab in VS Code.'
        },
        {
            'id': 'vscode-word-wrap',
            'label': 'VS Code Word Wrap',
            'description': 'Wrap long lines',
            'parent': 'dev-editor-settings',
            'help': 'Automatically wrap long lines in the VS Code editor.'
        },
        {
            'id': 'vscode-bracket-colorization',
            'label': 'Bracket Pair Colorization',
            'description': 'Color matching brackets',
            'parent': 'dev-editor-settings',
            'default': True,
            'help': 'Use colors to help identify matching bracket pairs in VS Code.'
        },
        {
            'id': 'vscode-sticky-scroll',
            'label': 'VS Code Sticky Scroll',
            'description': 'Show current scope',
            'parent': 'dev-editor-settings',
            'default': True,
            'help': 'Show the current function/class scope at the top of the editor while scrolling.'
        },
        {
            'id': 'vscode-inlay-hints',
            'label': 'VS Code Inlay Hints',
            'description': 'Show inline type hints',
            'parent': 'dev-editor-settings',
            'help': 'Display inline parameter names and type information in the editor.'
        },
        {
            'id': 'app-theme-integration',
            'label': 'Application Theme Integration',
            'description': 'Apply system theme to apps',
            'parent': 'dev-editor-settings',
            'default': True,
            'help': 'Automatically apply your selected system theme to supported applications.'
        },
        {
            'id': 'cursor',
            'label': 'Cursor',
            'description': 'Configure cursor',
            'parent': 'dev-editor-settings',
            'help': 'Configure cursor appearance and behavior.'
        },
    ]
    
    # Terminal Settings
    terminal_setting_items = [
        {
            'id': 'terminal-transparency',
            'label': 'Terminal Transparency',
            'description': 'Background transparency (0-100%)',
            'parent': 'dev-terminal-settings',
            'is_configurable': True,
            'default_value': 85,
            'help': 'Set the transparency level of your terminal background. 0% is opaque, 100% is fully transparent.'
        },
        {
            'id': 'terminal-font-size',
            'label': 'Terminal Font Size',
            'description': 'Font size in points',
            'parent': 'dev-terminal-settings',
            'is_configurable': True,
            'default_value': 12,
            'help': 'Set the font size for your terminal in points.'
        },
        {
            'id': 'terminal-cursor-blink',
            'label': 'Terminal Cursor Blink',
            'description': 'Enable cursor blinking',
            'parent': 'dev-terminal-settings',
            'default': True,
            'help': 'Enable or disable cursor blinking in the terminal.'
        },
    ]
    
    # Add all development items
    items.extend(go_items)
    items.extend(python_items)
    items.extend(javascript_items)
    items.extend(rust_items)
    items.extend(java_items)
    items.extend(cpp_items)
    items.extend(dotnet_items)
    items.extend(other_lang_items)
    items.extend(jetbrains_items)
    items.extend(code_editor_items)
    items.extend(text_editor_items)
    items.extend(vcs_items)
    items.extend(container_items)
    items.extend(sql_db_items)
    items.extend(nosql_db_items)
    items.extend(db_tool_items)
    items.extend(api_tool_items)
    items.extend(shell_items)
    items.extend(terminal_emulator_items)
    items.extend(shell_enhancement_items)
    items.extend(cloud_items)
    items.extend(build_tool_items)
    items.extend(testing_items)
    items.extend(doc_items)
    items.extend(dev_util_items)
    items.extend(editor_setting_items)
    items.extend(terminal_setting_items)
    
    # For subcategories that have manual children (like dev-languages with dev-go, dev-python etc),
    # we need to ADD the leaf items to the existing children, not replace them
    for subcat in dev_subcategories:
        existing_children = subcat.get('children', [])
        
        # Get all direct item children (not subcategories)
        item_children = [
            item['id'] for item in items 
            if item.get('parent') == subcat['id'] and not item.get('is_category')
        ]
        
        # If there are existing children (subcategories), add items to them
        # If no existing children, just use the items
        if existing_children:
            # Preserve existing subcategory children and add any direct items
            all_children = list(existing_children)  # Copy existing
            all_children.extend([child for child in item_children if child not in all_children])
            subcat['children'] = all_children
        else:
            subcat['children'] = item_children
    
    # AI/ML items
    ai_ml_items = [
        {
            'id': 'ollama',
            'label': 'Ollama',
            'description': 'Run LLMs locally',
            'parent': 'ai-ml',
            'help': 'Ollama allows you to run large language models locally on your machine.'
        },
        {
            'id': 'stable-diffusion',
            'label': 'Stable Diffusion',
            'description': 'AI image generation',
            'parent': 'ai-ml',
            'help': 'Stable Diffusion is a deep learning model for generating detailed images from text descriptions.'
        },
        {
            'id': 'pytorch',
            'label': 'PyTorch',
            'description': 'ML framework',
            'parent': 'ai-ml',
            'help': 'PyTorch is an open source machine learning framework.'
        },
        {
            'id': 'tensorflow',
            'label': 'TensorFlow',
            'description': 'ML platform',
            'parent': 'ai-ml',
            'help': 'TensorFlow is an end-to-end open source platform for machine learning.'
        },
        {
            'id': 'jupyter',
            'label': 'Jupyter Lab',
            'description': 'Interactive notebooks',
            'parent': 'ai-ml',
            'help': 'JupyterLab is the latest web-based interactive development environment for notebooks.'
        },
        {
            'id': 'anaconda',
            'label': 'Anaconda',
            'description': 'Data science platform',
            'parent': 'ai-ml',
            'help': 'Anaconda is a distribution of Python and R for scientific computing and data science.'
        },
    ]
    
    items.extend(ai_ml_items)
    ai_ml_cat = next(cat for cat in categories if cat['id'] == 'ai-ml')
    ai_ml_cat['children'] = [item['id'] for item in ai_ml_items]
    
    # Other categories remain as before...
    # (We'll organize them in subsequent passes)
    
    # Desktop Environment items (simplified for now)
    desktop_items = [
        {
            'id': 'gnome',
            'label': 'GNOME',
            'description': 'Modern desktop environment',
            'parent': 'desktop',
            'default': True,
            'help': 'GNOME is a free and open-source desktop environment for Unix-like operating systems.'
        },
        {
            'id': 'kde-plasma',
            'label': 'KDE Plasma',
            'description': 'Feature-rich desktop',
            'parent': 'desktop',
            'help': 'KDE Plasma is a graphical desktop environment with customizable layouts.'
        },
        {
            'id': 'xfce',
            'label': 'XFCE',
            'description': 'Lightweight desktop',
            'parent': 'desktop',
            'help': 'Xfce is a lightweight desktop environment for Unix-like operating systems.'
        },
    ]
    
    items.extend(desktop_items)
    desktop_cat = next(cat for cat in categories if cat['id'] == 'desktop')
    desktop_cat['children'] = [item['id'] for item in desktop_items]
    
    # Applications items (simplified for now)
    app_items = [
        {
            'id': 'firefox',
            'label': 'Firefox',
            'description': 'Web browser',
            'parent': 'applications',
            'default': True,
            'help': 'Mozilla Firefox is a free and open-source web browser.'
        },
        {
            'id': 'chrome',
            'label': 'Google Chrome',
            'description': 'Web browser',
            'parent': 'applications',
            'help': 'Google Chrome is a fast, secure, and free web browser.'
        },
        {
            'id': 'slack',
            'label': 'Slack',
            'description': 'Team communication',
            'parent': 'applications',
            'help': 'Slack is a messaging app for business that connects people to the information they need.'
        },
    ]
    
    items.extend(app_items)
    app_cat = next(cat for cat in categories if cat['id'] == 'applications')
    app_cat['children'] = [item['id'] for item in app_items]
    
    # Security items (simplified for now)
    security_items = [
        {
            'id': 'ufw',
            'label': 'UFW Firewall',
            'description': 'Uncomplicated Firewall',
            'parent': 'security',
            'default': True,
            'help': 'UFW (Uncomplicated Firewall) is a frontend for iptables and is particularly well-suited for host-based firewalls.'
        },
        {
            'id': 'fail2ban',
            'label': 'Fail2Ban',
            'description': 'Intrusion prevention',
            'parent': 'security',
            'help': 'Fail2Ban scans log files and bans IPs that show malicious signs.'
        },
    ]
    
    items.extend(security_items)
    security_cat = next(cat for cat in categories if cat['id'] == 'security')
    security_cat['children'] = [item['id'] for item in security_items]
    
    # System items (simplified for now)
    system_items = [
        {
            'id': 'swappiness',
            'label': 'Swappiness',
            'description': 'VM swappiness (0-100)',
            'parent': 'system',
            'is_configurable': True,
            'default_value': 10,
            'help': 'Swappiness controls how aggressively the kernel swaps memory pages. Lower values keep more data in RAM.'
        },
        {
            'id': 'enable-trim',
            'label': 'Enable SSD TRIM',
            'description': 'Weekly TRIM for SSDs',
            'parent': 'system',
            'default': True,
            'help': 'Enable weekly TRIM operations for SSD drives to maintain performance.'
        },
    ]
    
    items.extend(system_items)
    system_cat = next(cat for cat in categories if cat['id'] == 'system')
    system_cat['children'] = [item['id'] for item in system_items]
    
    # Fill in empty categories
    for cat in categories:
        if not cat.get('children'):
            cat['children'] = []
    
    return items