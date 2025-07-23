# Security Tools Role

This role installs a comprehensive suite of security testing, assessment, and privacy tools. 

**⚠️ WARNING**: These tools should only be used on systems you own or have explicit written permission to test. Unauthorized use may be illegal.

## Features

### Network Security Tools
- **Scanning**: Nmap/Zenmap, Masscan, RustScan, ARP-scan
- **Analysis**: Wireshark, tcpdump, tshark, EtherApe
- **Enumeration**: DNSrecon, DNSenum, Fierce, enum4linux
- **Framework**: Bettercap

### Vulnerability Scanners
- **Frameworks**: Metasploit, BeEF, Recon-ng
- **Web**: SQLMap, Nikto, OpenVAS/GVM
- **System**: Lynis, Searchsploit

### Web Security Tools
- **Proxies**: Burp Suite Community, OWASP ZAP
- **Scanners**: Dirb/DirBuster, Gobuster, WPScan
- **Testing**: WhatWeb, Wafw00f, SSLyze, testssl.sh
- **Exploitation**: XSStrike, Sublist3r, JWT_Tool

### Wireless Security
- **Frameworks**: Aircrack-ng, Kismet, Wifite2
- **GUI Tools**: Fern WiFi Cracker, LinSSID
- **Utilities**: Reaver, Bully, MDK3/4, WiFi Pumpkin

### Password Tools
- **Crackers**: John the Ripper, Hashcat, Hydra, Medusa
- **GUI**: Ophcrack, Johnny
- **Wordlists**: SecLists, rockyou
- **Generators**: Crunch, CeWL, RSMangler

### Digital Forensics
- **Frameworks**: Autopsy, Sleuth Kit, Volatility
- **Reverse Engineering**: Ghidra, Radare2/Cutter
- **File Recovery**: Foremost, Scalpel, PhotoRec
- **Analysis**: Binwalk, YARA, ExifTool

### Privacy Tools
- **Anonymous Browsing**: Tor, Tor Browser, I2P
- **Encryption**: VeraCrypt, Cryptomator, GnuPG
- **Proxies**: ProxyChains-NG, Torsocks
- **Metadata**: MAT2, OnionShare

### Container Security
- **Scanners**: Trivy, Grype, Clair
- **Analysis**: Dive, Syft, Docker Bench
- **Linters**: Hadolint, Dockle

### System Auditing
- **IDS/IPS**: OSSEC, Wazuh, Suricata, Snort
- **Monitoring**: Auditd, AIDE, Samhain
- **Rootkit Detection**: rkhunter, chkrootkit
- **Network Monitoring**: Zeek, Argus, NetFlow tools

### Development Security
- **Secret Scanning**: Gitleaks, TruffleHog, GitGuardian
- **SAST**: Semgrep, Bandit, Safety, Snyk
- **Dependency Check**: OWASP Dependency Check
- **Linters**: Various language-specific security linters

## Variables

```yaml
# Enable/disable tool categories
sectools_install_network_tools: false
sectools_install_vuln_scanners: false
sectools_install_web_tools: false
sectools_install_wireless_tools: false
sectools_install_password_tools: false
sectools_install_forensics: false
sectools_install_privacy_tools: false
sectools_install_container_tools: false
sectools_install_audit_tools: false
sectools_install_devsec_tools: false

# Use official repositories when available
sectools_use_official_repos: true

# Optional: Enable Kali/Parrot repositories
sectools_enable_kali_repo: false
sectools_enable_parrot_repo: false
```

## Example Playbook

```yaml
- hosts: all
  roles:
    - role: security-tools
      vars:
        sectools_install_network_tools: true
        sectools_install_web_tools: true
        sectools_install_privacy_tools: true
        sectools_network_tools:
          - nmap
          - zenmap
          - wireshark
        sectools_web_tools:
          - burpsuite
          - zaproxy
          - gobuster
        sectools_privacy_tools:
          - tor
          - torbrowser
          - veracrypt
```

## Ethical Use

These tools are provided for:
- Authorized penetration testing
- Security research
- Educational purposes
- Testing your own systems

Never use these tools on systems you don't own or lack permission to test.

## Tags

- `network-security`: Network security tools
- `vuln-scanners`: Vulnerability scanners
- `web-security`: Web application security tools
- `wireless`: Wireless security tools
- `password-tools`: Password cracking tools
- `forensics`: Digital forensics tools
- `privacy`: Privacy and encryption tools
- `container-security`: Container security tools
- `audit`: System auditing tools
- `devsec`: Development security tools