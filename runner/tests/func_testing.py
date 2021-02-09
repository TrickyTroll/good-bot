import unittest
import runner.funcmodule as funcmodule
import runner.tools as tools

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

        # TODO: Finish this test
        self.assertEqual(type(result),type({}))
        

if __name__ == '__main__':
    unittest.main()