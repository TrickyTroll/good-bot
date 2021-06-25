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
from os import link
import sys
import pathlib
import subprocess
import shlex
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
    """Tries to link an audio file to each `gif` recording.

    If there is no corresponding audio file for a recording, it is
    matched with a `None` value.

    This function uses `corresponding_audio()` for the matching.
    
    In the case that there are no `audio` directory in the scene,
    the function matches each recording to `None`.

    Args:
        scene_path (Path): The path towards the scene to match
            gifs and audio from.

    Returns:
        List[Tuple[Path, Union[Path, None]]]: A list of matches. Each
            match is a tuple that contains the gif path at index `[0]`
            and the audio path at index `[1]`. If there was no
            corresponding audio files, the tuple contains a `None`
            value at index `[1]`.
    """
    scene_gifs: List[Path] = fetch_scene_gifs(scene_path)
    audio_path: Path = scene_path / Path("audio")
    linked: List[Tuple[Path, Union[Path, None]]] = []

    if not audio_path.exists():
        return [(gif_path, None) for gif_path in scene_gifs]
    else:
        for gif_path in scene_gifs:
            linked.append(corresponding_audio(gif_path))

    return linked

def render(gif_and_audio: Tuple[Path, Union[Path, None]]) -> Path:
    """Renders and mp4 file using `ffmpeg`.

    An mp4 file is created at the same location and under the same
    name wheter there is a corresponding audio file or not.

    Args:
        gif_and_audio (Tuple[Path, Union[Path, None]]): A typle
            that contains the gif path at index `0` and the audio
            path at index `0`. The audio path can be `None`.

    Returns:
        Path: The path towards the rendered video. Follows this
            scheme:
                [project-path]/[scene-name]/video/[video_name].mp4
    """
    videos_path: Path = gif_and_audio[0].parent / Path("videos")
    # Changing extension from `.gif` to `.mp4`
    output_path: Path = videos_path + Path(f"{gif_and_audio[0].name.split('.')[0]}.mp4")
    if not gif_and_audio[1]:
        # There is no audio file, just render the video.
        subprocess.run([
            "ffmpeg",
            "-i",
            f"{gif_and_audio[0]}",
            "-movflags",
            "faststart",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            '"scale=trunc(iw/2)*2:trunc(ih/2)*2"',
            f"{output_path}"
        ])
    else:
        # Merge the audio too
        subprocess.run([
            "ffmpeg",
            "f",
            "concat",
            "-safe",
            "0",
            "-i",
            f"{gif_and_audio[0]}",
            "-i",
            f"{gif_and_audio[1]}",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-shortest",
            f"{output_path}"
        ])

    return output_path

def render_all(project_path: Path) -> List[Path]:
    scenes: List[Path] = []
    # Making sure that we are only adding scenes. Other
    # files could have been added by the user.
    for directory in project_path.iterdir():
        if "scene_" in directory.name:
            scenes.append(directory)

    for scene in scenes:
        scene_matches: List[Tuple[Path, Union[Path, None]]] = link_audio(scene)
