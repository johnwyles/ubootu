#!/usr/bin/env python3
"""
Setup configuration for Ubootu - Ubuntu Bootstrap Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="ubootu",
    version="1.0.0",
    author="John Wyles",
    author_email="",
    description="A professional Ubuntu desktop configuration tool with intuitive TUI interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnwyles/ubootu",
    packages=find_packages(include=["lib", "lib.*"]),
    package_data={
        "lib": ["**/*.yml", "**/*.yaml", "**/*.j2"],
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",
        "blessed>=1.20.0",
        "requests>=2.31.0",
        "ansible>=2.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ubootu=configure_standard_tui:main",
            "ubootu-setup=setup_bootstrap:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords="ubuntu, bootstrap, configuration, ansible, tui, desktop, setup",
)