#!/usr/bin/env python3
"""
Ubootu Epic Splash Screen
Professional Ubuntu Desktop Configuration Tool
"""

import os
import sys
import time

try:
    import curses

    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False

try:
    from rich.align import Align
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text

    HAS_RICH = True
except ImportError:
    HAS_RICH = False


class UbootuSplash:
    """Epic Ubootu splash screen with multiple rendering modes"""

    def __init__(self):
        self.version = "2.0"
        self.tagline = "Professional Ubuntu Desktop Configuration Tool"

    def get_ascii_logo(self, style="full"):
        """Get ASCII art logo in different styles"""

        if style == "full":
            return [
                "██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗",
                "██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║",
                "██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║",
                "██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║",
                "╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝",
                " ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ",
            ]
        elif style == "simple":
            return [
                "██╗   ██╗██████╗  ██████╗  ██████╗ ████████╗██╗   ██╗",
                "██║   ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║   ██║",
                "██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ██║   ██║",
                "██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██║   ██║",
                "╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝",
                " ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ",
            ]
        elif style == "basic":
            return [
                "#    # #####   ####   ####  ##### #    #",
                "#    # #    # #    # #    #   #   #    #",
                "#    # #####  #    # #    #   #   #    #",
                "#    # #    # #    # #    #   #   #    #",
                " ####  #####   ####   ####    #    #### ",
            ]
        else:  # fallback
            return ["UBOOTU", "======"]

    def show_rich_splash(self):
        """Show splash using Rich library (fancy)"""
        if not HAS_RICH:
            return False

        console = Console()

        # Clear screen
        console.clear()

        # Create the logo
        logo_lines = self.get_ascii_logo("full")
        logo_text = Text()

        # Add logo in vibrant electric blue
        for line in logo_lines:
            logo_text.append(line + "\n", style="bold bright_blue")

        # Create title and tagline
        title_text = Text()
        title_text.append("🚀 ", style="bright_yellow")
        title_text.append("UBOOTU", style="bold bright_magenta")
        title_text.append(" 🚀\n\n", style="bright_yellow")
        title_text.append(f"{self.tagline}\n", style="bright_cyan")
        title_text.append(f"Version {self.version}\n\n", style="bright_white")
        title_text.append("Configure Your Ubuntu Desktop Environment\n", style="bright_green")
        title_text.append("400+ Tools • Hierarchical Menus • Easy Setup", style="bright_cyan")

        # Create panels with vibrant colors
        logo_panel = Panel(Align.center(logo_text), border_style="bright_blue", padding=(1, 2))

        title_panel = Panel(Align.center(title_text), border_style="bright_green", padding=(1, 2))

        # Display splash
        console.print(logo_panel)
        console.print()
        console.print(title_panel)
        console.print()

        # Loading animation with percentage
        from rich.progress import BarColumn, PercentageColumn

        with Progress(
            SpinnerColumn("dots"),
            TextColumn("[bright_cyan]Loading Ubootu..."),
            BarColumn(),
            PercentageColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("loading", total=100)
            for i in range(100):
                time.sleep(0.03)
                progress.update(task, advance=1)

        # Clear loading and show ready message briefly
        console.print(
            "\n[bright_green]✅ Ready! Loading options...[/bright_green]",
            justify="center",
        )
        time.sleep(1)

        # Now show the options on the same splash screen
        console.clear()
        console.print(logo_panel)
        console.print()

        # Options panel
        options_text = Text()
        options_text.append("What would you like to do?\n\n", style="bold white")

        options = [
            "🚀 Fresh Install - Configure a brand new Ubuntu installation",
            "🔧 Modify Setup - Tweak your existing configuration",
            "📦 Apply Profile - Restore from a saved configuration",
            "💾 Backup Config - Save your current setup",
            "📜 View History - Browse configuration timeline",
            "🎯 Quick Actions - Common tasks and fixes",
            "❓ Help - Get help and documentation",
            "🚪 Exit - See you later!",
        ]

        for i, option in enumerate(options, 1):
            options_text.append(f"  {i}. {option}\n", style="bright_cyan")

        options_panel = Panel(
            Align.center(options_text),
            border_style="bright_green",
            padding=(1, 2),
            title="[bold]Choose Your Path[/bold]",
            title_align="center",
        )

        console.print(options_panel)
        console.print()

        # Wait for input
        try:
            choice = input("Enter your choice (1-8): ").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
                choice = "8"
        except (KeyboardInterrupt, EOFError):
            choice = "8"

        # Write choice to temp file for bash to read
        with open("/tmp/welcome_choice.txt", "w") as f:
            f.write(choice)

        return True

    def show_terminal_splash(self):
        """Show splash using basic terminal colors"""

        # ANSI color codes
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "bold": "\033[1m",
            "end": "\033[0m",
        }

        # Clear screen
        os.system("clear" if os.name == "posix" else "cls")

        print()
        print()

        # Logo in vibrant electric blue
        logo_lines = self.get_ascii_logo("basic")

        for line in logo_lines:
            print(f"{colors['blue']}{colors['bold']}{line.center(80)}{colors['end']}")

        print()
        print()

        # Title and description
        print(f"{colors['yellow']}{colors['bold']}{'🚀 ' + self.tagline + ' 🚀'.center(80)}{colors['end']}")
        version_text = f"Version {self.version} • Professional Ubuntu Desktop Configuration"
        print(f"{colors['cyan']}{version_text.center(80)}{colors['end']}")
        print()
        print(f"{colors['green']}{'Configure Your Ubuntu Desktop Environment'.center(80)}{colors['end']}")
        print(f"{colors['cyan']}{'400+ Tools • Hierarchical Menus • Easy Setup'.center(80)}{colors['end']}")
        print()
        print()

        # Loading animation
        print(f"{colors['cyan']}Loading Ubootu", end="", flush=True)
        for i in range(20):
            print(f"{colors['yellow']}.", end="", flush=True)
            time.sleep(0.1)
        print(f" {colors['green']}Ready!{colors['end']}")
        print()

        # Show options
        print(f"{colors['white']}{colors['bold']}What would you like to do?{colors['end']}")
        print()

        options = [
            "🚀 Fresh Install - Configure a brand new Ubuntu installation",
            "🔧 Modify Setup - Tweak your existing configuration",
            "📦 Apply Profile - Restore from a saved configuration",
            "💾 Backup Config - Save your current setup",
            "📜 View History - Browse configuration timeline",
            "🎯 Quick Actions - Common tasks and fixes",
            "❓ Help - Get help and documentation",
            "🚪 Exit - See you later!",
        ]

        for i, option in enumerate(options, 1):
            print(f"{colors['cyan']}  {i}. {option}{colors['end']}")

        print()

        try:
            choice = input("Enter your choice (1-8): ").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
                choice = "8"
        except (KeyboardInterrupt, EOFError):
            print(f"\n{colors['red']}Setup cancelled by user{colors['end']}")
            choice = "8"

        # Write choice to temp file for bash to read
        with open("/tmp/welcome_choice.txt", "w") as f:
            f.write(choice)

        return True

    def show_basic_splash(self):
        """Show basic splash for limited terminals"""

        print("\n" * 3)
        print("=" * 60)
        print("UNBOOTU".center(60))
        print(self.tagline.center(60))
        print(f"Version {self.version}".center(60))
        print("=" * 60)
        print()
        print("Features:".center(60))
        print("• 400+ Professional Tools".center(60))
        print("• Hierarchical Menu System".center(60))
        print("• Easy TUI Interface".center(60))
        print("• Complete Desktop Configuration".center(60))
        print()
        print("Configure Your Ubuntu Desktop Environment".center(60))
        print("=" * 60)
        print()

        print("Loading", end="", flush=True)
        for i in range(10):
            print(".", end="", flush=True)
            time.sleep(0.2)
        print(" Ready!")
        print()

        print("What would you like to do?")
        print()

        options = [
            "1. Fresh Install - Configure a brand new Ubuntu installation",
            "2. Modify Setup - Tweak your existing configuration",
            "3. Apply Profile - Restore from a saved configuration",
            "4. Backup Config - Save your current setup",
            "5. View History - Browse configuration timeline",
            "6. Quick Actions - Common tasks and fixes",
            "7. Help - Get help and documentation",
            "8. Exit - See you later!",
        ]

        for option in options:
            print(f"  {option}")

        print()

        try:
            choice = input("Enter your choice (1-8): ").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
                choice = "8"
        except (KeyboardInterrupt, EOFError):
            print("Setup cancelled by user")
            choice = "8"

        # Write choice to temp file for bash to read
        with open("/tmp/welcome_choice.txt", "w") as f:
            f.write(choice)

        return True

    def show_splash(self):
        """Show the best available splash screen"""

        # Try Rich first (fanciest)
        if HAS_RICH:
            try:
                return self.show_rich_splash()
            except:
                pass

        # Try terminal colors
        try:
            return self.show_terminal_splash()
        except:
            pass

        # Fallback to basic
        return self.show_basic_splash()


def show_ubootu_splash():
    """Main entry point for splash screen"""
    splash = UbootuSplash()
    return splash.show_splash()


if __name__ == "__main__":
    show_ubootu_splash()
