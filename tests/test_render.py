# -*- coding: utf-8 -*-
"""Testing functions from the `render` module."""
import pathlib
import tempfile
import pytest
import os
from goodbot import render

Path = pathlib.Path

SAMPLE_PROJECT = Path("./tests/examples/render-sample")


def test_fetch_scene_gifs():
    """
    Making sure that `fetch_scene_gifs` finds the right amount of gifs.
    """
    scene_1_path = SAMPLE_PROJECT / Path("scene_1")
    all_gifs = render.fetch_scene_gifs(scene_1_path)
    assert len(all_gifs) == 2


def test_fetch_scene_gifs_ignores():
    """
    Testing that the function `fetch_scene_gifs` ignores file types
    different than `gif`.
    """
    scene_2_path = SAMPLE_PROJECT / Path("scene_2")
    all_gifs_no_dummy = render.fetch_scene_gifs(scene_2_path)
    dummy_path = scene_2_path / Path("gifs/dummy.txt")
    with open(dummy_path, "w") as stream:
        stream.write("Hello, world!\n")

    all_gifs_with_dummy = render.fetch_scene_gifs(scene_2_path)

    os.remove(dummy_path)

    assert len(all_gifs_no_dummy) == len(all_gifs_with_dummy)


def test_is_asciicast():
    """
    testing that is_asciicast returns true on real asciicast
    files.
    """
    sample_dir = SAMPLE_PROJECT / Path("scene_1/asciicasts")

    for asciicast in sample_dir.iterdir():
        assert render.is_asciicast(asciicast)


def test_is_asciicast_false():
    """
    Making sure that is_asciicast returns false when a file
    is not an ascciinema recording.
    """
    sample_dir = SAMPLE_PROJECT / Path("scene_1/gifs")

    for asciicast in sample_dir.iterdir():
        assert not render.is_asciicast(asciicast)


def test_is_asciicast_wrong_version():
    """
    Testing is_asciicast on a file that has version=1 instead
    of 2. is_asciicast should return false in this case.
    """
    sample_file = Path("./tests/examples/file_0-wrong-version.cast")

    assert not render.is_asciicast(sample_file)


def test_fetch_scene_asciicasts():
    """
    Testing that asciicast fetching for a scene returns the
    correct amount of files.
    """
    test_cases = [
        {"dir": SAMPLE_PROJECT / Path("scene_1"), "want": 2},
        {"dir": SAMPLE_PROJECT / Path("scene_2"), "want": 1},
        {"dir": SAMPLE_PROJECT, "want": 0},
    ]

    for test in test_cases:
        assert len(render.fetch_scene_asciicasts(test["dir"])) == test["want"]


def test_fetch_project_asciicasts():
    """
    Testing that fetch_project_asciicasts returns the right amount of
    files.
    """
    test_cases = [{"dir": SAMPLE_PROJECT, "want": 4}, {"dir": Path("./tests/"), "want": 0}]

    for test in test_cases:
        assert len(render.fetch_project_asciicasts(test["dir"])) == test["want"]


def test_fetch_project_asciicasts_error():
    """
    Testing fetch_project_ascicasts' error handling. Testing on a file
    and a non-existent directory.
    """
    wrong_type: Path = Path("./tests/examples/no-audio.yaml")
    not_exists: Path = Path("./foobar/foo/bar")

    if not_exists.exists():
        raise FileExistsError(f"Test case {not_exists} should not exist. Please remove it.")

    with pytest.raises(FileNotFoundError):
        render.fetch_project_asciicasts(not_exists)

    with pytest.raises(NotADirectoryError):
        render.fetch_project_asciicasts(wrong_type)

def test_corresponding_audio():
    """
    Making sure that corresponding audio returns the correct
    pair of paths.
    """
    test_cases = [
        {
            "gif": SAMPLE_PROJECT / "scene_1/gifs/commands_1.gif",
            "want": (
                SAMPLE_PROJECT / "scene_1/gifs/commands_1.gif",
                SAMPLE_PROJECT / "scene_1/audio/read_1.mp3"
            )
        },
        {
            "gif": SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
            "want": (
                SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
                SAMPLE_PROJECT / "scene_1/audio/read_2.mp3"
            )
        },
        {
            "gif": SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif",
            "want": (
                SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif",
                None
            )
        }
    ]

    for test in test_cases:
        assert render.corresponding_audio(test["gif"]) == test["want"]

def test_link_audio():
    """
    Testing that link_audio links the proper items together. This is
    done by comparing each item in the returned list to the list that
    should be returned.
    """
    test_cases = [
        {
            "scene": SAMPLE_PROJECT / "scene_1",
            "want": [
                (
                    SAMPLE_PROJECT / "scene_1/gifs/commands_1.gif",
                    SAMPLE_PROJECT / "scene_1/audio/read_1.mp3"
                ),
                (
                    SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
                    SAMPLE_PROJECT / "scene_1/audio/read_2.mp3"
                )
            ]
        },
        {
            "scene": SAMPLE_PROJECT / "scene_3",
            "want": [
                (
                    SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif",
                    None
                )
            ]
        }
    ]

    for test in test_cases:
        for item in render.link_audio(test["scene"]):
            assert item in test["want"]
