#!/usr/bin/env python3
"""
Ubootu Profile Template Selection
Beautiful interface to show available profile templates for the Ultimate Ubuntu Experience Engine
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from rich.align import Align
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def show_profile_templates():
    """Show profile templates and get user choice"""

    if HAS_RICH:
        console = Console()

        # Title
        title_text = Text()
        title_text.append("🚀 Ubootu Profile Templates", style="bold magenta")
        title_text.append(
            "\n\nChoose a pre-configured profile or create a custom configuration:",
            style="white",
        )

        panel = Panel(Align.center(title_text), border_style="bright_magenta", padding=(1, 2))

        console.print(panel)
        console.print()

        # Profile options
        profiles = [
            (
                "1",
                "🔧 Developer Profile",
                "IDEs, Git, Docker, programming languages, dev tools",
            ),
            ("2", "🎮 Gaming Profile", "Steam, Discord, gaming utilities, media tools"),
            (
                "3",
                "🎨 Creative Profile",
                "GIMP, Blender, multimedia editing, design tools",
            ),
            (
                "4",
                "🔒 Security Profile",
                "Security tools, hardening, privacy applications",
            ),
            ("5", "⚡ Minimal Profile", "Just the essentials, lightweight setup"),
            (
                "c",
                "🛠️ Custom Configuration",
                "Choose exactly what you want (recommended)",
            ),
        ]

        for choice, name, description in profiles:
            console.print(f"  {choice}. [bold]{name}[/bold]")
            console.print(f"     {description}")
            console.print()

    else:
        # Fallback without rich
        print("=" * 60)
        print("🚀 Ubootu Profile Templates")
        print("=" * 60)
        print()
        print("Choose a pre-configured profile or create a custom configuration:")
        print()
        print("  1. 🔧 Developer Profile")
        print("     IDEs, Git, Docker, programming languages, dev tools")
        print()
        print("  2. 🎮 Gaming Profile")
        print("     Steam, Discord, gaming utilities, media tools")
        print()
        print("  3. 🎨 Creative Profile")
        print("     GIMP, Blender, multimedia editing, design tools")
        print()
        print("  4. 🔒 Security Profile")
        print("     Security tools, hardening, privacy applications")
        print()
        print("  5. ⚡ Minimal Profile")
        print("     Just the essentials, lightweight setup")
        print()
        print("  c. 🛠️ Custom Configuration")
        print("     Choose exactly what you want (recommended)")
        print()

    # Get user choice
    try:
        choice = input("Enter your choice [1-5,c] (default: c): ").strip().lower()

        if choice == "":
            choice = "c"
        elif choice not in ["1", "2", "3", "4", "5", "c"]:
            print("Invalid choice, defaulting to custom configuration")
            choice = "c"

        # Write choice to temp file for bash to read
        with open("/tmp/profile_choice.txt", "w") as f:
            f.write(choice)

        return True

    except (KeyboardInterrupt, EOFError):
        print("\nConfiguration cancelled by user")
        with open("/tmp/profile_choice.txt", "w") as f:
            f.write("c")  # Default to custom
        return False


if __name__ == "__main__":
    success = show_profile_templates()
    sys.exit(0 if success else 1)
