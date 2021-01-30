import yaml
import click
import classmodule
import os
from pathlib import Path

########################################################################
#                               YAML parsing                           #
########################################################################


def config_parser(file: click.File) -> dict:
    """Can be used to parse a configuration file.

    Args:
        file (click.File): The configuration file. This should be
        handled by click.

    Returns:
        dict: A dict with the parsed information.
    """
    parsed_file = yaml.safe_load(file)
    return parsed_file


def create_classes(file: click.File) -> list:

    parsed_file = config_parser(file)
    all_classes = []

    for todos in parsed_file:

        if "commands" in todos:
            all_classes.append(classmodule.Commands(
                commands=todos["commands"],
                expect=todos["expect"]))

    return all_classes

########################################################################
#                       Creating directories                           #
########################################################################


def create_dirs(directories: list, project_dir: str = "project") -> Path:

    project_dir = Path(project_dir)
    toggle = False
    if project_dir.is_dir():
        print(f"Directory {project_dir} exists!")
        toggle = True
    else:
        os.mkdir(project_dir)

    for directory in directories:

        new_dir = project_dir / Path(directory)

        if new_dir.is_dir():
            print(f"Folder {new_dir} exists!")
        else:
            os.mkdir(new_dir)

    if toggle:
        return project_dir
    else:
        return Path("./")

########################################################################
#                             shell commands                           #
########################################################################


def is_shell_command(command: dict) -> bool:
    """Checks if the command is a shell command.

    Args:
        command (dict): The command dict

    Returns:
        bool: Wether the command is a shell command or not.
    """
    toggle = False
    for key, value in command.values():
        if key == "command":
            toggle = True
    return toggle
