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
from typing import List, Dict, Tuple, Union

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

def fetch_scene_gifs(scene_path: Path) -> List[Path]:
    """Fetches each gif that has been rendered for a scene.

    Args:
        scene_path (Path): The path towards the scene.

    Returns:
        List[Path]: List of paths towards each gif. Paths
            are constructed like so:
                [project-path]/[scene-path]/gifs/[gif-name].gif  
    """
    gifs_path: Path = scene_path / Path("gifs")
    all_gifs: List[Path] = []
    for file in gifs_path.iterdir():
        # Assuming a user won't add a `.gif` file.
        if file.suffix == "gif":
            all_gifs.append(file)
    return all_gifs

def corresponding_audio(gif_path: Path) -> Tuple[Path, Union[Path, None]]:
    """
    Finds an audio file that corresponds to the provided gif recording.

    This function should be called by `link_audio()`. Checking whether
    or not the audio path exists is done in the `link_audio()`
    function.

    Args:
        gif_path (Path): The path towards the gif file. The file
            is going to be associated with an audio file with the
            same id.

    Returns:
        Tuple[Path, Union[Path, None]]: A tuple that contains the path
            towards the `gif` at index `[0]`, and the path towards the
            audio file at index `[1]`. If there is no corresponding
            audio file, index `[1]` is `None`.
    """
    audio_path: Path = gif_path.parent / Path("audio")
    # The file name is formatted like:
    # file_[id].gif
    identifier: str = gif_path.name.split("_")[1]
    # This function assumes an audio path exists.
    for audio_file in audio_path.iterdir():

        if identifier in audio_file.name:
            return (gif_path, audio_file)

    return (gif_path, None)

def link_audio(scene_path: Path) -> List[Tuple[Path, Union[Path, None]]]:
    scene_gifs: List[Path] = fetch_scene_gifs(scene_path)
    audio_path: Path = scene_path / Path("audio")
    if not audio_path.exists():
        return [(gif_path, None) for gif_path in scene_gifs]
    else:
        for gif_path in scene_gifs:
            if

def fetch_all(project_path: Path) -> List[Path]:
    scenes: List[Path] = []
    all_gif_paths: List[Path] = []
    # Making sure that we are only adding scenes. Other
    # files could have been added by the user.
    for directory in project_path.iterdir():
        if "scene_" in directory.name:
            scenes.append(directory)

    for scene in scenes:
        pass