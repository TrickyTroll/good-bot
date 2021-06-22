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
from shutil import which

# Checking ffmpeg installation
if not which("ffmpeg"):
    print("Missing requirement: ffmpeg")
    sys.exit()

def createScene(scene_path: str):
    pass
