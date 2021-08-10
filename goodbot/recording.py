# -*- coding: utf-8 -*-
"""
recording.py contains functions used by the cli module to create
Asciinema recordings using Good Bot's runner program.
"""

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

            print(f"The directory {directory} was ignored.")

    return all_scenes

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

def record_commands(project: Path) -> List[Path]:
    """Records a gif for every video in the commands directory of the
    specified scene.

    Args:
        project (pathlib.Path): The path towards the project to record.

    Returns:
        List[Path]: A list of paths towards each Asciinema recording
        created by this function.
    """

    print(f"Recording shell commands for {str(scene)}.")

    for command in commands_path.iterdir():
        file_name = Path(command.stem)

        subprocess.run(
            [
                "asciinema",
                "rec",
                "-c",
                f"runner {command.absolute()}",
                save_path / file_name.with_suffix(".cast"),
            ]
        )

    return save_path
