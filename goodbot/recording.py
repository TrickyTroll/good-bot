# -*- coding: utf-8 -*-
"""
recording.py contains functions used by the cli module to create
Asciinema recordings using Good Bot's runner program.
"""
import yaml

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
    if instructions_path.suffix == ".yaml":
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
