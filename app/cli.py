import click
import sys
from pathlib import Path

@click.group()

def app():
    """Automating video documentation."""
    pass

@click.command()

@click.option(
    "--environment",
    "-env",
    type = click.File(mode="r"),
    help = """\
        To provide environment variables to the program.
        """
)

@click.argument(
    "script",
    type = click.File('r'),
)

def run(setup):
    """To create a video from a YAML script."""
    pass

@app.add_command(run)

def main():
    app()