#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TermCast - Terminal Session Recording & Smart Replay Engine
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="termcast",
    version="1.0.0",
    author="TermCast Team",
    author_email="termcast@example.com",
    description="🎬 Lightweight Terminal Session Recording & Smart Replay Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/termcast",
    py_modules=["termcast"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "termcast=termcast:main",
        ],
    },
    keywords="terminal recording replay cli session asciinema ttyrec",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/termcast/issues",
        "Source": "https://github.com/gitstq/termcast",
        "Documentation": "https://github.com/gitstq/termcast#readme",
    },
)
