from pathlib import Path
from goodbot import recording
from tests.test_funcs import PROJECT_PATH, PARSED

VIDEO_TEST_DIR = Path("./tests/examples/video")


def test_is_scene_false():
    """
    Makes sure that the `is_scene()` function does not recognize
    a project path as a scene path.
    """
    not_a_scene_path = PROJECT_PATH
    assert recording.is_scene(not_a_scene_path) == False


def test_is_scene_true():
    """
    Makes sure that the `is_scene()` function recognizes proper
    scene paths.
    """
    a_scene_path = PROJECT_PATH / "scene_1"
    assert recording.is_scene(a_scene_path)


def test_list_scenes():
    """Testing that `list_scenes()` really lists every scene.

    This test assumes that the previous tests passed. If they
    didn't, this might fail even if `list_scenes()` is right.

    For example, if some directories are not created by the
    `create_dirs()` function, the amount of scenes in the file
    and the amount of scene directories won't match.

    """
    scene_amount = len(PARSED.keys())
    listed_scenes = recording.list_scenes(PROJECT_PATH)
    all_scenes = [PROJECT_PATH / f"scene_{i+1}" for i in range(scene_amount)]
    assert len(all_scenes) == len(listed_scenes) and sorted(all_scenes) == sorted(listed_scenes)


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
        assert len(recording.fetch_runner_instructions(test_case["file"])) == test_case["want"]


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
        assert len(recording.fetch_scene_runner_instructions(test_case["dir"])) == test_case["want"]


def test_fetch_project_runner_instructions():
    """
    Testing that fetch_project_runner_instructions finds the right
    amount of files.
    """
    want = 4
    assert len(recording.fetch_project_runner_instructions(VIDEO_TEST_DIR)) == want
