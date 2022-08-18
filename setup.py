# -*- coding: utf-8 -*-
"""Setup file for pip install"""
from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="music_mood_analysis",
    version="1.0.4",
    description="Music mood analysis",
    long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords=["python"],
    author="Richard Baltrusch",
    url="https://github.com/rbaltrusch/music_mood_analysis",
    packages=setuptools.find_packages("."),
    python_requires=">=3.8",
    include_package_data=True,
    package_data={"music_mood_analysis": ["py.typed"]}, # for mypy
    # This is a trick to avoid duplicating dependencies between both setup.py and requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    install_requires=project_dir.joinpath("requirements.txt")
    .read_text(encoding="utf-8")
    .split("\n"),
    zip_safe=False,
    license="AGPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
)
