# -*- coding: utf-8 -*-
"""`goodbot`'s command line interface"""

import pathlib
import click
from goodbot import funcmodule, render, audio, shell_commands, utils, recording


@click.group()
@click.option("--docker/--no-docker", default=True)
def app(docker):
    """Automating the recording of documentation videos."""
    # Allowing users to redefine this param. This is especially useful
    # if someone's dev environment is in a container (Gitpod for example).
    global PROJECT_ROOT
    if docker:
        PROJECT_ROOT = pathlib.Path("/project")
    else:
        if utils.in_docker():
            PROJECT_ROOT = pathlib.Path("/project")
        else:
            PROJECT_ROOT = pathlib.Path(".")


@app.command()
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


@app.command()
@click.argument("config", type=str)
@click.option("--project-path", "-p", type=str, default="")
def setup(config: str, project_path: str) -> None:
    """
    Sets up a directory that contains everything needed to record a
    video using `good-bot`.

    `setup` uses your configuration file to create a directory with
    recording instructions that `good-bot` understands.

    """

    if not project_path:
        prompt: str = """\
        Please provide a name for your project.
        """
        project_path = input(prompt)

    file_name = pathlib.Path(config)
    # Creating directories
    parsed = funcmodule.config_parser(PROJECT_ROOT / file_name)
    conf_info = funcmodule.config_info(parsed)
    to_create = funcmodule.create_dirs_list(conf_info)

    path = funcmodule.create_dirs(
        to_create, project_path, PROJECT_ROOT / pathlib.Path(project_path)
    )

    # Splitting script
    funcmodule.split_config(parsed, path)

    click.echo(f"Your project has been setup at: {project_path}")


@app.command()
@click.argument("projectpath", type=str)
@click.option("-d", "debug", default=False, show_default=True, type=bool)
@click.option("-l", "--language", type=str, default="en-US")
@click.option("-n", "--language-name", type=str, default="en-US-Standard-C")
def record(projectpath: str, language: str, language_name: str, debug: bool) -> None:
    """
    Record a video according to the instructions provided a directory.
    The directory should be created by the `setup` command.

    If you want to create audio content, make sure that your
    `GOOGLE_APPLICATION_CREDENTIALS` environment variable has been
    set to the path towards your API key.
    """
    dir_path = pathlib.Path(projectpath)

    click.echo(f"Using project : {projectpath}")
    all_scenes = utils.list_scenes(PROJECT_ROOT / dir_path)

    click.echo(f"The project '{dir_path}' contains:")

    for scene in all_scenes:
        click.echo(f"- {scene.name}")

    recording.record_project(PROJECT_ROOT / dir_path)


@app.command()
@click.option("-d", "debug", default=False, show_default=True, type=bool)
@click.argument("projectpath", type=str)
def render_video(projectpath: str, debug: bool) -> None:
    """
    Renders a project using pre-recorded gifs and mp3 files.

    Should be used by Good Bot's CLI since the gifs are rendered
    using an exernal program.
    """
    project_path = pathlib.Path(projectpath)

    render.render_all(PROJECT_ROOT / project_path)

    final_project = render.render_final(PROJECT_ROOT / project_path, debug)

    click.echo(
        f"Your video has been saved under {project_path / final_project.parent / final_project.name}."
    )


app.add_command(setup)
app.add_command(echo_config)
app.add_command(record)
app.add_command(render_video)


def main():
    app()
