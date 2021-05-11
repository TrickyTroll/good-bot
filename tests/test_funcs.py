import unittest
import goodbot.funcmodule as funcmodule

from pathlib import Path

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
