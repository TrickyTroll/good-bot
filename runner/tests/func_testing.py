import unittest
import runner.funcmodule as funcmodule

from pathlib import Path

TESTCONFS = Path("./examples")

class TestParsing(unittest.TestCase):

    def test_returns_dict(self):
        """Testing that the function returns a `dict`."""

        with open(TESTCONFS / "test_conf.yaml") as config:
            result = funcmodule.parse_config(config)

        self.assertEqual(type(result),type({}))
    
    def test_return_format(self):
        """Tests for the correct return format."""

        with open(TESTCONFS / "test_conf.yaml") as config:
            result = funcmodule.parse_config(config)

        for keys, values in result.values():
            self.assertEqual(type(result),type({}))
            self.assertEqual(type(values), type([]))
        

if __name__ == '__main__':
    unittest.main()