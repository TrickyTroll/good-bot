# -*- coding: utf-8 -*-
"""
recording.py contains functions used by the cli module to create
Asciinema recordings using Good Bot's runner program.
"""
import os
from pathlib import Path
import subprocess
import yaml

from rich.console import Console
from typing import List, Dict, Union, Any

from goodbot import utils


def is_runner_instructions(instructions_path: Path) -> bool:
    """
    is_runner_instructions checks whether or not the provided file could
    be a instructions file for Good Bot's runner program.

    The check is done by making sure that the file's extension is ".yaml"
    and that its contents match what a standard runner script would could
    contain.

    Args:
        instructions_path (Path): The path towards the file for which the
        check will be performed.
    Returns:
        bool: Whether or not the file is an instructions file for Good
        Bot Runner.
    """
    if instructions_path.suffix in utils.ALLOWED_INSTRUCTIONS_SUFFIX:
        with open(instructions_path, "r") as stream:
            contents: str = stream.read()
            try:
                conf: dict = yaml.safe_load(contents)
            except Exception as err:
                print(f"Got a problem parsing file {instructions_path}\n{err}")
                return False
    else:
        return False

    if len(conf.keys()) > 2:
        return False
    for key, value in conf.items():
        if key not in ("commands", "expect"):
            return False
        # value is of type `list`
        for item in value:
            if not isinstance(item, (str, dict)):
                return False

    return True


def fetch_runner_instructions(instructions_path: Path) -> List[Path]:
    """
    fetch_runner_instructions finds each text file in a directory
    that can be used as instructions for Good Bot's runner program.

    Args:
        instructions_path (Path): The path towards the directory that
        may contain instructions file.
    Returns:
        List[Path]: A list of resolved paths towards each instructions
        file that was found.
    """
    runner_instructions: List[Path] = []
    try:
        for instructions in instructions_path.iterdir():
            if is_runner_instructions(instructions):
                runner_instructions.append(instructions.resolve())
    except FileNotFoundError:
        return []

    return runner_instructions


def fetch_scene_runner_instructions(scene_path: Path) -> List[Path]:
    """
    fetch_scene_runner_instructions finds each runner instructions file
    in a scene using fetch_runner_instructions.

    Args:
        scene_path (Path): A path towards a scene that will be scanned
        for runner instructions.
    Returns:
        List[Path]: A list of paths towards each runner instructions
        file that was found.
    """
    scene_runner_instructions: List[Path] = []
    for directory in scene_path.iterdir():
        if str(directory.name).lower() == "commands":
            scene_runner_instructions = (
                scene_runner_instructions + fetch_runner_instructions(directory)
            )
    return scene_runner_instructions


def fetch_project_runner_instructions(project_path: Union[Path, str]) -> List[Path]:
    """
    fetch_project_runner_instructions finds each runner instructions
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
    all_runner_instructions: List[Path] = []
    for scene in project_path.iterdir():
        if "scene_" in scene.name:
            all_runner_instructions = (
                all_runner_instructions + fetch_scene_runner_instructions(scene)
            )
    return all_runner_instructions

def record_command(instructions_file: Path, debug: bool = False) -> Path:
    """Records a single command video from the specified instructions file.

    This function uses Good Bot's runner program to simulate a human typing
    the commands in the specified instructions file.

    Args:
        instructions_file (pathlib.Path): The path towards the Good-Bot
        runner instructions file to use.
        debug (bool): Whether or not to print the output of the command.
        Defaults to False.

    Returns:
        pathlib.Path: The path towards the Asciinema recording created
        by this function.
    """
    save_path: Path = (
        instructions_file.parent.parent / Path("asciicasts") / instructions_file.name
    ).with_suffix(".cast")

    if save_path.exists():
        os.remove(save_path)

    subprocess.run(
        ["asciinema", "rec", "-c", f"runner {instructions_file}", str(save_path)],
        capture_output=not debug,
    )

    return save_path


def record_commands(project: Path, debug: bool = False) -> List[Path]:
    """Records a gif for every video in the commands directory of the
    specified project.

    Args:
        project (pathlib.Path): The path towards the project to record.

    Returns:
        List[Path]: A list of paths towards each Asciinema recording
        created by this function.
    """
    all_runner_instructions: List[Path] = fetch_project_runner_instructions(project)
    all_recordings: List[Path] = []
    console: Console = Console()

    with console.status("[bold green]Recording videos...") as status:

        for command in all_runner_instructions:

            save_path: Path = (
                command.parent.parent / Path("asciicasts") / command.name
            ).with_suffix(".cast")

            if save_path.exists():
                os.remove(save_path)

            subprocess.run(
                ["asciinema", "rec", "-c", f"runner {command}", str(save_path)],
                capture_output=not debug,
            )

            console.log(f"Video contents in file {command} have been recorded.")
            all_recordings.append(save_path)

    return all_recordings
