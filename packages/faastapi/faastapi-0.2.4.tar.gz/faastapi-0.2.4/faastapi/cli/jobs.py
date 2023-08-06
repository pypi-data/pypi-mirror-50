import click


@click.group()
def job():
    pass


@job.command()  # noqa: F811
@click.option(
    "--file", "-f", type=click.Path(exists=True), help="Job configuration to use"
)
def new(file):
    """
    Deploy a new job
    """
    raise NotImplementedError("Coming in next versions!")
