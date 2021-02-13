import unittest
import runner.funcmodule as funcmodule

from pathlib import Path

CONFIGPATH = Path("./tests/examples")
class TestParsing(unittest.TestCase):

    def test_returns_dict(self):
        """Testing that the function returns a `dict`."""

        with open(CONFIGPATH / "test_conf.yaml", "r") as config:
            result = funcmodule.parse_config(config)

        self.assertEqual(type(result),type({}))
    
    def test_return_format(self):
        """Tests for the correct return format."""

        with open(CONFIGPATH / "test_conf.yaml", "r") as config:
            result = funcmodule.parse_config(config)

        for keys, values in result.items():
            self.assertEqual(type(result),type({}))
            self.assertEqual(type(values), type([]))
            self.assertEqual(type(keys), type(""))
        

if __name__ == '__main__':
    unittest.main()