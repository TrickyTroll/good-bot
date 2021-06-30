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
import os
import sys
import pathlib
import tempfile
import time
import subprocess
from shutil import which
from typing import List, Tuple, Union

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
        if file.suffix == ".gif":
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
    audio_path: Path = gif_path.parent.parent / Path("audio")
    # The file name is formatted like:
    # file_[id].gif
    identifier: str = gif_path.stem.split("_")[1]
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

    for gif_path in scene_gifs:
        linked.append(corresponding_audio(gif_path))

    return linked

def remove_first_frame(gif_path: Path) -> Path:
    """Removes the first frame from a gif file.

    Args:
        gif_path (Path): The path towards the gif from which the
            first frame will be removed. This is also where the
            shorter gif will be saved.

    Returns:
        Path: The path towards the newly created gif. This is the
            same value as the `gif_path` argument. 
    """
    save_path: Path = gif_path.parent / Path(gif_path.stem + "_edited" + ".gif")
    # `unoptimize` option ensures no transparent background added.
    subprocess.run(['gifsicle', '--unoptimize', f"{gif_path}", '--delete', '#0', '-o', f"{save_path}"])

    return save_path

def render(gif_and_audio: Tuple[Path, Union[Path, None]]) -> Path:
    """Renders and mp4 file using `ffmpeg`.

    An mp4 file is created at the same location and under the same
    name wheter there is a corresponding audio file or not.

    This function also calls `remove_first_frame()` before doing
    any conversion.

    Args:
        gif_and_audio (Tuple[Path, Union[Path, None]]): A typle
            that contains the gif path at index `0` and the audio
            path at index `0`. The audio path can be `None`.

    Returns:
        Path: The path towards the rendered video. Follows this
            scheme:
                [project-path]/[scene-name]/video/[video_name].mp4
    """
    gif_path: Path = remove_first_frame(gif_and_audio[0])
    videos_path: Path = gif_path.parent.parent / Path("videos")
    # Changing extension from `.gif` to `.mp4`
    video_name: Path = Path(f"{gif_and_audio[0].stem}.mp4")
    output_path: Path = videos_path / video_name

    if gif_and_audio[1]: # If there is an audio file.
        with tempfile.TemporaryDirectory() as tempdir:
            # Create a temporaty video
            temp_video_path: Path = Path(tempdir) / video_name
            subprocess.run([
                "ffmpeg",
                "-i",
                f"{gif_path}",
                "-movflags",
                "faststart",
                "-pix_fmt",
                "yuv420p",
                '-vf',
                'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                f"{temp_video_path}"
            ], check=True)
            # Merge the audio too
            subprocess.run([
                "ffmpeg",
                "-i",
                f"{temp_video_path}",
                "-i",
                f"{gif_and_audio[1]}",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                f"{output_path}"
            ], check=True)
    else:
        # There is no audio to merge.
        # No need to make a temp dir.
        subprocess.run([
            "ffmpeg",
            "-i",
            f"{gif_path}",
            "-movflags",
            "faststart",
            "-pix_fmt",
            "yuv420p",
            '-vf',
            'scale=trunc(iw/2)*2:trunc(ih/2)*2',
            f"{output_path}"
        ], check=True)

    return output_path

def render_all(project_path: Path) -> List[Path]:
    """Uses the `render()` function on each combination of a project.

    Combinations a found using the `scene_matches()` function.

    Args:
        project_path (Path): The path towards the project to render.

    Returns:
        List[Path]: A list of paths towards the location of each
            rendered mp4 file.
    """
    scenes: List[Path] = []
    all_renders: List[Path] = []
    # Making sure that we are only adding scenes. Other
    # files could have been added by the user.
    for directory in project_path.iterdir():
        if "scene_" in directory.name:
            scenes.append(directory)

    for scene in scenes:
        scene_matches: List[Tuple[Path, Union[Path, None]]] = link_audio(scene)
        for match in scene_matches:
            all_renders.append(render(match))

    return all_renders

def sort_videos(project_path: Path) -> List[Path]:
    """Sorts each videos in a project.

    Videos are sorted by scene and then by videos.

    The scenes are sorted using their `id`. The minimal
    `id` value is `1`, and there is no maximum.

    Once the scenes are sorted, each video in each scene
    is sorted, starting with the scene with id `1`. Each
    video is appended to a list of paths.

    Args:
        project_path (Path): The path towards the project
            from which the videos will be found and sorted.

    Returns:
        List[Path]: A sorted list of paths towards the video recordings.
    """

    # Sorting scenes
    scene_amount: int = 0
    all_scenes: List[Path] = []

    for dir in project_path.iterdir():
        if "scene_" in dir.name:
            scene_amount += 1
    
    for scene_index in range(scene_amount):
        for dir in project_path.iterdir():
            if "scene_" in dir.name:
                try:
                    scene_id: int = int(dir.stem.split("_")[1])
                except ValueError:
                    continue
                if scene_index + 1 == scene_id:
                    # All scenes will be in order
                    all_scenes.append(dir)
    
    all_videos: List[Path] = []

    # Sorting per scene.
    for scene in all_scenes:

        videos_path: Path = scene / Path("videos")
        videos_amount: int = 0

        for file in videos_path.iterdir():
            if file.suffix == ".mp4":
                videos_amount += 1
        
        for video_index in range(videos_amount):

            for video in videos_path.iterdir():

                if "file_" in video.name:
                    try:
                        video_id: int = int(video.stem.split("_")[1])
                    except ValueError:
                        continue
                
                    if video_index == video_id:

                        all_videos.append(video.absolute())
    
    return all_videos
    
def write_ffmpeg_instructions(project_path: Path) -> Path:
    """Writes paths to files to merge in a `.txt` file.

    Each path is on its own line. The paths are provided
    by the `sort_videos()` function.

    Args:
        project_path (Path): The path towards the project
            to write the instructions to. This is also
            where the `sort_videos()` function will look
            for videos.

    Returns:
        Path: The path towards the newly created `.txt` file.
    """
    file_path: Path = project_path / Path("instructions.txt")
    video_paths: List[Path] = sort_videos(project_path)

    with open(file_path, "w") as stream:
        for video_path in video_paths:
            stream.write(f"file '{video_path}'\n")
    
    return file_path

def render_final(project_path: Path) -> Path:
    """Renders the final video using `ffmpeg`.

    This function uses the `write_ffmpeg_instructions()` function,
    which in turn uses `sort_videos()` to get a list of rendered
    videos in order.

    Args:
        project_path (Path): The path to the project to merge
            videos from. `mp4` files must be created beforehand
            using the `render_all()` function.

    Returns:
        Path: The path towards the final video.
    """
    final_path: Path = project_path / Path("final/")

    if not final_path.exists():
        os.mkdir(final_path)
    
    instructions_file: Path = write_ffmpeg_instructions(project_path)
    output_path: Path = final_path / Path("final.mp4")

    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-segment_time_metadata", "1", "-i", f"{instructions_file}", "-af", "aresample=async=1",  f"{output_path}"])

    return output_path
    