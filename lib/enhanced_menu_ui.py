#!/usr/bin/env python3
"""
Enhanced Professional menu UI system for Ubootu with full hierarchical navigation
Version 2: With improved indicators, help system, emojis, and smart font menu
"""

import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from rich import box
    from rich.align import Align
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("ERROR: Rich library not found. Please install with: sudo apt install python3-rich")
    sys.exit(1)


# Help descriptions for all items
HELP_DESCRIPTIONS = {
    # Development IDEs
    "vscode": """Visual Studio Code is Microsoft's free, open-source code editor with excellent 
language support, debugging, Git integration, and a vast extension ecosystem.
Perfect for web development, Python, C++, and more. Installs via Snap.""",
    "intellij-idea": """IntelliJ IDEA Community Edition is JetBrains' powerful Java IDE with 
smart code completion, refactoring tools, and built-in version control.
Essential for Java/Kotlin development. Installs via Snap.""",
    "pycharm": """PyCharm Community Edition is the best Python IDE with intelligent code 
completion, debugging, testing, and virtual environment management.
Ideal for Django, Flask, scientific computing. Installs via Snap.""",
    # Languages
    "python": """Python 3 runtime with pip package manager. The most popular language for 
scripting, web development, data science, and automation. 
Includes Python 3.x and pip3. Essential for most developers.""",
    "nodejs": """Node.js JavaScript runtime built on Chrome's V8 engine. Essential for 
modern web development, React, Angular, Vue.js, and server-side JavaScript.
Includes npm package manager. Installs current LTS version.""",
    # System tools
    "swappiness": """Controls how aggressively the kernel swaps memory to disk.
Lower values (1-10) keep more in RAM - better for desktops/gaming.
Higher values (60-100) swap more aggressively - better for servers.
Default Ubuntu is 60, but 10 is recommended for desktop use.""",
    # CLI tools
    "bat": """A cat clone with syntax highlighting, Git integration, and automatic paging.
Shows line numbers, highlights changes, and supports 150+ languages.
Much better than cat for viewing code. Install: apt""",
    "ripgrep": """Extremely fast recursive grep that respects .gitignore by default.
5-10x faster than grep/ag. Supports regex, file type filtering.
Essential for searching large codebases. Alias: rg""",
    "fzf": """Fuzzy finder for terminal - interactive filter for any list.
Ctrl+R for command history, Ctrl+T for files, Alt+C for directories.
Integrates with vim, git, and more. Game-changer for productivity.""",
    # AI/ML Tools
    "ollama": """Ollama makes running large language models locally simple and efficient.
Supports models like Llama 3, Mistral, Gemma, and many more.
Just 'ollama pull llama3' then 'ollama run llama3' to start chatting.
100% private, no internet required after model download.""",
    "pytorch": """PyTorch is the most popular deep learning framework for research.
Dynamic computation graphs make debugging and experimentation easy.
Excellent GPU support with CUDA. Includes torchvision for computer vision.
Preferred by researchers and increasingly used in production.""",
    "jupyter-lab": """JupyterLab is the next-gen interface for Jupyter notebooks.
Perfect for data science, machine learning experiments, and visualization.
Supports Python, R, Julia. Mix code, markdown, and rich outputs.
Essential tool for interactive data analysis and model development.""",
    "stable-diffusion-webui": """AUTOMATIC1111's WebUI is the most popular Stable Diffusion interface.
Generate images from text prompts with extensive customization options.
Supports LoRA, ControlNet, custom models, and batch processing.
Requires a GPU with at least 6GB VRAM for best performance.""",
    "text-generation-webui": """Oobabooga's interface for running LLMs locally with many features.
Supports GGUF, GPTQ, AWQ models. Character roleplay, notebooks, extensions.
Works with models from Hugging Face. Comparable to ChatGPT but private.
Best choice for advanced local LLM usage with full control.""",
    "langchain": """LangChain helps build applications powered by language models.
Chain together LLMs, prompts, tools, and data sources into workflows.
Supports agents, RAG, memory, and integration with 100+ services.
The de facto standard for production LLM applications.""",
}


@dataclass
class MenuItem:
    """Represents a menu item with all necessary properties"""

    id: str
    label: str
    description: str
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    is_category: bool = False
    is_configurable: bool = False
    default: bool = False
    selected: bool = False
    config_type: str = "slider"
    config_value: any = None
    config_range: tuple = (1, 10)
    config_unit: str = ""
    config_options: Optional[List[tuple]] = None
    ansible_var: Optional[str] = None
    emoji: str = ""  # Added emoji field
    help_text: Optional[str] = None  # Added help text


class EnhancedMenuUI:
    """Professional hierarchical menu UI system with Rich formatting"""

    def __init__(self):
        self.console = Console()

        # Navigation state
        self.current_menu = "root"
        self.current_item = 0
        self.scroll_offset = 0
        self.breadcrumb_stack = ["root"]

        # Data structures
        self.menu_items: Dict[str, MenuItem] = {}
        self.selected_items: Set[str] = set()
        self.installed_fonts: Set[str] = set()  # Track which fonts user selected to install

        # UI state
        self.cancelled = False

        # Build menu structure
        self._build_menu_structure()

        # Apply defaults
        self._apply_defaults()

    def _build_menu_structure(self):
        """Build the complete hierarchical menu structure"""

        # Create root menu
        self.menu_items["root"] = MenuItem(
            "root",
            "🚀 Ubootu - Ubuntu System Setup",
            "Navigate: ↑↓ arrows, SPACE select, ENTER enter, H help     |     Press F1 for Actions Menu",
            is_category=True,
            children=["development", "ai-ml", "desktop", "applications", "security", "system"],
        )

        # Build each section
        self._build_development_menu()
        self._build_ai_ml_menu()
        self._build_desktop_menu()
        self._build_applications_menu()
        self._build_security_menu()
        self._build_system_menu()

        # Add actions menu
        self.menu_items["actions"] = MenuItem(
            "actions",
            "Actions",
            "Installation and configuration actions",
            parent="root",
            is_category=True,
            children=["action-install", "action-save", "action-reset", "action-exit"],
        )

        # Action items with better formatting
        self.menu_items["action-install"] = MenuItem(
            "action-install",
            "🚀 Start Installation",
            "Apply settings and install selected software",
            parent="actions",
            emoji="🚀",
        )

        self.menu_items["action-save"] = MenuItem(
            "action-save",
            "💾 Save Configuration",
            "Save current selections without installing",
            parent="actions",
            emoji="💾",
        )

        self.menu_items["action-reset"] = MenuItem(
            "action-reset",
            "🔄 Reset Configuration",
            "Clear all selections and return to defaults",
            parent="actions",
            emoji="🔄",
        )

        self.menu_items["action-exit"] = MenuItem(
            "action-exit",
            "❌ Exit without Saving",
            "Exit the configuration tool without saving",
            parent="actions",
            emoji="❌",
        )

    def _build_development_menu(self):
        """Build the development tools menu section"""
        # Main development category
        self.menu_items["development"] = MenuItem(
            "development",
            "💻 Development Tools",
            "Programming languages, IDEs, debugging tools",
            parent="root",
            is_category=True,
            children=["dev-ides", "dev-languages", "dev-tools", "dev-containers", "dev-cli-modern"],
            emoji="💻",
        )

        # Development subcategories
        self._build_ides_menu()
        self._build_languages_menu()
        self._build_dev_tools_menu()
        self._build_containers_menu()
        self._build_modern_cli_menu()

    def _build_ides_menu(self):
        """Build IDEs and editors menu"""
        self.menu_items["dev-ides"] = MenuItem(
            "dev-ides",
            "🛠️ IDEs & Editors",
            "Integrated development environments",
            parent="development",
            is_category=True,
            children=["vscode", "intellij-idea", "pycharm", "webstorm", "sublime", "vim", "emacs", "neovim", "zed"],
            emoji="🛠️",
        )

        # Individual IDE items with emojis
        ides = [
            ("vscode", "📝 Visual Studio Code", "Microsoft's popular code editor", True, "📝"),
            ("intellij-idea", "🧠 IntelliJ IDEA", "JetBrains Java IDE", True, "🧠"),
            ("pycharm", "🐍 PyCharm", "JetBrains Python IDE", True, "🐍"),
            ("webstorm", "🌐 WebStorm", "JetBrains JavaScript IDE", False, "🌐"),
            ("sublime", "✏️ Sublime Text", "Sophisticated text editor", False, "✏️"),
            ("vim", "📄 Vim", "Terminal-based text editor", False, "📄"),
            ("neovim", "📝 NeoVim", "Modern Vim fork with Lua", False, "📝"),
            ("emacs", "🔮 Emacs", "Extensible text editor", False, "🔮"),
            ("zed", "⚡ Zed", "High-performance multiplayer editor", False, "⚡"),
        ]

        for ide_id, label, desc, default, emoji in ides:
            self.menu_items[ide_id] = MenuItem(
                ide_id,
                label,
                desc,
                parent="dev-ides",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(ide_id),
            )

    def _build_languages_menu(self):
        """Build programming languages menu"""
        self.menu_items["dev-languages"] = MenuItem(
            "dev-languages",
            "🗣️ Programming Languages",
            "Runtimes, compilers, interpreters",
            parent="development",
            is_category=True,
            children=["python", "nodejs", "java", "go", "rust", "cpp", "php", "ruby", "dotnet"],
            emoji="🗣️",
        )

        languages = [
            ("python", "🐍 Python", "Python runtime and pip", True, "🐍"),
            ("nodejs", "🟨 Node.js", "JavaScript runtime", True, "🟨"),
            ("java", "☕ Java", "Java Development Kit", True, "☕"),
            ("go", "🐹 Go", "Go programming language", False, "🐹"),
            ("rust", "🦀 Rust", "Rust programming language", False, "🦀"),
            ("cpp", "🔷 C/C++", "GCC compiler and build tools", False, "🔷"),
            ("php", "🐘 PHP", "PHP interpreter", False, "🐘"),
            ("ruby", "💎 Ruby", "Ruby interpreter", False, "💎"),
            ("dotnet", "🟦 .NET", ".NET SDK and runtime", False, "🟦"),
        ]

        for lang_id, label, desc, default, emoji in languages:
            self.menu_items[lang_id] = MenuItem(
                lang_id,
                label,
                desc,
                parent="dev-languages",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(lang_id),
            )

    def _build_dev_tools_menu(self):
        """Build development tools menu"""
        self.menu_items["dev-tools"] = MenuItem(
            "dev-tools",
            "🔧 Development Tools",
            "Debugging, profiling, testing tools",
            parent="development",
            is_category=True,
            children=[
                "git",
                "docker",
                "postman",
                "insomnia",
                "dbeaver",
                "mysql-workbench",
                "pgadmin",
                "redis-desktop",
                "mongodb-compass",
                "github-desktop",
                "gitkraken",
                "smartgit",
                "lazygit",
                "gittyup",
            ],
            emoji="🔧",
        )

        tools = [
            ("git", "🐙 Git", "Version control system", True, "🐙"),
            ("docker", "🐳 Docker", "Container platform", True, "🐳"),
            ("postman", "📮 Postman", "API development tool", False, "📮"),
            ("insomnia", "🌙 Insomnia", "REST/GraphQL client", False, "🌙"),
            ("dbeaver", "🗄️ DBeaver", "Universal database tool", False, "🗄️"),
            ("mysql-workbench", "🐬 MySQL Workbench", "MySQL administration", False, "🐬"),
            ("pgadmin", "🐘 pgAdmin", "PostgreSQL administration", False, "🐘"),
            ("redis-desktop", "📊 Redis Desktop Manager", "Redis GUI", False, "📊"),
            ("mongodb-compass", "🍃 MongoDB Compass", "MongoDB GUI", False, "🍃"),
            ("github-desktop", "🐱 GitHub Desktop", "GitHub GUI client", False, "🐱"),
            ("gitkraken", "🐙 GitKraken", "Cross-platform Git GUI", False, "🐙"),
            ("smartgit", "🧠 SmartGit", "Professional Git GUI", False, "🧠"),
            ("lazygit", "😴 LazyGit", "Terminal UI for Git", True, "😴"),
            ("gittyup", "📈 Gittyup", "Clean Git GUI", False, "📈"),
        ]

        for tool_id, label, desc, default, emoji in tools:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="dev-tools",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_containers_menu(self):
        """Build containers and DevOps menu"""
        self.menu_items["dev-containers"] = MenuItem(
            "dev-containers",
            "🐳 Containers & DevOps",
            "Container platforms and orchestration",
            parent="development",
            is_category=True,
            children=[
                "docker-ce",
                "docker-compose",
                "kubernetes",
                "minikube",
                "helm",
                "terraform",
                "ansible",
                "vagrant",
                "podman",
            ],
            emoji="🐳",
        )

        containers = [
            ("docker-ce", "🐳 Docker CE", "Docker Community Edition", True, "🐳"),
            ("docker-compose", "📦 Docker Compose", "Multi-container orchestration", True, "📦"),
            ("kubernetes", "☸️ Kubernetes", "kubectl CLI tool", False, "☸️"),
            ("minikube", "🎯 Minikube", "Local Kubernetes", False, "🎯"),
            ("helm", "⎈ Helm", "Kubernetes package manager", False, "⎈"),
            ("terraform", "🏗️ Terraform", "Infrastructure as code", False, "🏗️"),
            ("ansible", "🔧 Ansible", "Configuration automation", False, "🔧"),
            ("vagrant", "📦 Vagrant", "VM automation", False, "📦"),
            ("podman", "🦭 Podman", "Daemonless container engine", False, "🦭"),
        ]

        for container_id, label, desc, default, emoji in containers:
            self.menu_items[container_id] = MenuItem(
                container_id,
                label,
                desc,
                parent="dev-containers",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(container_id),
            )

    def _build_modern_cli_menu(self):
        """Build modern CLI tools menu"""
        self.menu_items["dev-cli-modern"] = MenuItem(
            "dev-cli-modern",
            "🚀 Modern CLI Tools",
            "Next-gen command line utilities",
            parent="development",
            is_category=True,
            children=[
                "bat",
                "exa",
                "ripgrep",
                "fd",
                "dust",
                "duf",
                "procs",
                "bottom",
                "sd",
                "delta",
                "htop",
                "btop",
                "glances",
                "ncdu",
                "tldr",
                "fzf",
                "zoxide",
                "starship",
                "tmux",
                "zellij",
                "navi",
                "mcfly",
            ],
            emoji="🚀",
        )

        cli_tools = [
            ("bat", "🦇 bat", "Cat with syntax highlighting", True, "🦇"),
            ("exa", "📁 exa", "Modern ls replacement", True, "📁"),
            ("ripgrep", "🔍 ripgrep", "Fast grep alternative (rg)", True, "🔍"),
            ("fd", "🔎 fd", "Fast find alternative", True, "🔎"),
            ("dust", "💾 dust", "Intuitive du", False, "💾"),
            ("duf", "📊 duf", "Better df with colors", False, "📊"),
            ("procs", "📋 procs", "Modern ps replacement", False, "📋"),
            ("bottom", "📈 bottom", "System monitor", False, "📈"),
            ("sd", "✂️ sd", "Intuitive sed replacement", False, "✂️"),
            ("delta", "🎨 delta", "Syntax-highlighting diff", True, "🎨"),
            ("htop", "📊 htop", "Interactive process viewer", True, "📊"),
            ("btop", "🎮 btop++", "Beautiful resource monitor", True, "🎮"),
            ("glances", "👁️ glances", "System monitoring tool", True, "👁️"),
            ("ncdu", "📂 ncdu", "NCurses disk usage", True, "📂"),
            ("tldr", "📖 tldr", "Simplified man pages", True, "📖"),
            ("fzf", "🔍 fzf", "Fuzzy finder", True, "🔍"),
            ("zoxide", "⚡ zoxide", "Smarter cd command", True, "⚡"),
            ("starship", "🚀 starship", "Cross-shell prompt", True, "🚀"),
            ("tmux", "🖥️ tmux", "Terminal multiplexer", True, "🖥️"),
            ("zellij", "🪟 zellij", "Modern terminal workspace", False, "🪟"),
            ("navi", "🧭 navi", "Interactive cheatsheet", False, "🧭"),
            ("mcfly", "⏰ mcfly", "Smart shell history", False, "⏰"),
        ]

        for cli_id, label, desc, default, emoji in cli_tools:
            self.menu_items[cli_id] = MenuItem(
                cli_id,
                label,
                desc,
                parent="dev-cli-modern",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(cli_id),
            )

    def _build_ai_ml_menu(self):
        """Build AI & Machine Learning menu"""
        self.menu_items["ai-ml"] = MenuItem(
            "ai-ml",
            "🤖 AI & Machine Learning",
            "AI tools, ML frameworks, and language models",
            parent="root",
            is_category=True,
            children=["ai-cli-tools", "ml-frameworks", "image-generation", "local-llm-uis", "ai-agents"],
            emoji="🤖",
        )

        # Build AI subcategories
        self._build_ai_cli_tools()
        self._build_ml_frameworks()
        self._build_image_generation()
        self._build_local_llm_uis()
        self._build_ai_agents()

    def _build_ai_cli_tools(self):
        """Build AI CLI tools submenu"""
        self.menu_items["ai-cli-tools"] = MenuItem(
            "ai-cli-tools",
            "🤖 AI CLI Tools",
            "Command-line AI assistants and interfaces",
            parent="ai-ml",
            is_category=True,
            children=["ollama", "aichat", "gemini-cli", "claude-cli", "gptcli", "pygpt"],
            emoji="🤖",
        )

        ai_cli_tools = [
            ("ollama", "🦙 Ollama", "Run LLMs locally (Llama, Mistral, etc)", True, "🦙"),
            ("aichat", "💬 AIChat", "Multi-provider CLI (OpenAI, Claude, Gemini)", False, "💬"),
            ("gemini-cli", "✨ Gemini CLI", "Google's AI agent for terminals", False, "✨"),
            ("claude-cli", "🧠 Claude CLI", "Anthropic's Claude in terminal", False, "🧠"),
            ("gptcli", "🤖 GPT CLI", "OpenAI GPT command-line interface", False, "🤖"),
            ("pygpt", "🐍 PyGPT", "Desktop AI assistant with multiple models", False, "🐍"),
        ]

        for tool_id, label, desc, default, emoji in ai_cli_tools:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="ai-cli-tools",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_ml_frameworks(self):
        """Build ML frameworks submenu"""
        self.menu_items["ml-frameworks"] = MenuItem(
            "ml-frameworks",
            "🧠 ML Frameworks",
            "Machine learning libraries and tools",
            parent="ai-ml",
            is_category=True,
            children=[
                "pytorch",
                "tensorflow",
                "jupyter-lab",
                "scikit-learn",
                "pandas-numpy",
                "huggingface-cli",
                "cuda-toolkit",
            ],
            emoji="🧠",
        )

        ml_frameworks = [
            ("pytorch", "🔥 PyTorch", "Deep learning framework with GPU support", True, "🔥"),
            ("tensorflow", "🟧 TensorFlow", "Google's ML framework with Keras", False, "🟧"),
            ("jupyter-lab", "📓 JupyterLab", "Interactive notebooks for data science", True, "📓"),
            ("scikit-learn", "🔬 Scikit-learn", "Classical ML algorithms library", True, "🔬"),
            ("pandas-numpy", "🐼 Pandas & NumPy", "Data manipulation essentials", True, "🐼"),
            ("huggingface-cli", "🤗 Hugging Face CLI", "Transformers and model hub", False, "🤗"),
            ("cuda-toolkit", "🎮 CUDA Toolkit", "NVIDIA GPU acceleration", False, "🎮"),
        ]

        for tool_id, label, desc, default, emoji in ml_frameworks:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="ml-frameworks",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_image_generation(self):
        """Build image generation tools submenu"""
        self.menu_items["image-generation"] = MenuItem(
            "image-generation",
            "🎨 Image Generation",
            "AI-powered image generation tools",
            parent="ai-ml",
            is_category=True,
            children=["stable-diffusion-webui", "comfyui", "invokeai", "fooocus"],
            emoji="🎨",
        )

        image_gen_tools = [
            ("stable-diffusion-webui", "🖼️ AUTOMATIC1111 WebUI", "Popular Stable Diffusion interface", True, "🖼️"),
            ("comfyui", "🔗 ComfyUI", "Node-based SD workflow builder", False, "🔗"),
            ("invokeai", "🎯 InvokeAI", "Professional SD interface", False, "🎯"),
            ("fooocus", "📸 Fooocus", "Simplified SD interface", False, "📸"),
        ]

        for tool_id, label, desc, default, emoji in image_gen_tools:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="image-generation",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_local_llm_uis(self):
        """Build local LLM UI tools submenu"""
        self.menu_items["local-llm-uis"] = MenuItem(
            "local-llm-uis",
            "💬 Local LLM UIs",
            "Graphical interfaces for local language models",
            parent="ai-ml",
            is_category=True,
            children=["text-generation-webui", "lm-studio", "gpt4all", "jan-ai", "open-webui"],
            emoji="💬",
        )

        llm_ui_tools = [
            ("text-generation-webui", "🌐 Text Generation WebUI", "Oobabooga's versatile LLM interface", True, "🌐"),
            ("lm-studio", "🏢 LM Studio", "User-friendly local model runner", False, "🏢"),
            ("gpt4all", "💻 GPT4All", "Chat with docs using local models", False, "💻"),
            ("jan-ai", "⚡ Jan.ai", "Fast, clean local LLM interface", False, "⚡"),
            ("open-webui", "🎯 Open WebUI", "Web interface for Ollama", False, "🎯"),
        ]

        for tool_id, label, desc, default, emoji in llm_ui_tools:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="local-llm-uis",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_ai_agents(self):
        """Build AI agent frameworks submenu"""
        self.menu_items["ai-agents"] = MenuItem(
            "ai-agents",
            "🔧 AI Agent Frameworks",
            "Tools for building autonomous AI agents",
            parent="ai-ml",
            is_category=True,
            children=["langchain", "langgraph", "crewai", "autogen", "langflow", "flowise"],
            emoji="🔧",
        )

        agent_frameworks = [
            ("langchain", "🔗 LangChain", "Framework for chaining LLMs and tools", True, "🔗"),
            ("langgraph", "📊 LangGraph", "Graph-based agent workflows", False, "📊"),
            ("crewai", "👥 CrewAI", "Multi-agent collaboration framework", False, "👥"),
            ("autogen", "🤖 AutoGen", "Microsoft's conversational agents", False, "🤖"),
            ("langflow", "🌊 LangFlow", "Visual LangChain flow builder", False, "🌊"),
            ("flowise", "🌐 Flowise", "Low-code LLM app builder", False, "🌐"),
        ]

        for tool_id, label, desc, default, emoji in agent_frameworks:
            self.menu_items[tool_id] = MenuItem(
                tool_id,
                label,
                desc,
                parent="ai-agents",
                default=default,
                emoji=emoji,
                help_text=HELP_DESCRIPTIONS.get(tool_id),
            )

    def _build_desktop_menu(self):
        """Build desktop environment menu"""
        self.menu_items["desktop"] = MenuItem(
            "desktop",
            "🖥️ Desktop Environment",
            "Desktop environments, themes, and appearance",
            parent="root",
            is_category=True,
            children=["desktop-environments", "themes", "fonts-config"],
            emoji="🖥️",
        )

        # Desktop environment subcategory
        self.menu_items["desktop-environments"] = MenuItem(
            "desktop-environments",
            "🏠 Desktop Environments",
            "Choose your desktop environment",
            parent="desktop",
            is_category=True,
            children=["gnome", "kde", "xfce", "mate", "cinnamon", "budgie", "lxqt"],
            emoji="🏠",
        )

        desktops = [
            ("gnome", "🟠 GNOME", "Modern and clean desktop", True, "🟠"),
            ("kde", "🔷 KDE Plasma", "Highly customizable desktop", False, "🔷"),
            ("xfce", "🐭 XFCE", "Lightweight desktop", False, "🐭"),
            ("mate", "🧉 MATE", "Traditional desktop", False, "🧉"),
            ("cinnamon", "🟤 Cinnamon", "Modern traditional desktop", False, "🟤"),
            ("budgie", "🦜 Budgie", "Modern, clean desktop", False, "🦜"),
            ("lxqt", "🍃 LXQt", "Lightweight Qt desktop", False, "🍃"),
        ]

        for desktop_id, label, desc, default, emoji in desktops:
            self.menu_items[desktop_id] = MenuItem(
                desktop_id, label, desc, parent="desktop-environments", default=default, emoji=emoji
            )

        # Themes subcategory
        self.menu_items["themes"] = MenuItem(
            "themes",
            "🎨 Themes & Appearance",
            "Icons, themes, and visual customization",
            parent="desktop",
            is_category=True,
            children=["theme-dark", "theme-icons", "theme-cursors", "theme-sounds"],
            emoji="🎨",
        )

        themes = [
            ("theme-dark", "🌙 Dark Theme", "Enable dark mode system-wide", True, "🌙"),
            ("theme-icons", "🎭 Beautiful Icons", "Modern icon themes (Papirus)", True, "🎭"),
            ("theme-cursors", "🖱️ Custom Cursors", "Better cursor themes", False, "🖱️"),
            ("theme-sounds", "🔊 System Sounds", "Pleasant system sounds", False, "🔊"),
        ]

        for theme_id, label, desc, default, emoji in themes:
            self.menu_items[theme_id] = MenuItem(theme_id, label, desc, parent="themes", default=default, emoji=emoji)

        # Font configuration
        self._build_fonts_menu()

    def _build_fonts_menu(self):
        """Build comprehensive font configuration menu"""
        self.menu_items["fonts-config"] = MenuItem(
            "fonts-config",
            "🔤 Fonts & Typography",
            "System fonts and rendering configuration",
            parent="desktop",
            is_category=True,
            children=["font-packages", "nerd-fonts", "font-settings"],
            emoji="🔤",
        )

        # Font packages
        self.menu_items["font-packages"] = MenuItem(
            "font-packages",
            "📦 System Font Packages",
            "Essential system fonts",
            parent="fonts-config",
            is_category=True,
            children=[
                "fonts-ubuntu",
                "fonts-noto",
                "fonts-liberation",
                "fonts-roboto",
                "fonts-firacode",
                "fonts-cascadia",
                "fonts-jetbrains",
            ],
            emoji="📦",
        )

        system_fonts = [
            ("fonts-ubuntu", "Ubuntu Font Family", "Default Ubuntu fonts", True),
            ("fonts-noto", "Noto Fonts", "Google's font family", True),
            ("fonts-liberation", "Liberation Fonts", "Red Hat's fonts", True),
            ("fonts-roboto", "Roboto", "Android's font family", False),
            ("fonts-firacode", "Fira Code", "Programming ligatures", True),
            ("fonts-cascadia", "Cascadia Code", "Microsoft's coding font", False),
            ("fonts-jetbrains", "JetBrains Mono", "IDE font", True),
        ]

        for font_id, label, desc, default in system_fonts:
            self.menu_items[font_id] = MenuItem(font_id, label, desc, parent="font-packages", default=default)

        # Nerd Fonts
        self.menu_items["nerd-fonts"] = MenuItem(
            "nerd-fonts",
            "🤓 Nerd Fonts",
            "Fonts with programming ligatures and icons",
            parent="fonts-config",
            is_category=True,
            children=[
                "nf-jetbrains",
                "nf-hack",
                "nf-firacode",
                "nf-cascadia",
                "nf-sourcecodepro",
                "nf-ubuntu",
                "nf-inconsolata",
                "nf-meslo",
            ],
            emoji="🤓",
        )

        nerd_fonts = [
            ("nf-jetbrains", "JetBrainsMono Nerd Font", "Modern coding font", True),
            ("nf-hack", "Hack Nerd Font", "Source code font", True),
            ("nf-firacode", "FiraCode Nerd Font", "With ligatures", True),
            ("nf-cascadia", "CascadiaCode Nerd Font", "Microsoft's font", False),
            ("nf-sourcecodepro", "SourceCodePro Nerd Font", "Adobe's font", False),
            ("nf-ubuntu", "UbuntuMono Nerd Font", "Ubuntu's font", False),
            ("nf-inconsolata", "Inconsolata Nerd Font", "Humanist font", False),
            ("nf-meslo", "MesloLG Nerd Font", "Apple-style font", False),
        ]

        for font_id, label, desc, default in nerd_fonts:
            self.menu_items[font_id] = MenuItem(font_id, label, desc, parent="nerd-fonts", default=default)
            # Track installed fonts
            if default:
                self.installed_fonts.add(font_id)

        # Font settings
        self.menu_items["font-settings"] = MenuItem(
            "font-settings",
            "⚙️ Font Settings",
            "Font rendering and system configuration",
            parent="fonts-config",
            is_category=True,
            children=["font-interface", "font-document", "font-monospace", "font-antialiasing", "font-hinting"],
            emoji="⚙️",
        )

        # These will be configurable based on installed fonts
        self.menu_items["font-interface"] = MenuItem(
            "font-interface",
            "🖥️ Interface Font",
            "System UI font",
            parent="font-settings",
            is_configurable=True,
            config_type="dropdown",
            config_value="Ubuntu 11",
        )

        self.menu_items["font-document"] = MenuItem(
            "font-document",
            "📄 Document Font",
            "Default document font",
            parent="font-settings",
            is_configurable=True,
            config_type="dropdown",
            config_value="Ubuntu 11",
        )

        self.menu_items["font-monospace"] = MenuItem(
            "font-monospace",
            "💻 Monospace Font",
            "Terminal and code font",
            parent="font-settings",
            is_configurable=True,
            config_type="dropdown",
            config_value="Ubuntu Mono 11",
        )

        self.menu_items["font-antialiasing"] = MenuItem(
            "font-antialiasing",
            "🔤 Antialiasing",
            "Font smoothing method",
            parent="font-settings",
            is_configurable=True,
            config_type="dropdown",
            config_value="subpixel",
            config_options=[("subpixel", "Subpixel (LCD)"), ("grayscale", "Grayscale"), ("none", "None")],
        )

        self.menu_items["font-hinting"] = MenuItem(
            "font-hinting",
            "📐 Hinting",
            "Font hinting level",
            parent="font-settings",
            is_configurable=True,
            config_type="dropdown",
            config_value="slight",
            config_options=[("none", "None"), ("slight", "Slight"), ("medium", "Medium"), ("full", "Full")],
        )

    def _build_applications_menu(self):
        """Build applications menu"""
        self.menu_items["applications"] = MenuItem(
            "applications",
            "📱 Applications",
            "Essential and productivity applications",
            parent="root",
            is_category=True,
            children=["app-browsers", "app-media"],
            emoji="📱",
        )

        # Browser subcategory - Remove non-Linux browsers
        self.menu_items["app-browsers"] = MenuItem(
            "app-browsers",
            "🌐 Web Browsers",
            "Web browsing applications",
            parent="applications",
            is_category=True,
            children=["firefox", "chrome", "chromium", "brave", "vivaldi", "opera"],
            emoji="🌐",
        )

        browsers = [
            ("firefox", "🦊 Firefox", "Mozilla Firefox browser", True, "🦊"),
            ("chrome", "🌍 Google Chrome", "Google Chrome browser", False, "🌍"),
            ("chromium", "🔷 Chromium", "Open-source Chrome", False, "🔷"),
            ("brave", "🦁 Brave", "Privacy-focused browser", False, "🦁"),
            ("vivaldi", "🎨 Vivaldi", "Feature-rich browser", False, "🎨"),
            ("opera", "⭕ Opera", "Opera browser", False, "⭕"),
        ]

        for browser_id, label, desc, default, emoji in browsers:
            self.menu_items[browser_id] = MenuItem(
                browser_id, label, desc, parent="app-browsers", default=default, emoji=emoji
            )

        # Media applications
        self.menu_items["app-media"] = MenuItem(
            "app-media",
            "🎬 Media & Graphics",
            "Media players and editors",
            parent="applications",
            is_category=True,
            children=["vlc", "mpv", "spotify", "gimp", "inkscape", "blender", "kdenlive", "obs"],
            emoji="🎬",
        )

        media_apps = [
            ("vlc", "🎬 VLC", "Universal media player", True, "🎬"),
            ("mpv", "▶️ mpv", "Minimal media player", False, "▶️"),
            ("spotify", "🎵 Spotify", "Music streaming", False, "🎵"),
            ("gimp", "🎨 GIMP", "Image editor", False, "🎨"),
            ("inkscape", "✒️ Inkscape", "Vector graphics", False, "✒️"),
            ("blender", "🎭 Blender", "3D creation suite", False, "🎭"),
            ("kdenlive", "🎞️ Kdenlive", "Video editor", False, "🎞️"),
            ("obs", "📹 OBS Studio", "Streaming/recording", False, "📹"),
        ]

        for media_id, label, desc, default, emoji in media_apps:
            self.menu_items[media_id] = MenuItem(
                media_id, label, desc, parent="app-media", default=default, emoji=emoji
            )

    def _build_security_menu(self):
        """Build security tools menu"""
        self.menu_items["security"] = MenuItem(
            "security",
            "🔒 Security & Privacy",
            "Security tools, privacy settings, and hardening",
            parent="root",
            is_category=True,
            children=["security-firewall", "security-privacy"],
            emoji="🔒",
        )

        # Security subcategories
        self.menu_items["security-firewall"] = MenuItem(
            "security-firewall",
            "🛡️ Firewall & Network",
            "Network security and firewall configuration",
            parent="security",
            is_category=True,
            children=["ufw", "fail2ban", "opensnitch", "firejail"],
            emoji="🛡️",
        )

        security_items = [
            ("ufw", "🔥 UFW Firewall", "Uncomplicated firewall", True, "🔥"),
            ("fail2ban", "🚫 Fail2ban", "Intrusion prevention", True, "🚫"),
            ("opensnitch", "👁️ OpenSnitch", "Application firewall", False, "👁️"),
            ("firejail", "🔒 Firejail", "Sandbox applications", False, "🔒"),
        ]

        for sec_id, label, desc, default, emoji in security_items:
            self.menu_items[sec_id] = MenuItem(
                sec_id, label, desc, parent="security-firewall", default=default, emoji=emoji
            )

        # Privacy tools
        self.menu_items["security-privacy"] = MenuItem(
            "security-privacy",
            "🕵️ Privacy Tools",
            "Privacy and encryption tools",
            parent="security",
            is_category=True,
            children=["keepassxc", "bitwarden", "tor-browser", "veracrypt", "cryptomator"],
            emoji="🕵️",
        )

        privacy_tools = [
            ("keepassxc", "🔐 KeePassXC", "Password manager", True, "🔐"),
            ("bitwarden", "🔑 Bitwarden", "Cloud password manager", False, "🔑"),
            ("tor-browser", "🧅 Tor Browser", "Anonymous browsing", False, "🧅"),
            ("veracrypt", "💾 VeraCrypt", "Disk encryption", False, "💾"),
            ("cryptomator", "🗄️ Cryptomator", "Cloud encryption", False, "🗄️"),
        ]

        for priv_id, label, desc, default, emoji in privacy_tools:
            self.menu_items[priv_id] = MenuItem(
                priv_id, label, desc, parent="security-privacy", default=default, emoji=emoji
            )

    def _build_system_menu(self):
        """Build system configuration menu"""
        self.menu_items["system"] = MenuItem(
            "system",
            "⚙️ System Configuration",
            "System settings, performance, and tweaks",
            parent="root",
            is_category=True,
            children=["system-performance"],
            emoji="⚙️",
        )

        # System subcategories
        self.menu_items["system-performance"] = MenuItem(
            "system-performance",
            "🚀 Performance",
            "System performance and resource management",
            parent="system",
            is_category=True,
            children=["swappiness", "preload", "zram", "ananicy", "gamemode"],
            emoji="🚀",
        )

        # Add configurable swappiness item
        self.menu_items["swappiness"] = MenuItem(
            "swappiness",
            "💾 Memory Swappiness",
            "How aggressively system uses swap space",
            parent="system-performance",
            is_configurable=True,
            config_type="slider",
            config_value=10,
            config_range=(0, 100),
            config_unit="",
            emoji="💾",
            help_text=HELP_DESCRIPTIONS.get("swappiness"),
        )

        system_items = [
            ("preload", "⚡ Preload", "Preload frequent apps", True, "⚡"),
            ("zram", "🗜️ ZRAM", "Compressed RAM swap", False, "🗜️"),
            ("ananicy", "🎯 Ananicy CPP", "Auto-nice daemon", False, "🎯"),
            ("gamemode", "🎮 GameMode", "Gaming optimizations", False, "🎮"),
        ]

        for sys_id, label, desc, default, emoji in system_items:
            self.menu_items[sys_id] = MenuItem(
                sys_id, label, desc, parent="system-performance", default=default, emoji=emoji
            )

    def _apply_defaults(self):
        """Apply community-standard defaults"""
        for item in self.menu_items.values():
            if item.default and not item.is_category:
                self.selected_items.add(item.id)
                item.selected = True

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")

    def show_splash_screen(self):
        """Display animated splash screen"""
        self.clear_screen()

        splash_text = """
[bold cyan]     ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱[/]
[bold cyan]    ╱                                                          ╱[/]
[bold cyan]   ╱   [bold white]██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗[/] ╱[/]
[bold cyan]  ╱    [bold white]██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║[/]╱[/]
[bold cyan] ╱     [bold white]██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║[/][/]
[bold cyan]╱      [bold white]██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║[/][/]
       [bold white]╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝[/]
        [bold white]╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝[/]
                    [bold magenta]Professional Ubuntu Desktop Configuration Tool[/]
        """

        panel = Panel(splash_text, box=box.ROUNDED, border_style="bright_blue")
        self.console.print(panel)

        # Animated loading bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        ) as progress:
            task = progress.add_task("[cyan]Loading awesomeness...", total=100)

            loading_messages = [
                "Initializing Ubuntu magic...",
                "Preparing configuration wizardry...",
                "Loading customization options...",
                "Getting everything ready...",
            ]

            for i, message in enumerate(loading_messages):
                progress.update(task, advance=25, description=f"[cyan]{message}")
                time.sleep(0.5)

        time.sleep(0.5)

    def get_current_menu_items(self) -> List[MenuItem]:
        """Get items for the current menu"""
        current = self.menu_items.get(self.current_menu)
        if not current or not current.children:
            return []

        return [self.menu_items[child_id] for child_id in current.children if child_id in self.menu_items]

    def get_selection_indicator(self, item: MenuItem) -> str:
        """Get improved selection indicator for menu item"""
        if item.is_category:
            # Check children selection status
            children = [
                self.menu_items[child_id]
                for child_id in item.children
                if child_id in self.menu_items and not self.menu_items[child_id].is_category
            ]
            if not children:
                return "○"  # No selectable children

            selected_count = sum(1 for child in children if child.selected)
            if selected_count == 0:
                return "○"  # None selected
            elif selected_count == len(children):
                return "◉"  # All selected (filled circle)
            else:
                return "◎"  # Partial selection (circle with dot)
        else:
            return "✓" if item.selected else " "

    def run_hierarchical_tui(self) -> int:
        """Run the main hierarchical TUI"""
        try:
            self.show_splash_screen()
            time.sleep(1)

            while True:
                self.clear_screen()

                # Display header
                header = Panel(
                    Align.center(
                        f"[bold]🚀 Ubootu Configuration Tool 🚀[/]\n"
                        f"[dim]Current section: {self.menu_items[self.current_menu].label}[/]",
                        vertical="middle",
                    ),
                    box=box.DOUBLE_EDGE,
                    border_style="bright_blue",
                    padding=(1, 2),
                )
                self.console.print(header)
                self.console.print()

                # Display breadcrumb
                breadcrumb_text = " > ".join(
                    [
                        self.menu_items[item_id].label.replace(self.menu_items[item_id].emoji + " ", "")
                        for item_id in self.breadcrumb_stack
                    ]
                )
                self.console.print(f"[dim]Navigation: {breadcrumb_text}[/]")
                self.console.print()

                # Get current menu items
                menu_items = self.get_current_menu_items()

                if not menu_items:
                    self.console.print("[red]No items in current menu[/]")
                    break

                # Display menu items with better formatting
                for i, item in enumerate(menu_items):
                    # Highlight current item
                    style = "bold cyan" if i == self.current_item else ""

                    # Selection indicator
                    indicator = self.get_selection_indicator(item)

                    # Format with 3-space indentation for description
                    if i == self.current_item:
                        self.console.print(f"[{style}][{indicator}] {item.label}[/]")
                        if item.description:
                            self.console.print(f"[{style} dim]   {item.description}[/]")
                    else:
                        self.console.print(f"[{indicator}] {item.label}")
                        if item.description:
                            self.console.print(f"[dim]   {item.description}[/]")

                    # Add spacing between items
                    if i < len(menu_items) - 1:
                        self.console.print()

                self.console.print()

                # Instructions with help key prominently displayed
                instructions = (
                    "[bold]Navigation:[/] ↑/↓ arrows, ← back, → enter  "
                    "[bold]Selection:[/] SPACE toggle, A all, N none\n"
                    "[bold]Actions:[/] S save, R run, Q quit  "
                    "[bold yellow]Press H for detailed help on current item[/]"
                )
                self.console.print(Panel(instructions, box=box.MINIMAL))

                # Show selection summary
                selected_count = len(self.selected_items)
                self.console.print(f"\n[green]Selected items: {selected_count}[/]")

                # Get user input
                try:
                    choice = input("\nYour choice: ").strip().lower()

                    if choice in ["q", "quit", "exit"]:
                        break
                    elif choice == "h" and self.current_item < len(menu_items):
                        # Show help for current item
                        self._show_help(menu_items[self.current_item])
                    elif choice in ["↑", "up", "k"]:
                        self.current_item = max(0, self.current_item - 1)
                    elif choice in ["↓", "down", "j"]:
                        self.current_item = min(len(menu_items) - 1, self.current_item + 1)
                    elif choice in ["←", "back", "b"] and len(self.breadcrumb_stack) > 1:
                        self.breadcrumb_stack.pop()
                        self.current_menu = self.breadcrumb_stack[-1]
                        self.current_item = 0
                    elif choice in ["→", "enter", "forward", ""] and self.current_item < len(menu_items):
                        current_menu_item = menu_items[self.current_item]
                        if current_menu_item.is_category:
                            # Navigate into category
                            self.current_menu = current_menu_item.id
                            self.breadcrumb_stack.append(current_menu_item.id)
                            self.current_item = 0
                        elif current_menu_item.is_configurable:
                            # Configure item
                            self._configure_item(current_menu_item)
                        else:
                            # Toggle selection
                            self._toggle_selection(current_menu_item)
                    elif choice == " " and self.current_item < len(menu_items):
                        # Toggle selection
                        current_menu_item = menu_items[self.current_item]
                        self._toggle_selection(current_menu_item)
                    elif choice == "a":
                        # Select all in current menu
                        self._select_all_in_menu()
                    elif choice == "n":
                        # Deselect all in current menu
                        self._deselect_all_in_menu()
                    elif choice == "s":
                        # Save configuration
                        self._save_configuration()
                    elif choice == "r":
                        # Run installation
                        return self._run_installation()
                    elif choice == "f1":
                        # Show actions menu
                        self.current_menu = "actions"
                        self.breadcrumb_stack.append("actions")
                        self.current_item = 0

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/]")
                    input("Press Enter to continue...")

            return 0 if not self.cancelled else 1

        except Exception as e:
            self.console.print(f"[red]Fatal error: {e}[/]")
            return 1

    def _show_help(self, item: MenuItem):
        """Show detailed help for an item"""
        self.clear_screen()

        # Create help panel
        help_text = item.help_text or f"No detailed help available for {item.label}"

        help_panel = Panel(
            f"[bold]{item.emoji} {item.label}[/]\n\n" f"[italic]{item.description}[/]\n\n" f"{help_text}",
            title="[bold yellow]Help Information[/]",
            box=box.ROUNDED,
            border_style="yellow",
            padding=(1, 2),
        )

        self.console.print(help_panel)

        # Show additional info if available
        if item.is_configurable:
            self.console.print(f"\n[bold]Configuration:[/]")
            self.console.print(f"  Type: {item.config_type}")
            self.console.print(f"  Current value: {item.config_value}{item.config_unit}")
            if item.config_range:
                self.console.print(f"  Range: {item.config_range[0]}-{item.config_range[1]}")

        if item.default:
            self.console.print(f"\n[green]✓ This item is selected by default[/]")

        self.console.print("\n[dim]Press Enter to continue...[/]")
        input()

    def _select_all_in_menu(self):
        """Select all items in current menu"""
        menu_items = self.get_current_menu_items()
        for item in menu_items:
            if not item.is_category and not item.is_configurable:
                item.selected = True
                self.selected_items.add(item.id)

    def _deselect_all_in_menu(self):
        """Deselect all items in current menu"""
        menu_items = self.get_current_menu_items()
        for item in menu_items:
            if not item.is_category and not item.is_configurable:
                item.selected = False
                self.selected_items.discard(item.id)

    def _toggle_selection(self, item: MenuItem):
        """Toggle selection of an item"""
        if item.is_category:
            # Toggle all children
            children = [
                self.menu_items[child_id]
                for child_id in item.children
                if child_id in self.menu_items and not self.menu_items[child_id].is_category
            ]

            # Check if all are selected
            all_selected = all(child.selected for child in children)

            # Toggle all to opposite state
            for child in children:
                if all_selected:
                    child.selected = False
                    self.selected_items.discard(child.id)
                else:
                    child.selected = True
                    self.selected_items.add(child.id)
        else:
            # Toggle individual item
            if item.selected:
                item.selected = False
                self.selected_items.discard(item.id)
            else:
                item.selected = True
                self.selected_items.add(item.id)

    def _configure_item(self, item: MenuItem):
        """Configure a configurable item with improved slider"""
        self.clear_screen()

        config_panel = Panel(
            f"[bold]Configure {item.label}[/]\n" f"[dim]{item.description}[/]",
            box=box.ROUNDED,
            border_style="bright_blue",
        )
        self.console.print(config_panel)
        self.console.print()

        if item.config_type == "slider":
            min_val, max_val = item.config_range
            current = item.config_value

            # Show common values for context
            if item.id == "swappiness":
                self.console.print("[bold]Common values:[/]")
                self.console.print("  • 10  - Desktop/Gaming (recommended)")
                self.console.print("  • 60  - Default Ubuntu")
                self.console.print("  • 1   - Maximum RAM usage")
                self.console.print()

            # Visual slider representation
            slider_width = 40
            position = int((current - min_val) / (max_val - min_val) * slider_width)
            slider_bar = "─" * position + "●" + "─" * (slider_width - position)

            self.console.print(f"Current: [{current}]")
            self.console.print()
            self.console.print(f"◄{slider_bar}► {min_val}-{max_val}")
            self.console.print()
            self.console.print("Enter value directly or use ↑↓ for ±1, PgUp/PgDn for ±10")

            try:
                new_value = input(f"\nEnter new value [{min_val}-{max_val}]: ").strip()
                if new_value:
                    new_value = int(new_value)
                    if min_val <= new_value <= max_val:
                        item.config_value = new_value
                        self.console.print(f"\n[green]✓ Updated to {new_value}{item.config_unit}[/]")
                    else:
                        self.console.print(f"\n[red]Value must be between {min_val} and {max_val}[/]")

                input("\nPress Enter to continue...")
            except ValueError:
                self.console.print("[red]Invalid number[/]")
                input("\nPress Enter to continue...")

        elif item.config_type == "dropdown":
            # Handle dropdown configuration (for fonts)
            if item.id.startswith("font-") and item.id != "font-antialiasing" and item.id != "font-hinting":
                # Dynamic font list based on installed fonts
                available_fonts = self._get_available_fonts()

                self.console.print("[bold]Available fonts:[/]")
                for i, (font_id, font_name) in enumerate(available_fonts):
                    marker = "▶" if font_name == item.config_value else " "
                    self.console.print(f"{marker} {i+1}. {font_name}")

                try:
                    choice = input(f"\nSelect font [1-{len(available_fonts)}]: ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(available_fonts):
                            item.config_value = available_fonts[idx][1]
                            self.console.print(f"\n[green]✓ Updated to {item.config_value}[/]")

                    input("\nPress Enter to continue...")
                except Exception:
                    input("\nPress Enter to continue...")
            else:
                # Regular dropdown
                self.console.print("[bold]Options:[/]")
                for i, (opt_id, opt_name) in enumerate(item.config_options or []):
                    marker = "▶" if opt_id == item.config_value else " "
                    self.console.print(f"{marker} {i+1}. {opt_name}")

                try:
                    choice = input(f"\nSelect option [1-{len(item.config_options)}]: ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(item.config_options):
                            item.config_value = item.config_options[idx][0]
                            self.console.print(f"\n[green]✓ Updated to {item.config_options[idx][1]}[/]")

                    input("\nPress Enter to continue...")
                except Exception:
                    input("\nPress Enter to continue...")

    def _get_available_fonts(self) -> List[Tuple[str, str]]:
        """Get list of fonts based on what user selected to install"""
        fonts = [("ubuntu", "Ubuntu 11")]  # Default always available

        # Add fonts based on selections
        if "fonts-noto" in self.selected_items:
            fonts.append(("noto", "Noto Sans 11"))
        if "fonts-roboto" in self.selected_items:
            fonts.append(("roboto", "Roboto 11"))
        if "fonts-liberation" in self.selected_items:
            fonts.append(("liberation", "Liberation Sans 11"))

        # Add Nerd Fonts if selected
        if "nf-jetbrains" in self.selected_items:
            fonts.append(("jetbrains-nerd", "JetBrainsMono Nerd Font 11"))
        if "nf-hack" in self.selected_items:
            fonts.append(("hack-nerd", "Hack Nerd Font 11"))
        if "nf-firacode" in self.selected_items:
            fonts.append(("firacode-nerd", "FiraCode Nerd Font 11"))

        # For monospace fonts, return appropriate options
        if self.current_item < len(self.get_current_menu_items()):
            current_item = self.get_current_menu_items()[self.current_item]
            if current_item.id == "font-monospace":
                fonts = [("ubuntu-mono", "Ubuntu Mono 11")]
                if "nf-jetbrains" in self.selected_items:
                    fonts.append(("jetbrains-mono-nerd", "JetBrainsMono Nerd Font 11"))
                if "nf-hack" in self.selected_items:
                    fonts.append(("hack-nerd", "Hack Nerd Font 11"))
                if "nf-firacode" in self.selected_items:
                    fonts.append(("firacode-nerd", "FiraCode Nerd Font 11"))

        return fonts

    def _save_configuration(self):
        """Save current configuration to file"""
        config_data = {
            "metadata": {"version": "1.0", "created_at": time.strftime("%Y-%m-%d %H:%M:%S")},
            "selected_items": list(self.selected_items),
            "configurable_items": {},
            "ansible_variables": {},
        }

        # Add configurable items
        for item in self.menu_items.values():
            if item.is_configurable and item.config_value is not None:
                config_data["configurable_items"][item.id] = {"id": item.id, "value": item.config_value}

        try:
            import yaml

            with open("config.yml", "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)

            self.console.print("[green]✓ Configuration saved to config.yml[/]")
            input("Press Enter to continue...")
        except ImportError:
            self.console.print("[red]PyYAML not found. Cannot save configuration.[/]")
            input("Press Enter to continue...")
        except Exception as e:
            self.console.print(f"[red]Error saving configuration: {e}[/]")
            input("Press Enter to continue...")

    def _run_installation(self) -> int:
        """Run the installation process"""
        self.console.print("\n[bold green]🚀 Starting Installation Process[/]")

        if not self.selected_items:
            self.console.print("[yellow]No items selected for installation.[/]")
            input("Press Enter to continue...")
            return 0

        # Show what will be installed
        self.console.print(f"\n[bold]Selected items ({len(self.selected_items)}):[/]")
        for item_id in sorted(self.selected_items):
            if item_id in self.menu_items:
                item = self.menu_items[item_id]
                self.console.print(f"  • {item.emoji} {item.label}")

        # Confirm installation
        try:
            confirm = Confirm.ask("\nProceed with installation?")
            if not confirm:
                return 0
        except KeyboardInterrupt:
            return 1

        # Save configuration first
        self._save_configuration()

        # Show success message
        self.console.print("\n[bold green]✅ Configuration saved successfully![/]")
        self.console.print("[dim]You can now run the Ansible playbook to apply changes.[/]")

        input("Press Enter to exit...")
        return 0


def create_enhanced_menu_ui():
    """Factory function to create EnhancedMenuUI instance"""
    return EnhancedMenuUI()


def run_tui(selected_sections=None):
    """Run the enhanced TUI"""
    ui = EnhancedMenuUI()
    return ui.run_hierarchical_tui()


def main():
    """Main entry point"""
    import sys

    # Check for help flag
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Ubootu Configuration Tool")
        print("Usage: enhanced_menu_ui.py [sections...]")
        print("\nAvailable sections:")
        print("  development - Development tools and languages")
        print("  desktop     - Desktop environments and themes")
        print("  applications - User applications")
        print("  security    - Security tools and hardening")
        print("  system      - System configuration")
        sys.exit(0)

    # Parse command line arguments for section selection
    selected_sections = None
    if len(sys.argv) > 1:
        args = [arg for arg in sys.argv[1:] if arg not in ["--help", "-h"]]
        if args:
            selected_sections = args

    # Run the TUI
    try:
        exit_code = run_tui(selected_sections)
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nError: Failed to run TUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
