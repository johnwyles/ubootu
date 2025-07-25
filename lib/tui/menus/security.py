#!/usr/bin/env python3
"""
Security menu for the Ubootu TUI
"""

from typing import Dict

from lib.tui.menus.base import MenuBuilder, MenuItem


class SecurityMenuBuilder(MenuBuilder):
    """Builds the security menu section"""

    def build(self) -> Dict[str, MenuItem]:
        """Build security menu structure"""
        self.items.clear()

        # Main security category
        self.add_category(
            "security",
            "Security & Privacy",
            "Firewalls, encryption, privacy tools",
            parent="root",
            children=["security-basic", "security-tools", "security-privacy"],
        )

        # Security subcategories
        self._build_basic_security()
        self._build_security_tools()
        self._build_privacy_tools()

        return self.items

    def _build_basic_security(self):
        """Build basic security measures menu"""
        self.add_category(
            "security-basic",
            "Basic Security",
            "Firewall, antivirus, updates",
            parent="security",
            children=["ufw-firewall", "clamav", "auto-updates", "fail2ban"],
        )

        self.add_selectable(
            "ufw-firewall",
            "UFW Firewall",
            "Uncomplicated Firewall for Ubuntu",
            parent="security-basic",
            default=True,
        )

        self.add_selectable(
            "clamav", "ClamAV", "Open source antivirus", parent="security-basic"
        )

        self.add_selectable(
            "auto-updates",
            "Automatic Updates",
            "Enable automatic security updates",
            parent="security-basic",
            default=True,
        )

        self.add_selectable(
            "fail2ban",
            "Fail2Ban",
            "Intrusion prevention system",
            parent="security-basic",
        )

    def _build_security_tools(self):
        """Build penetration testing and security tools menu"""
        self.add_category(
            "security-tools",
            "Security Tools",
            "Penetration testing, auditing",
            parent="security",
            children=[
                "nmap",
                "wireshark",
                "metasploit",
                "burpsuite",
                "john",
                "hashcat",
                "aircrack-ng",
                "hydra",
                "sqlmap",
                "nikto",
                "dirb",
                "gobuster",
                "ffuf",
                "wfuzz",
                "zaproxy",
                "beef",
                "maltego",
                "recon-ng",
                "theharvester",
                "shodan",
                "masscan",
                "ettercap",
                "bettercap",
                "mitmproxy",
                "responder",
                "impacket",
                "crackmapexec",
                "bloodhound",
                "empire",
                "covenant",
                "cobalt-strike",
            ],
        )

        # Network scanning tools
        self.add_selectable(
            "nmap",
            "Nmap",
            "Network discovery and security auditing",
            parent="security-tools",
        )

        self.add_selectable(
            "wireshark",
            "Wireshark",
            "Network protocol analyzer",
            parent="security-tools",
        )

        self.add_selectable(
            "masscan",
            "Masscan",
            "Fast port scanner",
            parent="security-tools",
            ansible_var="security_tools_masscan",
        )

        # Penetration testing frameworks
        self.add_selectable(
            "metasploit",
            "Metasploit",
            "Penetration testing framework",
            parent="security-tools",
        )

        self.add_selectable(
            "burpsuite",
            "Burp Suite",
            "Web application security testing",
            parent="security-tools",
        )

        # Password cracking tools
        self.add_selectable(
            "john", "John the Ripper", "Password cracking tool", parent="security-tools"
        )

        self.add_selectable(
            "hashcat",
            "Hashcat",
            "Advanced password recovery",
            parent="security-tools",
            ansible_var="security_tools_hashcat",
        )

        self.add_selectable(
            "hydra",
            "Hydra",
            "Network logon cracker",
            parent="security-tools",
            ansible_var="security_tools_hydra",
        )

        # Wireless security
        self.add_selectable(
            "aircrack-ng",
            "Aircrack-ng",
            "WiFi security auditing",
            parent="security-tools",
            ansible_var="security_tools_aircrack_ng",
        )

        # Web application testing
        self.add_selectable(
            "sqlmap",
            "SQLMap",
            "SQL injection tool",
            parent="security-tools",
            ansible_var="security_tools_sqlmap",
        )

        self.add_selectable(
            "nikto",
            "Nikto",
            "Web server scanner",
            parent="security-tools",
            ansible_var="security_tools_nikto",
        )

        self.add_selectable(
            "dirb",
            "DIRB",
            "Web content scanner",
            parent="security-tools",
            ansible_var="security_tools_dirb",
        )

        self.add_selectable(
            "gobuster",
            "Gobuster",
            "Directory/file brute-forcer",
            parent="security-tools",
            ansible_var="security_tools_gobuster",
        )

        self.add_selectable(
            "ffuf",
            "FFUF",
            "Fast web fuzzer",
            parent="security-tools",
            ansible_var="security_tools_ffuf",
        )

        self.add_selectable(
            "wfuzz",
            "Wfuzz",
            "Web application fuzzer",
            parent="security-tools",
            ansible_var="security_tools_wfuzz",
        )

        self.add_selectable(
            "zaproxy",
            "OWASP ZAP",
            "Web app security scanner",
            parent="security-tools",
            ansible_var="security_tools_zaproxy",
        )

        # Browser exploitation
        self.add_selectable(
            "beef",
            "BeEF",
            "Browser exploitation framework",
            parent="security-tools",
            ansible_var="security_tools_beef",
        )

        # OSINT and reconnaissance
        self.add_selectable(
            "maltego",
            "Maltego",
            "OSINT and forensics",
            parent="security-tools",
            ansible_var="security_tools_maltego",
        )

        self.add_selectable(
            "recon-ng",
            "Recon-ng",
            "Web reconnaissance framework",
            parent="security-tools",
            ansible_var="security_tools_recon_ng",
        )

        self.add_selectable(
            "theharvester",
            "theHarvester",
            "E-mail and subdomain harvester",
            parent="security-tools",
            ansible_var="security_tools_theharvester",
        )

        self.add_selectable(
            "shodan",
            "Shodan CLI",
            "Internet device scanner",
            parent="security-tools",
            ansible_var="security_tools_shodan",
        )

        # Network attack tools
        self.add_selectable(
            "ettercap",
            "Ettercap",
            "Network security tool",
            parent="security-tools",
            ansible_var="security_tools_ettercap",
        )

        self.add_selectable(
            "bettercap",
            "Bettercap",
            "Network attack tool",
            parent="security-tools",
            ansible_var="security_tools_bettercap",
        )

        self.add_selectable(
            "mitmproxy",
            "mitmproxy",
            "Interactive HTTPS proxy",
            parent="security-tools",
            ansible_var="security_tools_mitmproxy",
        )

        # Active Directory tools
        self.add_selectable(
            "responder",
            "Responder",
            "LLMNR/NBT-NS/MDNS poisoner",
            parent="security-tools",
            ansible_var="security_tools_responder",
        )

        self.add_selectable(
            "impacket",
            "Impacket",
            "Network protocols toolkit",
            parent="security-tools",
            ansible_var="security_tools_impacket",
        )

        self.add_selectable(
            "crackmapexec",
            "CrackMapExec",
            "Network pentesting toolkit",
            parent="security-tools",
            ansible_var="security_tools_crackmapexec",
        )

        self.add_selectable(
            "bloodhound",
            "BloodHound",
            "AD attack path mapping",
            parent="security-tools",
            ansible_var="security_tools_bloodhound",
        )

        # Post-exploitation frameworks
        self.add_selectable(
            "empire",
            "Empire",
            "Post-exploitation framework",
            parent="security-tools",
            ansible_var="security_tools_empire",
        )

        self.add_selectable(
            "covenant",
            "Covenant",
            "C2 framework",
            parent="security-tools",
            ansible_var="security_tools_covenant",
        )

        self.add_selectable(
            "cobalt-strike",
            "Cobalt Strike",
            "Adversary simulation",
            parent="security-tools",
            ansible_var="security_tools_cobalt_strike",
        )

    def _build_privacy_tools(self):
        """Build privacy and encryption tools menu"""
        self.add_category(
            "security-privacy",
            "Privacy Tools",
            "VPN, encryption, anonymous browsing",
            parent="security",
            children=[
                "tor-browser",
                "veracrypt",
                "cryptomator",
                "keepassxc",
                "bitwarden",
                "1password",
                "enpass",
                "pass",
                "gopass",
                "buttercup",
                "keeweb",
                "protonvpn",
                "mullvad-vpn",
                "expressvpn",
                "nordvpn",
                "surfshark",
                "windscribe",
                "ivpn",
                "privateinternetaccess",
                "signal",
                "session",
                "briar",
                "element",
                "jami",
                "onionshare",
                "mat2",
                "bleachbit",
                "secure-delete",
                "wipe",
                "gnupg",
                "kleopatra",
                "seahorse",
            ],
        )

        # Anonymous browsing
        self.add_selectable(
            "tor-browser",
            "Tor Browser",
            "Anonymous web browsing",
            parent="security-privacy",
        )

        # Encryption tools
        self.add_selectable(
            "veracrypt",
            "VeraCrypt",
            "Disk encryption software",
            parent="security-privacy",
        )

        self.add_selectable(
            "cryptomator",
            "Cryptomator",
            "Cloud encryption",
            parent="security-privacy",
            ansible_var="privacy_cryptomator",
        )

        # Password managers
        self.add_selectable(
            "keepassxc",
            "KeePassXC",
            "Password manager",
            parent="security-privacy",
            default=True,
        )

        self.add_selectable(
            "bitwarden",
            "Bitwarden",
            "Password manager",
            parent="security-privacy",
            ansible_var="privacy_bitwarden",
        )

        self.add_selectable(
            "1password",
            "1Password",
            "Password manager",
            parent="security-privacy",
            ansible_var="privacy_1password",
        )

        self.add_selectable(
            "enpass",
            "Enpass",
            "Password manager",
            parent="security-privacy",
            ansible_var="privacy_enpass",
        )

        self.add_selectable(
            "pass",
            "Pass",
            "Unix password manager",
            parent="security-privacy",
            ansible_var="privacy_pass",
        )

        self.add_selectable(
            "gopass",
            "Gopass",
            "Team password manager",
            parent="security-privacy",
            ansible_var="privacy_gopass",
        )

        self.add_selectable(
            "buttercup",
            "Buttercup",
            "Password manager",
            parent="security-privacy",
            ansible_var="privacy_buttercup",
        )

        self.add_selectable(
            "keeweb",
            "KeeWeb",
            "Web-based password manager",
            parent="security-privacy",
            ansible_var="privacy_keeweb",
        )

        # VPN services
        self.add_selectable(
            "protonvpn", "ProtonVPN", "Secure VPN service", parent="security-privacy"
        )

        self.add_selectable(
            "mullvad-vpn",
            "Mullvad VPN",
            "Privacy-focused VPN",
            parent="security-privacy",
            ansible_var="privacy_mullvad_vpn",
        )

        self.add_selectable(
            "expressvpn",
            "ExpressVPN",
            "Fast VPN service",
            parent="security-privacy",
            ansible_var="privacy_expressvpn",
        )

        self.add_selectable(
            "nordvpn",
            "NordVPN",
            "Popular VPN service",
            parent="security-privacy",
            ansible_var="privacy_nordvpn",
        )

        self.add_selectable(
            "surfshark",
            "Surfshark",
            "VPN service",
            parent="security-privacy",
            ansible_var="privacy_surfshark",
        )

        self.add_selectable(
            "windscribe",
            "Windscribe",
            "VPN with free tier",
            parent="security-privacy",
            ansible_var="privacy_windscribe",
        )

        self.add_selectable(
            "ivpn",
            "IVPN",
            "Privacy-focused VPN",
            parent="security-privacy",
            ansible_var="privacy_ivpn",
        )

        self.add_selectable(
            "privateinternetaccess",
            "PIA VPN",
            "Private Internet Access",
            parent="security-privacy",
            ansible_var="privacy_pia",
        )

        # Secure messaging
        self.add_selectable(
            "signal", "Signal", "Secure messaging app", parent="security-privacy"
        )

        self.add_selectable(
            "session",
            "Session",
            "Anonymous messenger",
            parent="security-privacy",
            ansible_var="privacy_session",
        )

        self.add_selectable(
            "briar",
            "Briar",
            "Secure messaging",
            parent="security-privacy",
            ansible_var="privacy_briar",
        )

        self.add_selectable(
            "element",
            "Element",
            "Matrix client for secure chat",
            parent="security-privacy",
        )

        self.add_selectable(
            "jami",
            "Jami",
            "P2P communication",
            parent="security-privacy",
            ansible_var="privacy_jami",
        )

        # Privacy tools
        self.add_selectable(
            "onionshare",
            "OnionShare",
            "Anonymous file sharing",
            parent="security-privacy",
            ansible_var="privacy_onionshare",
        )

        self.add_selectable(
            "mat2",
            "MAT2",
            "Metadata removal tool",
            parent="security-privacy",
            ansible_var="privacy_mat2",
        )

        self.add_selectable(
            "bleachbit",
            "BleachBit",
            "System cleaner",
            parent="security-privacy",
            ansible_var="privacy_bleachbit",
        )

        # Secure deletion
        self.add_selectable(
            "secure-delete",
            "Secure Delete",
            "Secure file deletion",
            parent="security-privacy",
            ansible_var="privacy_secure_delete",
        )

        self.add_selectable(
            "wipe",
            "Wipe",
            "Secure file wiping",
            parent="security-privacy",
            ansible_var="privacy_wipe",
        )

        # Encryption/signing tools
        self.add_selectable(
            "gnupg",
            "GnuPG",
            "Encryption tools",
            parent="security-privacy",
            ansible_var="privacy_gnupg",
        )

        self.add_selectable(
            "kleopatra",
            "Kleopatra",
            "Certificate manager",
            parent="security-privacy",
            ansible_var="privacy_kleopatra",
        )

        self.add_selectable(
            "seahorse",
            "Seahorse",
            "GNOME keyring manager",
            parent="security-privacy",
            ansible_var="privacy_seahorse",
        )
