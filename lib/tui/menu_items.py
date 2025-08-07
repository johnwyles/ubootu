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
            "id": "development",
            "label": "Development Tools",
            "description": "Programming languages, IDEs, tools",
            "icon": "💻",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "ai-ml",
            "label": "AI & Machine Learning",
            "description": "AI tools, ML frameworks, LLMs",
            "icon": "🤖",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "desktop",
            "label": "Desktop Environment",
            "description": "Desktop environments and themes",
            "icon": "🖥️",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "applications",
            "label": "General Applications",
            "description": "Miscellaneous applications",
            "icon": "📦",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "security",
            "label": "Security & Privacy",
            "description": "Firewall, VPN, encryption tools",
            "icon": "🔒",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "system",
            "label": "System Configuration",
            "description": "Performance, services, hardware",
            "icon": "⚙️",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "customization",
            "label": "Application Customization",
            "description": "Customize appearance and behavior of apps",
            "icon": "🎨",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "themes",
            "label": "Themes & Appearance",
            "description": "Universal color schemes and themes",
            "icon": "🌈",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "gaming",
            "label": "Gaming",
            "description": "Gaming platforms and tools",
            "icon": "🎮",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "multimedia",
            "label": "Multimedia Production",
            "description": "Audio, video, and graphics creation",
            "icon": "🎬",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "networking",
            "label": "Networking",
            "description": "Network tools and configuration",
            "icon": "🌐",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "virtualization",
            "label": "Virtualization",
            "description": "Virtual machines and containers",
            "icon": "📦",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "cloud-tools",
            "label": "Cloud Tools",
            "description": "Cloud platform CLIs and tools",
            "icon": "☁️",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "security-testing",
            "label": "Security Testing",
            "description": "Penetration testing and security analysis tools",
            "icon": "🔐",
            "is_category": True,
            "parent": None,
            "children": [],
        },
    ]

    # Add new application-specific categories
    app_categories = [
        {
            "id": "graphics-media",
            "label": "Graphics & Media",
            "description": "Image editing, 3D graphics, and media manipulation",
            "icon": "🖼️",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "productivity-office",
            "label": "Productivity & Office",
            "description": "Office suites, email clients, and productivity tools",
            "icon": "💼",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "communication",
            "label": "Communication",
            "description": "Chat, video conferencing, and messaging apps",
            "icon": "💬",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "audio-music",
            "label": "Audio & Music",
            "description": "Audio players, editors, and music production",
            "icon": "🎵",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "video-streaming",
            "label": "Video & Streaming",
            "description": "Video players, editors, and streaming tools",
            "icon": "🎥",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "text-editors-ides",
            "label": "Text Editors & IDEs",
            "description": "Code editors and integrated development environments",
            "icon": "📝",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "web-browsers",
            "label": "Web Browsers",
            "description": "Internet browsers and web tools",
            "icon": "🌐",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "file-management",
            "label": "File Management",
            "description": "File managers and organization tools",
            "icon": "📁",
            "is_category": True,
            "parent": None,
            "children": [],
        },
        {
            "id": "system-tools",
            "label": "System Tools",
            "description": "System utilities and maintenance tools",
            "icon": "🔧",
            "is_category": True,
            "parent": None,
            "children": [],
        },
    ]

    categories.extend(app_categories)

    # Add root categories first
    items.extend(categories)

    # Development subcategories
    dev_subcategories = [
        # Programming Languages
        {
            "id": "dev-languages",
            "label": "Programming Languages",
            "description": "Compilers, interpreters, and runtimes",
            "icon": "🔤",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        {
            "id": "dev-go",
            "label": "Go",
            "description": "Go language and tools",
            "icon": "🐹",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-python",
            "label": "Python",
            "description": "Python language and tools",
            "icon": "🐍",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-javascript",
            "label": "JavaScript/TypeScript",
            "description": "JS/TS runtimes and tools",
            "icon": "📜",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-rust",
            "label": "Rust",
            "description": "Rust language and tools",
            "icon": "🦀",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-java",
            "label": "Java/Kotlin",
            "description": "JVM languages and tools",
            "icon": "☕",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-cpp",
            "label": "C/C++",
            "description": "C/C++ compilers and tools",
            "icon": "🏗️",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-dotnet",
            "label": ".NET/C#",
            "description": ".NET SDK and tools",
            "icon": "🟦",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        {
            "id": "dev-other-langs",
            "label": "Other Languages",
            "description": "Additional programming languages",
            "icon": "📚",
            "is_category": True,
            "parent": "dev-languages",
            "children": [],
        },
        # IDEs and Editors
        {
            "id": "dev-ides",
            "label": "IDEs & Editors",
            "description": "Integrated development environments",
            "icon": "📝",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        {
            "id": "dev-jetbrains",
            "label": "JetBrains IDEs",
            "description": "Professional IDEs by JetBrains",
            "icon": "🧠",
            "is_category": True,
            "parent": "dev-ides",
            "children": [],
        },
        {
            "id": "dev-code-editors",
            "label": "Code Editors",
            "description": "Modern code editors",
            "icon": "✏️",
            "is_category": True,
            "parent": "dev-ides",
            "children": [],
        },
        {
            "id": "dev-text-editors",
            "label": "Text Editors",
            "description": "Terminal and GUI text editors",
            "icon": "📄",
            "is_category": True,
            "parent": "dev-ides",
            "children": [],
        },
        # Version Control
        {
            "id": "dev-vcs",
            "label": "Version Control",
            "description": "Source control systems",
            "icon": "🌿",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Containers & Orchestration
        {
            "id": "dev-containers",
            "label": "Containers & Orchestration",
            "description": "Container platforms and tools",
            "icon": "📦",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Databases
        {
            "id": "dev-databases",
            "label": "Databases",
            "description": "Database servers and tools",
            "icon": "🗄️",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        {
            "id": "dev-sql-databases",
            "label": "SQL Databases",
            "description": "Relational databases",
            "icon": "🔍",
            "is_category": True,
            "parent": "dev-databases",
            "children": [],
        },
        {
            "id": "dev-nosql-databases",
            "label": "NoSQL Databases",
            "description": "Non-relational databases",
            "icon": "📊",
            "is_category": True,
            "parent": "dev-databases",
            "children": [],
        },
        {
            "id": "dev-db-tools",
            "label": "Database Tools",
            "description": "Database management tools",
            "icon": "🛠️",
            "is_category": True,
            "parent": "dev-databases",
            "children": [],
        },
        # API & Web Tools
        {
            "id": "dev-api-tools",
            "label": "API & Web Tools",
            "description": "API testing and web development",
            "icon": "🌐",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Terminal & Shell
        {
            "id": "dev-terminal",
            "label": "Terminal & Shell",
            "description": "Shells and terminal tools",
            "icon": "💻",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        {
            "id": "dev-shells",
            "label": "Shells",
            "description": "Command line shells",
            "icon": "🐚",
            "is_category": True,
            "parent": "dev-terminal",
            "children": [],
        },
        {
            "id": "dev-terminal-emulators",
            "label": "Terminal Emulators",
            "description": "Terminal applications",
            "icon": "🖥️",
            "is_category": True,
            "parent": "dev-terminal",
            "children": [],
        },
        {
            "id": "dev-shell-enhancements",
            "label": "Shell Enhancements",
            "description": "Prompts and utilities",
            "icon": "✨",
            "is_category": True,
            "parent": "dev-terminal",
            "children": [],
        },
        # Cloud & Infrastructure
        {
            "id": "dev-cloud",
            "label": "Cloud & Infrastructure",
            "description": "Cloud CLIs and IaC tools",
            "icon": "☁️",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Build & Development Tools
        {
            "id": "dev-build-tools",
            "label": "Build & Package Tools",
            "description": "Build systems and package managers",
            "icon": "🔨",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Testing & Quality
        {
            "id": "dev-testing",
            "label": "Testing & Quality",
            "description": "Testing frameworks and tools",
            "icon": "🧪",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Documentation
        {
            "id": "dev-documentation",
            "label": "Documentation",
            "description": "Documentation generators",
            "icon": "📚",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Development Utilities
        {
            "id": "dev-utilities",
            "label": "Development Utilities",
            "description": "Miscellaneous dev tools",
            "icon": "🔧",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        # Settings
        {
            "id": "dev-editor-settings",
            "label": "Editor Settings",
            "description": "Configure editor preferences",
            "icon": "⚙️",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
        {
            "id": "dev-terminal-settings",
            "label": "Terminal Settings",
            "description": "Configure terminal preferences",
            "icon": "⚙️",
            "is_category": True,
            "parent": "development",
            "children": [],
        },
    ]

    items.extend(dev_subcategories)

    # Update children for development category
    development_cat = next(cat for cat in categories if cat["id"] == "development")
    development_cat["children"] = [
        "dev-languages",
        "dev-ides",
        "dev-vcs",
        "dev-containers",
        "dev-databases",
        "dev-api-tools",
        "dev-terminal",
        "dev-cloud",
        "dev-build-tools",
        "dev-testing",
        "dev-documentation",
        "dev-utilities",
        "dev-editor-settings",
        "dev-terminal-settings",
    ]

    # Update children for subcategories
    dev_languages = next(cat for cat in dev_subcategories if cat["id"] == "dev-languages")
    dev_languages["children"] = [
        "dev-go",
        "dev-python",
        "dev-javascript",
        "dev-rust",
        "dev-java",
        "dev-cpp",
        "dev-dotnet",
        "dev-other-langs",
    ]

    dev_ides = next(cat for cat in dev_subcategories if cat["id"] == "dev-ides")
    dev_ides["children"] = ["dev-jetbrains", "dev-code-editors", "dev-text-editors"]

    dev_databases = next(cat for cat in dev_subcategories if cat["id"] == "dev-databases")
    dev_databases["children"] = ["dev-sql-databases", "dev-nosql-databases", "dev-db-tools"]

    dev_terminal = next(cat for cat in dev_subcategories if cat["id"] == "dev-terminal")
    dev_terminal["children"] = ["dev-shells", "dev-terminal-emulators", "dev-shell-enhancements"]

    # Development items organized by category

    # Go tools
    go_items = [
        {
            "id": "go",
            "label": "Go",
            "description": "Google's programming language",
            "parent": "dev-go",
            "default": False,
            "help": "Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.",
        },
        {
            "id": "goland",
            "label": "GoLand",
            "description": "Go IDE by JetBrains",
            "parent": "dev-go",
            "help": "GoLand is JetBrains' IDE for Go development with advanced code analysis.",
        },
        {
            "id": "gofmt",
            "label": "gofmt",
            "description": "Go formatter",
            "parent": "dev-go",
            "help": "gofmt is a tool that automatically formats Go source code.",
        },
    ]

    # Python tools
    python_items = [
        {
            "id": "python",
            "label": "Python 3",
            "description": "Python runtime and pip",
            "parent": "dev-python",
            "default": True,
            "help": "Python 3 runtime with pip package manager. The most popular language for scripting, web development, data science, and automation.",
        },
        {
            "id": "pycharm-community",
            "label": "PyCharm Community",
            "description": "Python IDE by JetBrains",
            "parent": "dev-python",
            "help": "PyCharm Community Edition is the best Python IDE with intelligent code completion, debugging, testing, and virtual environment management.",
        },
        {
            "id": "poetry",
            "label": "Poetry",
            "description": "Python dependency management",
            "parent": "dev-python",
            "help": "Poetry is a modern dependency management and packaging tool for Python.",
        },
        {
            "id": "pipenv",
            "label": "Pipenv",
            "description": "Python dev workflow tool",
            "parent": "dev-python",
            "help": "Pipenv automatically creates and manages a virtualenv for your projects.",
        },
        {
            "id": "pyenv",
            "label": "pyenv",
            "description": "Python version management",
            "parent": "dev-python",
            "help": "pyenv lets you easily switch between multiple versions of Python.",
        },
        {
            "id": "black",
            "label": "Black",
            "description": "Python code formatter",
            "parent": "dev-python",
            "help": "Black is the uncompromising Python code formatter.",
        },
        {
            "id": "pytest",
            "label": "pytest",
            "description": "Python testing framework",
            "parent": "dev-python",
            "help": "pytest is a mature full-featured Python testing tool.",
        },
    ]

    # JavaScript/TypeScript tools
    javascript_items = [
        {
            "id": "nodejs",
            "label": "Node.js",
            "description": "JavaScript runtime",
            "parent": "dev-javascript",
            "default": True,
            "help": "Node.js JavaScript runtime built on Chrome's V8 engine. Essential for modern web development, React, Angular, Vue.js, and server-side JavaScript.",
        },
        {
            "id": "webstorm",
            "label": "WebStorm",
            "description": "JavaScript IDE by JetBrains",
            "parent": "dev-javascript",
            "help": "WebStorm is JetBrains' powerful IDE for JavaScript and related technologies.",
        },
        {
            "id": "yarn",
            "label": "Yarn",
            "description": "Fast package manager",
            "parent": "dev-javascript",
            "help": "Yarn is a fast, reliable, and secure dependency management tool.",
        },
        {
            "id": "pnpm",
            "label": "pnpm",
            "description": "Efficient package manager",
            "parent": "dev-javascript",
            "help": "pnpm is a fast, disk space efficient package manager.",
        },
        {
            "id": "nvm",
            "label": "NVM",
            "description": "Node version manager",
            "parent": "dev-javascript",
            "help": "NVM allows you to quickly install and use different versions of Node.",
        },
        {
            "id": "prettier",
            "label": "Prettier",
            "description": "Code formatter",
            "parent": "dev-javascript",
            "help": "Prettier is an opinionated code formatter for JavaScript, TypeScript, and more.",
        },
        {
            "id": "eslint",
            "label": "ESLint",
            "description": "JavaScript linter",
            "parent": "dev-javascript",
            "help": "ESLint is a tool for identifying and reporting on patterns in JavaScript.",
        },
        {
            "id": "jest",
            "label": "Jest",
            "description": "JavaScript testing",
            "parent": "dev-javascript",
            "help": "Jest is a delightful JavaScript testing framework with a focus on simplicity.",
        },
        {
            "id": "mocha",
            "label": "Mocha",
            "description": "Test framework",
            "parent": "dev-javascript",
            "help": "Mocha is a feature-rich JavaScript test framework running on Node.js.",
        },
        {
            "id": "bundler",
            "label": "Bundler",
            "description": "Module bundler",
            "parent": "dev-javascript",
            "help": "Modern JavaScript module bundler for building applications.",
        },
    ]

    # Rust tools
    rust_items = [
        {
            "id": "rust",
            "label": "Rust",
            "description": "Systems programming language",
            "parent": "dev-rust",
            "help": "Rust is a language empowering everyone to build reliable and efficient software with memory safety and zero-cost abstractions.",
        },
        {
            "id": "cargo",
            "label": "Cargo",
            "description": "Rust package manager",
            "parent": "dev-rust",
            "help": "Cargo is the Rust package manager that downloads dependencies and compiles packages.",
        },
        {
            "id": "rustup",
            "label": "rustup",
            "description": "Rust toolchain installer",
            "parent": "dev-rust",
            "help": "rustup is the Rust toolchain installer and version management tool.",
        },
        {
            "id": "rustfmt",
            "label": "rustfmt",
            "description": "Rust code formatter",
            "parent": "dev-rust",
            "help": "rustfmt is a tool for formatting Rust code according to style guidelines.",
        },
    ]

    # Java/Kotlin tools
    java_items = [
        {
            "id": "java",
            "label": "Java (OpenJDK)",
            "description": "Java Development Kit",
            "parent": "dev-java",
            "help": "OpenJDK is the open-source implementation of the Java Platform.",
        },
        {
            "id": "kotlin",
            "label": "Kotlin",
            "description": "Modern JVM language",
            "parent": "dev-java",
            "help": "Kotlin is a modern programming language that makes developers happier.",
        },
        {
            "id": "intellij-idea-community",
            "label": "IntelliJ IDEA Community",
            "description": "Java/Kotlin IDE",
            "parent": "dev-java",
            "help": "IntelliJ IDEA Community Edition is JetBrains' powerful Java IDE with smart code completion, refactoring tools, and built-in version control.",
        },
        {
            "id": "android-studio",
            "label": "Android Studio",
            "description": "Android development",
            "parent": "dev-java",
            "help": "Android Studio is the official IDE for Android app development based on IntelliJ IDEA.",
        },
        {
            "id": "gradle",
            "label": "Gradle",
            "description": "Build automation tool",
            "parent": "dev-java",
            "help": "Gradle is a build automation tool for multi-language software development.",
        },
        {
            "id": "maven",
            "label": "Maven",
            "description": "Project management tool",
            "parent": "dev-java",
            "help": "Apache Maven is a software project management and comprehension tool.",
        },
    ]

    # C/C++ tools
    cpp_items = [
        {
            "id": "clion",
            "label": "CLion",
            "description": "C/C++ IDE by JetBrains",
            "parent": "dev-cpp",
            "help": "CLion is JetBrains' cross-platform IDE for C and C++ development.",
        },
        {
            "id": "cmake",
            "label": "CMake",
            "description": "Build system generator",
            "parent": "dev-cpp",
            "help": "CMake is a cross-platform build system generator.",
        },
    ]

    # .NET/C# tools
    dotnet_items = [
        {
            "id": "dotnet",
            "label": ".NET SDK",
            "description": ".NET development platform",
            "parent": "dev-dotnet",
            "help": ".NET is a free, cross-platform, open source developer platform.",
        },
        {
            "id": "rider",
            "label": "Rider",
            "description": ".NET IDE by JetBrains",
            "parent": "dev-dotnet",
            "help": "Rider is JetBrains' cross-platform .NET IDE based on IntelliJ and ReSharper.",
        },
    ]

    # Other languages
    other_lang_items = [
        {
            "id": "php",
            "label": "PHP",
            "description": "PHP scripting language",
            "parent": "dev-other-langs",
            "help": "PHP is a popular general-purpose scripting language for web development.",
        },
        {
            "id": "ruby",
            "label": "Ruby",
            "description": "Ruby programming language",
            "parent": "dev-other-langs",
            "help": "Ruby is a dynamic, interpreted programming language focused on simplicity.",
        },
        {
            "id": "perl",
            "label": "Perl",
            "description": "Perl programming language",
            "parent": "dev-other-langs",
            "help": "Perl is a highly capable, feature-rich programming language.",
        },
        {
            "id": "lua",
            "label": "Lua",
            "description": "Lightweight scripting",
            "parent": "dev-other-langs",
            "help": "Lua is a powerful, efficient, lightweight, embeddable scripting language.",
        },
        {
            "id": "clojure",
            "label": "Clojure",
            "description": "Lisp on the JVM",
            "parent": "dev-other-langs",
            "help": "Clojure is a dynamic, functional programming language on the JVM.",
        },
        {
            "id": "elixir",
            "label": "Elixir",
            "description": "Functional language",
            "parent": "dev-other-langs",
            "help": "Elixir is a dynamic, functional language designed for building scalable applications.",
        },
        {
            "id": "haskell",
            "label": "Haskell",
            "description": "Pure functional language",
            "parent": "dev-other-langs",
            "help": "Haskell is an advanced, purely functional programming language.",
        },
        {
            "id": "scala",
            "label": "Scala",
            "description": "JVM language",
            "parent": "dev-other-langs",
            "help": "Scala combines object-oriented and functional programming in one language.",
        },
        {
            "id": "swift",
            "label": "Swift",
            "description": "Apple's language",
            "parent": "dev-other-langs",
            "help": "Swift is a powerful and intuitive programming language for Apple platforms.",
        },
        {
            "id": "dart",
            "label": "Dart",
            "description": "Flutter language",
            "parent": "dev-other-langs",
            "help": "Dart is a client-optimized language for fast apps on any platform.",
        },
        {
            "id": "julia",
            "label": "Julia",
            "description": "Scientific computing",
            "parent": "dev-other-langs",
            "help": "Julia is a high-level, high-performance language for technical computing.",
        },
        {
            "id": "nim",
            "label": "Nim",
            "description": "Systems language",
            "parent": "dev-other-langs",
            "help": "Nim is a statically typed compiled systems programming language.",
        },
        {
            "id": "zig",
            "label": "Zig",
            "description": "Systems language",
            "parent": "dev-other-langs",
            "help": "Zig is a general-purpose programming language and toolchain.",
        },
    ]

    # JetBrains IDEs
    jetbrains_items = [
        {
            "id": "datagrip",
            "label": "DataGrip",
            "description": "Database IDE",
            "parent": "dev-jetbrains",
            "help": "DataGrip is JetBrains' IDE for databases and SQL with smart query console.",
        },
    ]

    # Code Editors
    code_editor_items = [
        {
            "id": "vscode",
            "label": "Visual Studio Code",
            "description": "Modern code editor",
            "parent": "dev-code-editors",
            "default": True,
            "help": """Visual Studio Code is Microsoft's free, open-source code editor with excellent language support, debugging, Git integration, and a vast extension ecosystem.

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
- Integrates with system file manager context menu""",
        },
        {
            "id": "cursor",
            "label": "Cursor",
            "description": "AI-powered code editor",
            "parent": "dev-code-editors",
            "help": "Cursor is an AI-first code editor that helps you code faster with AI assistance.",
        },
        {
            "id": "zed",
            "label": "Zed",
            "description": "High-performance code editor",
            "parent": "dev-code-editors",
            "help": "Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.",
        },
        {
            "id": "sublime-text",
            "label": "Sublime Text",
            "description": "Fast text editor",
            "parent": "dev-code-editors",
            "help": "Sublime Text is a sophisticated text editor for code, markup and prose with a slick user interface and extraordinary features.",
        },
    ]

    # Text Editors
    text_editor_items = [
        {
            "id": "vim",
            "label": "Vim",
            "description": "Terminal editor",
            "parent": "dev-text-editors",
            "help": "Vim is a highly configurable text editor built to enable efficient text editing. It's an improved version of the vi editor.",
        },
        {
            "id": "neovim",
            "label": "Neovim",
            "description": "Modern Vim fork",
            "parent": "dev-text-editors",
            "help": "Neovim is a refactor of Vim aiming to improve extensibility and maintainability with better plugin architecture.",
        },
        {
            "id": "emacs",
            "label": "Emacs",
            "description": "Extensible text editor",
            "parent": "dev-text-editors",
            "help": "GNU Emacs is an extensible, customizable, self-documenting text editor.",
        },
    ]

    # Version Control
    vcs_items = [
        {
            "id": "git",
            "label": "Git",
            "description": "Version control",
            "parent": "dev-vcs",
            "default": True,
            "help": "Git is a free and open source distributed version control system designed to handle everything from small to very large projects.",
        },
        {
            "id": "git-config-global",
            "label": "Git Global Configuration",
            "description": "Set up Git user info",
            "parent": "dev-vcs",
            "help": "Configure Git with your name and email for all repositories.",
        },
        {
            "id": "ssh-key-github",
            "label": "SSH Key for GitHub",
            "description": "Generate GitHub SSH key",
            "parent": "dev-vcs",
            "help": "Generate an SSH key and add it to your GitHub account for secure access.",
        },
    ]

    # Containers & Orchestration
    container_items = [
        {
            "id": "docker",
            "label": "Docker",
            "description": "Container platform",
            "parent": "dev-containers",
            "default": True,
            "help": """Docker is a platform for developers to develop, deploy, and run applications with containers.

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
- Testing and staging environments""",
        },
        {
            "id": "docker-compose",
            "label": "Docker Compose",
            "description": "Multi-container orchestration",
            "parent": "dev-containers",
            "help": "Docker Compose is a tool for defining and running multi-container Docker applications with YAML configuration.",
        },
        {
            "id": "kubernetes",
            "label": "Kubernetes",
            "description": "Container orchestration",
            "parent": "dev-containers",
            "help": """Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.

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
- CI/CD pipeline integration""",
        },
    ]

    # SQL Databases
    sql_db_items = [
        {
            "id": "postgresql",
            "label": "PostgreSQL",
            "description": "Advanced SQL database",
            "parent": "dev-sql-databases",
            "help": "PostgreSQL is a powerful, open source object-relational database system.",
        },
        {
            "id": "mysql",
            "label": "MySQL",
            "description": "Popular SQL database",
            "parent": "dev-sql-databases",
            "help": "MySQL is the world's most popular open source database.",
        },
        {
            "id": "mariadb",
            "label": "MariaDB",
            "description": "MySQL fork",
            "parent": "dev-sql-databases",
            "help": "MariaDB is a community-developed fork of MySQL with enhanced features.",
        },
    ]

    # NoSQL Databases
    nosql_db_items = [
        {
            "id": "mongodb",
            "label": "MongoDB",
            "description": "Document database",
            "parent": "dev-nosql-databases",
            "help": "MongoDB is a document-oriented NoSQL database used for high volume data storage.",
        },
        {
            "id": "redis",
            "label": "Redis",
            "description": "In-memory data store",
            "parent": "dev-nosql-databases",
            "help": "Redis is an in-memory data structure store used as a database, cache, and message broker.",
        },
        {
            "id": "elasticsearch",
            "label": "Elasticsearch",
            "description": "Search engine",
            "parent": "dev-nosql-databases",
            "help": "Elasticsearch is a distributed, RESTful search and analytics engine.",
        },
        {
            "id": "cassandra",
            "label": "Cassandra",
            "description": "Wide column store",
            "parent": "dev-nosql-databases",
            "help": "Apache Cassandra is a distributed NoSQL database management system.",
        },
        {
            "id": "couchdb",
            "label": "CouchDB",
            "description": "Document database",
            "parent": "dev-nosql-databases",
            "help": "Apache CouchDB is a document-oriented NoSQL database.",
        },
        {
            "id": "influxdb",
            "label": "InfluxDB",
            "description": "Time series database",
            "parent": "dev-nosql-databases",
            "help": "InfluxDB is a time series database designed for high-write and high-query loads.",
        },
    ]

    # Database Tools
    db_tool_items = [
        {
            "id": "dbeaver",
            "label": "DBeaver",
            "description": "Universal database tool",
            "parent": "dev-db-tools",
            "help": "DBeaver is a free multi-platform database tool for developers, SQL programmers, and DBAs.",
        },
        {
            "id": "pgadmin",
            "label": "pgAdmin",
            "description": "PostgreSQL management",
            "parent": "dev-db-tools",
            "help": "pgAdmin is the most popular and feature-rich Open Source administration platform for PostgreSQL.",
        },
        {
            "id": "mysql-workbench",
            "label": "MySQL Workbench",
            "description": "MySQL database design",
            "parent": "dev-db-tools",
            "help": "MySQL Workbench is a unified visual tool for database architects, developers, and DBAs.",
        },
    ]

    # API & Web Tools
    api_tool_items = [
        {
            "id": "postman",
            "label": "Postman",
            "description": "API development platform",
            "parent": "dev-api-tools",
            "help": "Postman is an API platform for building and using APIs with testing and documentation.",
        },
        {
            "id": "insomnia",
            "label": "Insomnia",
            "description": "REST and GraphQL client",
            "parent": "dev-api-tools",
            "help": "Insomnia is a powerful REST and GraphQL client with a beautiful interface.",
        },
        {
            "id": "httpie",
            "label": "HTTPie",
            "description": "CLI HTTP client",
            "parent": "dev-api-tools",
            "help": "HTTPie is a command-line HTTP client with an intuitive UI and JSON support.",
        },
    ]

    # Shells
    shell_items = [
        {
            "id": "bash",
            "label": "Bash",
            "description": "Bourne Again Shell",
            "parent": "dev-shells",
            "default": True,
            "help": "Bash is the GNU Project's shell and the default shell on most Linux systems.",
        },
        {
            "id": "zsh",
            "label": "Zsh",
            "description": "Z Shell",
            "parent": "dev-shells",
            "help": "Zsh is a shell designed for interactive use with many features from bash, ksh, and tcsh.",
        },
        {
            "id": "fish",
            "label": "Fish",
            "description": "Friendly shell",
            "parent": "dev-shells",
            "help": "Fish is a smart and user-friendly command line shell with autosuggestions.",
        },
        {
            "id": "nushell",
            "label": "Nushell",
            "description": "Modern shell",
            "parent": "dev-shells",
            "help": "Nushell is a modern shell that understands data structures.",
        },
        {
            "id": "elvish",
            "label": "Elvish",
            "description": "Expressive shell",
            "parent": "dev-shells",
            "help": "Elvish is an expressive programming language and a versatile interactive shell.",
        },
    ]

    # Terminal Emulators
    terminal_emulator_items = [
        {
            "id": "kitty",
            "label": "Kitty",
            "description": "GPU-accelerated terminal",
            "parent": "dev-terminal-emulators",
            "help": "Kitty is a fast, feature-rich, GPU based terminal emulator.",
        },
        {
            "id": "alacritty",
            "label": "Alacritty",
            "description": "GPU-accelerated terminal",
            "parent": "dev-terminal-emulators",
            "help": "Alacritty is a modern terminal emulator with sensible defaults and extensive configuration.",
        },
        {
            "id": "wezterm",
            "label": "WezTerm",
            "description": "GPU-accelerated terminal",
            "parent": "dev-terminal-emulators",
            "help": "WezTerm is a GPU-accelerated cross-platform terminal emulator and multiplexer.",
        },
        {
            "id": "ghostty",
            "label": "Ghostty",
            "description": "Fast, feature-rich terminal with native UI",
            "parent": "dev-terminal-emulators",
            "help": "Ghostty is a modern, fast, feature-rich terminal emulator that uses platform-native UI and GPU acceleration. Created by Mitchell Hashimoto.",
        },
    ]

    # Shell Enhancements
    shell_enhancement_items = [
        {
            "id": "prompt-starship",
            "label": "Starship Prompt",
            "description": "Fast cross-shell prompt",
            "parent": "dev-shell-enhancements",
            "help": "Starship is a minimal, blazing-fast, and customizable prompt for any shell.",
        },
        {
            "id": "prompt-ohmyposh",
            "label": "Oh My Posh",
            "description": "Prompt theme engine",
            "parent": "dev-shell-enhancements",
            "help": "Oh My Posh is a prompt theme engine for any shell with many built-in themes.",
        },
        {
            "id": "prompt-pure",
            "label": "Pure Prompt",
            "description": "Minimal Zsh prompt",
            "parent": "dev-shell-enhancements",
            "help": "Pure is a pretty, minimal and fast ZSH prompt.",
        },
        {
            "id": "prompt-spaceship",
            "label": "Spaceship Prompt",
            "description": "Minimalistic Zsh prompt",
            "parent": "dev-shell-enhancements",
            "help": "Spaceship is a minimalistic, powerful and customizable Zsh prompt.",
        },
        {
            "id": "tmux",
            "label": "tmux",
            "description": "Terminal multiplexer",
            "parent": "dev-shell-enhancements",
            "help": "tmux is a terminal multiplexer that lets you switch between several programs in one terminal.",
        },
        {
            "id": "screen",
            "label": "GNU Screen",
            "description": "Terminal multiplexer",
            "parent": "dev-shell-enhancements",
            "help": "GNU Screen is a full-screen window manager that multiplexes a physical terminal.",
        },
    ]

    # Cloud & Infrastructure
    cloud_items = [
        {
            "id": "aws-cli",
            "label": "AWS CLI",
            "description": "Amazon Web Services CLI",
            "parent": "dev-cloud",
            "help": "AWS CLI is a unified tool to manage your AWS services from the command line.",
        },
        {
            "id": "gcloud",
            "label": "Google Cloud SDK",
            "description": "Google Cloud Platform CLI",
            "parent": "dev-cloud",
            "help": "Google Cloud SDK is a set of tools for Google Cloud Platform including gcloud, gsutil, and bq.",
        },
        {
            "id": "azure-cli",
            "label": "Azure CLI",
            "description": "Microsoft Azure CLI",
            "parent": "dev-cloud",
            "help": "Azure CLI is a cross-platform command-line tool to manage Azure resources.",
        },
        {
            "id": "terraform",
            "label": "Terraform",
            "description": "Infrastructure as Code",
            "parent": "dev-cloud",
            "help": "Terraform is an infrastructure as code tool for building, changing, and versioning infrastructure.",
        },
        {
            "id": "pulumi",
            "label": "Pulumi",
            "description": "Modern Infrastructure as Code",
            "parent": "dev-cloud",
            "help": "Pulumi is an infrastructure as code platform that allows you to use familiar programming languages.",
        },
    ]

    # Build Tools
    build_tool_items = [
        {
            "id": "make",
            "label": "GNU Make",
            "description": "Build automation",
            "parent": "dev-build-tools",
            "help": "GNU Make is a tool which controls the generation of executables from source code.",
        },
        {
            "id": "bazel",
            "label": "Bazel",
            "description": "Build and test tool",
            "parent": "dev-build-tools",
            "help": "Bazel is Google's build tool for building and testing software at any scale.",
        },
        {
            "id": "ninja",
            "label": "Ninja",
            "description": "Small build system",
            "parent": "dev-build-tools",
            "help": "Ninja is a small build system with a focus on speed.",
        },
    ]

    # Testing Tools
    testing_items = [
        {
            "id": "selenium",
            "label": "Selenium",
            "description": "Web testing framework",
            "parent": "dev-testing",
            "help": "Selenium is a suite of tools for automating web browsers.",
        },
        {
            "id": "cypress",
            "label": "Cypress",
            "description": "E2E testing framework",
            "parent": "dev-testing",
            "help": "Cypress is a JavaScript end-to-end testing framework.",
        },
        {
            "id": "playwright",
            "label": "Playwright",
            "description": "Browser automation",
            "parent": "dev-testing",
            "help": "Playwright enables reliable end-to-end testing for modern web apps.",
        },
    ]

    # Documentation Tools
    doc_items = [
        {
            "id": "sphinx",
            "label": "Sphinx",
            "description": "Python documentation",
            "parent": "dev-documentation",
            "help": "Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.",
        },
        {
            "id": "mkdocs",
            "label": "MkDocs",
            "description": "Project documentation",
            "parent": "dev-documentation",
            "help": "MkDocs is a fast, simple and downright gorgeous static site generator for documentation.",
        },
        {
            "id": "doxygen",
            "label": "Doxygen",
            "description": "Source code documentation",
            "parent": "dev-documentation",
            "help": "Doxygen is the de facto standard tool for generating documentation from annotated source code.",
        },
    ]

    # Development Utilities
    dev_util_items = [
        {
            "id": "ctags",
            "label": "ctags",
            "description": "Code indexing",
            "parent": "dev-utilities",
            "help": "ctags generates an index file of language objects found in source files.",
        },
        {
            "id": "gnu-global",
            "label": "GNU Global",
            "description": "Source code tagging",
            "parent": "dev-utilities",
            "help": "GNU Global is a source code tagging system that works with many languages.",
        },
        {
            "id": "binutils",
            "label": "GNU Binutils",
            "description": "Binary utilities",
            "parent": "dev-utilities",
            "help": "GNU Binutils is a collection of binary tools including assembler, linker, and others.",
        },
        {
            "id": "wine",
            "label": "Wine",
            "description": "Windows compatibility layer",
            "parent": "dev-utilities",
            "help": """Wine allows you to run Windows applications on Linux.
Installs:
- Wine stable (latest version)
- Wine32 and Wine64 libraries
- Winetricks for easy configuration
- Common Windows fonts
- Mono and Gecko for .NET/IE compatibility""",
        },
        {
            "id": "ansible-cloud",
            "label": "Ansible",
            "description": "Automation platform",
            "parent": "dev-utilities",
            "help": "Ansible automates cloud provisioning, configuration management, and application deployment.",
        },
        {
            "id": "gdb",
            "label": "GDB",
            "description": "GNU debugger",
            "parent": "dev-utilities",
            "help": "GDB, the GNU Project debugger, allows you to see what is going on inside programs.",
        },
        {
            "id": "valgrind",
            "label": "Valgrind",
            "description": "Memory debugger",
            "parent": "dev-utilities",
            "help": "Valgrind is an instrumentation framework for building dynamic analysis tools.",
        },
        {
            "id": "strace",
            "label": "strace",
            "description": "System call tracer",
            "parent": "dev-utilities",
            "help": "strace is a diagnostic, debugging and instructional userspace utility for Linux.",
        },
        {
            "id": "ltrace",
            "label": "ltrace",
            "description": "Library call tracer",
            "parent": "dev-utilities",
            "help": "ltrace is a program that intercepts and records dynamic library calls.",
        },
        {
            "id": "perf",
            "label": "perf",
            "description": "Performance analysis",
            "parent": "dev-utilities",
            "help": "perf is a performance analyzing tool in Linux for profiling applications.",
        },
        {
            "id": "heaptrack",
            "label": "Heaptrack",
            "description": "Heap memory profiler",
            "parent": "dev-utilities",
            "help": "Heaptrack is a heap memory profiler that tracks allocations.",
        },
        {
            "id": "jq",
            "label": "jq",
            "description": "JSON processor",
            "parent": "dev-utilities",
            "help": "jq is a lightweight and flexible command-line JSON processor.",
        },
        {
            "id": "yq",
            "label": "yq",
            "description": "YAML processor",
            "parent": "dev-utilities",
            "help": "yq is a portable command-line YAML processor.",
        },
    ]

    # Editor Settings
    editor_setting_items = [
        {
            "id": "vscode-vim-mode",
            "label": "VS Code Vim Mode",
            "description": "Enable Vim keybindings",
            "parent": "dev-editor-settings",
            "help": "Enable Vim keybindings in Visual Studio Code for efficient text editing.",
        },
        {
            "id": "vscode-theme-sync",
            "label": "VS Code Theme Sync",
            "description": "Sync with system theme",
            "parent": "dev-editor-settings",
            "help": "Automatically switch VS Code theme to match your system theme.",
        },
        {
            "id": "editor-minimap",
            "label": "Editor Minimap",
            "description": "Show code minimap",
            "parent": "dev-editor-settings",
            "default": True,
            "help": "Show a minimap overview of your code on the side of the editor.",
        },
        {
            "id": "editor-ligatures",
            "label": "Editor Ligatures",
            "description": "Enable font ligatures",
            "parent": "dev-editor-settings",
            "default": True,
            "help": "Enable programming ligatures if using a font that supports them (like Fira Code).",
        },
        {
            "id": "editor-font-family",
            "label": "Editor Font",
            "description": "Choose editor font",
            "parent": "dev-editor-settings",
            "is_configurable": True,
            "config_type": "select",
            "options": [
                "JetBrains Mono",
                "Fira Code",
                "Source Code Pro",
                "Cascadia Code",
                "Monaco",
                "Consolas",
                "Menlo",
                "Ubuntu Mono",
                "Hack",
                "Inconsolata",
                "Roboto Mono",
                "SF Mono",
                "IBM Plex Mono",
                "Iosevka",
                "Victor Mono",
                "Input Mono",
            ],
            "default_value": "JetBrains Mono",
            "help": "Choose the font family for code editors. JetBrains Mono and Fira Code include programming ligatures.",
        },
        {
            "id": "vscode-font-size",
            "label": "VS Code Font Size",
            "description": "Editor font size",
            "parent": "dev-editor-settings",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24],
            "default_value": 14,
            "unit": "px",
            "help": "Set the font size for the VS Code editor (pixels).",
        },
        {
            "id": "editor-line-height",
            "label": "Line Height",
            "description": "Space between lines",
            "parent": "dev-editor-settings",
            "is_configurable": True,
            "config_type": "slider",
            "min_value": 1.0,
            "max_value": 3.0,
            "step": 0.1,
            "default_value": 1.5,
            "help": "Set the line height multiplier for better readability.",
        },
        {
            "id": "vscode-tab-size",
            "label": "VS Code Tab Size",
            "description": "Spaces per tab",
            "parent": "dev-editor-settings",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [2, 4, 8],
            "default_value": 4,
            "help": "Number of spaces to use for each tab in VS Code.",
        },
        {
            "id": "vscode-word-wrap",
            "label": "VS Code Word Wrap",
            "description": "Wrap long lines",
            "parent": "dev-editor-settings",
            "help": "Automatically wrap long lines in the VS Code editor.",
        },
        {
            "id": "vscode-bracket-colorization",
            "label": "Bracket Pair Colorization",
            "description": "Color matching brackets",
            "parent": "dev-editor-settings",
            "default": True,
            "help": "Use colors to help identify matching bracket pairs in VS Code.",
        },
        {
            "id": "vscode-sticky-scroll",
            "label": "VS Code Sticky Scroll",
            "description": "Show current scope",
            "parent": "dev-editor-settings",
            "default": True,
            "help": "Show the current function/class scope at the top of the editor while scrolling.",
        },
        {
            "id": "vscode-inlay-hints",
            "label": "VS Code Inlay Hints",
            "description": "Show inline type hints",
            "parent": "dev-editor-settings",
            "help": "Display inline parameter names and type information in the editor.",
        },
        {
            "id": "app-theme-integration",
            "label": "Application Theme Integration",
            "description": "Apply system theme to apps",
            "parent": "dev-editor-settings",
            "default": True,
            "help": "Automatically apply your selected system theme to supported applications.",
        },
        {
            "id": "cursor",
            "label": "Cursor",
            "description": "Configure cursor",
            "parent": "dev-editor-settings",
            "help": "Configure cursor appearance and behavior.",
        },
    ]

    # Terminal Settings
    terminal_setting_items = [
        {
            "id": "terminal-font-family",
            "label": "Terminal Font",
            "description": "Choose terminal font",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "select",
            "options": [
                "JetBrains Mono",
                "Fira Code",
                "Source Code Pro",
                "Cascadia Code",
                "Ubuntu Mono",
                "Hack",
                "Inconsolata",
                "Roboto Mono",
                "SF Mono",
                "IBM Plex Mono",
                "Iosevka",
                "Victor Mono",
                "Anonymous Pro",
                "Cousine",
                "DejaVu Sans Mono",
                "Droid Sans Mono",
                "Liberation Mono",
            ],
            "default_value": "JetBrains Mono",
            "help": "Choose the font family for your terminal. JetBrains Mono and Fira Code include programming ligatures.",
        },
        {
            "id": "terminal-font-size",
            "label": "Terminal Font Size",
            "description": "Font size in points",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24],
            "default_value": 12,
            "unit": "pt",
            "help": "Set the font size for your terminal in points.",
        },
        {
            "id": "terminal-transparency",
            "label": "Terminal Transparency",
            "description": "Background transparency",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "slider",
            "min_value": 0,
            "max_value": 100,
            "default_value": 85,
            "unit": "%",
            "help": "Set the transparency level of your terminal background. 0% is opaque, 100% is fully transparent.",
        },
        {
            "id": "terminal-blur",
            "label": "Background Blur",
            "description": "Blur behind terminal",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "slider",
            "min_value": 0,
            "max_value": 20,
            "default_value": 5,
            "unit": "px",
            "help": "Apply blur effect to content behind transparent terminal windows.",
        },
        {
            "id": "terminal-cursor-style",
            "label": "Terminal Cursor Style",
            "description": "Terminal cursor shape",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "select",
            "options": ["Block", "Underline", "Bar"],
            "default_value": "Block",
            "help": "Choose the cursor style for your terminal.",
        },
        {
            "id": "terminal-cursor-blink",
            "label": "Terminal Cursor Blink",
            "description": "Enable cursor blinking",
            "parent": "dev-terminal-settings",
            "default": True,
            "help": "Enable or disable cursor blinking in the terminal.",
        },
        {
            "id": "terminal-scrollback",
            "label": "Scrollback Lines",
            "description": "Number of history lines",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [1000, 2000, 5000, 10000, 20000, 50000, 100000],
            "default_value": 10000,
            "help": "Number of lines to keep in terminal scrollback history.",
        },
        {
            "id": "terminal-bell",
            "label": "Terminal Bell",
            "description": "Audible or visual bell",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "select",
            "options": ["None", "Audible", "Visual", "Both"],
            "default_value": "Visual",
            "help": "Configure terminal bell behavior for alerts.",
        },
        {
            "id": "terminal-padding",
            "label": "Terminal Padding",
            "description": "Padding around text",
            "parent": "dev-terminal-settings",
            "is_configurable": True,
            "config_type": "spinner",
            "values": [0, 2, 4, 6, 8, 10, 12, 16, 20],
            "default_value": 8,
            "unit": "px",
            "help": "Set padding around terminal text for better readability.",
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
    # Code editors moved to text-editors-ides category
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
        existing_children = subcat.get("children", [])

        # Get all direct item children (not subcategories)
        item_children = [
            item["id"] for item in items if item.get("parent") == subcat["id"] and not item.get("is_category")
        ]

        # If there are existing children (subcategories), add items to them
        # If no existing children, just use the items
        if existing_children:
            # Preserve existing subcategory children and add any direct items
            all_children = list(existing_children)  # Copy existing
            all_children.extend([child for child in item_children if child not in all_children])
            subcat["children"] = all_children
        else:
            subcat["children"] = item_children

    # AI/ML items
    ai_ml_items = [
        {
            "id": "ollama",
            "label": "Ollama",
            "description": "Run LLMs locally",
            "parent": "ai-ml",
            "help": "Ollama allows you to run large language models locally on your machine.",
        },
        {
            "id": "stable-diffusion",
            "label": "Stable Diffusion",
            "description": "AI image generation",
            "parent": "ai-ml",
            "help": "Stable Diffusion is a deep learning model for generating detailed images from text descriptions.",
        },
        {
            "id": "pytorch",
            "label": "PyTorch",
            "description": "ML framework",
            "parent": "ai-ml",
            "help": "PyTorch is an open source machine learning framework.",
        },
        {
            "id": "tensorflow",
            "label": "TensorFlow",
            "description": "ML platform",
            "parent": "ai-ml",
            "help": "TensorFlow is an end-to-end open source platform for machine learning.",
        },
        {
            "id": "jupyter",
            "label": "Jupyter Lab",
            "description": "Interactive notebooks",
            "parent": "ai-ml",
            "help": "JupyterLab is the latest web-based interactive development environment for notebooks.",
        },
        {
            "id": "anaconda",
            "label": "Anaconda",
            "description": "Data science platform",
            "parent": "ai-ml",
            "help": "Anaconda is a distribution of Python and R for scientific computing and data science.",
        },
    ]

    items.extend(ai_ml_items)
    ai_ml_cat = next(cat for cat in categories if cat["id"] == "ai-ml")
    ai_ml_cat["children"] = [item["id"] for item in ai_ml_items]

    # Other categories remain as before...
    # (We'll organize them in subsequent passes)

    # Desktop Environment items (simplified for now)
    desktop_items = [
        {
            "id": "gnome",
            "label": "GNOME",
            "description": "Modern desktop environment",
            "parent": "desktop",
            "default": True,
            "help": "GNOME is a free and open-source desktop environment for Unix-like operating systems.",
        },
        {
            "id": "kde-plasma",
            "label": "KDE Plasma",
            "description": "Feature-rich desktop",
            "parent": "desktop",
            "help": "KDE Plasma is a graphical desktop environment with customizable layouts.",
        },
        {
            "id": "xfce",
            "label": "XFCE",
            "description": "Lightweight desktop",
            "parent": "desktop",
            "help": "Xfce is a lightweight desktop environment for Unix-like operating systems.",
        },
    ]

    items.extend(desktop_items)
    desktop_cat = next(cat for cat in categories if cat["id"] == "desktop")
    desktop_cat["children"] = [item["id"] for item in desktop_items]

    # Applications items (simplified for now)
    # Web Browsers
    web_browser_items = [
        {
            "id": "firefox",
            "label": "Firefox",
            "description": "Open-source web browser",
            "parent": "web-browsers",
            "default": True,
            "help": "Mozilla Firefox is a free and open-source web browser.",
        },
        {
            "id": "chrome",
            "label": "Google Chrome",
            "description": "Fast web browser by Google",
            "parent": "web-browsers",
            "help": "Google Chrome is a fast, secure, and free web browser.",
        },
        {
            "id": "brave",
            "label": "Brave",
            "description": "Privacy-focused browser",
            "parent": "web-browsers",
            "help": "Brave is a privacy-focused browser that blocks ads and trackers.",
        },
        {
            "id": "vivaldi",
            "label": "Vivaldi",
            "description": "Customizable browser",
            "parent": "web-browsers",
            "help": "Vivaldi is a freeware, cross-platform web browser with extensive customization.",
        },
        {
            "id": "opera",
            "label": "Opera",
            "description": "Feature-rich browser",
            "parent": "web-browsers",
            "help": "Opera is a multi-platform web browser with built-in VPN and ad blocker.",
        },
    ]

    # Communication
    communication_items = [
        {
            "id": "slack",
            "label": "Slack",
            "description": "Team messaging",
            "parent": "communication",
            "help": "Slack is a messaging app for business that connects people to the information they need.",
        },
        {
            "id": "discord",
            "label": "Discord",
            "description": "Voice and text chat",
            "parent": "communication",
            "help": "Discord is a VoIP and instant messaging platform for communities.",
        },
        {
            "id": "teams",
            "label": "Microsoft Teams",
            "description": "Business communication",
            "parent": "communication",
            "help": "Microsoft Teams is a proprietary business communication platform.",
        },
        {
            "id": "zoom",
            "label": "Zoom",
            "description": "Video conferencing",
            "parent": "communication",
            "help": "Zoom is a proprietary videotelephony software program.",
        },
        {
            "id": "telegram",
            "label": "Telegram",
            "description": "Secure messaging",
            "parent": "communication",
            "help": "Telegram is a cloud-based instant messaging service.",
        },
        {
            "id": "signal",
            "label": "Signal",
            "description": "Private messaging",
            "parent": "communication",
            "help": "Signal is a cross-platform encrypted messaging service.",
        },
        {
            "id": "element",
            "label": "Element",
            "description": "Matrix client",
            "parent": "communication",
            "help": "Element is a free and open-source software instant messaging client.",
        },
    ]

    # Graphics & Media
    graphics_items = [
        {
            "id": "gimp",
            "label": "GIMP",
            "description": "Image editor",
            "parent": "graphics-media",
            "help": "GIMP is a free and open-source raster graphics editor.",
        },
        {
            "id": "inkscape",
            "label": "Inkscape",
            "description": "Vector graphics editor",
            "parent": "graphics-media",
            "help": "Inkscape is a free and open-source vector graphics editor.",
        },
        {
            "id": "blender",
            "label": "Blender",
            "description": "3D creation suite",
            "parent": "graphics-media",
            "help": "Blender is a free and open-source 3D computer graphics software.",
        },
        {
            "id": "krita",
            "label": "Krita",
            "description": "Digital painting",
            "parent": "graphics-media",
            "help": "Krita is a free and open-source raster graphics editor designed for digital painting.",
        },
        {
            "id": "darktable",
            "label": "Darktable",
            "description": "RAW photo editor",
            "parent": "graphics-media",
            "help": "Darktable is a free and open-source photography application and raw developer.",
        },
    ]

    # Text Editors & IDEs
    editor_items = [
        {
            "id": "vscode",
            "label": "Visual Studio Code",
            "description": "Code editor by Microsoft",
            "parent": "text-editors-ides",
            "default": True,
            "help": "Visual Studio Code is a free source-code editor made by Microsoft.",
        },
        {
            "id": "sublime-text",
            "label": "Sublime Text",
            "description": "Sophisticated text editor",
            "parent": "text-editors-ides",
            "help": "Sublime Text is a shareware cross-platform source code editor.",
        },
        {
            "id": "atom",
            "label": "Atom",
            "description": "Hackable text editor",
            "parent": "text-editors-ides",
            "help": "Atom is a free and open-source text and source code editor.",
        },
        {
            "id": "intellij-idea",
            "label": "IntelliJ IDEA",
            "description": "Java IDE",
            "parent": "text-editors-ides",
            "help": "IntelliJ IDEA is an integrated development environment for Java.",
        },
        {
            "id": "pycharm",
            "label": "PyCharm",
            "description": "Python IDE",
            "parent": "text-editors-ides",
            "help": "PyCharm is an integrated development environment for Python.",
        },
    ]

    # Audio & Music
    audio_items = [
        {
            "id": "spotify",
            "label": "Spotify",
            "description": "Music streaming",
            "parent": "audio-music",
            "help": "Spotify is a proprietary Swedish audio streaming and media services provider.",
        },
        {
            "id": "audacity",
            "label": "Audacity",
            "description": "Audio editor",
            "parent": "audio-music",
            "help": "Audacity is a free and open-source digital audio editor and recording application.",
        },
        {
            "id": "ardour",
            "label": "Ardour",
            "description": "Digital audio workstation",
            "parent": "audio-music",
            "help": "Ardour is a hard disk recorder and digital audio workstation application.",
        },
        {
            "id": "lmms",
            "label": "LMMS",
            "description": "Music production",
            "parent": "audio-music",
            "help": "LMMS is a digital audio workstation application program.",
        },
        {
            "id": "rhythmbox",
            "label": "Rhythmbox",
            "description": "Music player",
            "parent": "audio-music",
            "help": "Rhythmbox is a music playing application for GNOME.",
        },
    ]

    # Video & Streaming
    video_items = [
        {
            "id": "vlc",
            "label": "VLC Media Player",
            "description": "Multimedia player",
            "parent": "video-streaming",
            "default": True,
            "help": "VLC is a free and open-source, portable, cross-platform media player.",
        },
        {
            "id": "obs-studio",
            "label": "OBS Studio",
            "description": "Broadcasting software",
            "parent": "video-streaming",
            "help": "OBS Studio is a free and open-source software for video recording and live streaming.",
        },
        {
            "id": "kdenlive",
            "label": "Kdenlive",
            "description": "Video editor",
            "parent": "video-streaming",
            "help": "Kdenlive is a free and open-source video editing software.",
        },
        {
            "id": "mpv",
            "label": "MPV",
            "description": "Minimal media player",
            "parent": "video-streaming",
            "help": "MPV is a free and open-source media player software.",
        },
        {
            "id": "handbrake",
            "label": "HandBrake",
            "description": "Video transcoder",
            "parent": "video-streaming",
            "help": "HandBrake is a free and open-source transcoder for digital video files.",
        },
    ]

    # Productivity & Office
    productivity_items = [
        {
            "id": "libreoffice",
            "label": "LibreOffice",
            "description": "Office suite",
            "parent": "productivity-office",
            "default": True,
            "help": "LibreOffice is a free and open-source office productivity software suite.",
        },
        {
            "id": "thunderbird",
            "label": "Thunderbird",
            "description": "Email client",
            "parent": "productivity-office",
            "help": "Mozilla Thunderbird is a free and open-source email client.",
        },
        {
            "id": "evolution",
            "label": "Evolution",
            "description": "Groupware suite",
            "parent": "productivity-office",
            "help": "Evolution is the official personal information manager for GNOME.",
        },
        {
            "id": "onlyoffice",
            "label": "OnlyOffice",
            "description": "Office suite",
            "parent": "productivity-office",
            "help": "OnlyOffice is a free software office suite developed by Ascensio System SIA.",
        },
        {
            "id": "slack",
            "label": "Slack",
            "description": "Team collaboration",
            "parent": "productivity-office",
            "help": "Slack is a messaging app for business that connects people to the information they need.",
        },
        {
            "id": "teams",
            "label": "Microsoft Teams",
            "description": "Team collaboration",
            "parent": "productivity-office",
            "help": "Microsoft Teams is a unified communication and collaboration platform.",
        },
    ]

    # System Tools
    system_tools_items = [
        {
            "id": "gparted",
            "label": "GParted",
            "description": "Partition editor",
            "parent": "system-tools",
            "help": "GParted is a free partition editor for graphically managing disk partitions.",
        },
        {
            "id": "timeshift",
            "label": "Timeshift",
            "description": "System restore utility",
            "parent": "system-tools",
            "help": "Timeshift is a system restore tool for Linux.",
        },
        {
            "id": "bleachbit",
            "label": "BleachBit",
            "description": "System cleaner",
            "parent": "system-tools",
            "help": "BleachBit is a free and open-source disk space cleaner, privacy manager, and computer system optimizer.",
        },
        {
            "id": "stacer",
            "label": "Stacer",
            "description": "System optimizer",
            "parent": "system-tools",
            "help": "Stacer is an open source system optimizer and application monitor.",
        },
        {
            "id": "synaptic",
            "label": "Synaptic",
            "description": "Package manager GUI",
            "parent": "system-tools",
            "help": "Synaptic is a graphical package management tool based on APT.",
        },
    ]

    # File Management
    file_mgmt_items = [
        {
            "id": "double-commander",
            "label": "Double Commander",
            "description": "Dual-pane file manager",
            "parent": "file-management",
            "help": "Double Commander is a free cross-platform open source file manager with two panels.",
        },
        {
            "id": "midnight-commander",
            "label": "Midnight Commander",
            "description": "Terminal file manager",
            "parent": "file-management",
            "help": "GNU Midnight Commander is a free cross-platform orthodox file manager.",
        },
        {
            "id": "nemo",
            "label": "Nemo",
            "description": "File manager",
            "parent": "file-management",
            "help": "Nemo is a file manager for the Cinnamon desktop environment.",
        },
        {
            "id": "thunar",
            "label": "Thunar",
            "description": "File manager",
            "parent": "file-management",
            "help": "Thunar is a file manager for Linux and other Unix-like systems.",
        },
    ]

    # Combine all application items
    app_items = []
    app_items.extend(web_browser_items)
    app_items.extend(communication_items)
    app_items.extend(graphics_items)
    app_items.extend(editor_items)
    app_items.extend(audio_items)
    app_items.extend(video_items)
    app_items.extend(productivity_items)
    app_items.extend(system_tools_items)
    app_items.extend(file_mgmt_items)

    items.extend(app_items)

    # Update application category children references
    for cat_id, item_list in [
        ("web-browsers", web_browser_items),
        ("communication", communication_items),
        ("graphics-media", graphics_items),
        ("text-editors-ides", editor_items),
        ("audio-music", audio_items),
        ("video-streaming", video_items),
        ("productivity-office", productivity_items),
        ("system-tools", system_tools_items),
        ("file-management", file_mgmt_items),
    ]:
        cat = next((c for c in categories if c["id"] == cat_id), None)
        if cat:
            cat["children"] = [item["id"] for item in item_list]

    # Keep general applications empty for now
    app_cat = next(cat for cat in categories if cat["id"] == "applications")
    app_cat["children"] = []

    # Security items (simplified for now)
    security_items = [
        {
            "id": "ufw",
            "label": "UFW Firewall",
            "description": "Uncomplicated Firewall",
            "parent": "security",
            "default": True,
            "help": "UFW (Uncomplicated Firewall) is a frontend for iptables and is particularly well-suited for host-based firewalls.",
        },
        {
            "id": "fail2ban",
            "label": "Fail2Ban",
            "description": "Intrusion prevention",
            "parent": "security",
            "help": "Fail2Ban scans log files and bans IPs that show malicious signs.",
        },
    ]

    items.extend(security_items)
    security_cat = next(cat for cat in categories if cat["id"] == "security")
    security_cat["children"] = [item["id"] for item in security_items]

    # Security Testing subcategories
    security_testing_subcategories = [
        {
            "id": "network-security",
            "label": "Network Security",
            "description": "Network scanning and analysis tools",
            "icon": "🌐",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "web-security",
            "label": "Web Security",
            "description": "Web application security testing",
            "icon": "🕸️",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "password-tools",
            "label": "Password Tools",
            "description": "Password cracking and analysis",
            "icon": "🔑",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "wireless-security",
            "label": "Wireless Security",
            "description": "WiFi and wireless testing tools",
            "icon": "📡",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "forensics",
            "label": "Digital Forensics",
            "description": "Forensic analysis and recovery tools",
            "icon": "🔍",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "vulnerability-scanners",
            "label": "Vulnerability Scanners",
            "description": "System vulnerability assessment",
            "icon": "🛡️",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
        {
            "id": "privacy-tools",
            "label": "Privacy Tools",
            "description": "Privacy testing and anonymity tools",
            "icon": "🕵️",
            "is_category": True,
            "parent": "security-testing",
            "children": [],
        },
    ]

    items.extend(security_testing_subcategories)

    # Network Security Tools
    network_security_items = [
        {
            "id": "nmap",
            "label": "Nmap",
            "description": "Network scanner",
            "parent": "network-security",
            "help": """WARNING: Only use on networks you own or have explicit written permission to test.

Nmap ("Network Mapper") is a powerful network discovery and security auditing tool. It can determine what hosts are available on the network, what services those hosts are offering, what operating systems they are running, and dozens of other characteristics.

This will install:
- nmap - Command-line network scanner
- zenmap - GUI frontend for nmap
- ncat - Modern reimplementation of netcat
- ndiff - Utility for comparing nmap scan results

Common legal uses:
- Network inventory and asset management
- Security auditing of your own systems
- Monitoring service uptime
- Detecting unauthorized devices on your network""",
        },
        {
            "id": "wireshark",
            "label": "Wireshark",
            "description": "Packet analyzer",
            "parent": "network-security",
            "help": """WARNING: Only capture traffic on networks you own or have explicit permission to monitor.

Wireshark is the world's most popular network protocol analyzer. It lets you capture and interactively browse traffic running on a computer network.

This will install:
- wireshark - GUI packet analyzer
- tshark - Command-line packet analyzer
- wireshark-qt - Qt-based GUI (default)
- dumpcap - Network traffic capture tool

Configuration:
- Adds user to wireshark group for non-root packet capture
- Sets up proper permissions for network interfaces
- Configures default capture filters

Legal uses:
- Troubleshooting network problems
- Examining security problems on your own network
- Debugging protocol implementations
- Learning network protocol internals""",
        },
        {
            "id": "tcpdump",
            "label": "tcpdump",
            "description": "Command-line packet analyzer",
            "parent": "network-security",
            "help": "WARNING: Only use on networks you own or have permission to monitor. tcpdump is a powerful command-line packet analyzer.",
        },
        {
            "id": "netcat",
            "label": "Netcat",
            "description": "Network utility",
            "parent": "network-security",
            "help": "Netcat is a versatile networking utility for reading/writing network connections. Use only on authorized systems.",
        },
        {
            "id": "masscan",
            "label": "Masscan",
            "description": "Fast port scanner",
            "parent": "network-security",
            "help": "WARNING: Only scan networks you own or have permission to test. Masscan is an extremely fast port scanner.",
        },
    ]

    # Web Security Tools
    web_security_items = [
        {
            "id": "burp-suite",
            "label": "Burp Suite Community",
            "description": "Web vulnerability scanner",
            "parent": "web-security",
            "help": """WARNING: Only test web applications you own or have written permission to test.

Burp Suite is an integrated platform for performing security testing of web applications. The Community Edition provides essential manual tools for web security testing.

This will install:
- Burp Suite Community Edition
- Java runtime (required dependency)
- Desktop launcher and menu entry

Features included:
- Proxy for intercepting HTTP/S traffic
- Repeater for manipulating and resending requests
- Sequencer for testing token randomness
- Decoder for encoding/decoding data
- Comparer for comparing responses

Legal uses:
- Testing your own web applications
- Security assessments with client permission
- Web development debugging
- Learning web security concepts""",
        },
        {
            "id": "owasp-zap",
            "label": "OWASP ZAP",
            "description": "Web app security scanner",
            "parent": "web-security",
            "help": "WARNING: Only test applications you own or have permission to test. OWASP ZAP is a free web application security scanner.",
        },
        {
            "id": "sqlmap",
            "label": "SQLMap",
            "description": "SQL injection tool",
            "parent": "web-security",
            "help": "WARNING: Only use on applications you own or have explicit permission to test. SQLMap automates SQL injection detection and exploitation.",
        },
        {
            "id": "nikto",
            "label": "Nikto",
            "description": "Web server scanner",
            "parent": "web-security",
            "help": "WARNING: Only scan servers you own or have permission to test. Nikto is a web server vulnerability scanner.",
        },
        {
            "id": "dirbuster",
            "label": "DirBuster",
            "description": "Directory/file brute forcer",
            "parent": "web-security",
            "help": "WARNING: Only use on web servers you own or have permission to test. DirBuster brute forces directories and files on web servers.",
        },
    ]

    # Password Tools
    password_tools_items = [
        {
            "id": "john",
            "label": "John the Ripper",
            "description": "Password cracker",
            "parent": "password-tools",
            "help": """WARNING: Only use on password hashes you own or have explicit authorization to test.

John the Ripper is a fast password cracker designed to detect weak Unix passwords. It supports hundreds of hash and cipher types.

This will install:
- john - Main password cracking tool
- john-data - Password lists and rules
- unique - Remove duplicates from wordlists
- unshadow - Combine passwd and shadow files

Legal uses:
- Testing password strength in your organization
- Recovering your own forgotten passwords
- Security audits with proper authorization
- Password policy compliance testing""",
        },
        {
            "id": "hashcat",
            "label": "Hashcat",
            "description": "Advanced password recovery",
            "parent": "password-tools",
            "help": "WARNING: Only use on hashes you own or have authorization to crack. Hashcat is an advanced CPU/GPU-based password recovery utility.",
        },
        {
            "id": "hydra",
            "label": "Hydra",
            "description": "Network login cracker",
            "parent": "password-tools",
            "help": "WARNING: Only use on systems you own or have explicit permission to test. Hydra is a parallelized network login cracker.",
        },
        {
            "id": "crackmap-exec",
            "label": "CrackMapExec",
            "description": "Network authentication testing",
            "parent": "password-tools",
            "help": "WARNING: Only use on networks you own or have permission to test. CrackMapExec is a post-exploitation tool for testing network authentication.",
        },
    ]

    # Wireless Security Tools
    wireless_security_items = [
        {
            "id": "aircrack-ng",
            "label": "Aircrack-ng",
            "description": "WiFi security auditing",
            "parent": "wireless-security",
            "help": "WARNING: Only test networks you own or have explicit permission to audit. Aircrack-ng is a WiFi security auditing tool suite.",
        },
        {
            "id": "kismet",
            "label": "Kismet",
            "description": "Wireless network detector",
            "parent": "wireless-security",
            "help": "WARNING: Check local laws before using. Kismet is a wireless network and device detector, sniffer, and intrusion detection system.",
        },
        {
            "id": "reaver",
            "label": "Reaver",
            "description": "WPS attack tool",
            "parent": "wireless-security",
            "help": "WARNING: Only use on your own networks. Reaver performs brute force attacks against WiFi Protected Setup (WPS).",
        },
        {
            "id": "wifite",
            "label": "Wifite",
            "description": "Automated wireless auditor",
            "parent": "wireless-security",
            "help": "WARNING: Only audit networks you own. Wifite is an automated wireless attack tool.",
        },
    ]

    # Forensics Tools
    forensics_items = [
        {
            "id": "autopsy",
            "label": "Autopsy",
            "description": "Digital forensics platform",
            "parent": "forensics",
            "help": "Autopsy is a graphical interface to The Sleuth Kit and other digital forensics tools. Use only on systems you have legal authority to examine.",
        },
        {
            "id": "volatility",
            "label": "Volatility",
            "description": "Memory forensics framework",
            "parent": "forensics",
            "help": "Volatility is an advanced memory forensics framework. Use only on memory dumps you have authorization to analyze.",
        },
        {
            "id": "foremost",
            "label": "Foremost",
            "description": "File recovery tool",
            "parent": "forensics",
            "help": "Foremost is a forensic tool for recovering files based on headers and footers. Use only on drives you own or have permission to analyze.",
        },
        {
            "id": "binwalk",
            "label": "Binwalk",
            "description": "Firmware analysis tool",
            "parent": "forensics",
            "help": "Binwalk is a tool for analyzing and extracting firmware images. Use only on firmware you have rights to examine.",
        },
    ]

    # Vulnerability Scanners
    vuln_scanner_items = [
        {
            "id": "openvas",
            "label": "OpenVAS",
            "description": "Vulnerability assessment",
            "parent": "vulnerability-scanners",
            "help": "WARNING: Only scan systems you own or have permission to test. OpenVAS is a full-featured vulnerability assessment tool.",
        },
        {
            "id": "lynis",
            "label": "Lynis",
            "description": "Security auditing tool",
            "parent": "vulnerability-scanners",
            "help": "Lynis is a security auditing tool for Unix-based systems. Use on your own systems or with proper authorization.",
        },
        {
            "id": "chkrootkit",
            "label": "chkrootkit",
            "description": "Rootkit scanner",
            "parent": "vulnerability-scanners",
            "help": "chkrootkit is a tool to locally check for signs of a rootkit. Run on your own systems for security monitoring.",
        },
        {
            "id": "rkhunter",
            "label": "rkhunter",
            "description": "Rootkit hunter",
            "parent": "vulnerability-scanners",
            "help": "Rootkit Hunter scans for rootkits, backdoors and possible local exploits. Use for security monitoring of your own systems.",
        },
    ]

    # Combine all security testing items
    security_testing_items = []
    security_testing_items.extend(network_security_items)
    security_testing_items.extend(web_security_items)
    security_testing_items.extend(password_tools_items)
    security_testing_items.extend(wireless_security_items)
    security_testing_items.extend(forensics_items)
    security_testing_items.extend(vuln_scanner_items)

    # Privacy Tools items
    privacy_tools_items = [
        {
            "id": "tor-browser",
            "label": "Tor Browser",
            "description": "Anonymous web browsing",
            "parent": "privacy-tools",
            "help": """Tor Browser provides anonymous web browsing.
Features:
- Routes traffic through Tor network
- Blocks trackers
- Resists fingerprinting
- Multi-layered encryption
Note: For maximum anonymity, use Tails OS.""",
        },
        {
            "id": "tails-installer",
            "label": "Tails Installer",
            "description": "Create Tails live USB",
            "parent": "privacy-tools",
            "help": "Tails (The Amnesic Incognito Live System) installer for creating anonymous live USB systems.",
        },
        {
            "id": "onionshare",
            "label": "OnionShare",
            "description": "Anonymous file sharing",
            "parent": "privacy-tools",
            "help": "OnionShare lets you securely and anonymously share files using Tor.",
        },
        {
            "id": "mat2",
            "label": "MAT2",
            "description": "Metadata removal tool",
            "parent": "privacy-tools",
            "help": """Metadata Anonymisation Toolkit 2 removes metadata from files.
Supports:
- Images (JPEG, PNG, etc.)
- Office documents
- PDFs
- Audio/Video files
- Archives""",
        },
        {
            "id": "bleachbit",
            "label": "BleachBit",
            "description": "System cleaner",
            "parent": "privacy-tools",
            "help": "BleachBit cleans files to free disk space and maintain privacy.",
        },
        {
            "id": "proxychains",
            "label": "ProxyChains",
            "description": "Force apps through proxy",
            "parent": "privacy-tools",
            "help": "ProxyChains forces any TCP connection through SOCKS4, SOCKS5 or HTTP proxies.",
        },
        {
            "id": "anonsurf",
            "label": "AnonSurf",
            "description": "System-wide anonymization",
            "parent": "privacy-tools",
            "help": "AnonSurf routes all system traffic through Tor network.",
        },
        {
            "id": "kloak",
            "label": "kloak",
            "description": "Keystroke anonymization",
            "parent": "privacy-tools",
            "help": "kloak obfuscates typing patterns to prevent keystroke fingerprinting.",
        },
    ]

    security_testing_items.extend(privacy_tools_items)

    items.extend(security_testing_items)

    # Update security testing category children
    security_testing_cat = next(cat for cat in categories if cat["id"] == "security-testing")
    security_testing_cat["children"] = [item["id"] for item in security_testing_subcategories]

    # Update subcategory children
    for subcat_id, item_list in [
        ("network-security", network_security_items),
        ("web-security", web_security_items),
        ("password-tools", password_tools_items),
        ("wireless-security", wireless_security_items),
        ("forensics", forensics_items),
        ("vulnerability-scanners", vuln_scanner_items),
        ("privacy-tools", privacy_tools_items),
    ]:
        subcat = next((c for c in security_testing_subcategories if c["id"] == subcat_id), None)
        if subcat:
            subcat["children"] = [item["id"] for item in item_list]

    # Themes & Appearance
    theme_subcategories = [
        {
            "id": "theme-universal",
            "label": "Universal Themes",
            "description": "Themes that work across multiple applications",
            "icon": "🎨",
            "is_category": True,
            "parent": "themes",
            "children": [],
        },
        {
            "id": "theme-settings",
            "label": "Theme Settings",
            "description": "Configure theme behavior and preferences",
            "icon": "⚙️",
            "is_category": True,
            "parent": "themes",
            "children": [],
        },
        {
            "id": "theme-custom",
            "label": "Custom Colors",
            "description": "Create your own color scheme",
            "icon": "🎯",
            "is_category": True,
            "parent": "themes",
            "children": [],
        },
    ]

    items.extend(theme_subcategories)

    # Universal theme items
    universal_theme_items = [
        {
            "id": "theme-dracula",
            "label": "Dracula",
            "description": "Dark theme with vibrant colors",
            "parent": "theme-universal",
            "help": "A dark theme with bold contrast and vibrant colors that reduces eye strain. Available for 300+ apps including terminals, VS Code, Firefox, Chrome, and more.",
        },
        {
            "id": "theme-catppuccin-mocha",
            "label": "Catppuccin Mocha",
            "description": "Soothing pastel dark theme",
            "parent": "theme-universal",
            "help": "A warm, dark theme with soothing pastel colors. Part of the Catppuccin family with consistent colors across all applications.",
        },
        {
            "id": "theme-catppuccin-macchiato",
            "label": "Catppuccin Macchiato",
            "description": "Mid-tone pastel theme",
            "parent": "theme-universal",
            "help": "A medium-dark theme with gentle pastel colors. Slightly lighter than Mocha but still easy on the eyes.",
        },
        {
            "id": "theme-catppuccin-frappe",
            "label": "Catppuccin Frappé",
            "description": "Cool-toned pastel dark theme",
            "parent": "theme-universal",
            "help": "A cool, muted dark theme with soft pastel colors. Perfect for long coding sessions.",
        },
        {
            "id": "theme-catppuccin-latte",
            "label": "Catppuccin Latte",
            "description": "Light pastel theme",
            "parent": "theme-universal",
            "help": "A light theme with warm pastel colors. The only light variant in the Catppuccin family.",
        },
        {
            "id": "theme-tokyo-night",
            "label": "Tokyo Night",
            "description": "Tokyo at night inspired theme",
            "parent": "theme-universal",
            "help": "A clean, dark theme celebrating the lights of Downtown Tokyo at night. Features deep blues and purples with excellent contrast.",
        },
        {
            "id": "theme-tokyo-night-storm",
            "label": "Tokyo Night Storm",
            "description": "Darker variant of Tokyo Night",
            "parent": "theme-universal",
            "help": "A darker, more muted variant of Tokyo Night with stormy blue-gray tones.",
        },
        {
            "id": "theme-tokyo-night-light",
            "label": "Tokyo Night Light",
            "description": "Light variant of Tokyo Night",
            "parent": "theme-universal",
            "help": "A light theme variant of Tokyo Night with soft pastels and excellent readability.",
        },
        {
            "id": "theme-nord",
            "label": "Nord",
            "description": "Arctic, north-bluish theme",
            "parent": "theme-universal",
            "help": "An arctic, north-bluish clean and elegant theme. Features a carefully selected color palette inspired by the Arctic.",
        },
        {
            "id": "theme-gruvbox-dark",
            "label": "Gruvbox Dark",
            "description": "Retro groove dark theme",
            "parent": "theme-universal",
            "help": "A retro groove color scheme with warm colors and vintage feel. Designed to be easy on the eyes.",
        },
        {
            "id": "theme-gruvbox-light",
            "label": "Gruvbox Light",
            "description": "Retro groove light theme",
            "parent": "theme-universal",
            "help": "The light variant of Gruvbox with the same retro feel but optimized for bright environments.",
        },
        {
            "id": "theme-one-dark",
            "label": "One Dark",
            "description": "Atom-inspired dark theme",
            "parent": "theme-universal",
            "help": "A dark theme inspired by Atom One Dark. Features vibrant colors with excellent syntax highlighting.",
        },
        {
            "id": "theme-solarized-dark",
            "label": "Solarized Dark",
            "description": "Precision dark color scheme",
            "parent": "theme-universal",
            "help": "A precision color scheme for accurate color reproduction. Developed with both RGB and LAB color models.",
        },
        {
            "id": "theme-solarized-light",
            "label": "Solarized Light",
            "description": "Precision light color scheme",
            "parent": "theme-universal",
            "help": "The light variant of Solarized with the same precise color values optimized for light backgrounds.",
        },
        {
            "id": "theme-monokai",
            "label": "Monokai",
            "description": "Vibrant, high-contrast theme",
            "parent": "theme-universal",
            "help": "A vibrant, high-contrast theme originally created for TextMate. Popular for its colorful syntax highlighting.",
        },
        {
            "id": "theme-material",
            "label": "Material",
            "description": "Google Material Design theme",
            "parent": "theme-universal",
            "help": "Based on Google Material Design principles with rich colors and smooth gradients.",
        },
        {
            "id": "theme-ayu-dark",
            "label": "Ayu Dark",
            "description": "Simple theme with bright colors",
            "parent": "theme-universal",
            "help": "A simple theme with bright colors and comes in three versions: dark, mirage, and light.",
        },
        {
            "id": "theme-everforest",
            "label": "Everforest",
            "description": "Green-based comfortable theme",
            "parent": "theme-universal",
            "help": "A green based color scheme designed to be warm and soft, inspired by the evergreen forest.",
        },
    ]

    # Theme settings
    theme_setting_items = [
        {
            "id": "theme-auto-switch",
            "label": "Auto Theme Switch",
            "description": "Switch theme based on time",
            "parent": "theme-settings",
            "help": "Automatically switch between light and dark themes based on time of day or system settings.",
        },
        {
            "id": "theme-sync-apps",
            "label": "Sync Across Apps",
            "description": "Apply theme to all supported apps",
            "parent": "theme-settings",
            "default": True,
            "help": "When changing theme, automatically apply it to all supported applications.",
        },
        {
            "id": "theme-terminal-opacity",
            "label": "Terminal Background Opacity",
            "description": "Terminal transparency level",
            "parent": "theme-settings",
            "is_configurable": True,
            "config_type": "slider",
            "min_value": 0,
            "max_value": 100,
            "default_value": 90,
            "unit": "%",
            "help": "Set the opacity of terminal backgrounds. 100% is fully opaque, 0% is fully transparent.",
        },
        {
            "id": "theme-ui-scale",
            "label": "UI Scale Factor",
            "description": "Scale UI elements",
            "parent": "theme-settings",
            "is_configurable": True,
            "config_type": "select",
            "options": ["0.75", "0.90", "1.00", "1.10", "1.25", "1.50", "2.00"],
            "default_value": "1.00",
            "help": "Scale all UI elements for better visibility on high-DPI displays.",
        },
    ]

    # Custom color settings
    custom_color_items = [
        {
            "id": "custom-background",
            "label": "Background Color",
            "description": "Main background color",
            "parent": "theme-custom",
            "is_configurable": True,
            "config_type": "color",
            "default_value": "#1e1e2e",
            "help": "Set the main background color for your custom theme.",
        },
        {
            "id": "custom-foreground",
            "label": "Foreground Color",
            "description": "Main text color",
            "parent": "theme-custom",
            "is_configurable": True,
            "config_type": "color",
            "default_value": "#cdd6f4",
            "help": "Set the main text/foreground color for your custom theme.",
        },
        {
            "id": "custom-accent",
            "label": "Accent Color",
            "description": "Highlight/accent color",
            "parent": "theme-custom",
            "is_configurable": True,
            "config_type": "color",
            "default_value": "#89b4fa",
            "help": "Set the accent color used for highlights and important UI elements.",
        },
    ]

    items.extend(universal_theme_items)
    items.extend(theme_setting_items)
    items.extend(custom_color_items)

    # Update themes category children
    themes_cat = next(cat for cat in categories if cat["id"] == "themes")
    themes_cat["children"] = ["theme-universal", "theme-settings", "theme-custom"]

    # Update subcategory children
    for subcat in theme_subcategories:
        if subcat["id"] == "theme-universal":
            subcat["children"] = [item["id"] for item in universal_theme_items]
        elif subcat["id"] == "theme-settings":
            subcat["children"] = [item["id"] for item in theme_setting_items]
        elif subcat["id"] == "theme-custom":
            subcat["children"] = [item["id"] for item in custom_color_items]

    # System items (simplified for now)
    system_items = [
        {
            "id": "boot-diagnostics",
            "label": "Boot Diagnostics & Error Visibility",
            "description": "Show boot errors and system health checks",
            "parent": "system",
            "default": False,
            "ansible_var": "enable_boot_diagnostics",
            "help": """Enable boot diagnostics and error visibility tools.
This will:
- Add option to disable Plymouth splash screen for troubleshooting
- Configure GRUB to show boot messages when needed
- Create system health check scripts that run after boot
- Install boot error reporting tools
- Monitor for hardware failures (storage, graphics, etc.)
- Track boot performance over time
- Create diagnostic boot menu entry in GRUB

Useful for:
- Troubleshooting boot problems
- Detecting failing hardware early
- Monitoring system health
- Optimizing boot performance

Access tools with:
- boot-report: Generate comprehensive diagnostic report
- boot-errors: Quick view of recent boot errors
- systemd-analyze: Check boot performance""",
        },
        {
            "id": "swappiness",
            "label": "Swappiness",
            "description": "VM swappiness (0-100)",
            "parent": "system",
            "is_configurable": True,
            "default_value": 10,
            "help": "Swappiness controls how aggressively the kernel swaps memory pages. Lower values keep more data in RAM.",
        },
        {
            "id": "enable-trim",
            "label": "Enable SSD TRIM",
            "description": "Weekly TRIM for SSDs",
            "parent": "system",
            "default": True,
            "help": "Enable weekly TRIM operations for SSD drives to maintain performance.",
        },
    ]

    items.extend(system_items)
    system_cat = next(cat for cat in categories if cat["id"] == "system")
    system_cat["children"] = [item["id"] for item in system_items]

    # Gaming items
    gaming_items = [
        {
            "id": "steam",
            "label": "Steam",
            "description": "Digital distribution platform for games",
            "parent": "gaming",
            "help": """Steam is Valve's digital distribution platform for PC gaming.
This will install:
- Steam client (latest version)
- 32-bit libraries required for Steam
- Steam runtime dependencies
- Vulkan drivers for better game performance
Features:
- Access to thousands of games
- Cloud saves
- Steam Workshop for mods
- Steam Play/Proton for Windows game compatibility
- In-home streaming
- Big Picture mode for TV gaming
System integration:
- Desktop shortcut created
- Steam protocol handler registered
- Automatic updates enabled
Note: First launch will download additional Steam runtime components.""",
        },
        {
            "id": "lutris",
            "label": "Lutris",
            "description": "Open gaming platform for Linux",
            "parent": "gaming",
            "help": """Lutris is an open-source gaming platform that makes gaming on Linux easier.
Installs:
- Lutris client
- Wine dependencies
- Common game runtime libraries
Features:
- Install games from GOG, Steam, Battle.net, Origin, Uplay
- Automated installer scripts for games
- Wine/Proton management
- Emulator support
- Game library management""",
        },
        {
            "id": "wine",
            "label": "Wine",
            "description": "Windows compatibility layer",
            "parent": "gaming",
            "help": """Wine allows you to run Windows applications on Linux.
Installs:
- Wine stable (latest version)
- Wine32 and Wine64 libraries
- Winetricks for easy configuration
- Common Windows fonts
- Mono and Gecko for .NET/IE compatibility""",
        },
        {
            "id": "playonlinux",
            "label": "PlayOnLinux",
            "description": "Graphical frontend for Wine",
            "parent": "gaming",
            "help": "PlayOnLinux simplifies Wine configuration for games and applications with automated scripts.",
        },
        {
            "id": "gamemode",
            "label": "GameMode",
            "description": "Optimize system performance for gaming",
            "parent": "gaming",
            "default": True,
            "help": """GameMode automatically optimizes your system for gaming performance.
Features:
- CPU governor set to performance mode
- I/O priority adjustments
- GPU performance mode
- Screensaver inhibition
- Custom game-specific optimizations
Automatically activated by supported games.""",
        },
        {
            "id": "mangohud",
            "label": "MangoHud",
            "description": "Vulkan/OpenGL overlay for monitoring",
            "parent": "gaming",
            "help": "MangoHud provides an overlay showing FPS, temperatures, CPU/GPU load while gaming.",
        },
        {
            "id": "discord",
            "label": "Discord",
            "description": "Voice and text chat for gamers",
            "parent": "gaming",
            "help": "Discord is a popular communication platform for gaming communities.",
        },
        {
            "id": "obs-studio",
            "label": "OBS Studio",
            "description": "Streaming and recording software",
            "parent": "gaming",
            "help": """OBS Studio for game streaming and recording.
Features:
- High performance real-time video/audio capturing
- Scene composition
- Twitch/YouTube streaming support
- GPU encoding support""",
        },
    ]

    items.extend(gaming_items)
    gaming_cat = next(cat for cat in categories if cat["id"] == "gaming")
    gaming_cat["children"] = [item["id"] for item in gaming_items]

    # Multimedia Production items
    multimedia_items = [
        {
            "id": "blender",
            "label": "Blender",
            "description": "3D creation suite",
            "parent": "multimedia",
            "help": """Blender is a professional, free and open-source 3D creation suite.
Features:
- 3D modeling, sculpting, and texturing
- Animation and rigging
- Video editing and compositing
- Game engine
- Python scripting
- GPU rendering support (CUDA/OpenCL)""",
        },
        {
            "id": "kdenlive",
            "label": "Kdenlive",
            "description": "Video editor",
            "parent": "multimedia",
            "help": """Kdenlive is a powerful non-linear video editor.
Features:
- Multi-track editing
- Wide format support
- Effects and transitions
- Proxy editing for 4K
- Hardware acceleration""",
        },
        {
            "id": "davinci-resolve",
            "label": "DaVinci Resolve",
            "description": "Professional video editor and color grading",
            "parent": "multimedia",
            "help": """DaVinci Resolve is a professional video editing and color grading application.
Note: This installs the free version. Requires manual download acceptance.
Features:
- Professional editing tools
- Industry-leading color correction
- Fusion visual effects
- Fairlight audio post-production""",
        },
        {
            "id": "obs-studio-multimedia",
            "label": "OBS Studio",
            "description": "Broadcasting and recording",
            "parent": "multimedia",
            "help": "Open Broadcaster Software for live streaming and recording.",
        },
        {
            "id": "openshot",
            "label": "OpenShot",
            "description": "Simple video editor",
            "parent": "multimedia",
            "help": "OpenShot is an easy-to-use, quick to learn, and powerful video editor.",
        },
        {
            "id": "natron",
            "label": "Natron",
            "description": "Compositing software",
            "parent": "multimedia",
            "help": "Natron is an open-source compositing software for visual effects and motion graphics.",
        },
        {
            "id": "olive",
            "label": "Olive",
            "description": "Non-linear video editor",
            "parent": "multimedia",
            "help": "Olive is a free non-linear video editor aiming for professional features.",
        },
        {
            "id": "pitivi",
            "label": "Pitivi",
            "description": "Video editor for Linux",
            "parent": "multimedia",
            "help": "Pitivi is a video editor designed to be intuitive and integrate well with GNOME.",
        },
    ]

    items.extend(multimedia_items)
    multimedia_cat = next(cat for cat in categories if cat["id"] == "multimedia")
    multimedia_cat["children"] = [item["id"] for item in multimedia_items]

    # Networking items
    networking_items = [
        {
            "id": "wireshark",
            "label": "Wireshark",
            "description": "Network protocol analyzer",
            "parent": "networking",
            "help": """Wireshark is the world's foremost network protocol analyzer.
Features:
- Deep inspection of hundreds of protocols
- Live capture and offline analysis
- Rich VoIP analysis
- Decryption support for many protocols
Note: Adds user to wireshark group for capture permissions.""",
        },
        {
            "id": "nmap",
            "label": "Nmap",
            "description": "Network discovery and security auditing",
            "parent": "networking",
            "help": "Network exploration tool and security/port scanner.",
        },
        {
            "id": "netcat",
            "label": "Netcat",
            "description": "TCP/IP swiss army knife",
            "parent": "networking",
            "help": "Netcat - networking utility for reading/writing network connections.",
        },
        {
            "id": "iftop",
            "label": "iftop",
            "description": "Display bandwidth usage",
            "parent": "networking",
            "help": "iftop displays bandwidth usage on an interface by host.",
        },
        {
            "id": "vnstat",
            "label": "vnStat",
            "description": "Network traffic monitor",
            "parent": "networking",
            "help": "vnStat is a network traffic monitor that keeps a log of network traffic.",
        },
        {
            "id": "nethogs",
            "label": "NetHogs",
            "description": "Per-process bandwidth monitor",
            "parent": "networking",
            "help": "NetHogs groups bandwidth by process instead of by IP or interface.",
        },
        {
            "id": "mtr",
            "label": "MTR",
            "description": "Network diagnostic tool",
            "parent": "networking",
            "help": "MTR combines ping and traceroute functionality in a single tool.",
        },
        {
            "id": "tcpdump",
            "label": "tcpdump",
            "description": "Command-line packet analyzer",
            "parent": "networking",
            "help": "tcpdump is a powerful command-line packet analyzer.",
        },
        {
            "id": "ethtool",
            "label": "ethtool",
            "description": "Ethernet device settings",
            "parent": "networking",
            "help": "ethtool is used to query and control network device driver settings.",
        },
        {
            "id": "iperf3",
            "label": "iPerf3",
            "description": "Network bandwidth testing",
            "parent": "networking",
            "help": "iPerf3 is a tool for active measurements of network bandwidth.",
        },
    ]

    items.extend(networking_items)
    networking_cat = next(cat for cat in categories if cat["id"] == "networking")
    networking_cat["children"] = [item["id"] for item in networking_items]

    # Virtualization items
    virtualization_items = [
        {
            "id": "virtualbox",
            "label": "VirtualBox",
            "description": "Full virtualization solution",
            "parent": "virtualization",
            "help": """Oracle VM VirtualBox is a powerful virtualization product.
Installs:
- VirtualBox application
- VirtualBox kernel modules
- VirtualBox Extension Pack
- Guest additions ISO
Features:
- Run multiple operating systems
- Snapshots and cloning
- Shared folders and clipboard
- USB device support
- Network configuration options""",
        },
        {
            "id": "virt-manager",
            "label": "Virt-Manager",
            "description": "QEMU/KVM virtualization manager",
            "parent": "virtualization",
            "help": """Virtual Machine Manager for QEMU/KVM.
Installs:
- virt-manager GUI
- libvirt daemon
- QEMU/KVM
- Virtual network configuration
Features:
- Native virtualization performance
- Live migration
- Storage pools
- Network management""",
        },
        {
            "id": "gnome-boxes",
            "label": "GNOME Boxes",
            "description": "Simple virtualization for GNOME",
            "parent": "virtualization",
            "help": "GNOME Boxes provides a simple interface for virtualization.",
        },
        {
            "id": "vagrant",
            "label": "Vagrant",
            "description": "Development environment automation",
            "parent": "virtualization",
            "help": """Vagrant automates development environment setup.
Features:
- Reproducible environments
- Provider abstraction (VirtualBox, VMware, etc.)
- Provisioning integration
- Multi-machine environments""",
        },
        {
            "id": "lxd",
            "label": "LXD",
            "description": "System container manager",
            "parent": "virtualization",
            "help": """LXD is a next generation system container manager.
Features:
- Fast, lightweight containers
- Image-based workflow
- Live migration
- REST API
- Storage and network management""",
        },
        {
            "id": "multipass",
            "label": "Multipass",
            "description": "Ubuntu VM manager",
            "parent": "virtualization",
            "help": "Multipass provides instant Ubuntu VMs with a single command.",
        },
        {
            "id": "vmware-workstation",
            "label": "VMware Workstation",
            "description": "Professional virtualization (requires license)",
            "parent": "virtualization",
            "help": "VMware Workstation Pro is a commercial virtualization solution. Requires separate license purchase.",
        },
    ]

    items.extend(virtualization_items)
    virtualization_cat = next(cat for cat in categories if cat["id"] == "virtualization")
    virtualization_cat["children"] = [item["id"] for item in virtualization_items]

    # Cloud Tools items
    cloud_tools_items = [
        {
            "id": "aws-cli",
            "label": "AWS CLI",
            "description": "Amazon Web Services command-line interface",
            "parent": "cloud-tools",
            "help": """AWS Command Line Interface for managing Amazon Web Services.
Features:
- Manage EC2, S3, Lambda, and all AWS services
- Multiple profile support
- Output formatting options
- Shell command completion""",
        },
        {
            "id": "azure-cli",
            "label": "Azure CLI",
            "description": "Microsoft Azure command-line interface",
            "parent": "cloud-tools",
            "help": """Azure CLI for managing Microsoft Azure resources.
Features:
- Cross-platform command-line experience
- Interactive mode with auto-completion
- JMESPath query support
- Multiple output formats""",
        },
        {
            "id": "gcloud",
            "label": "Google Cloud SDK",
            "description": "Google Cloud Platform CLI tools",
            "parent": "cloud-tools",
            "help": """Google Cloud SDK including gcloud, gsutil, and bq.
Components:
- gcloud - manage Google Cloud resources
- gsutil - Google Storage utilities
- bq - BigQuery command-line tool
- kubectl - Kubernetes control""",
        },
        {
            "id": "kubectl",
            "label": "kubectl",
            "description": "Kubernetes command-line tool",
            "parent": "cloud-tools",
            "help": "kubectl is the Kubernetes command-line tool for deploying and managing applications on Kubernetes.",
        },
        {
            "id": "helm",
            "label": "Helm",
            "description": "Kubernetes package manager",
            "parent": "cloud-tools",
            "help": "Helm is the package manager for Kubernetes, simplifying deployment of applications.",
        },
        {
            "id": "terraform",
            "label": "Terraform",
            "description": "Infrastructure as Code tool",
            "parent": "cloud-tools",
            "help": """Terraform enables infrastructure as code for any cloud.
Features:
- Declarative infrastructure
- Multi-cloud support
- State management
- Module ecosystem""",
        },
        {
            "id": "ansible-cloud",
            "label": "Ansible",
            "description": "Automation platform",
            "parent": "cloud-tools",
            "help": "Ansible automates cloud provisioning, configuration management, and application deployment.",
        },
        {
            "id": "doctl",
            "label": "doctl",
            "description": "DigitalOcean command-line tool",
            "parent": "cloud-tools",
            "help": "doctl is the official DigitalOcean command-line client.",
        },
        {
            "id": "linode-cli",
            "label": "Linode CLI",
            "description": "Linode command-line interface",
            "parent": "cloud-tools",
            "help": "Linode CLI for managing Linode cloud resources.",
        },
    ]

    items.extend(cloud_tools_items)
    cloud_tools_cat = next(cat for cat in categories if cat["id"] == "cloud-tools")
    cloud_tools_cat["children"] = [item["id"] for item in cloud_tools_items]

    # Application Customization items
    customization_items = [
        {
            "id": "gnome-tweaks",
            "label": "GNOME Tweaks",
            "description": "Advanced GNOME settings",
            "parent": "customization",
            "help": "GNOME Tweaks provides additional configuration options for the GNOME desktop.",
        },
        {
            "id": "dconf-editor",
            "label": "dconf Editor",
            "description": "Low-level GNOME configuration",
            "parent": "customization",
            "help": "dconf Editor provides direct access to GNOME configuration database.",
        },
        {
            "id": "dotfiles-manager",
            "label": "GNU Stow",
            "description": "Dotfiles symlink manager",
            "parent": "customization",
            "help": """GNU Stow manages dotfiles through symlinks.
Features:
- Organize dotfiles in packages
- Easy installation/removal
- Version control friendly
- No configuration needed""",
        },
        {
            "id": "yadm",
            "label": "YADM",
            "description": "Yet Another Dotfiles Manager",
            "parent": "customization",
            "help": "YADM is a dotfile manager that leverages Git with additional features for dotfile management.",
        },
        {
            "id": "chezmoi",
            "label": "chezmoi",
            "description": "Manage dotfiles across machines",
            "parent": "customization",
            "help": """chezmoi manages your dotfiles securely across multiple machines.
Features:
- Template support
- Password manager integration
- Machine-specific configuration
- Encryption support""",
        },
        {
            "id": "conky",
            "label": "Conky",
            "description": "System monitor for desktop",
            "parent": "customization",
            "help": "Conky is a highly configurable system monitor that displays information on your desktop.",
        },
        {
            "id": "plank",
            "label": "Plank",
            "description": "Simple dock",
            "parent": "customization",
            "help": "Plank is a simple, clean dock for Linux desktops.",
        },
        {
            "id": "ulauncher",
            "label": "Ulauncher",
            "description": "Application launcher",
            "parent": "customization",
            "help": "Ulauncher is a fast application launcher with extension support.",
        },
        {
            "id": "albert",
            "label": "Albert",
            "description": "Desktop agnostic launcher",
            "parent": "customization",
            "help": "Albert is a desktop agnostic launcher inspired by Alfred.",
        },
    ]

    items.extend(customization_items)
    customization_cat = next(cat for cat in categories if cat["id"] == "customization")
    customization_cat["children"] = [item["id"] for item in customization_items]

    # General Applications items (miscellaneous)
    general_app_items = [
        {
            "id": "caffeine",
            "label": "Caffeine",
            "description": "Prevent screen sleep",
            "parent": "applications",
            "help": "Caffeine prevents your screen from going to sleep.",
        },
        {
            "id": "redshift",
            "label": "Redshift",
            "description": "Blue light filter",
            "parent": "applications",
            "help": "Redshift adjusts screen color temperature based on time of day to reduce eye strain.",
        },
        {
            "id": "copyq",
            "label": "CopyQ",
            "description": "Clipboard manager",
            "parent": "applications",
            "help": "CopyQ is an advanced clipboard manager with searchable history.",
        },
        {
            "id": "flameshot",
            "label": "Flameshot",
            "description": "Screenshot tool",
            "parent": "applications",
            "help": "Powerful screenshot software with annotation features.",
        },
        {
            "id": "peek",
            "label": "Peek",
            "description": "GIF recorder",
            "parent": "applications",
            "help": "Simple animated GIF screen recorder.",
        },
        {
            "id": "etcher",
            "label": "balenaEtcher",
            "description": "USB/SD card writer",
            "parent": "applications",
            "help": "Flash OS images to SD cards and USB drives safely and easily.",
        },
        {
            "id": "ventoy",
            "label": "Ventoy",
            "description": "Bootable USB creator",
            "parent": "applications",
            "help": "Create bootable USB drive for multiple ISO files.",
        },
        {
            "id": "gparted",
            "label": "GParted",
            "description": "Partition editor",
            "parent": "applications",
            "help": "GNOME Partition Editor for managing disk partitions.",
        },
        {
            "id": "timeshift",
            "label": "Timeshift",
            "description": "System backup tool",
            "parent": "applications",
            "default": True,
            "help": """Timeshift creates filesystem snapshots for system restore.
Features:
- BTRFS/RSYNC snapshot support
- Scheduled snapshots
- Boot from snapshot
- Easy restoration""",
        },
    ]

    items.extend(general_app_items)
    applications_cat = next(cat for cat in categories if cat["id"] == "applications")
    applications_cat["children"] = [item["id"] for item in general_app_items]

    # Fill in empty categories
    for cat in categories:
        if not cat.get("children"):
            cat["children"] = []

    return items
