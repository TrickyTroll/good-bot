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
