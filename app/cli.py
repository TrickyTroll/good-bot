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
    type = click.File(mode="r")
    help = """\
        To provide environment variables to the program.
        """
)

@click.argument(
    "script",
    type = click.File('r'),
)

def setup(script):
    """To create a new video based on your script."""

    
    return None

@click.command()

def run(setup):
    """To start the video using the setted up env"""
    pass

@app.add_command(run)
@app.add_command(setup)

if __name__ == "__main__":
    app()