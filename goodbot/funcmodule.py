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
from rich.console import Console
from typing import List, Dict, Union, Any

from google.cloud import texttospeech

Path = pathlib.Path


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
        raise TypeError("create_dirs_list(): This function takes a dictionnary as an input.")

    dirs_list: List[dict] = []

    for key, value in all_confs.items():

        # Those dirs are created no matter the content
        to_create: List[str] = ["asciicasts", "embeds", "gifs", "videos"]

        for key_2, value_2 in value.items():
            if value_2:  # There are items in the list.
                to_create.append(key_2)

        if "read" in to_create:
            to_create.append("audio")  # MP3 files

        dirs_list.append({f"scene_{key}": to_create})

    return dirs_list


# TODO: Do not prompt if project_path defined as flag
def create_dirs(
    directories: list, host_dir: Union[str, Path], project_dir: Union[str, Path] = "my_project"
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


def write_read_instructions(read_instructions: str, scene_path: Path, index: int) -> Path:
    """Writes a new `read` instructions file.

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
    """Writes a command instruction `yaml` file.

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
    file_path: Path = commands_path / Path(f"commands_{index + 1}")
    to_write: str = yaml.safe_dump(commands_instructions)

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

            if "read" in scene_item.keys():
                to_read: str = scene_item["read"]
                write_read_instructions(to_read, scene_path, index)

            if "commands" in scene_item.keys():
                try:
                    commands: Dict[str, List[str]] = {
                        "commands": scene_item["commands"],
                        "expect": scene_item["expect"],
                    }
                    write_commands_instructions(commands, scene_path, index)
                except KeyError as error:
                    print(f"Missing key: {error.args[0]}")
                    print("Scene items:")
                    print(scene_item)

    return project_path


########################################################################
#                             Video creation                           #
########################################################################

# Command execution and recording.
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
def record_audio(
    scene: Path, save_path: Path, lang: str = "en-US", lang_name: str = "en-US-Standard-C"
) -> Path:
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
    contains: List[str] = list(scene.iterdir())
    categories: List[str] = [command.name for command in contains]

    if not "read" in categories:
        return Path(".")

    read_path: Path = scene / Path("read")

    for item in read_path.iterdir():
        with open(item, "r") as stream:
            # Assuming everything to read is on one line
            to_read = stream.readlines()[0]
            to_read = to_read.strip()

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=to_read)

        voice = texttospeech.VoiceSelectionParams(
            language_code=lang, name=lang_name, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        file_name = item.stem
        write_path = (save_path / file_name).with_suffix(".mp3")

        with open(write_path, "wb") as out:
            out.write(response.audio_content)
            click.echo(f"Audio content written to file {write_path.absolute()}")

    return save_path
