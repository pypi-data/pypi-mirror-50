import os
from shutil import copy2
from typing import Optional, Dict
import textwrap

try:
    from jinja2 import Environment, PackageLoader, Template

    JINJA2_INSTALLED = 1
except ImportError:
    JINJA2_INSTALLED = 0
try:
    import yaml

    PYYAML_INSTALLED = 1
except ImportError:
    PYYAML_INSTALLED = 0
from ..logger import logger
from ..temp import TempDirectory
from ..exceptions import MissingDependencyError
from .template_model import TemplateConfig
from .plugins import get_plugins_env_and_extras


if PYYAML_INSTALLED == 0:
    raise MissingDependencyError("pyyaml", "cli")
if JINJA2_INSTALLED == 0:
    raise MissingDependencyError("jinja2", "cli")


env = Environment(loader=PackageLoader("faastapi", "templates"))


def is_url_resource(field):
    return field.startswith("http://") or field.startswith("https://")


env.tests["url_resource"] = is_url_resource


def read_yaml(path: str) -> dict:
    with open(path, "r") as _file:
        _dict = yaml.load(_file, yaml.SafeLoader)
    return _dict


class FunctionTemplate:
    """ A class representing a Jinja2 template that can be used to render Dockerfiles """

    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]
    TEMPLATES_DIR = "templates"
    DOCKER_TEMPLATE = "Dockerfile.j2"
    FUNCTION_TEMPLATE = "handler.py.j2"
    FUNCTION_FILE_TEMPLATE = "function.yml.j2"
    SERVER_TEMPLATE = "main.py.j2"
    MODELS_TEMPLATE = "models.py.j2"
    ENV_TEMPLATE = ".env.yml.j2"

    def __init__(self, configuration: dict):

        """
        Init a FunctionTemplate based on a string template
        """
        self.temp_dir = TempDirectory()
        self.temp_dir.mkdir("function")
        self.configuration = self.extract_configuration(configuration)
        self.set_plugins_env_and_extras()
        self.set_function_name_env_variable()
        self.vars = self.configuration.dict()
        self.vars["environment_as_string"] = self.dump_environment()
        self.dockerfile_template = self.DOCKER_TEMPLATE
        self.server_template = self.SERVER_TEMPLATE
        self.handler_template = self.FUNCTION_TEMPLATE
        self.functionfile_template = self.FUNCTION_FILE_TEMPLATE
        self.models_template = self.MODELS_TEMPLATE
        self.env_template = self.ENV_TEMPLATE
        self.__jinja_env__ = Environment(
            loader=PackageLoader("faastapi", self.TEMPLATES_DIR),
            trim_blocks=False,
            lstrip_blocks=False,
        )

    @classmethod
    def from_config(cls, config_path):
        """
        Return an instance of FunctionTemplate based on a configuration file path
        """
        configuration = read_yaml(config_path)
        return cls(configuration=configuration)

    def extract_configuration(self, config: dict) -> dict:
        """
        Extract relevant configuration information from given dictionary
        """
        return TemplateConfig(**config)

    def validate_method(self) -> None:
        if self.configuration.run.method.upper() not in self.ALLOWED_METHODS:
            raise ValueError(f"Allowed methods are: {self.ALLOWED_METHODS}")

    def __load_template__(self, template) -> Template:
        """
        Load a template into jinja engine and return the loaded template
        """
        return self.__jinja_env__.get_template(template)

    def __render_template__(
        self, template: str, vars: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Render a template as a string
        """
        loaded_template = self.__load_template__(template)
        if vars:
            rendered_text = loaded_template.render(**vars)
        else:
            rendered_text = loaded_template.render()
        return rendered_text

    def __write_temp_template__(
        self, output: str, template: str, vars: Optional[Dict[str, str]] = None
    ):
        rendered_template = self.__render_template__(template=template, vars=vars)
        return self.temp_dir.write(rendered_template, output)

    def __write_template__(
        self, output: str, template: str, vars: Optional[Dict[str, str]] = None
    ):
        rendered_template = self.__render_template__(template=template, vars=vars)
        with open(output, "w+") as _file:
            _file.write(rendered_template)
        return output

    def __write__(
        self,
        template: str,
        file_name: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> str:
        if file_name is None and file_path is None:
            raise ValueError(
                "You must either given a file name in file_name option or a complete file path"
                "in file_path options"
            )
        if file_path:
            output = self.__write_template__(
                output=file_path, template=template, vars=self.vars
            )
        else:
            output = self.__write_temp_template__(
                output=file_name, template=template, vars=self.vars
            )
        return output

    def render_dockerfile(self):
        return self.__render_template__(
            template=self.dockerfile_template, vars=self.vars
        )

    def write_dockerfile(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.dockerfile_template,
            file_path=file_path,
            file_name="Dockerfile",
        )
        return output

    def render_functionfile(self):
        return self.__render_template__(
            template=self.functionfile_template, vars=self.vars
        )

    def write_functionfile(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.functionfile_template,
            file_path=file_path,
            file_name="function.yml",
        )
        return output

    def render_server(self):
        """
        Render the server template. Returns rendered template as string.
        """
        return self.__render_template__(template=self.server_template, vars=self.vars)

    def write_server(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.server_template, file_path=file_path, file_name="main.py"
        )
        return output

    def render_models(self) -> str:
        """
        Render the model template. Returns rendered template as string.
        """
        return self.__render_template__(template=self.models_template, vars=self.vars)

    def write_models(self, file_path: Optional[str] = None) -> str:
        """
        Write handler.py to file.
        """
        output = self.__write__(
            template=self.models_template,
            file_path=file_path,
            file_name="function/models.py",
        )
        return output

    def write_env_file(self, file_path: Optional[str] = None) -> str:
        """
        Write environment variables to file
        """
        output = self.__write__(
            template=self.env_template, file_path=file_path, file_name="env.yml"
        )
        return output

    def write_requirements(
        self,
        requirements_file: Optional[str] = "requirements.txt",
        file_path: Optional[str] = None,
    ) -> str:
        if file_path is None:
            file_path = os.path.join(self.temp_dir.path, "requirements.txt")
        output = copy2(requirements_file, file_path)
        return output

    def generate_function(self):
        dockerfile_path = self.write_dockerfile()
        logger.debug(f"Successfully written Dockerfile at {dockerfile_path}")

        server_path = self.write_server()
        logger.debug(f"Successfully written server at {server_path}")

        funcfile_path = self.write_functionfile()
        logger.debug(f"Successfully written function.yml at {funcfile_path}")

        if isinstance(self.configuration.run.output, dict) or isinstance(
            self.configuration.run.input, dict
        ):
            models_path = self.write_models()
            logger.debug(f"Successfully written models at {models_path}")

        handler_path = self.temp_dir.copy_file(
            src=self.configuration.run.script, dest="handler.py", directory="function"
        )
        logger.debug(f"Successfully written handler at {handler_path}")

        if self.configuration.build.requirements:
            self.write_requirements(
                requirements_file=self.configuration.build.requirements
            )

        self.write_env_file()

        if self.configuration.build.copy_files is not None:
            for _copy in self.configuration.build.copy_files:
                if not is_url_resource(_copy.src):
                    self.temp_dir.copy_file(_copy.src, directory="./")

    def set_plugins_env_and_extras(self):
        extras, env = get_plugins_env_and_extras(self.configuration.build.plugins)
        self.configuration.build.extras = extras
        self.configuration.run.environment.update(env)

    def set_function_name_env_variable(self):
        self.configuration.run.environment[
            "app_openfaas_function"
        ] = self.configuration.meta.name

    def render(self, output):
        self.generate_function()
        logger.debug(f"Copying content of directory {self.temp_dir.path} into {output}")
        self.temp_dir.copy(output)
        logger.info(f"Succcessfully generated function in directory {output}")
        self.temp_dir.close()

    def dump_config(self) -> str:
        string = yaml.dump(self.configuration.dict(), default_flow_style=False)
        return string

    def dump_environment(self, indent=6) -> str:
        string = yaml.dump(self.configuration.run.environment, default_flow_style=False)
        return textwrap.indent(string, prefix=" " * indent)
