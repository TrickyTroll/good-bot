from io import TextIOWrapper
import yaml

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

    return parsed