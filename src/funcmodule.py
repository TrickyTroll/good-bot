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
        "commands": [],
        "scenes": [],
        "editor": [],
        "slides": [],
        "read": [],
    }
    for keys, values in parsed_config:

        conf_info["scenes"].append(keys)

        for item in values:
            for k, v in item.items():
                if k == "commands":
                    conf_info["cli_commands"].append(v)
                if k == "read":
                    conf_info["read"].append(v)
                elif k == "slides":
                    conf_info["slides"].append(v)
                elif k == "editor":
                    conf_info["editor"].append(v)
                else:
                    print(f"{k} is not a supported command.")

    return conf_info

########################################################################
#                       Creating directories                           #
########################################################################

def create_dirs_list(conf_info: dict) -> Path:

    to_create = []

    for keys, values in conf_info.items():
        if values: # There are items in the list.
            to_create.append(keys)
        

    if "read" in to_create:
        to_create.append("audio") # MP3 files

    # Those dirs are created no matter the content
    to_create.append("gifs") # Gifs files
    to_create.append("recording") # MP4 files
    to_create.append("project") # Final video

    return to_create

def create_dirs(directories: list, project_dir: str = "my_project") -> Path:
    """Creates directories for the project. This function should be
    called on the host's computer, not in the container. Docker will
    mount the project afterwards.

    Args:
        directories (list): A list of subdirs to create
        project_dir (str, optional): The name of the project. It will
        be used to name the root directory for the project.
         Defaults to "my_project".

    Returns:
        Path : The path towards where the project has been created if
        the command succeded. If it didn't, this returns the path
        towards the current directory.
    """
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

def split_config():
    # Should use parse_config to split the configuration files and
    # save them in the appropriate directories.
    pass

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
