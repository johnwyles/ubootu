# Ubuntu Package Compatibility Guide

## Supported Ubuntu Versions
- Ubuntu 22.04 LTS (Jammy Jellyfish)
- Ubuntu 24.04 LTS (Noble Numbat)
- Ubuntu 24.10 (Oracular Oriole)
- Ubuntu 25.04 (Plucky Puffin) - Development

## Package Installation Methods

### APT Packages (Preferred)
Most packages are installed via APT from official Ubuntu repositories or trusted third-party PPAs.

### Snap Packages
Some applications are available only as snaps or work better as snaps:
- **Discord** - Only available as snap
- **Spotify** - Snap recommended for auto-updates
- **VS Code** - Available as both APT and snap
- **Slack** - Available as both APT and snap
- **Teams** - Snap version more stable
- **Postman** - Snap only
- **DBeaver** - Available as both

### Flatpak Packages
Alternative for sandboxed applications:
- **Bottles** - Windows app compatibility
- **Flatseal** - Flatpak permissions manager
- **Extension Manager** - GNOME extensions

## Known Compatibility Issues

### Ubuntu 24.04+ Changes
- **PPA Format**: Some older PPAs may not have Noble/Oracular support
- **Python**: Default is Python 3.12+, some tools may need compatibility updates
- **Wayland**: Default session, X11 apps may need XWayland

### Package-Specific Notes

#### Development Tools
- **Docker**: Use official Docker repository, not Ubuntu's docker.io package
- **Node.js**: Use NodeSource repository for latest versions
- **Go**: Use official Go snap or binary installation

#### Desktop Environments
- **GNOME**: Version differs between LTS and non-LTS releases
- **KDE Plasma**: Use Kubuntu backports PPA for latest version
- **Extensions**: GNOME extensions need version-specific compatibility

#### System Tools
- **systemd**: Version differences may affect service files
- **NetworkManager**: Configuration format changes between versions

## Repository Fallbacks

When a repository doesn't support the current Ubuntu version, the system falls back to the previous LTS:
- Plucky (25.04) → Noble (24.04)
- Oracular (24.10) → Noble (24.04)

## Testing Recommendations

1. Always test in a VM first for production systems
2. Check package availability: `apt-cache policy <package>`
3. Verify snap availability: `snap find <package>`
4. Review third-party repository support before upgrading Ubuntu

## Troubleshooting

### APT Issues
```bash
# Fix broken packages
sudo apt --fix-broken install

# Clean package cache
sudo apt clean && sudo apt autoclean

# Update repository info
sudo apt update
```

### Snap Issues
```bash
# Refresh snaps
sudo snap refresh

# Check snap services
snap services
```

### Repository Issues
- Missing GPG keys: Keys are stored in `/usr/share/keyrings/`
- Duplicate sources: Check `/etc/apt/sources.list.d/`
- Outdated mirrors: Update `/etc/apt/sources.list`