import pytest
import shutil
import goodbot.audio as audio

from pathlib import Path
from hypothesis import given, strategies as st

AUDIO_TEST_DIR = Path("./tests/examples/audio")

def test_fetch_audio_instructions():
    """
    Making sure that fetch_audio_instructions finds enough files
    to read.
    """
    to_check = [
        {
            "dir": AUDIO_TEST_DIR / Path("scene_1/read"),
            "want": 2
        },
        {
            "dir": AUDIO_TEST_DIR / Path("scene_2/read"),
            "want": 1
        },
        {
            "dir": AUDIO_TEST_DIR / Path("scene_3/read"),
            "want": 0
        }
    ]
    for test_case in to_check:
        assert len(audio.fetch_audio_instructions(test_case["dir"])) == test_case["want"]
