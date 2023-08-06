import subprocess
import os
from shlex import split
import click
from ..logger import logger
from ..generator import FunctionTemplate


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
    _env["APP_ENABLE_OPENFAAS"] = "0"
    _cmd = f"uvicorn {app} --host={host} --port={port} --log-level={log_level} {'--reload' * int(reload)}"
    logger.info(f"Starting application with command: '{_cmd}'")
    ps = subprocess.run(split(_cmd), shell=False, env=_env)
    return ps


@entry_point.command()
@click.argument("path")
@click.option("--template", help="Template to use", default="main.py.j2")
def new(path, template):
    """
    Create a new FastAPI application
    """
    template = FunctionTemplate()
    template.render(output=path)


def build_openfaas():
    """
    Build an OpenFaas function
    """
    pass


def deploy():
    """
    Deploy an OpenFaas function
    """
    pass
