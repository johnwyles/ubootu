#!/usr/bin/env python3
"""
APT health checker and fixer - prevents common repository issues
"""

import glob
import logging
import os
import subprocess
import sys
import warnings
from typing import List, Tuple

# Suppress all warnings including permission warnings
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

# Specifically suppress the apt module warnings if it gets imported
try:
    import apt

    # Disable apt's cache update warnings
    apt.apt_pkg.config.set("Acquire::http::No-Cache", "true")
    apt.apt_pkg.config.set("Acquire::http::Pipeline-Depth", "0")
except ImportError:
    pass


def clean_apt_sources() -> List[str]:
    """Clean up APT sources to prevent common issues"""
    issues_fixed = []

    # 1. Remove backup files that cause warnings
    backup_patterns = [
        "/etc/apt/sources.list.d/*.backup*",
        "/etc/apt/sources.list.d/*.save",
        "/etc/apt/sources.list.d/*~",
        "/etc/apt/sources.list.d/*.bak",
    ]

    for pattern in backup_patterns:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                issues_fixed.append(f"Removed backup file: {os.path.basename(file)}")
            except Exception:
                pass

    # 2. Check for duplicate repositories (.list and .sources for same repo)
    sources_dir = "/etc/apt/sources.list.d/"
    if os.path.exists(sources_dir):
        list_files = glob.glob(os.path.join(sources_dir, "*.list"))
        sources_files = glob.glob(os.path.join(sources_dir, "*.sources"))

        # Create base name sets
        list_bases = {os.path.basename(f)[:-5] for f in list_files}  # Remove .list
        sources_bases = {os.path.basename(f)[:-8] for f in sources_files}  # Remove .sources

        # Find duplicates
        duplicates = list_bases & sources_bases
        for dup in duplicates:
            list_file = os.path.join(sources_dir, f"{dup}.list")
            sources_file = os.path.join(sources_dir, f"{dup}.sources")

            # Check if .list file has contrib (invalid for Ubuntu)
            try:
                # Skip files we can't read due to permissions
                if not os.access(list_file, os.R_OK):
                    continue
                with open(list_file, "r") as f:
                    if "contrib" in f.read():
                        os.remove(list_file)
                        issues_fixed.append(f"Removed {dup}.list (contained invalid contrib)")
                        continue
            except Exception:
                pass

            # Otherwise prefer .sources format (newer)
            if os.path.exists(list_file) and os.path.exists(sources_file):
                try:
                    os.remove(list_file)
                    issues_fixed.append(f"Removed duplicate {dup}.list (kept .sources)")
                except Exception:
                    pass

    # 3. Remove any contrib components (Debian-specific, invalid for Ubuntu)
    # Check main sources.list
    try:
        sources_list = "/etc/apt/sources.list"
        if os.path.exists(sources_list):
            with open(sources_list, "r") as f:
                content = f.read()
            if "contrib" in content:
                new_content = content.replace(" contrib", "")
                with open(sources_list, "w") as f:
                    f.write(new_content)
                issues_fixed.append("Removed contrib from /etc/apt/sources.list")
    except Exception:
        pass

    # Check sources.list.d files
    for pattern in [
        "/etc/apt/sources.list.d/*.list",
        "/etc/apt/sources.list.d/*.sources",
    ]:
        for file in glob.glob(pattern):
            try:
                # Skip files we can't read due to permissions
                if not os.access(file, os.R_OK):
                    continue
                with open(file, "r") as f:
                    content = f.read()
                if "contrib" in content:
                    # Special handling for archive_ubuntu files
                    if "archive_ubuntu" in file and file.endswith(".list"):
                        os.remove(file)
                        issues_fixed.append(f"Removed {os.path.basename(file)} (invalid contrib)")
                    else:
                        new_content = content.replace(" contrib", "").replace("contrib ", "")
                        with open(file, "w") as f:
                            f.write(new_content)
                        issues_fixed.append(f"Removed contrib from {os.path.basename(file)}")
            except Exception:
                pass

    return issues_fixed


def check_apt_basic() -> Tuple[bool, str]:
    """Basic APT health check - non-blocking approach"""
    try:
        # First clean up known issues
        issues_fixed = clean_apt_sources()
        if issues_fixed:
            print("🧹 Cleaned up APT sources:")
            for issue in issues_fixed:
                print(f"   - {issue}")
            print()

        # Simple check: can we run apt list?
        result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True, timeout=15)

        if result.returncode == 0:
            return True, "APT is working correctly"
        else:
            return False, f"APT returned error code {result.returncode}"

    except subprocess.TimeoutExpired:
        return False, "APT command timed out"
    except Exception as e:
        return False, f"APT check failed: {str(e)}"


def get_apt_recommendations() -> List[str]:
    """Get recommendations for common APT issues"""
    recommendations = [
        "Common APT fixes:",
        "sudo apt clean && sudo apt update",
        "sudo apt --fix-broken install",
        "sudo rm -f /var/lib/dpkg/lock*",
        "sudo dpkg --configure -a",
    ]
    return recommendations


def main():
    """Main function - provides helpful output without blocking"""
    print("🔍 APT Health Check")
    print("=" * 50)

    is_healthy, message = check_apt_basic()

    if is_healthy:
        print(f"✅ {message}")
        print("APT is ready for package installation.")
        sys.exit(0)
    else:
        print(f"⚠️  {message}")
        print("\nThis won't stop the bootstrap, but you might want to fix APT issues.")
        print("\n💡 Common fixes:")

        for i, rec in enumerate(get_apt_recommendations(), 1):
            print(f"   {i}. {rec}")

        print("\n🚀 The bootstrap will continue anyway...")
        print("If you encounter package installation issues, try the fixes above.")

        # Exit with code 1 to indicate warning, but setup.sh will handle this gracefully
        sys.exit(1)


if __name__ == "__main__":
    main()
