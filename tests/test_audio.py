import pytest
import tempfile
import shutil
import os
import goodbot.audio as audio

from pathlib import Path
from distutils.dir_util import copy_tree

AUDIO_TEST_DIR = Path("./tests/examples/audio")


def test_fetch_audio_instructions():
    """
    Making sure that fetch_audio_instructions finds enough files
    to read.
    """
    to_check = [
        {"file": AUDIO_TEST_DIR / Path("scene_1/read"), "want": 2},
        {"file": AUDIO_TEST_DIR / Path("scene_2/read"), "want": 1},
        {"file": AUDIO_TEST_DIR / Path("scene_3/read"), "want": 0},
    ]
    for test_case in to_check:
        assert len(audio.fetch_audio_instructions(test_case["file"])) == test_case["want"]


def test_fetch_scene_audio_instructions():
    """
    Testing that fetch_scene_audio_instructions returns the correct
    amount of items.
    """
    to_check = [
        {"dir": AUDIO_TEST_DIR / Path("scene_1"), "want": 2},
        {"dir": AUDIO_TEST_DIR / Path("scene_2"), "want": 1},
        {"dir": AUDIO_TEST_DIR / Path("scene_3"), "want": 0},
    ]

    for test_case in to_check:
        assert len(audio.fetch_scene_audio_instructions(test_case["dir"])) == test_case["want"]


def test_fetch_project_audio_instructions():
    """
    Testing that fetch_project_audio_instructions finds the right
    amount of files.
    """
    want = 3
    assert len(audio.fetch_project_audio_instructions(AUDIO_TEST_DIR)) == want


@pytest.mark.skip(reason="It costs money.")
def test_record_audio():
    """
    Making sure that record_audio records the right amount of files for
    a project.
    """
    with tempfile.TemporaryDirectory() as temp:
        copy_tree("./tests/examples/audio", temp)
        project_path = Path(temp)
        # Re-recording
        audio_scripts = audio.fetch_project_audio_instructions(project_path)
        recorded = audio.record_audio(project_path)
        assert len(recorded) == len(audio_scripts)
