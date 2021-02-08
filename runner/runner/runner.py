import sys
import click
from runner import classmodule
from runner import funcmodule

@click.command()

@click.argument(
    'input',
    type = click.File('r')
)

def gb_run(input: click.File) -> None:
    """Runs a command using the Commands class.
    It runs the command according to the configuration file that is
    passed as the 'input' argument
    """
    parsed = funcmodule.parse_config(input)

    try:
        commands = parsed["commands"]
        expect = parsed["expect"]

    except KeyError:
        print("Missing element in the dictionary.")
        sys.exit()

    command = classmodule.Commands(commands, expect)

    command.run()

    return None

def main():
# if __name__ == "__main__":
    gb_run()
