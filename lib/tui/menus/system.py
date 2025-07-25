#!/usr/bin/env python3
"""
System configuration menu for the Ubootu TUI
"""

from typing import Dict

from lib.tui.menus.base import MenuBuilder, MenuItem


class SystemMenuBuilder(MenuBuilder):
    """Builds the system configuration menu section"""

    def build(self) -> Dict[str, MenuItem]:
        """Build system menu structure"""
        self.items.clear()

        # Main system category
        self.add_category(
            "system",
            "System Configuration",
            "Performance, services, hardware, servers",
            parent="root",
            children=[
                "system-perf",
                "system-services",
                "system-webservers",
                "system-databases",
                "system-monitoring",
                "system-hardware",
            ],
        )

        # System subcategories
        self._build_performance()
        self._build_services()
        self._build_webservers()
        self._build_databases()
        self._build_monitoring()
        self._build_hardware()

        return self.items

    def _build_performance(self):
        """Build performance optimization menu"""
        self.add_category(
            "system-perf",
            "Performance",
            "CPU, memory, disk optimization",
            parent="system",
            children=[
                "preload",
                "zram",
                "profile-sync",
                "powertop",
                "cpu-governor",
                "swappiness",
            ],
        )

        self.add_selectable("preload", "Preload", "Application prefetching daemon", parent="system-perf")

        self.add_selectable("zram", "ZRAM", "Compressed RAM block device", parent="system-perf")

        self.add_selectable(
            "profile-sync",
            "Profile Sync Daemon",
            "Keep browser profiles in RAM",
            parent="system-perf",
        )

        self.add_selectable("powertop", "PowerTOP", "Power consumption analyzer", parent="system-perf")

        self.add_configurable(
            "cpu-governor",
            "CPU Governor",
            "CPU frequency scaling governor",
            parent="system-perf",
            config_type="dropdown",
            config_value="ondemand",
            config_options=[
                ("ondemand", "On Demand - Balance performance/power"),
                ("performance", "Performance - Maximum speed"),
                ("powersave", "Power Save - Maximum battery life"),
                ("conservative", "Conservative - Gradual scaling"),
                ("schedutil", "Schedutil - Scheduler-based scaling"),
            ],
            ansible_var="system_cpu_governor",
        )

        self.add_configurable(
            "swappiness",
            "Swappiness",
            "How aggressively kernel swaps memory",
            parent="system-perf",
            config_type="slider",
            config_range=(0, 100),
            config_value=10,
            config_unit="",
            ansible_var="system_swappiness",
        )

    def _build_services(self):
        """Build system services menu"""
        self.add_category(
            "system-services",
            "System Services",
            "SSH, file sharing, networking, backups",
            parent="system",
            children=[
                "ssh-server",
                "ssh-hardening",
                "ssh-keygen",
                "rsync-server",
                "samba",
                "nfs",
                "ftp-server",
                "cups",
                "cron-jobs",
                "systemd-timers",
                "dns-server",
                "dhcp-server",
                "vpn-server",
                "backup-tools",
            ],
        )

        # SSH and remote access
        self.add_selectable(
            "ssh-server",
            "SSH Server",
            "OpenSSH server for remote access",
            parent="system-services",
        )

        self.add_selectable(
            "ssh-hardening",
            "SSH Hardening",
            "Secure SSH configuration (key-only auth, etc.)",
            parent="system-services",
            ansible_var="system_ssh_hardening",
        )

        self.add_selectable(
            "ssh-keygen",
            "SSH Key Generation",
            "Generate SSH key pairs for secure access",
            parent="system-services",
            ansible_var="system_ssh_keygen",
        )

        self.add_selectable(
            "rsync-server",
            "Rsync Server",
            "File synchronization server",
            parent="system-services",
            ansible_var="system_rsync_server",
        )

        # File sharing
        self.add_selectable("samba", "Samba", "Windows file sharing", parent="system-services")

        self.add_selectable("nfs", "NFS Server", "Network File System server", parent="system-services")

        self.add_selectable(
            "ftp-server",
            "FTP Server (vsftpd)",
            "Very Secure FTP daemon",
            parent="system-services",
            ansible_var="system_ftp_server",
        )

        # System services
        self.add_selectable("cups", "CUPS", "Common Unix Printing System", parent="system-services")

        self.add_selectable(
            "cron-jobs",
            "Cron Jobs",
            "Scheduled task automation",
            parent="system-services",
            ansible_var="system_cron_jobs",
        )

        self.add_selectable(
            "systemd-timers",
            "Systemd Timers",
            "Modern scheduled tasks with systemd",
            parent="system-services",
            ansible_var="system_systemd_timers",
        )

        # Network services
        self.add_selectable(
            "dns-server",
            "DNS Server (Bind9)",
            "Domain Name System server",
            parent="system-services",
            ansible_var="system_dns_server",
        )

        self.add_selectable(
            "dhcp-server",
            "DHCP Server",
            "Dynamic Host Configuration Protocol server",
            parent="system-services",
            ansible_var="system_dhcp_server",
        )

        self.add_selectable(
            "vpn-server",
            "VPN Server (WireGuard)",
            "Modern VPN server",
            parent="system-services",
            ansible_var="system_vpn_server",
        )

        self.add_selectable(
            "backup-tools",
            "Backup Tools",
            "rsnapshot, borgbackup, restic",
            parent="system-services",
            ansible_var="system_backup_tools",
        )

    def _build_webservers(self):
        """Build web servers and proxies menu"""
        self.add_category(
            "system-webservers",
            "Web Servers & Proxies",
            "Nginx, Apache, reverse proxies, load balancers",
            parent="system",
            children=[
                "nginx",
                "nginx-modules",
                "apache2",
                "apache2-modules",
                "caddy",
                "haproxy",
                "traefik",
                "certbot",
                "ssl-certs",
            ],
        )

        # Web servers
        self.add_selectable(
            "nginx",
            "Nginx",
            "High-performance web server and reverse proxy",
            parent="system-webservers",
            ansible_var="webserver_nginx",
        )

        self.add_selectable(
            "nginx-modules",
            "Nginx Modules",
            "Additional Nginx modules (ModSecurity, etc.)",
            parent="system-webservers",
            ansible_var="webserver_nginx_modules",
        )

        self.add_selectable(
            "apache2",
            "Apache2",
            "Apache HTTP Server",
            parent="system-webservers",
            ansible_var="webserver_apache2",
        )

        self.add_selectable(
            "apache2-modules",
            "Apache2 Modules",
            "mod_security, mod_rewrite, mod_ssl, etc.",
            parent="system-webservers",
            ansible_var="webserver_apache2_modules",
        )

        self.add_selectable(
            "caddy",
            "Caddy",
            "Modern web server with automatic HTTPS",
            parent="system-webservers",
            ansible_var="webserver_caddy",
        )

        # Proxies and load balancers
        self.add_selectable(
            "haproxy",
            "HAProxy",
            "High-performance load balancer",
            parent="system-webservers",
            ansible_var="webserver_haproxy",
        )

        self.add_selectable(
            "traefik",
            "Traefik",
            "Modern reverse proxy with auto-discovery",
            parent="system-webservers",
            ansible_var="webserver_traefik",
        )

        # SSL/TLS
        self.add_selectable(
            "certbot",
            "Certbot",
            "Let's Encrypt certificate automation",
            parent="system-webservers",
            ansible_var="webserver_certbot",
        )

        self.add_selectable(
            "ssl-certs",
            "SSL Certificate Tools",
            "OpenSSL, certificate management utilities",
            parent="system-webservers",
            ansible_var="webserver_ssl_tools",
        )

    def _build_databases(self):
        """Build databases menu"""
        self.add_category(
            "system-databases",
            "Databases",
            "SQL, NoSQL, caching, and search engines",
            parent="system",
            children=[
                "postgresql",
                "mysql",
                "mariadb",
                "mongodb",
                "redis",
                "elasticsearch",
                "sqlite3",
                "memcached",
                "influxdb",
            ],
        )

        # SQL databases
        self.add_selectable(
            "postgresql",
            "PostgreSQL",
            "Advanced open-source relational database",
            parent="system-databases",
            ansible_var="db_postgresql",
        )

        self.add_selectable(
            "mysql",
            "MySQL",
            "Popular open-source relational database",
            parent="system-databases",
            ansible_var="db_mysql",
        )

        self.add_selectable(
            "mariadb",
            "MariaDB",
            "MySQL fork with enhanced features",
            parent="system-databases",
            ansible_var="db_mariadb",
        )

        self.add_selectable(
            "sqlite3",
            "SQLite3",
            "Lightweight embedded database",
            parent="system-databases",
            ansible_var="db_sqlite3",
        )

        # NoSQL databases
        self.add_selectable(
            "mongodb",
            "MongoDB",
            "Document-oriented NoSQL database",
            parent="system-databases",
            ansible_var="db_mongodb",
        )

        self.add_selectable(
            "redis",
            "Redis",
            "In-memory data structure store",
            parent="system-databases",
            ansible_var="db_redis",
        )

        self.add_selectable(
            "elasticsearch",
            "Elasticsearch",
            "Distributed search and analytics engine",
            parent="system-databases",
            ansible_var="db_elasticsearch",
        )

        # Caching
        self.add_selectable(
            "memcached",
            "Memcached",
            "High-performance memory caching system",
            parent="system-databases",
            ansible_var="db_memcached",
        )

        # Time series
        self.add_selectable(
            "influxdb",
            "InfluxDB",
            "Time series database for metrics",
            parent="system-databases",
            ansible_var="db_influxdb",
        )

    def _build_monitoring(self):
        """Build monitoring and management tools menu"""
        self.add_category(
            "system-monitoring",
            "Monitoring & Management",
            "System monitoring, metrics, and management tools",
            parent="system",
            children=[
                "prometheus",
                "grafana",
                "netdata",
                "zabbix-agent",
                "nagios",
                "glances",
                "cockpit",
                "webmin",
                "fail2ban",
                "logwatch",
            ],
        )

        # Metrics and monitoring
        self.add_selectable(
            "prometheus",
            "Prometheus",
            "Monitoring system and time series database",
            parent="system-monitoring",
            ansible_var="monitor_prometheus",
        )

        self.add_selectable(
            "grafana",
            "Grafana",
            "Analytics and monitoring dashboard",
            parent="system-monitoring",
            ansible_var="monitor_grafana",
        )

        self.add_selectable(
            "netdata",
            "Netdata",
            "Real-time performance monitoring",
            parent="system-monitoring",
            ansible_var="monitor_netdata",
        )

        self.add_selectable(
            "zabbix-agent",
            "Zabbix Agent",
            "Enterprise monitoring agent",
            parent="system-monitoring",
            ansible_var="monitor_zabbix_agent",
        )

        self.add_selectable(
            "nagios",
            "Nagios",
            "IT infrastructure monitoring",
            parent="system-monitoring",
            ansible_var="monitor_nagios",
        )

        self.add_selectable(
            "glances",
            "Glances",
            "Cross-platform system monitoring",
            parent="system-monitoring",
            ansible_var="monitor_glances",
        )

        # Management interfaces
        self.add_selectable(
            "cockpit",
            "Cockpit",
            "Web-based server management interface",
            parent="system-monitoring",
            ansible_var="monitor_cockpit",
        )

        self.add_selectable(
            "webmin",
            "Webmin",
            "Web-based system administration",
            parent="system-monitoring",
            ansible_var="monitor_webmin",
        )

        # Log monitoring and security
        self.add_selectable(
            "fail2ban",
            "Fail2ban",
            "Intrusion prevention system",
            parent="system-monitoring",
        )

        self.add_selectable(
            "logwatch",
            "Logwatch",
            "Log analysis and reporting",
            parent="system-monitoring",
            ansible_var="monitor_logwatch",
        )

    def _build_hardware(self):
        """Build hardware support menu"""
        self.add_category(
            "system-hardware",
            "Hardware Support",
            "Drivers, firmware, peripherals",
            parent="system",
            children=["nvidia-drivers", "amd-drivers", "bluetooth", "printers"],
        )

        self.add_selectable(
            "nvidia-drivers",
            "NVIDIA Drivers",
            "Proprietary NVIDIA graphics drivers",
            parent="system-hardware",
        )

        self.add_selectable(
            "amd-drivers",
            "AMD Drivers",
            "AMD graphics drivers and firmware",
            parent="system-hardware",
        )

        self.add_selectable(
            "bluetooth",
            "Bluetooth Support",
            "Bluetooth hardware support",
            parent="system-hardware",
        )

        self.add_selectable(
            "printers",
            "Printer Support",
            "Additional printer drivers",
            parent="system-hardware",
        )
