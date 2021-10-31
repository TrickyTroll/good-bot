# -*- coding: utf-8 -*-
"""
editor.py contains functions used by the cli module to create
Asciinema recordings of text files being edited. It uses the
`ezvi` program to automate typing in the `vi` editor.
"""
import os
import subprocess
from pathlib import Path
from rich.console import Console
from typing import List, Union
from ezvi.funcmodule import check_ezvi_config

from goodbot import utils


def is_editor_instructions(editor_script_path: Path) -> bool:
    """
    Checks if the filed saved under `editor_script_path` is a valid
    `ezvi` configuration file.

    The check is made using a config checker function from `ezvi`.

    Args:
        editor_script_path (Path): The path towards the file that
        will be checked.

    Returns:
        bool: Whether or not the file is an `ezvi` instructions file.
    """
    if editor_script_path in utils.ALLOWED_INSTRUCTIONS_SUFFIX:
        # ezvi check here
        try:
            check_ezvi_config(editor_script_path)

        except TypeError:  # The file's format is probabaly invalid.
            return False
        except NotImplementedError:
            # The format is valid, but the user want's to use commands
            # that have not been implemented.
            return False

    return True


def fetch_scene_editor_instructions(scene_path: Path) -> List[Path]:
    """
    fetch_scene_editor_instructions finds each `ezvi` instructions
    files in a scene.

    To check if a file is an `ezvi` instructions file, this function
    uses `is_editor_instructions()`.

    This function can then be used by `fetch_project_editor_instructions()`
    to get all `ezvi` instructions files in a project.

    Args:
        scene_path (Path): The path towards the scene that will be searched.

    Returns:
        List[Path]: A list of paths towards each `ezvi` instructions file
        that was found.
    """
    scene_editor_instructions: List[Path] = []
    editor_contents_dir: Path = scene_path / "editor"

    if editor_contents_dir.exists():
        for file in editor_contents_dir.iterdir():
            if is_editor_instructions(file):
                scene_editor_instructions.append(file)

    return scene_editor_instructions


def fetch_project_editor_instructions(project_path: Union[Path, str]) -> List[Path]:
    """
    fetch_project_editor_instructions finds each ezvi instructions
    file in a Good Bot project. It uses fetch_scene_runner_instructions
    to find each instructions file scene by scene.

    Args:
        project_path (Union[Path, str]): The path towards the project
        where this function will look for instructions files.
    Returns:
        List[Path]: A list of paths towards each instructions file that
        was found.
    """
    if not isinstance(project_path, Path):
        try:
            project_path = Path(project_path)
        except Exception as err:
            raise TypeError(
                f"Could not convert the provided argument to a Path object:\n{err}"
            )
    all_editor_instructions: List[Path] = []
    for scene in project_path.iterdir():
        if "scene_" in scene.name:
            all_editor_instructions = (
                all_editor_instructions + fetch_scene_editor_instructions(scene)
            )
    return all_editor_instructions

def record_editor(instruction_file: Path, debug: bool = False) -> Path:

    save_path: Path = (
        instruction_file.parent.parent / Path("asciicasts") / instruction_file.name
    ).with_suffix(".cast")

    if save_path.exists():
        os.remove(save_path)

    subprocess.run(
        ["asciinema", "rec", "-c", f"ezvi yaml {instruction_file}", str(save_path)],
        capture_output=not debug,
    )

    return save_path
