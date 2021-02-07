import os
from pathlib import Path

import click
import yaml

import classmodule


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


def config_info(parsed_config: dict) -> dict:
    """
    Returns useful info on the configuration file.

    Args:
        parsed_config (dict): The parsed configuration file. This should
        be handled by the config_parser func.

    Returns:
        dict: A dictionary that contains usful information about the
        configuration.
    """

    conf_info = {
        "cli_commands": [],
        "scenes": [],
        "text_edit": [],
        "slides": []
    }

    for item in parsed_config:
        for keys, values in item.values():
            if "scene" in keys:
                if item["scene"] not in conf_info["scenes"]:
                    conf_info["scenes"].append(f"scene_{item['scene']}")
            if "commands" in keys:
                conf_info["cli_commands"].append(item)
            elif "slides" in keys:
                conf_info["slides"].append(item)
            elif "editor" in keys:
                conf_info["text_edit"].append(item)
            else:
                print("This item does not match any of the supported commands.")

    return conf_info

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
