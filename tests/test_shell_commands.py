import tempfile
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path
from goodbot import shell_commands, render
from tests.test_funcs import PROJECT_PATH, PARSED

VIDEO_TEST_DIR = Path("./tests/examples/video")


def test_fetch_runner_instructions():
    """
    Making sure that fetch_runner_instructions finds enough instructions
    files
    """
    to_check = [
        {"file": VIDEO_TEST_DIR / Path("scene_1/commands"), "want": 2},
        {"file": VIDEO_TEST_DIR / Path("scene_2/commands"), "want": 1},
        {"file": VIDEO_TEST_DIR / Path("scene_3/commands"), "want": 1},
        {"file": VIDEO_TEST_DIR / Path("scene_fake/commands"), "want": 0},
    ]
    for test_case in to_check:
        assert len(shell_commands.fetch_runner_instructions(test_case["file"])) == test_case["want"]


def test_fetch_scene_runner_instructions():
    """
    Testing that fetch_scene_runner_instructions returns the correct
    amount of items.
    """
    to_check = [
        {"dir": VIDEO_TEST_DIR / Path("scene_1"), "want": 2},
        {"dir": VIDEO_TEST_DIR / Path("scene_2"), "want": 1},
        {"dir": VIDEO_TEST_DIR / Path("scene_3"), "want": 1},
        {"dir": VIDEO_TEST_DIR / Path("scene_fake"), "want": 0},
    ]

    for test_case in to_check:
        assert len(shell_commands.fetch_scene_runner_instructions(test_case["dir"])) == test_case["want"]


def test_fetch_project_runner_instructions():
    """
    Testing that fetch_project_runner_instructions finds the right
    amount of files.
    """
    want = 4
    assert len(shell_commands.fetch_project_runner_instructions(VIDEO_TEST_DIR)) == want


def test_record_commands():
    """
    Making sure that record_commands records the correct amount of
    files in a project.
    """
    with tempfile.TemporaryDirectory() as temp:
        copy_tree("./tests/examples/video", temp)
        project_path = Path(temp)
        # Removing the fake scene
        shutil.rmtree(project_path / ("scene_fake"))
        # Removing existing asciicasts
        all_asciicasts = render.fetch_project_asciicasts(project_path)
        for path in all_asciicasts:
            os.remove(path)
        # Re-recording
        rerecorded = shell_commands.record_commands(project_path)
        # making sure that re-recorded is the same as the previous
        # recordings
        for asciicast in all_asciicasts:
            assert asciicast in rerecorded
