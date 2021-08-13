# -*- coding: utf-8 -*-
"""Testing functions from the `render` module."""
import pathlib
import tempfile
import subprocess
import pytest
import os
import shutil
from distutils.dir_util import copy_tree
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
                SAMPLE_PROJECT / "scene_1/audio/read_1.mp3",
            ),
        },
        {
            "gif": SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
            "want": (
                SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
                SAMPLE_PROJECT / "scene_1/audio/read_2.mp3",
            ),
        },
        {
            "gif": SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif",
            "want": (SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif", None),
        },
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
                    SAMPLE_PROJECT / "scene_1/audio/read_1.mp3",
                ),
                (
                    SAMPLE_PROJECT / "scene_1/gifs/commands_2.gif",
                    SAMPLE_PROJECT / "scene_1/audio/read_2.mp3",
                ),
            ],
        },
        {
            "scene": SAMPLE_PROJECT / "scene_3",
            "want": [(SAMPLE_PROJECT / "scene_3/gifs/commands_1.gif", None)],
        },
    ]

    for test in test_cases:
        for item in render.link_audio(test["scene"]):
            assert item in test["want"]


def test_remove_first_frame():
    """
    Testing that remove_first_frame really removes a frame from the GIF
    file. This test only makes sure that a frame is removed, not that it
    is the first one.

    This test uses gifsicle's -I option, which gives information on a
    GIF file. The first line of the output looks something like this:

    * tests/examples/render-sample/test-rm-frame/commands_1.gif 20 images

    By splitting this line on " " characters and getting the number
    next-to-last in the list.
    """

    def get_frames_amount(gif_path):
        gifsicle_output = subprocess.run(
            ["gifsicle", "-I", str(gif_path)], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        first_line = gifsicle_output.split("\n")[0]
        return first_line.split(" ")[-2]

    gif_sample_path = SAMPLE_PROJECT / "test-rm-frame/commands_1.gif"
    want = int(get_frames_amount(gif_sample_path)) - 1
    shorter_gif = render.remove_first_frame(gif_sample_path)
    got = int(get_frames_amount(shorter_gif))
    os.remove(shorter_gif)
    assert want == got


def test_render_function():
    """
    Testing that the function render properly creates a new video.
    """
    with tempfile.TemporaryDirectory() as temp:
        copy_tree(SAMPLE_PROJECT, temp)
        gif_and_audio = render.corresponding_audio(Path(temp) / "scene_1/gifs/commands_1.gif")
        video = render.render(gif_and_audio)
        created = video.exists()
        os.remove(video)
        assert created


def test_render_all():
    """
    Testing that render_all creates every video required.
    """
    with tempfile.TemporaryDirectory() as temp:
        copy_tree(SAMPLE_PROJECT, temp)
        to_record = []
        for directory in Path(temp).iterdir():
            if "scene_" in directory.name:
                to_record.append(render.link_audio(directory))
        recorded = render.render_all(Path(temp))
        want = 0
        for content in to_record:
            want += len(content)
        assert want == len(recorded)
        for recording in recorded:
            assert recording.exists()


def test_sort_videos():
    """
    This test could be improved.

    Making sure that sort videos properly sorts videos from the
    project. Simply checking the list again to make sure that
    everything is in order.
    """

    def get_scene_id(video):
        return int(video.parent.parent.name.split("_")[1].split(".")[0])

    def get_video_id(video):
        return int(video.name.split("_")[1].split(".")[0])

    with tempfile.TemporaryDirectory() as temp:
        copy_tree(SAMPLE_PROJECT, temp)
        temp = Path(temp)
        recorded = render.render_all(temp)

        sorted_vids = render.sort_videos(temp)
        assert len(sorted_vids) > 0
        scene_counter = 1
        vid_counter = 1
        for index, video in enumerate(sorted_vids):
            assert get_scene_id(video) == scene_counter
            assert get_video_id(video) == vid_counter
            if index < len(sorted_vids) - 1:
                if get_scene_id(sorted_vids[index + 1]) > scene_counter:
                    vid_counter = 1
                    scene_counter += 1
                else:
                    vid_counter += 1
        for path in recorded:
            assert path in sorted_vids


def test_write_ffmpeg_instructions():
    """
    Making sure that write_ffmpeg_instructions writes every item in
    the list created by sort_videos and that the paths in the file
    do exist.
    """

    def trim_path(path):
        # The line in the file that contains the path has a format
        # similar to this:
        # file '[PATH]'\n
        # To extract the path, we can split on " " to get only the
        # "'[PATH]'\n" part and then remove the "'" and "\n" chars.
        return path.split(" ")[1].rstrip()[1:-1]

    with tempfile.TemporaryDirectory() as temp:
        copy_tree(SAMPLE_PROJECT, temp)
        recorded = render.render_all(Path(temp))
        sorted_vids = render.sort_videos(Path(temp))
        instructions = render.write_ffmpeg_instructions(Path(temp))
        with open(instructions, "r") as stream:
            paths = stream.readlines()
        for index, path in enumerate(paths):
            path = trim_path(path)
            assert sorted_vids[index] == Path(temp) / Path(path)
            assert Path(path).exists()


def test_render_final():
    """
    This test could be improved.

    Testing that render_final really produces a final video at the
    right location.
    """
    with tempfile.TemporaryDirectory() as temp:
        copy_tree(SAMPLE_PROJECT, temp)
        render.render_all(Path(temp))
        render.render_final(Path(temp))
        assert (Path(temp) / "final/final.mp4").exists()
