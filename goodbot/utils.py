# -*- coding: utf-8 -*-
"""
utils.py module. Contains utility functions.
"""
import os

from pathlib import Path
from typing import List

ALLOWED_INSTRUCTIONS_SUFFIX = (".yaml", ".txt", "")


def in_docker() -> bool:
    """Checks if code is currently running in a Docker container.

    Checks if Docker is in control groups or if there is a `.dockerenv`
    file at the filesystem's root directory.

    Returns:
        bool: Whether or not the code is running in a Docker container.
    """
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


def is_scene(directory: Path) -> bool:
    """Checks if a directory is a scene that contains instructions.

    To be a scene, a directory must:

        * Contain files.
        * Its name must start with `scene`.

    Args
        directory (Path): The path towards the directory to
        check.
    Returns:
        bool: Whether the directory is a scene that contains elements
        or not.
    """

    if directory.is_dir():
        dir_name = directory.name
        contains_something = any(directory.iterdir())
    else:
        return False

    return dir_name[0:5] == "scene" and contains_something


def list_scenes(project_dir: Path) -> List[Path]:
    """Lists every scene contained in the `project_dir` path.

    `list_scenes` uses the `is_scene` function to check whether
    or not a directory si a "scene".

    To be a scene, a directory must:

        * Contain files.
        * Its name must start with `scene`.

    This function will also tell the user if a subdirectory of
    `project_dir` was ignored.

    Args:
        project_dir (Path): The path towards the directory that
            potentially contains scenes.

    Returns:
        List[Path]: A `list` of `Path`s towards each scene contained
            in `project_dir`. If `project_dir` did not contain
            any scene, the returned `list` will be empty.

    """

    all_scenes: List[Path] = []

    for directory in project_dir.iterdir():

        if is_scene(directory):

            all_scenes.append(directory)

        else:

            print(f"The directory {directory} was ignored since it is not a valid Good-Bot scene.")

    return all_scenes


def sort_scenes(scenes: List[Path]) -> List[Path]:
    """Sorts a list of scenes.

    Sorts a list of scenes by their name.

    Args:
        scenes (List[Path]): A `list` of `Path`s towards the scenes
            to sort.

    Returns:
        List[Path]: A `list` of `Path`s towards the sorted scenes.
    """
    return sorted(scenes, key=lambda scene: scene.name)
