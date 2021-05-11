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
