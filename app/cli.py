import click
import sys
from pathlib import Path

@click.group()

def app():
    """Automating video documentation."""
    pass

@click.command()

@click.argument(
    "script",
    type = click.File('r'),
)

def make_vid(script):
    """To create a new video based on your script."""
    return None
