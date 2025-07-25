#!/usr/bin/env python3
"""
Applications menu for the Ubootu TUI
"""

from typing import Dict

from lib.tui.menus.base import MenuBuilder, MenuItem


class ApplicationsMenuBuilder(MenuBuilder):
    """Builds the applications menu section"""

    def build(self) -> Dict[str, MenuItem]:
        """Build applications menu structure"""
        self.items.clear()

        # Main applications category
        self.add_category(
            "applications",
            "Applications",
            "Web browsers, media players, productivity tools",
            parent="root",
            children=[
                "app-browsers",
                "app-media",
                "app-productivity",
                "app-communication",
            ],
        )

        # Application subcategories
        self._build_browsers()
        self._build_media()
        self._build_productivity()
        self._build_communication()

        return self.items

    def _build_browsers(self):
        """Build web browsers menu"""
        self.add_category(
            "app-browsers",
            "Web Browsers",
            "Internet browsers",
            parent="applications",
            children=[
                "firefox",
                "firefox-developer",
                "chrome",
                "chromium",
                "brave",
                "opera",
                "vivaldi",
                "edge",
                "waterfox",
                "librewolf",
                "tor-browser",
                "min",
                "qutebrowser",
                "midori",
                "epiphany",
                "falkon",
                "seamonkey",
                "palemoon",
                "basilisk",
                "ungoogled-chromium",
            ],
        )

        # Browser items
        self.add_selectable(
            "firefox",
            "Firefox",
            "Mozilla Firefox web browser",
            parent="app-browsers",
            default=True,
        )

        self.add_selectable(
            "firefox-developer",
            "Firefox Developer Edition",
            "Browser for developers",
            parent="app-browsers",
        )

        self.add_selectable(
            "chrome",
            "Google Chrome",
            "Google Chrome web browser",
            parent="app-browsers",
        )

        self.add_selectable(
            "chromium", "Chromium", "Open source browser", parent="app-browsers"
        )

        self.add_selectable(
            "brave", "Brave Browser", "Privacy-focused browser", parent="app-browsers"
        )

        self.add_selectable(
            "opera", "Opera", "Feature-rich web browser", parent="app-browsers"
        )

        self.add_selectable(
            "vivaldi", "Vivaldi", "Customizable browser", parent="app-browsers"
        )

        self.add_selectable(
            "edge", "Microsoft Edge", "Microsoft's browser", parent="app-browsers"
        )

        self.add_selectable(
            "waterfox", "Waterfox", "Firefox-based browser", parent="app-browsers"
        )

        self.add_selectable(
            "librewolf", "LibreWolf", "Privacy-hardened Firefox", parent="app-browsers"
        )

        self.add_selectable(
            "tor-browser",
            "Tor Browser",
            "Anonymous web browsing",
            parent="app-browsers",
        )

        self.add_selectable(
            "min", "Min Browser", "Minimal web browser", parent="app-browsers"
        )

        self.add_selectable(
            "qutebrowser",
            "qutebrowser",
            "Keyboard-driven browser",
            parent="app-browsers",
        )

        self.add_selectable(
            "midori", "Midori", "Lightweight web browser", parent="app-browsers"
        )

        self.add_selectable(
            "epiphany",
            "GNOME Web (Epiphany)",
            "GNOME's web browser",
            parent="app-browsers",
        )

        self.add_selectable(
            "falkon", "Falkon", "KDE web browser", parent="app-browsers"
        )

        self.add_selectable(
            "seamonkey", "SeaMonkey", "Internet suite", parent="app-browsers"
        )

        self.add_selectable(
            "palemoon", "Pale Moon", "Firefox-based browser", parent="app-browsers"
        )

        self.add_selectable(
            "basilisk", "Basilisk", "Firefox-based browser", parent="app-browsers"
        )

        self.add_selectable(
            "ungoogled-chromium",
            "Ungoogled Chromium",
            "De-googled Chromium",
            parent="app-browsers",
        )

    def _build_media(self):
        """Build media and entertainment menu"""
        self.add_category(
            "app-media",
            "Media & Entertainment",
            "Music, video, image viewers",
            parent="applications",
            children=[
                "vlc",
                "mpv",
                "celluloid",
                "smplayer",
                "spotify",
                "rhythmbox",
                "clementine",
                "strawberry",
                "audacious",
                "lollypop",
                "gimp",
                "krita",
                "inkscape",
                "darktable",
                "rawtherapee",
                "digikam",
                "audacity",
                "ardour",
                "lmms",
                "hydrogen",
                "blender",
                "freecad",
                "openscad",
                "kdenlive",
                "shotcut",
                "openshot",
                "pitivi",
                "davinci-resolve",
                "obs-studio",
                "simplescreenrecorder",
                "kazam",
                "peek",
                "flameshot",
                "shutter",
            ],
        )

        # Video players
        self.add_selectable(
            "vlc",
            "VLC Media Player",
            "Versatile media player",
            parent="app-media",
            default=True,
        )

        self.add_selectable(
            "mpv", "mpv", "Lightweight video player", parent="app-media"
        )

        self.add_selectable(
            "celluloid", "Celluloid", "Simple GTK+ frontend for mpv", parent="app-media"
        )

        self.add_selectable(
            "smplayer", "SMPlayer", "Feature-rich media player", parent="app-media"
        )

        # Music players
        self.add_selectable(
            "spotify", "Spotify", "Music streaming service", parent="app-media"
        )

        self.add_selectable(
            "rhythmbox", "Rhythmbox", "GNOME music player", parent="app-media"
        )

        self.add_selectable(
            "clementine",
            "Clementine",
            "Music player and library organizer",
            parent="app-media",
        )

        self.add_selectable(
            "strawberry", "Strawberry", "Modern music player", parent="app-media"
        )

        self.add_selectable(
            "audacious", "Audacious", "Lightweight audio player", parent="app-media"
        )

        self.add_selectable(
            "lollypop", "Lollypop", "Modern music player", parent="app-media"
        )

        # Image editors
        self.add_selectable(
            "gimp",
            "GIMP",
            "GNU Image Manipulation Program",
            parent="app-media",
            default=True,
        )

        self.add_selectable(
            "krita", "Krita", "Digital painting application", parent="app-media"
        )

        self.add_selectable(
            "inkscape", "Inkscape", "Vector graphics editor", parent="app-media"
        )

        self.add_selectable(
            "darktable", "darktable", "Photography workflow", parent="app-media"
        )

        self.add_selectable(
            "rawtherapee", "RawTherapee", "Raw image processing", parent="app-media"
        )

        self.add_selectable(
            "digikam", "digiKam", "Photo management", parent="app-media"
        )

        # Audio production
        self.add_selectable(
            "audacity", "Audacity", "Audio editing software", parent="app-media"
        )

        self.add_selectable(
            "ardour", "Ardour", "Digital audio workstation", parent="app-media"
        )

        self.add_selectable(
            "lmms", "LMMS", "Music production suite", parent="app-media"
        )

        self.add_selectable("hydrogen", "Hydrogen", "Drum machine", parent="app-media")

        # 3D and CAD
        self.add_selectable(
            "blender", "Blender", "3D creation suite", parent="app-media"
        )

        self.add_selectable(
            "freecad", "FreeCAD", "Parametric 3D CAD modeler", parent="app-media"
        )

        self.add_selectable(
            "openscad", "OpenSCAD", "Script-based 3D CAD modeler", parent="app-media"
        )

        # Video editing
        self.add_selectable(
            "kdenlive", "Kdenlive", "Professional video editor", parent="app-media"
        )

        self.add_selectable(
            "shotcut", "Shotcut", "Open source video editor", parent="app-media"
        )

        self.add_selectable(
            "openshot", "OpenShot", "Easy-to-use video editor", parent="app-media"
        )

        self.add_selectable(
            "pitivi", "Pitivi", "Video editor for GNOME", parent="app-media"
        )

        self.add_selectable(
            "davinci-resolve",
            "DaVinci Resolve",
            "Professional video editor",
            parent="app-media",
        )

        # Screen recording/capture
        self.add_selectable(
            "obs-studio",
            "OBS Studio",
            "Streaming and recording software",
            parent="app-media",
        )

        self.add_selectable(
            "simplescreenrecorder",
            "SimpleScreenRecorder",
            "Screen recording software",
            parent="app-media",
        )

        self.add_selectable(
            "kazam", "Kazam", "Desktop screen recorder", parent="app-media"
        )

        self.add_selectable(
            "peek", "Peek", "Animated GIF screen recorder", parent="app-media"
        )

        self.add_selectable(
            "flameshot", "Flameshot", "Screenshot software", parent="app-media"
        )

        self.add_selectable("shutter", "Shutter", "Screenshot tool", parent="app-media")

    def _build_productivity(self):
        """Build productivity applications menu"""
        self.add_category(
            "app-productivity",
            "Productivity",
            "Office suites, note-taking, planning",
            parent="applications",
            children=[
                "libreoffice",
                "onlyoffice",
                "thunderbird",
                "evolution",
                "notion",
                "obsidian",
                "logseq",
                "joplin",
                "standard-notes",
                "zettlr",
                "typora",
                "marktext",
                "ghostwriter",
                "todoist",
                "planner",
                "gnome-todo",
                "super-productivity",
                "focalboard",
                "wekan",
                "nextcloud-desktop",
                "dropbox",
                "megasync",
                "rclone-browser",
            ],
        )

        # Office suites
        self.add_selectable(
            "libreoffice",
            "LibreOffice",
            "Complete office suite",
            parent="app-productivity",
            default=True,
        )

        self.add_selectable(
            "onlyoffice",
            "OnlyOffice",
            "Office suite with MS compatibility",
            parent="app-productivity",
        )

        # Email clients
        self.add_selectable(
            "thunderbird",
            "Thunderbird",
            "Email client by Mozilla",
            parent="app-productivity",
            default=True,
        )

        self.add_selectable(
            "evolution",
            "Evolution",
            "Email and calendar client",
            parent="app-productivity",
        )

        # Note-taking applications
        self.add_selectable(
            "notion", "Notion", "All-in-one workspace", parent="app-productivity"
        )

        self.add_selectable(
            "obsidian",
            "Obsidian",
            "Knowledge management tool",
            parent="app-productivity",
        )

        self.add_selectable(
            "logseq", "Logseq", "Local-first knowledge graph", parent="app-productivity"
        )

        self.add_selectable(
            "joplin", "Joplin", "Open source note-taking", parent="app-productivity"
        )

        self.add_selectable(
            "standard-notes",
            "Standard Notes",
            "Encrypted notes app",
            parent="app-productivity",
        )

        self.add_selectable(
            "zettlr",
            "Zettlr",
            "Markdown editor for academics",
            parent="app-productivity",
        )

        self.add_selectable(
            "typora", "Typora", "Markdown editor and reader", parent="app-productivity"
        )

        self.add_selectable(
            "marktext",
            "Mark Text",
            "Real-time markdown editor",
            parent="app-productivity",
        )

        self.add_selectable(
            "ghostwriter",
            "ghostwriter",
            "Distraction-free markdown editor",
            parent="app-productivity",
        )

        # Team communication
        self.add_selectable(
            "slack", "Slack", "Team communication platform", parent="app-productivity"
        )

        self.add_selectable(
            "mattermost",
            "Mattermost",
            "Open source team communication",
            parent="app-productivity",
        )

        self.add_selectable(
            "element",
            "Element",
            "Matrix client for secure chat",
            parent="app-productivity",
        )

        # Task management
        self.add_selectable(
            "todoist",
            "Todoist",
            "Task management application",
            parent="app-productivity",
        )

        self.add_selectable(
            "planner", "Planner", "Task manager for GNOME", parent="app-productivity"
        )

        self.add_selectable(
            "gnome-todo",
            "GNOME To Do",
            "Simple task manager",
            parent="app-productivity",
        )

        self.add_selectable(
            "super-productivity",
            "Super Productivity",
            "Advanced todo list app",
            parent="app-productivity",
        )

        self.add_selectable(
            "focalboard",
            "Focalboard",
            "Project management tool",
            parent="app-productivity",
        )

        self.add_selectable(
            "wekan", "WeKan", "Open source kanban board", parent="app-productivity"
        )

        # Cloud storage
        self.add_selectable(
            "nextcloud-desktop",
            "Nextcloud Desktop",
            "Nextcloud sync client",
            parent="app-productivity",
        )

        self.add_selectable(
            "dropbox", "Dropbox", "Cloud storage service", parent="app-productivity"
        )

        self.add_selectable(
            "megasync",
            "MEGA Sync",
            "MEGA cloud storage client",
            parent="app-productivity",
        )

        self.add_selectable(
            "rclone-browser",
            "Rclone Browser",
            "GUI for rclone",
            parent="app-productivity",
        )

    def _build_communication(self):
        """Build communication applications menu"""
        self.add_category(
            "app-communication",
            "Communication",
            "Chat, video calls, social media",
            parent="applications",
            children=[
                "discord",
                "teams",
                "zoom",
                "telegram",
                "whatsapp-for-linux",
                "signal",
                "element",
                "riot",
                "gitter",
                "rocket-chat",
                "mattermost-desktop",
                "slack",
                "skype",
                "jitsi-meet",
                "wire",
                "session",
                "jami",
                "matrix",
                "mumble",
                "teamspeak",
                "pidgin",
                "hexchat",
                "irssi",
                "weechat",
                "quassel",
                "konversation",
                "polari",
            ],
        )

        # Modern messaging platforms
        self.add_selectable(
            "discord",
            "Discord",
            "Voice, video and text chat",
            parent="app-communication",
        )

        self.add_selectable(
            "teams",
            "Microsoft Teams",
            "Business communication platform",
            parent="app-communication",
        )

        self.add_selectable(
            "zoom", "Zoom", "Video conferencing software", parent="app-communication"
        )

        self.add_selectable(
            "telegram",
            "Telegram Desktop",
            "Cloud-based messaging app",
            parent="app-communication",
        )

        self.add_selectable(
            "whatsapp-for-linux",
            "WhatsApp for Linux",
            "Unofficial WhatsApp client",
            parent="app-communication",
        )

        # Privacy-focused messaging
        self.add_selectable(
            "signal", "Signal", "Private messaging app", parent="app-communication"
        )

        self.add_selectable(
            "element", "Element", "Matrix protocol client", parent="app-communication"
        )

        self.add_selectable(
            "riot", "Riot.im", "Matrix client (legacy)", parent="app-communication"
        )

        self.add_selectable(
            "wire", "Wire", "Secure messenger", parent="app-communication"
        )

        self.add_selectable(
            "session", "Session", "Private messenger", parent="app-communication"
        )

        self.add_selectable(
            "jami",
            "Jami",
            "GNU Ring communication platform",
            parent="app-communication",
        )

        # Business communication
        self.add_selectable(
            "slack", "Slack", "Business messaging platform", parent="app-communication"
        )

        self.add_selectable(
            "mattermost-desktop",
            "Mattermost",
            "Open source Slack alternative",
            parent="app-communication",
        )

        self.add_selectable(
            "rocket-chat",
            "Rocket.Chat",
            "Team chat platform",
            parent="app-communication",
        )

        self.add_selectable(
            "gitter", "Gitter", "Chat for developers", parent="app-communication"
        )

        # Video calling
        self.add_selectable(
            "skype", "Skype", "Video calling service", parent="app-communication"
        )

        self.add_selectable(
            "jitsi-meet",
            "Jitsi Meet",
            "Open source video conferencing",
            parent="app-communication",
        )

        # Voice chat/gaming
        self.add_selectable(
            "mumble", "Mumble", "Low-latency voice chat", parent="app-communication"
        )

        self.add_selectable(
            "teamspeak",
            "TeamSpeak",
            "Voice communication software",
            parent="app-communication",
        )

        # IRC clients
        self.add_selectable(
            "hexchat", "HexChat", "IRC client", parent="app-communication"
        )

        self.add_selectable(
            "irssi", "Irssi", "Terminal-based IRC client", parent="app-communication"
        )

        self.add_selectable(
            "weechat", "WeeChat", "Extensible chat client", parent="app-communication"
        )

        self.add_selectable(
            "quassel", "Quassel IRC", "Modern IRC client", parent="app-communication"
        )

        self.add_selectable(
            "konversation", "Konversation", "KDE IRC client", parent="app-communication"
        )

        self.add_selectable(
            "polari", "Polari", "GNOME IRC client", parent="app-communication"
        )

        # Multi-protocol clients
        self.add_selectable(
            "pidgin",
            "Pidgin",
            "Multi-protocol instant messenger",
            parent="app-communication",
        )

        # Matrix ecosystem
        self.add_selectable(
            "matrix",
            "Matrix Clients",
            "Various Matrix protocol clients",
            parent="app-communication",
        )
