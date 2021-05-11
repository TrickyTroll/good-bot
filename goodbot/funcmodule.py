import os
import sys
import yaml
import click
import shutil
import subprocess
import pathlib

from google.cloud import texttospeech

Path = pathlib.Path


########################################################################
#                               YAML parsing                           #
########################################################################


def config_parser(file: pathlib.Path) -> dict:
    """Parses the YAML config and recturns it as a dictionnary.

    Args:
        file: The path towards the config file.

    Returns:
        A dictionnary representation of the configuration file.
    """
    with open(file) as stream:
        configuration = stream.read()

    parsed_file = yaml.safe_load(configuration)

    if type(parsed_file) != dict:
        click.echo("Your config is not formatted properly.")
        click.echo(parsed_file)
        sys.exit()

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

    all_confs = {}

    conf_template = {
        "commands": [],
        "expect": [],
        "scenes": [],
        "editor": [],
        "slides": [],
        "read": [],
    }

    breakpoint()
    all_scenes = [(i + 1) for i in range(max(parsed_config.keys()))]

    for key in all_scenes:

        values = parsed_config[key]

        if not values:
            click.echo(f"Scene #{keys} is empty, please remove it.")
            sys.exit()

        conf_info = conf_template.copy()

        for item in values:
            print("Value: " + str(item))
            for k, v in item.items():
                if k == "commands":
                    to_append = {"commands": item["commands"]}
                    if "expect" in item.keys():
                        to_append["expect"] = item["expect"]
                    conf_info["commands"].append(to_append)
                elif k == "expect":
                    continue
                elif k == "read":
                    conf_info["read"].append(v)
                elif k == "slides":
                    conf_info["slides"].append(v)
                elif k == "editor":
                    conf_info["editor"].append(v)
                else:
                    click.echo(f'"{k}" is not a supported command.')
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

    dirs_list = []

    for k, v in all_confs.items():

        to_create = []

        for keys, values in v.items():
            if values:  # There are items in the list.
                to_create.append(keys)

        if "read" in to_create:
            to_create.append("audio")  # MP3 files

        # Those dirs are created no matter the content
        to_create.append("asciicasts")  # asciicasts

        dirs_list.append({f"scene_{k}": to_create})

    return dirs_list


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
    for k, v in todos.items():

        scene_path = Path(f"scene_{k}")

        for key, value in v.items():

            write_path = Path(key)

            if "read" in key:
                ext = ".txt"
            else:
                ext = ".yaml"

            for i in range(len(value)):

                try:
                    to_write = yaml.safe_dump(value[i])

                except TypeError:
                    sys.exit()

                file_name = Path(f"file_{i}")
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

    if dir_name[0:5] == "scene" and contains_something:

        return True

    else:

        return False


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

    if "commands" in categories:
        is_commands = True
    else:
        is_commands = False

    if not is_commands:
        return Path(os.getcwd())
    else:
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

    if "read" in categories:
        is_read = True
    else:
        is_read = False

    audio_dir = save_path

    if not is_read:
        return Path(os.getcwd())
    else:
        read_path = scene / Path("read")

    for item in read_path.iterdir():
        with open(item, "r") as stream:
            # Assuming everything to read is on one line
            # TODO: Read a multi line file.
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