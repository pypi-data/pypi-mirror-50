import click


@click.group(chain=True)
def cli():
    pass


@cli.command("sdist")
def sdist():
    click.echo("sdist called")


@cli.command("bdist_wheel")
def bdist_wheel():
    click.echo("bdist_wheel called")


if __name__ == "__main__":
    cli()
