import click

@click.group()
def cli():
    """Federal Data Processor CLI."""
    pass

@cli.command()
def ingest():
    """Run sample ingest on fixtures (stub)."""
    click.echo("Ingesting sample fixtures...")

@cli.command()
@click.argument("term")
def search(term: str):
    """Search EOs by term (stub)."""
    click.echo(f"Searching for: {term}")

if __name__ == "__main__":
    cli()
