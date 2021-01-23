import click
import funcmodule
import classmodule

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
    type = click.File("r")
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

app.add_command(greet)
app

def main():
    app()