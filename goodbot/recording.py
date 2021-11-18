from pathlib import Path
from typing import List, Dict, Union

# Each recording module has to be imported here
from goodbot import editor, shell_commands, audio
from goodbot.utils import is_scene
from goodbot.funcmodule import ALLOWED_CONTENT_TYPES

# Each element in a scene has an id. The id is the order
# that should be followed when recording. They start at
# 1.


def get_content_file_id(content_file: Union[Path, str]) -> int:

    if isinstance(content_file, str):
        content_file = Path(content_file)

    file_name: str = content_file.stem

    try:
        return int(file_name.split("_")[1])
    except ValueError:
        raise ValueError(
            f"{content_file} does not seem to follow Good-Bot's naming scheme."
        )
    except IndexError:
        raise ValueError(
            f"{content_file} does not seem to follow Good-Bot's naming scheme."
        )


def sort_content_files(content_file_paths: List[Path]) -> List[Path]:

    content_map: Dict[int, Path] = {}

    for content_file in content_file_paths:

        try:
            content_map[get_content_file_id(content_file)] = content_file
        except ValueError as error:
            print(error)
            print("The file has been excluded from the list of things to record.")

    return [content_map[key] for key in sorted(content_map)]


def directory_content_files(content_dir: Path) -> List[Path]:

    all_content_files: List[Path] = []

    for file in content_dir.iterdir():
        if file.suffix in (".txt", ".yaml"):
            all_content_files.append(file)

    return all_content_files


def find_to_record(scene_path: Path) -> List[Path]:

    to_record_in_scene: List[Path] = []

    for directory in scene_path.iterdir():
        if directory.name in ALLOWED_CONTENT_TYPES and directory.name != "read":
            to_record_in_scene += directory_content_files(directory)
            to_record_in_scene += directory_content_files(directory)

    return sort_content_files(to_record_in_scene)


def record_scene(scene_path: Path, docker: bool = False, no_docker: bool = False):
    # Things in a scene are already numbered starting at 1
    to_record_sorted: List[Path] = find_to_record(scene_path)

    for file_to_record in to_record_sorted:
        if file_to_record.parent.name == "commands":
            shell_commands.record_command(file_to_record, docker, no_docker)
        elif file_to_record.parent.name == "edit":
            editor.record_editor(file_to_record)
        # Each type of content to record goes here.
