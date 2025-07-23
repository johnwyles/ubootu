# Security Role

This role implements comprehensive security hardening for Ubuntu desktop systems.

## Features

### Firewall Configuration
- UFW (Uncomplicated Firewall) setup with sensible defaults
- Rate limiting for SSH connections
- Automatic detection and configuration for installed services

### SSH Hardening
- Disable root login
- Disable password authentication (key-only)
- Configure secure ciphers and MACs
- Set up connection timeouts and limits
- Banner configuration

### Fail2ban
- Protection against brute force attacks
- Automatic banning of malicious IPs
- Pre-configured jails for SSH and common services

### Password Managers
- Support for multiple password managers:
  - KeePassXC
  - Bitwarden
  - 1Password
  - Enpass
  - pass (command-line)

### System Hardening
- Kernel parameter tuning
- Network security settings
- Disable unused filesystems and protocols
- AppArmor enforcement
- Secure shared memory
- Login configuration
- File permission hardening

### Additional Security Features
- ClamAV antivirus with scheduled scans
- Automatic security updates
- SSH key generation
- Security limits configuration

## Variables

Key variables that can be configured:

```yaml
# Firewall
enable_firewall: true
firewall_allowed_ports:
  - 22/tcp
  - 80/tcp
  - 443/tcp

# SSH
ssh_permit_root_login: false
ssh_password_authentication: false
ssh_port: 22

# Fail2ban
enable_fail2ban: true
fail2ban_bantime: 3600
fail2ban_maxretry: 3

# Password managers
password_managers: []  # Options: keepassxc, bitwarden, 1password, enpass, pass

# Antivirus
install_clamav: false
clamav_scan_schedule: "daily"

# Updates
enable_automatic_updates: true
automatic_updates_reboot: false

# SSH keys
generate_ssh_keys: false
ssh_key_type: "ed25519"
```

## Dependencies

- `common` role (for base system setup)

## Example Playbook

```yaml
- hosts: all
  roles:
    - role: security
      vars:
        enable_firewall: true
        enable_fail2ban: true
        password_managers:
          - keepassxc
          - bitwarden
        generate_ssh_keys: true
        ssh_key_type: ed25519
```

## Tags

- `firewall`: Firewall configuration
- `ssh`: SSH hardening
- `fail2ban`: Fail2ban setup
- `password-managers`: Password manager installation
- `antivirus`: ClamAV setup
- `updates`: Automatic updates
- `hardening`: System hardening
- `ssh-keys`: SSH key generation