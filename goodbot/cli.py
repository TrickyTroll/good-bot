# -*- coding: utf-8 -*-
"""`goodbot`'s command line interface"""

import pathlib
import click
import os
from goodbot import funcmodule


def in_docker() -> bool:
    """Checks if code is currently running in a Docker container.

    Checks if Docker is in control groups or if there is a `.dockerenv`
    file at the filesystem's root directory.

    Returns:
        bool: Whether or not the code is running in a Docker container.
    """
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


if in_docker():
    PROJECT_ROOT = pathlib.Path("/project")
else:
    PROJECT_ROOT = pathlib.Path(".")


@click.group()
def app():
    """Automating the recording of documentation videos."""


@click.command()
@click.argument("config", type=str)
def echo_config(config: str) -> None:
    """Prints a configuration file as seen by `good-bot`.

    This is useful if you want to see how your file has been
    interpreted by the program. Sometimes, common words will
    be interpreted as keywords. This can create very different
    results than what you expected from your script.

    """
    file_name = pathlib.Path(config)
    parsed = funcmodule.config_parser(PROJECT_ROOT / file_name)
    click.echo(parsed)


@click.command()
@click.argument("config", type=str)
@click.option(
    "--project-name",
    prompt="""\
    Please provide a name for your project.
    """,
)
def setup(config: str, project_name: str) -> None:
    """
    Sets up a directory that contains everything needed to record a
    video using `good-bot`.

    `setup` uses your configuration file to create a directory with
    recording instructions that `good-bot` understands.

    """

    file_name = pathlib.Path(config)
    project_name = pathlib.Path(project_name)
    # Creating directories
    parsed = funcmodule.config_parser(PROJECT_ROOT / file_name)
    conf_info = funcmodule.config_info(parsed)
    to_create = funcmodule.create_dirs_list(conf_info)

    path = funcmodule.create_dirs(to_create, PROJECT_ROOT / project_name)

    # Splitting script
    funcmodule.split_config(parsed, path)

    click.echo(f"Your project has been setup at: {path}")


@click.command()
@click.argument("projectpath", type=str)
def record(projectpath: str) -> None:
    """
    Record a video according to the instructions provided a directory. 
    The directory should be created by the `setup` command.

    If you want to create audio content, make sure that your
    `GOOGLE_APPLICATION_CREDENTIALS` environment variable has been
    set to the path towards your API key.
    """
    dir_path = pathlib.Path(projectpath)

    click.echo(f"Using project : {projectpath}")
    all_scenes = funcmodule.list_scenes(PROJECT_ROOT / dir_path)

    click.echo(f"The project '{dir_path}' contains:")

    for scene in all_scenes:
        click.echo(f"- {scene.name}")

    for scene in all_scenes:
        click.echo(f"Working on {scene}...")

        funcmodule.record_commands(scene, scene / pathlib.Path("asciicasts"))
        funcmodule.record_audio(scene, scene / pathlib.Path("audio"))


app.add_command(setup)
app.add_command(greet)
app.add_command(echo_config)
app.add_command(record)


def main():
    app()
