import yaml
import click
from pathlib import Path

########################################################################
#                               YAML parsing                           #
########################################################################

def config_parser(file: click.File) -> dict:
    """Can be used to parse a configuration file.

    Args:
        file (click.File): The configuration file. This should be
        handled by click.

    Returns:
        dict: A dict with the parsed information.
    """
    parsed = yaml.safe_load(file)
    return parsed_file