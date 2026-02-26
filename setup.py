#!/usr/bin/env python
"""Setuptools configuration for QDA."""

from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="QDA",
    version="0.1.0",
    author="metalcorebear",
    author_email="mark.mbailey@gmail.com",
    description="A tool for quantitatively measuring discursive similarity between bodies of text.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/metalcorebear/Quantitative-Discursive-Analysis",
    py_modules=["QDA"],
    install_requires=["networkx>=2.8", "textblob>=0.17", "numpy>=1.23"],
    extras_require={"dev": ["pytest>=7.0"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
