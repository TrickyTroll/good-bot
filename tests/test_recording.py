from pathlib import Path
import pytest

from goodbot import recording

def test_get_content_file_id_works_with_strings():
    """
    Test that get_content_file_id works with strings
    """
    assert recording.get_content_file_id("commands_1.yaml") == 1

def test_get_content_file_id():
    """
    Test that `get_content_file_id()` returns the correct
    value for different paths.

    A file id is the integer value after a `_` character in
    a file name.
    """
    all_samples = [
        (Path("/foo/bar_1.yaml"), 1),
        (Path("/foo/bar_2.yaml"), 2),
        ("/foo/bar_3.yaml", 3),
        ("../example/commands_0.yaml", 0)
    ]

    for sample in all_samples:
        assert recording.get_content_file_id(sample[0]) == sample[1]

def test_get_content_file_id_raises():
    """
    Makes sure that `get_content_file_id()` raises an error
    if the file name does not contain a `_` character followed
    by an integer value.
    """

    with pytest.raises(ValueError):
        recording.get_content_file_id("commands.yaml")

def test_sort_content_files():
    """
    Making sure that `sort_content_files()` returns a list
    of paths sorted by the file id when it receives a list
    of Path objects as an input.
    """

    samples = [
        ([Path("../example/commands_0.yaml"), Path("../example/commands_1.yaml"), Path("../example/commands_2.yaml")],
        [Path("../example/commands_0.yaml"), Path("../example/commands_1.yaml"), Path("../example/commands_2.yaml")]),
        ([Path("../example/commands_2.yaml"), Path("../example/commands_1.yaml"), Path("../example/commands_0.yaml")],
        [Path("../example/commands_0.yaml"), Path("../example/commands_1.yaml"), Path("../example/commands_2.yaml")]),
        ([Path("../example/commands_0.yaml"), Path("../example/commands_0.yaml")],
        [Path("../example/commands_0.yaml")]),
        ([Path("../example/commands_1.yaml"), Path("../example/commands_0.yaml"), Path("../example/commands_0.yaml")],
        [Path("../example/commands_0.yaml"), Path("../example/commands_1.yaml")]),
    ]

    for sample in samples:
        assert recording.sort_content_files(sample[0]) == sample[1]

def test_directory_content_files():
    """
    Making sure that `directory_content_files()` returns each
    `.yaml` and `.txt` files in the provided directory.

    Missing test cases for `.txt` files.
    """

    scene_dir = Path("./tests/examples/recording-sample/scene_2/")
    scene_2_want_commands = [Path("./tests/examples/recording-sample/scene_2/commands/commands_1.yaml")]
    scene_2_want_editor = [Path("./tests/examples/recording-sample/scene_2/edit/edit_2.yaml")]
    commands = recording.directory_content_files(scene_dir / "commands")

    for item in commands:
        assert item in scene_2_want_commands

    assert len(commands) == len(scene_2_want_commands)
    editor = recording.directory_content_files(scene_dir / "edit")

    for item in editor:
        assert item in scene_2_want_editor

    assert len(editor) == len(scene_2_want_editor)

def tests_find_to_record():
    """
    Testing that `find_to_record()` finds each file to record in a project.
    Audio instructions aren't covered by this function.
    """

    scene_dir_2 = Path("./tests/examples/recording-sample/scene_2/")
    scene_2_want = [Path("./tests/examples/recording-sample/scene_2/commands/commands_1.yaml"), Path("./tests/example/recording-sample/scene_2/commands_1.yaml"), Path("./tests/examples/recording-sample/scene_2/edit/edit_2.yaml")]

    for item in recording.find_to_record(scene_dir_2):
        assert item in scene_2_want

    scene_dir_1 = Path("./tests/examples/recording-sample/scene_1/")
    scene_1_want = [Path("./tests/examples/recording-sample/scene_1/commands/commands_1.yaml")]

    for item in recording.find_to_record(scene_dir_1):
        assert item in scene_1_want