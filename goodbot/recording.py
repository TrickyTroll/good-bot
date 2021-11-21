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
    """Get a Good-Bot's content file's id.

    The id is always after the last underscore in the file name.

    Args:
        content_file (Union[Path, str]): A path towards a Good Bot's content file.

    Raises:
        ValueError: If a file does not follow the `[name]_[id].[ext]` pattern because
            the id is not an integer (it cannot be converted to an `int`).
        ValueError: If a file does not follow the `[name]_[id].[ext]` pattern because
            there is no underscore in the file name.

    Returns:
        int: The file's id.
    """
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
    """Sort content files by their id.

    The sorting is done by creating a map of the ids and their corresponding
    file names. Then, the files are sorted by the ids.

    If two files have the same id, there is no real guarantee on which one
    will be first.

    Args:
        content_file_paths (List[Path]): A list of paths towards multiple
            content files.

    Returns:
        List[Path]: A list of paths towards each file, but sorted by their id.
    """

    content_map: Dict[int, Path] = {}

    for content_file in content_file_paths:

        try:
            content_map[get_content_file_id(content_file)] = content_file
        except ValueError as error:
            print(error)
            print("The file has been excluded from the list of things to record.")

    return [content_map[key] for key in sorted(content_map)]


def directory_content_files(content_dir: Path) -> List[Path]:
    """Get all content files in a directory.

    A content file is a file with a `.txt` or `.yaml` extension.

    Args:
        content_dir (Path): The path towards the directory where
            the content files are located.

    Returns:
        List[Path]: A list of paths towards each content file that
            was found.
    """

    all_content_files: List[Path] = []

    for file in content_dir.iterdir():
        if file.suffix in (".txt", ".yaml"):
            all_content_files.append(file)

    return all_content_files


def find_to_record(scene_path: Path) -> List[Path]:
    """Finds each content file to record in a scene.

    This function uses `directory_content_files()` and `sort_content_files()`
    on each directory in the scene that is also in the `ALLOWED_CONTENT_TYPES`
    tuple.

    The content files are returned in the order that they should be recorded.

    Args:
        scene_path (Path): The path towards the scene where the content files
            are located.

    Returns:
        List[Path]: An ordered list of paths towards each content file that was 
            found.
    """

    to_record_in_scene: List[Path] = []

    for directory in scene_path.iterdir():
        if directory.name in ALLOWED_CONTENT_TYPES and directory.name != "read":
            to_record_in_scene += directory_content_files(directory)
            to_record_in_scene += directory_content_files(directory)

    return sort_content_files(to_record_in_scene)


def record_scene(scene_path: Path, docker: bool = False, no_docker: bool = False):
    """Record each content file in a scene.

    Uses `find_to_record()` to find each content file to record in the scene.
    Then, either the `record_command()` or the `record_editor()` is used depending
    on the content type.

    This function is where other functionalities for Good-Bot should be added.

    Args:
        scene_path (Path): The path towards the scene to record.
        docker (bool, optional): Whether or not to pass the `--docker` flag to the
            `record_command()` function. This will override Good-Bot's docker detection
            feature and force the program to assume that it is running in a container.
            Defaults to False.
        no_docker (bool, optional): Whether or not to pass the `--no-docker` flag to
            the `record_command()` function. This will override Good-Bot's docker
            detection feature and force the program to assume that it is **not** running
            in a container. Defaults to False.
    """
    # Things in a scene are already numbered starting at 1
    to_record_sorted: List[Path] = find_to_record(scene_path)

    for file_to_record in to_record_sorted:
        if file_to_record.parent.name == "commands":
            shell_commands.record_command(file_to_record, docker, no_docker, debug=True)
        elif file_to_record.parent.name == "edit":
            editor.record_editor(file_to_record)
        # Each type of content to record goes here.

# Debugging
if __name__ == "__main__":
    record_scene(Path("./toto/scene_1"))
