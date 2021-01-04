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
    click.echo("Hello,world")
    return None

app.add_command(run)

if __name__ == "__main__":
    # execute only if run as a script
    app()