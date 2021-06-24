# -*- coding: utf-8 -*-
"""`goodbot`'s render module.

Contains functions used by the good-bot-cli app to render asciicast
recordings in a mp4 video.

Uses prerendered gifs and audio from Google TTS to make the final
rendering.

The conversion asciicast -> gif is done using the asciicast2gif
docker image.

This module requires ffmpeg.
"""
import sys
import pathlib
from shutil import which

Path = pathlib.Path

# Checking ffmpeg installation
def check_dependencies() -> None:
    """Checks if every dependency is installed.

    If not, the missing requirements are printed to the user
    and the program exits.

    Current dependencies checks:

    * `ffmpeg`.
    """
    missing = False
    if not which("ffmpeg"):
        missing = True
        print("Missing requirement: ffmpeg")
    if missing:
        sys.exit()

def fetch_asciicasts(project_path: Path) -> List
