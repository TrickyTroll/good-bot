import yaml
import click
import classmodule
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
    parsed_file = yaml.safe_load(file)
    return parsed_file

def create_classes(file: click.File) -> list:

    parsed_file = config_parser(file)
    all_classes = []

    for todos in parsed_file:

        if "commands" in todos:
            all_classes.append(classmodule.Commands(
                commands = todos["commands"],
                expect = todos["expect"]))
    
    return all_classes

########################################################################
#                             shell commands                           #
########################################################################

def is_shell_command(command: dict) -> bool:
    """Checks if the command is a shell command.

    Args:
        command (dict): The command dict

    Returns:
        bool: Wether the command is a shell command or not.
    """
    toggle = False
    for key, value in command.values():
        if key == "command":
            toggle = True
    return toggle