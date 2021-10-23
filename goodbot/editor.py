# -*- coding: utf-8 -*-
"""
recording.py contains functions used by the cli module to create
Asciinema recordings using Good Bot's runner program.
"""
import yaml
import os
import subprocess
from rich.console import Console
from pathlib import Path
from typing import List, Dict, Union, Any
from ezvi.funcmodule import check_config

from goodbot import utils

def is_editor_instructions(editor_script_path: Path) -> bool:
    if editor_script_path in utils.ALLOWED_INSTRUCTION_SUFFIX:
        # ezvi check here
        return
    return

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
            raise TypeError(f"Could not convert the provided argument to a Path object:\n{err}")
    all_runner_instructions: List[Path] = []
    for scene in project_path.iterdir():
        if "scene_" in scene.name:
            all_runner_instructions = all_runner_instructions + fetch_scene_runner_instructions(
                scene
            )
    return all_runner_instructions
