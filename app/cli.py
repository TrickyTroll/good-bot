import click

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

app.add_command(greet)

def main():
    app()