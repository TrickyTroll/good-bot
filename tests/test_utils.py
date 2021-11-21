from distutils.dir_util import copy_tree
from pathlib import Path
from goodbot import utils
from tests.test_funcs import PROJECT_PATH, PARSED

VIDEO_TEST_DIR = Path("./tests/examples/video")


def test_is_scene_false():
    """
    Makes sure that the `is_scene()` function does not recognize
    a project path as a scene path.
    """
    not_a_scene_path = PROJECT_PATH
    assert utils.is_scene(not_a_scene_path) == False


def test_is_scene_true():
    """
    Makes sure that the `is_scene()` function recognizes proper
    scene paths.
    """
    a_scene_path = PROJECT_PATH / "scene_1"
    assert utils.is_scene(a_scene_path)


def test_list_scenes():
    """Testing that `list_scenes()` really lists every scene.

    This test assumes that the previous tests passed. If they
    didn't, this might fail even if `list_scenes()` is right.

    For example, if some directories are not created by the
    `create_dirs()` function, the amount of scenes in the file
    and the amount of scene directories won't match.

    """
    scene_amount = len(PARSED.keys())
    listed_scenes = utils.list_scenes(PROJECT_PATH)
    all_scenes = [PROJECT_PATH / f"scene_{i+1}" for i in range(scene_amount)]
    assert len(all_scenes) == len(listed_scenes) and sorted(all_scenes) == sorted(listed_scenes)

def test_sort_scenes():
    """Making sure that `sort_scnees()` sorts the scenes properly.
    """
    test_cases = (
        [Path("scene_1"), Path("scene_2"), Path("scene_3")],
        [Path("scene_3"), Path("scene_2"), Path("scene_1")],
        [Path("scene_2")],
        []
    )

    want = (
        [Path("scene_1"), Path("scene_2"), Path("scene_3")],
        [Path("scene_1"), Path("scene_2"), Path("scene_3")],
        [Path("scene_2")],
        []
    )

    for index, test in enumerate(test_cases):
        assert utils.sort_scenes(test) == want[index]
