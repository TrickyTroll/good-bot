import os
import unittest
import tempfile
import pytest
import shutil
import pathlib
import yaml
import goodbot.funcmodule as funcmodule

from hypothesis import given, strategies as st

Path = pathlib.Path
read = os.read

CONFIGPATH = Path("./tests/examples")

# Creating a project
TEMP_DIR = tempfile.mkdtemp()
PROJECT_PATH = Path(TEMP_DIR) / Path("toto")
PARSED = funcmodule.config_parser(CONFIGPATH / "test_conf.yaml")
CONF_INFO = funcmodule.config_info(PARSED)
DIRS_LIST = funcmodule.create_dirs_list(CONF_INFO)
funcmodule.create_dirs(DIRS_LIST, PROJECT_PATH)
funcmodule.split_config(PARSED, PROJECT_PATH)

# Read strings samples for hypothesis
read_strings = [
    "Hello, world!",
    """\
<speak>
  <emphasis level="strong">To be</emphasis>
  <break time="200ms"/> or not to be, <break time="400ms"/>
  <emphasis level="moderate">that</emphasis>
  is the question.<break time="400ms"/>
  Whether ‘tis nobler in the mind to suffer
  The slings and arrows of outrageous fortune,<break time="200ms"/>
  Or to take arms against a sea of troubles
  And by opposing end them.
</speak>""",
    "Je vais vous présenter mon super héros préféré.",
]

# Adding examples to the `sample_configs` list.
sample_configs = []

for file in Path("./examples").iterdir():
    if file.is_dir():
        pass
    with open(file, "r") as stream:
        config = stream.read()
    sample_configs.append(yaml.safe_load(config))

class TestParser(unittest.TestCase):
    """Testing `good-bot`'s config parser.

    From the function `config_parser()`:
    ------------------------------------

    Testing:
        * `config_parser()` returns a `dict`.
        * The returned structure contains ints as keys.
        * The returned structure's values are of type `dict`.
        * The values of the previous strucutre are of type `list`.

    """

    PARSED = funcmodule.config_parser(CONFIGPATH / "test_conf.yaml")

    def test_returns_dict(self):
        """
        Testing if the function `config_parser()` returns a `dict`.
        """
        self.assertEqual(type(self.PARSED), dict)

    def test_keys_int(self):
        """
        Making sure that every key in the parsed config is of type
        `int`.
        """
        for key in self.PARSED.keys():
            self.assertEqual(type(key), int)

    def test_values_dict(self):
        """
        Making sure that every item in the parsed config is of type
        `list`.
        """
        for item in self.PARSED.values():
            self.assertEqual(type(item), list)

    def test_values_of_values_list(self):
        """
        Testing type of the items contained in the items of the
        parsed configuration. They should be of type `dict`.
        """
        for item in self.PARSED.values():
            for thing in item:
                self.assertEqual(type(thing), dict)


class TestInfo(unittest.TestCase):
    """Tests for the `config_info` function.

    From the function `config_info()`:
    ----------------------------------

    Testing:
        * Returns a `dict`.
        * Keys in the `dict` are of type `int`.
        * Values in the returned `dict` are of type `dict`.

    From values in the `dict` returned by `config_info()`:
    ======================================================

    Testing:
        * Keys are of type `str`.
        * Keys are contained in ["commands", "expect", "scenes", "editor", "slides", "read"].
        * Values are of type `list`.

    """

    parsed = funcmodule.config_parser(CONFIGPATH / "test_conf.yaml")

    RETURNED = funcmodule.config_info(parsed)
    VALUES = RETURNED.values()

    def test_returns_dict(self):
        """Testing that `config_parser()` returns a `dict`."""
        self.assertEqual(type(self.RETURNED), dict)

    def test_dict_keys(self):
        """Testing the type of the dictionnary keys.

        They should be of type `int`.

        """
        for key in self.RETURNED.keys():
            self.assertEqual(type(key), int)

    def test_dict_values(self):
        """Testing the type of the dictionnary values.

        They should be of type `dict`.

        """
        for value in self.RETURNED.values():
            self.assertEqual(type(value), dict)

    def test_value_keys(self):
        """
        From the values in the dictionnary returned by `config_info`.
        These values should be of type `dict`, as tested previously.

        * Testing that the keys of those `dict` are of type `str`.
        * Testing that the keys are contained in the following list:

        ```python
        ["commands", "expect", "scenes", "editor", "slides", "read"]
        ```
        """
        all_keys = ["commands", "expect", "scenes", "editor", "slides", "read"]

        for item in self.VALUES:
            for key in item.keys():
                self.assertEqual(type(key), str)
                self.assertTrue(key in all_keys)

    def test_value_values(self):
        """
        From the values in the dictionnary returned by `config_info`.
        These values should be of type `dict`, as tested previously.

        Testing that the values of those `dict` are of type `list`.
        """

        for item in self.VALUES:
            for value in item.values():
                self.assertEqual(type(value), list)


class TestDirsList(unittest.TestCase):
    """Testing the `create_dirs_list()` function.

    Testing:
        * Error handling on other input types.
        * Returned value is a `list`.
        * Items in the list are of type `dict`.
    """

    parsed = funcmodule.config_parser(CONFIGPATH / "test_conf.yaml")
    RETURNED = funcmodule.config_info(parsed)
    DIRS_LIST = funcmodule.create_dirs_list(RETURNED)

    def test_error_handling(self):
        """Testing error handling on bad input types."""
        self.assertRaises(TypeError, funcmodule.create_dirs_list, "Hi!")
        self.assertRaises(
            TypeError, funcmodule.create_dirs_list, ["a wrong type"]
        )

    def test_returns_dict(self):
        """Making sure that `create_dirs_list()` returns a list."""
        self.assertEqual(type(self.DIRS_LIST), list)

    def test_contains_strings(self):
        for item in self.DIRS_LIST:
            self.assertEqual(type(item), dict)


class TestCreateDirs(unittest.TestCase):
    """Testing the `create_dirs()` function.

    Testing:
        * Error handling on other input types.
        * Returns a value of type `pathlib.Path`.
    """

    def test_error_handling(self):
        """
        Testing that the function `create_dirs()` raises errors on
        other input types than `list`
        """
        # These should not create any dir and raise errors before
        # anything else.
        # This fist tests has a wrong directory list argument.
        self.assertRaises(
            TypeError,
            funcmodule.create_dirs,
            {"1": "This is a scene!"},
            TEMP_DIR,
        )
        # The second test has a wrong path to create the directories.
        self.assertRaises(
            TypeError, funcmodule.create_dirs, DIRS_LIST, ["path", "as", "list"]
        )

    def test_return_type(self):
        """Testing that the returned value is of type `pathlib.Path`"""
        with tempfile.TemporaryDirectory() as temp:
            returned_path = funcmodule.create_dirs(
                DIRS_LIST, temp + "/my_project"
            )
            # This next assert would probably fail on Windows.
            self.assertTrue(
                isinstance(returned_path, (Path, pathlib.PosixPath))
            )


# Using pytest from now on.
def test_split_config_commands():
    """Tests that the `split_config()` functions writes every command.

    This test counts the amount of files that `split_config()` should
    create. This number can be obtained from the parsed configuration
    file.

    This number is then compared to the real amount of files created
    for commands.

    This test will only pass if they are equal.

    """

    scene_amount = len(PARSED)
    commands_expected = 0
    commands_amount = 0

    for i in range(scene_amount):

        for item in PARSED[i + 1]:
            if "commands" in item.keys():
                commands_expected += 1

        try:
            commands_amount += len(
                list((PROJECT_PATH / Path(f"scene_{i + 1}/commands")).iterdir())
            )
        except FileNotFoundError:
            continue

    assert commands_amount == commands_expected


def test_split_config_read():
    """Tests that the `split_config` command creates every read files.

    This is very similar to the `test_split_config_commands()` test,
    but for read files that will be sent to the text-to-speech program.
    """

    scene_amount = len(PARSED)
    read_expected = 0
    read_amount = 0

    for i in range(scene_amount):

        for item in PARSED[i + 1]:
            if "read" in item.keys():
                read_expected += 1

        try:
            read_amount += len(
                list((PROJECT_PATH / Path(f"scene_{i + 1}/read")).iterdir())
            )
        except FileNotFoundError:
            continue

    assert read_amount == read_expected


def test_is_scene_false():
    """
    Makes sure that the `is_scene()` function does not recognize
    a project path as a scene path.
    """
    not_a_scene_path = PROJECT_PATH
    assert funcmodule.is_scene(not_a_scene_path) == False


def test_is_scene_true():
    """
    Makes sure that the `is_scene()` function recognizes proper
    scene paths.
    """
    a_scene_path = PROJECT_PATH / "scene_1"
    assert funcmodule.is_scene(a_scene_path)


def test_list_scenes():
    """Testing that `list_scenes()` really lists every scene.

    This test assumes that the previous tests passed. If they
    didn't, this might fail even if `list_scenes()` is right.

    For example, if some directories are not created by the
    `create_dirs()` function, the amount of scenes in the file
    and the amount of scene directories won't match.

    """
    scene_amount = len(PARSED.keys())
    listed_scenes = funcmodule.list_scenes(PROJECT_PATH)
    all_scenes = [PROJECT_PATH / f"scene_{i+1}" for i in range(scene_amount)]
    assert len(all_scenes) == len(listed_scenes) and sorted(
        all_scenes
    ) == sorted(listed_scenes)


@given(to_read=st.sampled_from(read_strings), file_index=st.integers())
def test_write_read_instructions_rtype(to_read, file_index):
    """Making sure that the return value is ok.

    To be ok, return value must either be of type `str` or `Path`.
    This ensures that the returned value can then be used to open
    the file later on.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/read")
        new_file = funcmodule.write_read_instructions(
            to_read, temp_dir, file_index
        )
    assert isinstance(new_file, (Path, str))


@given(to_read=st.sampled_from(read_strings), file_index=st.integers())
def test_write_read_instructions_path(to_read, file_index):
    """Testing that the returned path is the right one.

    Only testing that the path exists for now.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/read")
        new_file = funcmodule.write_read_instructions(
            to_read, temp_dir, file_index
        )
        assert os.path.exists(new_file)


@given(to_read=st.sampled_from(read_strings), file_index=st.integers())
def test_write_read_instructions_file_name(to_read, file_index):
    """
    Testing that the name of the file created by
    `write_read_instructions()` is correct.

    The file must be named `read_[id]`, where `id` must be
    equal to the index passed to the function + 1.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/read")
        new_file = funcmodule.write_read_instructions(
            to_read, temp_dir, file_index
        )
    assert str(file_index + 1) in new_file.name


@given(to_read=st.sampled_from(read_strings), file_index=st.integers())
def test_read_getting_same_result(to_read, file_index):
    """
    Testing that opening and reading the final file
    gives the same result as the original string.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/read")
        new_file = funcmodule.write_read_instructions(
            to_read, temp_dir, file_index
        )
        with open(new_file) as stream:
            read_file = stream.read()
        assert read_file == to_read


@given(st.sampled_from(sample_configs), st.integers())
def test_write_commands(commands, file_index):
    """Making sure that the return value is ok.

    To be ok, return value must either be of type `str` or `Path`.
    This ensures that the returned value can then be used to open
    the file later on.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/commands")
        new_file = funcmodule.write_commands_instructions(
            commands, temp_dir, file_index
        )
    assert isinstance(new_file, (Path, str))


@given(st.sampled_from(sample_configs), st.integers())
def test_write_commands_instructions_path(commands, file_index):
    """Testing that the returned path is the right one.

    Only testing that the path exists for now.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/commands")
        new_file = funcmodule.write_commands_instructions(
            commands, temp_dir, file_index
        )
        assert os.path.exists(new_file)


@given(st.sampled_from(sample_configs), st.integers())
def test_write_commands_instructions_file_name(commands, file_index):
    """
    Testing that the name of the file created by
    `write_commands_instructions()` is correct.

    The file must be named `read_[id]`, where `id` must be
    equal to the index passed to the function + 1.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/commands")
        new_file = funcmodule.write_commands_instructions(
            commands, temp_dir, file_index
        )
    assert str(file_index + 1) in new_file.name


@given(st.sampled_from(sample_configs), st.integers())
def test_getting_same_result(commands, file_index):
    """
    Testing that opening and reading the final file
    gives the same result as the original string.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(temp_dir + "/commands")
        new_file = funcmodule.write_commands_instructions(
            commands, temp_dir, file_index
        )
        with open(new_file) as stream:
            read_file = stream.read()
        assert yaml.safe_load(read_file) == commands
