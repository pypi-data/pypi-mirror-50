from ..exceptions import MissingDependencyError

try:
    import click
except ImportError:
    raise MissingDependencyError("click", "cli")
from .functions import function
from .jobs import job


@click.group()
def entry_point():
    pass


entry_point.add_command(function)
entry_point.add_command(job)
