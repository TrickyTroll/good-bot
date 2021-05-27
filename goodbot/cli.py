import pathlib
import click
import funcmodule

# Should be /project if in container.
PROJECT_ROOT = pathlib.Path("/project")


@click.group()
def app():
    """Automating the recording of documentation videos."""


@click.command()
def greet():
    """Greets the user.

    Returns:
        None: None
    """
    click.echo("Hello, world!")


@click.command()
@click.argument("config", type=str)
def echo_config(config: str) -> None:
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
    Records everything that is required for the documentation.
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

if __name__ == "__main__":
    app()
