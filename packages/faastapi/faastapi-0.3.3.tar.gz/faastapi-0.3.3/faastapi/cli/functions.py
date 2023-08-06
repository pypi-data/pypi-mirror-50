import subprocess
import os
import sys
from shutil import move, rmtree
from shlex import split
import click
from ..logger import logger
from .generator import FunctionTemplate, read_yaml


@click.group()
def function():
    pass


@function.command()
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
    subprocess.run(split(_cmd), shell=False, env=_env)


@function.command()
@click.argument("directory", default="openfaas")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True),
    help="Function configuration to use",
    default="faastapi.yml",
)
@click.option("--force", is_flag=True, default=False)
def new(directory, file, force):
    """
    Create a new FastAPI application
    """
    _old = None
    if os.path.exists(directory):
        if not force:
            logger.error(
                f"A directory named {directory} already exists. "
                "Use --force option to override it."
            )
            sys.exit(1)
        else:
            _old = f"{directory}.bak"
            move(directory, _old)
    template = FunctionTemplate.from_config(file)
    logger.debug(f"Rendering template with configuration:\n{template.dump_config()}")
    try:
        template.render(output=directory)
    except Exception as _err:
        if _old:
            move(_old, directory)
            raise _err
    else:
        if _old:
            rmtree(_old)


@function.command()
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Function configuration to use",
    default="faastapi.yml",
)
@click.option("--build", is_flag=True, default=False)
def deploy(file, build):
    """
    Deploy an OpenFaas function
    """
    raise NotImplementedError("Coming in next versions!")
