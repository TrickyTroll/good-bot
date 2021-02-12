import sys
import yaml
from io import TextIOWrapper

def parse_config(conf: TextIOWrapper) -> dict:
    """Parses a config file to generate a dict.

    Should only be used on the files that contain a command.
    Not to be used on the main conf file.

    Args:
        conf (TextIOWrapper): The opened text file

    Returns:
        dict: A dict that contains info on the command.
    """
    parsed = yaml.safe_load(conf)
    
    if type(parsed) != dict:
        print("Wrong type of config file")
        sys.exit()

    return parsed

# For debugging
if __name__ == "__main__":
    import os
    current_dir = os.getcwd()
    with open("./runner/tests/examples/test_conf.yaml", "r") as stream:
        parse_config(stream)
