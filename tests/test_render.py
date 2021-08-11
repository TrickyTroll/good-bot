# -*- coding: utf-8 -*-
"""Testing functions from the `render` module."""
import pathlib
import tempfile
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
        {
            "dir": SAMPLE_PROJECT / Path("scene_1"),
            "want": 2
        },
        {
            "dir": SAMPLE_PROJECT / Path("scene_2"),
            "want": 1
        },
        {
            "dir": SAMPLE_PROJECT,
            "want": 0
        }
    ]

    for test in test_cases:
        assert len(render.fetch_scene_asciicasts(test["dir"])) == test["want"]

def test_fetch_project_asciicasts():
    """
    Testing that fetch_project_asciicasts returns the right amount of
    files.
    """
    test_cases = [
        {
            "dir": SAMPLE_PROJECT,
            "want": 4
        },
        {
            "dir": Path("./tests/"),
            "want": 0
        }
    ]

    for test in test_cases:
        assert len(render.fetch_project_asciicasts(test["dir"])) == test["want"]
