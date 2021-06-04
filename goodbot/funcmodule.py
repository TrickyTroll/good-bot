# -*- coding: utf-8 -*-
"""`goodbot`'s funcmodule.

This module contains every function used by `goodbot`'s command line
interface.
"""

import os
import sys
import pathlib
import subprocess
import shutil
import click
import yaml
from typing import List, Dict, Union, Any

from google.cloud import texttospeech

Path = pathlib.Path


########################################################################
#                               YAML parsing                           #
########################################################################


def config_parser(file_path: pathlib.Path) -> dict:
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


def config_info(parsed_config: Dict[str, Union[str, dict]]) -> dict:
    """Gets useful information on the configuration file.

    Useful to find:

    * How many scene directories should be created.
    * Whether or not to create audio directories.
    * Types of things to do.

    Args:
        parsed_config (Dict[str, Union[str, dict]]): The parsed
            configuration file. This should be returned by the
            `config_parser()` function.

    Raises:
        ValueError: If a scene contains nothing. Tells the user to
            remove the scene.

    Returns:
        dict: A `dict` that contains every type of thing to create
            as `keys`. The `values` are lists of instructions for
            every type of thing to create.
    """

    all_confs: Dict[str, list] = {}

    all_scenes: List[int] = [(i + 1) for i in range(max(parsed_config.keys()))]

    for key in all_scenes:

        values: List[Dict[str, str]] = parsed_config[key]

        if not values:
            raise ValueError(f"Scene #{key} is empty, please remove it.")

        conf_info: Dict[str, list] = {
            "commands": [],
            "expect": [],
            "scenes": [],
            "editor": [],
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
                elif key_2 == "editor":
                    conf_info["editor"].append(value_2)
                else:
                    click.echo(f'"{key_2}" is not a supported command.')
                    sys.exit()

        all_confs[key] = conf_info

    return all_confs


########################################################################
#                       Creating directories                           #
########################################################################


def create_dirs_list(all_confs: dict) -> list:
    """Creates required directories for a project.

    Uses the information provided by ``config_info()``
    to create directories according to the user's configuration
    file.

    Args:
        all_confs (dict): A ``dict`` of configuration information.
            This should be created using the ``config_info()``
            function.

    Returns:
        list: A list of directories to create.
    """
    if not isinstance(all_confs, dict):
        raise TypeError(
            "create_dirs_list(): This function takes a dictionnary as an input."
        )

    dirs_list = []

    for key, value in all_confs.items():

        to_create = []

        for key_2, value_2 in value.items():
            if value_2:  # There are items in the list.
                to_create.append(key_2)

        if "read" in to_create:
            to_create.append("audio")  # MP3 files

        # Those dirs are created no matter the content
        to_create.append("asciicasts")  # asciicasts

        dirs_list.append({f"scene_{key}": to_create})

    return dirs_list


def create_dirs(directories: list, project_dir: str or Path = "my_project") -> Path:
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

        click.echo(f"Directory {project_dir} exists!")
        resp = input(f"Would you like to overwrite {project_dir}?: ")

        if resp.lower() == "yes":

            # Erase the directory
            overwrite = True
            confirm = input(f"Are you sure you want to remove {project_dir}?: ")

            if confirm.lower() == "yes":
                shutil.rmtree(project_dir)

                # Then make a new one

                os.mkdir(project_dir)

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


def split_config(parsed: click.File, project_path: Path) -> Path:
    """Splits the main config file into sub configurations for
    every type of action.

    Args:
        parsed (click.File): The parsed configuration file. This
        should be handled by the `parse_config` function.
        project_path (Path): The path towards the project. This
        path is returned by the `create_dirs` function.

    Returns:
        Path: The same project path that was passed.
    """
    todos = config_info(parsed)

    # This should probably be grouped
    for key, value in todos.items():

        scene_path = Path(f"scene_{key}")

        for key_2, value_2 in value.items():

            write_path = Path(key_2)

            if "read" in key_2:
                ext = ".txt"
            else:
                ext = ".yaml"

            for index, element in enumerate(value_2):

                try:
                    to_write = yaml.safe_dump(element)

                except TypeError:
                    sys.exit()

                file_name = Path(f"file_{index}")
                file_path = project_path / scene_path / write_path / file_name

                click.echo(f"Creating {file_path.with_suffix(ext)}")

                with open(file_path.with_suffix(ext), "w") as file:

                    file.write(to_write)

    return project_path


########################################################################
#                             Video creation                           #
########################################################################

# Command execution and recording.
def is_scene(directory: Path) -> bool:
    """Checks if a directory is a scene that contains instructions.

    Args:
        directory (pathlib.Path): The path towards the directory to
        check.
    Returns:
        bool: Wether the directory is a scene that contains elements
        or not.
    """

    if directory.is_dir():
        dir_name = directory.name
        contains_something = any(directory.iterdir())
    else:
        return False

    return dir_name[0:5] == "scene" and contains_something


def list_scenes(project_dir: click.Path) -> list:
    """Lists scenes in the project directory.

    Args:
        project_dir (click.Path): The path towards the location of the
        project.
    Returns:
        list: A list of directories (Paths).
    """
    project_dir = Path(project_dir)
    all_scenes = []

    for directory in project_dir.iterdir():

        if is_scene(directory):

            all_scenes.append(directory)

        else:

            click.echo(f"The directory {directory} was ignored.")

    return all_scenes


def record_commands(scene: Path, save_path: Path) -> Path:
    """Records a gif for every video in the commands directory of the
    specified scene.

    Args:
        scene (pathlib.Path): The path towards the scene to record.
        save_path (pathlib.Path): The path towards the directory
        where the gifs will be saved.
    Returns:
        pathlib.Path: The path towards the gif that has been recorded.
        If nothing has been recorded, this function returns the path
        of the current working directory instead.
    """

    contains = list(scene.iterdir())
    categories = [command.name for command in contains]

    is_commands = "commands" in categories

    if not is_commands:
        return Path(os.getcwd())

    commands_path = scene / Path("commands")

    click.echo(f"Recording shell commands for {str(scene)}.")

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


# Audio recording
def record_audio(scene: Path, save_path: Path) -> Path:
    """Records audio by reading the `read` files using Google TTS.

    Args:
        scene (click.Path): The path towards the files to read.
        Only the first line of these files will be read.
        save_path (click.Path): The path where the mp3 audio file
        will be saved. This does not include the file name, as it
        will be kept from the read path.
    Returns:
        click.Path: The path where the audio file is saved. This
        now includes the name of the file.
    """
    contains = list(scene.iterdir())
    categories = [command.name for command in contains]

    is_read = "read" in categories

    audio_dir = save_path

    if not is_read:
        return Path(os.getcwd())

    read_path = scene / Path("read")

    for item in read_path.iterdir():
        with open(item, "r") as stream:
            # Assuming everything to read is on one line
            to_read = stream.readlines()[0]
            to_read = to_read.strip()

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=to_read)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        file_name = item.stem
        write_path = (save_path / file_name).with_suffix(".mp3")

        with open(write_path, "wb") as out:
            out.write(response.audio_content)
            click.echo(f"Audio content written to file {write_path.absolute()}")

    return audio_dir
