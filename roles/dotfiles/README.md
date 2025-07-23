# Dotfiles Role

This role manages user configuration files (dotfiles) for various applications and tools.

## Features

- **Shell Configuration**: Bash, Zsh, Fish shell customization with aliases and functions
- **Git Configuration**: User settings, aliases, global gitignore
- **Vim/Neovim**: Plugin management, custom configuration, color schemes
- **tmux**: Custom key bindings, plugin management, theme configuration
- **SSH**: Client configuration with host entries
- **VS Code**: Settings, keybindings, snippets
- **Dotfiles Management**: Support for GNU Stow, chezmoi, or yadm

## Variables

Key variables that can be configured:

```yaml
# Dotfiles repository
dotfiles_repo: ""  # Your dotfiles Git repository URL

# What to manage
managed_dotfiles:
  - shell
  - git
  - vim
  - tmux
  - ssh
  - vscode

# Shell aliases
shell_custom_aliases:
  - { alias: 'll', command: 'ls -alF' }
  - { alias: 'gs', command: 'git status' }

# Git configuration
git_user_name: "Your Name"
git_user_email: "your.email@example.com"
git_default_branch: "main"

# Vim settings
vim_colorscheme: "dracula"
vim_enable_plugins: true

# tmux settings
tmux_prefix_key: "C-a"
tmux_enable_mouse: true

# Dotfiles manager
dotfiles_use_manager: true
dotfiles_manager: "stow"  # Options: stow, chezmoi, yadm
```

## Dependencies

None

## Example Playbook

```yaml
- hosts: all
  roles:
    - role: dotfiles
      vars:
        managed_dotfiles:
          - shell
          - git
          - vim
          - tmux
        git_user_name: "John Doe"
        git_user_email: "john@example.com"
        vim_colorscheme: "gruvbox"
        tmux_enable_mouse: true
        dotfiles_use_manager: true
        dotfiles_manager: "stow"
```

## Tags

- `clone`: Clone existing dotfiles repository
- `shell`: Configure shell (bash/zsh/fish)
- `git`: Configure Git
- `vim`: Configure Vim/Neovim
- `tmux`: Configure tmux
- `ssh`: Configure SSH client
- `vscode`: Configure VS Code
- `manager`: Set up dotfiles manager

## Dotfiles Managers

### GNU Stow
Creates a `~/dotfiles` directory structure where each application has its own subdirectory. Use `stow <app>` to create symlinks.

### chezmoi
A dotfiles manager that supports templating, encryption, and multiple machines.

### yadm
Yet Another Dotfiles Manager - Git-based with built-in support for alternate files and encryption.

## Custom Functions

The role adds several useful shell functions:
- `mkcd`: Create directory and cd into it
- `extract`: Extract various archive formats
- `backup`: Create timestamped backup of a file