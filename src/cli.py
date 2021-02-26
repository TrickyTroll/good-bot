import pathlib
import click
import funcmodule


@click.group()
def app():
    """Automating the recording of documentation videos."""
    pass


@click.command()
def greet():
    """Greets the user.

    Returns:
        None: None
    """
    click.echo("Hello, world!")

    return None


@click.command()
@click.argument(
    "config",
    type=click.File("r")
)
def echo_config(config: click.File) -> None:
    """To echo the configuration file

    Args:
        config (click.File): The config file provided by the user.
    Returns:
        None: None
    """
    parsed = funcmodule.config_parser(config)
    click.echo(parsed)
    return None


@click.command()
@click.argument(
    "config",
    type=click.File("r")
)
@click.option(
    "--project-name",
    prompt='''\
    Please provide a name for your project.
    ''')
def setup(config: click.File, project_name: str) -> None:
    """Create a directory that contains everything required to make
    a documentation video!

    Args:
        config (click.File): The configuration file. This should be
        handled by click.
        project_name (str): The name of the project. Will be used
        to create the project's root directory.

    Returns:
        None: None
    """
    # Creating directories
    parsed = funcmodule.config_parser(config)
    conf_info = funcmodule.config_info(parsed)
    to_create = funcmodule.create_dirs_list(conf_info)

    path = funcmodule.create_dirs(to_create, project_name)

    # Splitting script
    funcmodule.split_config(parsed, path)

    click.echo(f"Your project has been setup at: {path}")

    return None


@click.command()
@click.argument(
    "projectpath",
    type = click.Path(exists=True),
    help='''\
    The path towards the project that you want to build. Your project
    directory shoud be created using the `setup` command.
    ''')
    
def build(projectpath: click.Path) -> None:
    """
    Makes a video from the instructions stored in a project 
    directory.
    """
    
    return None



app.add_command(setup)
app.add_command(greet)
app.add_command(echo_config)

if __name__ == "__main__":
    app()
