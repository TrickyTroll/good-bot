import unittest
import tempfile
import shutil
import pathlib
import goodbot.funcmodule as funcmodule

Path = pathlib.Path

CONFIGPATH = Path("./tests/examples")


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
        self.assertRaises(TypeError, funcmodule.create_dirs_list, ["a wrong type"])

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
    temp = tempfile.mkdtemp()
    project_name = Path(temp) / Path("toto")
    parsed = funcmodule.config_parser(CONFIGPATH / "test_conf.yaml")
    conf_info = funcmodule.config_info(parsed)
    dirs_list = funcmodule.create_dirs_list(conf_info)
    def test_error_handling(self):
        """
        Testing that the function `create_dirs()` raises errors on
        other input types than `list`
        """
        # These should not create any dir and raise errors before
        # anything else.
        # This fist tests has a wrong directory list argument.
        self.assertRaises(TypeError, funcmodule.create_dirs, {"1": "This is a scene!"}, self.temp)
        # The second test has a wrong path to create the directories.
        self.assertRaises(TypeError, funcmodule.create_dirs, self.dirs_list, ["path", "as", "list"])

    def test_return_type(self):
        """Testing that the returned value is of type `pathlib.Path`"""
        returned_path = funcmodule.create_dirs(self.dirs_list)
        self.assertTrue(isinstance(returned_path, (Path, pathlib.PosixPath)))
