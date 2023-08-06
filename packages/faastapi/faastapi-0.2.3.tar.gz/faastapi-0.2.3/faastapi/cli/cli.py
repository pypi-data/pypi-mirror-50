import subprocess
import os
from shlex import split

try:
    import click

    CLICK_INSTALLED = 1
except ImportError:
    CLICK_INSTALLED = 0
from ..logger import logger
from ..exceptions import MissingDependencyError
from .generator import FunctionTemplate, read_yaml


if CLICK_INSTALLED == 0:
    raise MissingDependencyError("click", "cli")


@click.group()
def entry_point():
    pass


@entry_point.command()
@click.option("--app", help="Application to serve", default="main:app")
@click.option("--host", help="Host to listen to", default="127.0.0.1")
@click.option("--port", help="Port to listen to", default=8000)
@click.option("--log-level", help="Log level", default="debug")
@click.option("--reload", help="Enable hot reload", default=True)
@click.option("--app-name", help="Name of application", default="app")
def serve(app, host, port, log_level, reload, app_name):
    """
    Serve a function for local development purpose
    """
    _env = os.environ.copy()
    if os.path.exists("env.yml"):
        env_variables = read_yaml("env.yml")
    try:
        _vars = env_variables["environment"]
    except KeyError:
        pass
    else:
        _env.update(_vars)
    _env["APP_ENABLE_OPENFAAS"] = "0"
    _cmd = f"uvicorn {app} --host={host} --port={port} --log-level={log_level} {'--reload' * int(reload)}"
    logger.info(f"Starting application with command: '{_cmd}'")
    ps = subprocess.run(split(_cmd), shell=False, env=_env)
    return ps


@entry_point.command()
@click.argument("path", default="openfaas")
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Configuration to use",
    default="faastapi.yml",
)
def new(path, file):
    """
    Create a new FastAPI application
    """
    template = FunctionTemplate.from_config(file)
    logger.debug(f"Rendering template with configuration:\n{template.dump_config()}")
    template.render(output=path)


# @entry_point.command()
# @click.option(
#     "--file",
#     "-f",
#     type=click.Path(exists=True),
#     help="Configuration to use",
#     default="faastapi.yml",
# )
# @click.option(
#     "--build/--no-build",
#     default=False
# )
# def push(file, build):
#     """
#     Build an OpenFaas function
#     """
#     if build:
