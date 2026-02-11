import click


@click.group()
@click.version_option()
def main():
    """Parma Health Toolkit CLI"""
    pass


@main.command()
def hello():
    """Test command"""
    click.echo("Hello from Parma Health Toolkit!")


if __name__ == "__main__":
    main()
