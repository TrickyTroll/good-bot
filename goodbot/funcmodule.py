# -*- coding: utf-8 -*-
"""`goodbot`'s funcmodule.

This module contains every function used by `goodbot`'s command line
interface.
"""

import os
import sys
import pathlib
import shutil
import click
import yaml
from rich.console import Console
from typing import List, Dict, Union, Any, KeysView

Path = pathlib.Path

ALLOWED_CONTENT_TYPES: tuple = ("edit", "read", "commands")

########################################################################
#                               YAML parsing                           #
########################################################################


def config_parser(file_path: pathlib.Path) -> Dict[int, list]:
    """Opens and parses a `yaml` configuration file.

    Uses [PyYAML](https://pyyaml.org) to parse the configuration file.

    Args:
        file_path (pathlib.Path): The path towards the user's
        configuration file.

    Raises:
        TypeError: Raises a `TypeError` if the parsed object is
            not of type `dict`. It means that the configuration file
            wasn't formatted properly.

    Returns:
        dict: A Python object representation of the `.yaml`
            configuration file.
    """
    with open(file_path) as stream:
        configuration: str = stream.read()

    parsed_file: dict = yaml.safe_load(configuration)

    if not isinstance(parsed_file, dict):
        raise TypeError("Your config is not formatted properly.")

    return parsed_file


def config_info(parsed_config: Dict[int, List[dict]]) -> Dict[int, Dict[str, list]]:
    """Gets useful information on the configuration file.

    Useful to find:

    * How many scene directories should be created.
    * Whether or not to create audio directories.
    * Types of things to do.

    Args:
        parsed_config (Dict[int, List[dict]]): The parsed
            configuration file. This should be returned by the
            `config_parser()` function.

    Raises:
        ValueError: If a scene contains nothing. Tells the user to
            remove the scene.

    Returns:
        Dict[int, Dict[str, list]]: A `dict` that contains every type of thing to
            create as `keys`. The `values` are lists of instructions for
            every type of thing to create.
    """

    all_confs: Dict[int, Dict[str, list]] = {}

    all_scenes: List[int] = [(i + 1) for i in range(max(parsed_config.keys()))]

    for key in all_scenes:

        values: List[Dict[str, str]] = parsed_config[key]

        if not values:
            raise ValueError(f"Scene #{key} is empty, please remove it.")

        conf_info: Dict[str, list] = {
            "commands": [],
            "expect": [],
            "scenes": [],
            "edit": [],
            "slides": [],
            "read": [],
        }

        for item in values:
            for key_2, value_2 in item.items():
                if key_2 == "commands":
                    to_append = {"commands": item["commands"]}
                    if "expect" in item.keys():
                        to_append["expect"] = item["expect"]
                    conf_info["commands"].append(to_append)
                elif key_2 == "expect":
                    # Expect key are handled in the previous case.
                    continue
                elif key_2 == "read":
                    conf_info["read"].append(value_2)
                elif key_2 == "slides":
                    conf_info["slides"].append(value_2)
                elif key_2 == "edit":
                    conf_info["edit"].append(value_2)
                else:
                    click.echo(f'"{key_2}" is not a supported command.')
                    sys.exit()

        all_confs[key] = conf_info

    return all_confs


########################################################################
#                       Creating directories                           #
########################################################################


def create_dirs_list(all_confs: Dict[int, Dict[str, list]]) -> List[dict]:
    """Creates required directories for a project.

    Uses the information provided by `config_info()`
    to create directories according to the user's configuration
    file.

    Args:
        all_confs (Dict[str, list]): A `dict` of configuration
            information. This should be created using the
            `config_info()` function.

    Returns:
        List[dict]: A list of directories to create. Each `item` in
            the list is a `dict` that contains scene names as `keys`
            and scene elements as `values`. Scene elements are what
            `good-bot` will record or create.
    """
    if not isinstance(all_confs, dict):
        raise TypeError(
            "create_dirs_list(): This function takes a dictionnary as an input."
        )

    dirs_list: List[dict] = []

    for (
        scene_number,
        contents,
    ) in all_confs.items():  # Keys are scene numbers, values is the content

        # Those dirs are always created
        to_create: List[str] = ["asciicasts", "embeds", "gifs", "videos"]

        for content_type, instructions in contents.items():
            if instructions:  # There are items in the list.
                to_create.append(content_type)  # Things like the editor are added here.

        # Read has been added in the previous block
        if "read" in to_create:
            to_create.append("audio")  # MP3 files

        dirs_list.append({f"scene_{scene_number}": to_create})

    return dirs_list


def create_dirs(
    directories: list,
    host_dir: Union[str, Path],
    project_dir: Union[str, Path] = "my_project",
) -> Path:
    """Creates directories for the project. This function should be
    called on the host's computer, not in the container. Docker will
    mount the project afterwards.

    Args:
        directories (list): A list of subdirs to create
        project_dir (str or Path, optional): The name of the project. It will
        be used to name the root directory for the project. Defaults to "my_project".

    Returns:
        Path : The path towards where the project has been created if
        the command succeded. If it didn't, this returns the path
        towards the current directory.
    """
    if not isinstance(directories, list):
        raise TypeError("`directories` must be a list of dictionnaries.")
    if not isinstance(project_dir, (str, Path, pathlib.PosixPath, pathlib.WindowsPath)):
        raise TypeError(f"`project_dir` must be of type `str`, not {type(project_dir)}")

    project_dir = Path(project_dir)
    overwrite = False

    if project_dir.is_dir():

        click.echo(f"Directory {host_dir} exists!")
        resp = input(f"Would you like to overwrite {host_dir}?: ")

        if resp.lower() == "yes":

            # Erase the directory
            overwrite = True
            confirm = input(f"Are you sure you want to remove {host_dir}?: ")

            if confirm.lower() == "yes":
                shutil.rmtree(project_dir)

                # Then make a new one

                os.mkdir(project_dir)

            else:
                sys.exit()

        else:
            sys.exit()

    else:
        os.mkdir(project_dir)

    for item in directories:

        # There should only be one key, no need for
        # a for loop.
        scene_id = list(item.keys())[0]
        scene = Path(scene_id)

        # There should only be one value too
        # This shoud probably stored as a tuple now that
        # I think about it...
        for directory in list(item.values())[0]:

            new_dir = project_dir / scene / Path(directory)

            if new_dir.is_dir() and not overwrite:
                click.echo(f"Folder {new_dir} exists!")
            else:
                os.makedirs(new_dir)

    return project_dir.absolute()


def write_read_instructions(
    read_instructions: str, scene_path: Path, index: int
) -> Path:
    """*Deprecated, use `write_yaml_instructions` instead.*

    The instructions come from the `read` key in the user's `yaml`
    configuration file. Files created by this function are what is
    sent to the TTS engine by the `record_audio()` function.

    Args:
        read_instructions (str): A string of text that will be written to the
            `.txt` file. Can contain `ssml` syntax. The string is written
            as-is.
        scene_path (Path): The path towards the scene where
            `read_instructions` come from.
        index (int): The index of the command block.

    Returns:
        Path: The path towards where the new text file has been written.
    """
    read_path: Path = scene_path / Path("read")

    file_name: str = f"read_{index + 1}.txt"
    file_path: Path = read_path / Path(file_name)

    with open(file_path, "w") as stream:
        stream.write(read_instructions)

    return file_path


def write_commands_instructions(
    commands_instructions: Dict[str, List[str]], scene_path: Path, index: int
) -> Path:
    """*Deprecated, use `write_yaml_instructions` instead.*

    Writes a command instruction `yaml` file.

    These are the files that [`runner`](github.com/TrickyTroll/good-bot-runner)
    takes as input to type commands and expect stuff.

    Args:
        commands_instructions (Dict[str, List[str]]): A dictionary of commands
            and things to expect. Keys should be either `commands` or
            `expect`. The values should be a list of commands and a list of
            things to expect.
        scene_path (Path): The path towards the scene where the
            `commands_instructions` come from.
        index (int): The index of the command block.

    Returns:
        Path: The path towards where the new `yaml` file has been written.
    """
    commands_path: Path = scene_path / Path("commands")
    file_path: Path = commands_path / Path(f"commands_{index + 1}").with_suffix(".yaml")
    to_write: str = yaml.safe_dump(commands_instructions)

    with open(file_path, "w") as stream:
        stream.write(to_write)

    return file_path


def write_yaml_instructions(
    instructions: Any, scene_path: Path, content_type: str, id: int
) -> Path:
    """
    write_yaml_instructions writes instructions for a certaincommand in the
    YAML format.

    Commands should be passed as dictionnaries, where keys are instruction
    types (command, expect, read, ...) and values are the arguments for those
    commands.

    Args:
        instructions (dict): The instruction dictionnary that will be written in
        a YAML file.
        scene_path (Path): The path towards the scene where the instructions come
        from. Used to write the file to the proper location.
        content_type (str): The type of command targetted by the instructions.
        Allowed commands are contained in the `ALLOWED_CONTENT_TYPES` variable.
        id (int): The id of the file. Starts at 0 and is incremented for each
        element in a scene. It is included in the name of the file so that each
        component can be recorded in the correct order.

    Returns:
        Path: The path towards the newly created  YAML file.
    """
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"The type {content_type} is not implemented.")
    content_type_path: Path = scene_path / Path(content_type)
    content_type_path.mkdir(exist_ok=True)
    file_path: Path = content_type_path / Path(f"{content_type}_{id + 1}").with_suffix(
        ".yaml"
    )
    to_write: str = yaml.safe_dump(instructions)

    with open(file_path, "w") as stream:
        stream.write(to_write)

    return file_path


def split_config(parsed: Dict[int, List[dict]], project_path: Path) -> Path:
    """Splits the main `yaml` script file in many smaller scripts.

    The subscripts are then written in directories that correspond
    to their categories. For example, commands to send to the `runner`
    program will be written in the `commands` directory, while the
    text files sent to the text to speech program will be written in
    the `read` directory.

    Args:
        parsed (Dict[int, List[dict]]): The parsed configuration file.
            This should be created by the `config_parser()` function.
        project_path (Path): The path towards the project directory.
            This value is returned by `create_dirs`.

    Returns:
        Path: The path towards the project.
    """
    # This should probably be grouped
    for scene_number, scene_contents in parsed.items():

        scene_path: Path = project_path / Path(f"scene_{scene_number}")

        for index, scene_item in enumerate(scene_contents):

            scene_item_keys: KeysView[Any] = scene_item.keys()

            # Reading text
            if "read" in scene_item_keys:
                to_read: str = scene_item["read"]
                write_yaml_instructions(to_read, scene_path, "read", index)

            # Typing commands
            if "commands" in scene_item_keys:
                try:
                    commands: Dict[str, List[str]] = {
                        "commands": scene_item["commands"],
                        "expect": scene_item["expect"],
                    }
                    write_yaml_instructions(commands, scene_path, "commands", index)

                except KeyError as error:
                    print(f"Missing key: {error.args[0]}")
                    print("Scene items:")
                    print(scene_item)

            # Editing text files
            if "edit" in scene_item_keys:
                to_edit: List[dict] = scene_item["edit"]
                write_yaml_instructions(to_edit, scene_path, "edit", index)

    return project_path


if __name__ == "__main__":
    conf_path = Path("./examples/basics/config.yaml")
    parsed_config = config_parser(conf_path)
    info = config_info(parsed_config)
    print(info)
