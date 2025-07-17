# Applications Role

This role installs and configures common desktop applications based on user preferences.

## Features

- **Web Browsers**: Chrome, Chromium, Brave, Vivaldi, Edge
- **Communication**: Slack, Discord, Teams, Zoom, Signal, Telegram
- **Productivity**: LibreOffice, Obsidian, Notion, Thunderbird, Evolution, Joplin
- **Multimedia**: VLC, Spotify, GIMP, Inkscape, OBS Studio, Kdenlive, Audacity
- **Cloud Storage**: Dropbox, Google Drive (Insync), OneDrive, Nextcloud
- **Utilities**: System tools, archive managers, PDF tools, screenshot tools

## Variables

Key variables that can be configured:

```yaml
# Web browsers to install (besides Firefox)
web_browsers: []  # Options: google-chrome, chromium, brave, vivaldi, edge

# Default browser
default_browser: firefox

# Communication apps
communication_apps: []  # Options: slack, discord, teams, zoom, signal, telegram

# Productivity
install_libreoffice: true
productivity_apps: []  # Options: obsidian, notion, thunderbird, evolution, joplin

# Multimedia
multimedia_apps:
  - vlc
  - gimp

# Cloud storage
cloud_storage: []  # Options: dropbox, insync, onedrive, nextcloud
```

## Dependencies

- `common` role (for base system setup)

## Example Playbook

```yaml
- hosts: all
  roles:
    - role: applications
      vars:
        web_browsers:
          - brave
          - google-chrome
        default_browser: brave
        communication_apps:
          - discord
          - signal
        multimedia_apps:
          - vlc
          - spotify
          - obs-studio
```

## Tags

- `browsers`: Install web browsers
- `communication`: Install communication apps
- `productivity`: Install productivity apps
- `multimedia`: Install multimedia apps
- `cloud`: Install cloud storage clients
- `utilities`: Install system utilities
- `defaults`: Configure default applications