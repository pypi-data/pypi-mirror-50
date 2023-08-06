import os
from shutil import copy2
from typing import Optional, Dict

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
from .logger import logger
from .temp import TempDirectory
from .exceptions import MissingDependencyError


if PYYAML_INSTALLED == 0:
    raise MissingDependencyError("pyyaml", "cli")
if JINJA2_INSTALLED == 0:
    raise MissingDependencyError("jinja2", "cli")


env = Environment(loader=PackageLoader("faastapi", "templates"))


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

    def __init__(
        self,
        name="demo-faastapi",
        image="gcharbon/demo-faastapi",
        tag="0.1.4",
        configuration: Optional[dict] = None,
    ):

        """
        Init a FunctionTemplate based on a string template
        """
        self.temp_dir = TempDirectory()
        self.temp_dir.mkdir("function")
        self.__configuration__ = configuration
        if configuration:
            self.configuration = self.extract_configuration(configuration)
        else:
            self.configuration = {}
        self.dockerfile_template = self.DOCKER_TEMPLATE
        self.server_template = self.SERVER_TEMPLATE
        self.handler_template = self.FUNCTION_TEMPLATE
        self.functionfile_template = self.FUNCTION_FILE_TEMPLATE
        self.models_template = self.MODELS_TEMPLATE
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
        return cls(configuration)

    def extract_configuration(self, config: dict) -> dict:
        """
        Extract relevant configuration information from given dictionary
        """
        return config

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
                output=file_path, template=template, vars=self.configuration
            )
        else:
            output = self.__write_temp_template__(
                output=file_name, template=template, vars=self.configuration
            )
        return output

    def render_dockerfile(self):
        return self.__render_template__(
            template=self.dockerfile_template, vars=self.configuration
        )

    def write_dockerfile(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.dockerfile_template,
            file_path=file_path,
            file_name="function/Dockerfile",
        )
        logger.debug(f"Successfully written Dockerfile at {output}")
        return output

    def render_functionfile(self):
        return self.__render_template__(
            template=self.functionfile_template, vars=self.configuration
        )

    def write_functionfile(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.functionfile_template,
            file_path=file_path,
            file_name="function.yml",
        )
        logger.debug(f"Successfully written OpenFaas function file at {output}")
        return output

    def render_server(self):
        """
        Render the server template. Returns rendered template as string.
        """
        return self.__render_template__(
            template=self.server_template, vars=self.configuration
        )

    def write_server(self, file_path: Optional[str] = None):
        output = self.__write__(
            template=self.server_template,
            file_path=file_path,
            file_name="function/main.py",
        )
        logger.debug("Successfully written server at {0}".format(output))
        return output

    def render_handler(self) -> str:
        """
        Render the handler template. Returns rendered template as string.
        """
        return self.__render_template__(
            template=self.handler_template, vars=self.configuration
        )

    def write_handler(self, file_path: Optional[str] = None) -> str:
        """
        Write handler.py to file.
        """
        output = self.__write__(
            template=self.handler_template,
            file_path=file_path,
            file_name="function/handler.py",
        )
        logger.debug("Successfully written handler at {0}".format(output))
        return output

    def render_models(self) -> str:
        """
        Render the model template. Returns rendered template as string.
        """
        return self.__render_template__(
            template=self.models_template, vars=self.configuration
        )

    def write_models(self, file_path: Optional[str] = None) -> str:
        """
        Write handler.py to file.
        """
        output = self.__write__(
            template=self.models_template,
            file_path=file_path,
            file_name="function/models.py",
        )
        logger.debug("Successfully written models at {0}".format(output))
        return output

    def write_requirements(
        self,
        requirements_file: Optional[str] = "requirements.txt",
        file_path: Optional[str] = None,
    ) -> str:
        if file_path is None:
            file_path = os.path.join(self.temp_dir.path, requirements_file)
        output = copy2(src=requirements_file, dest=file_path)
        logger.debug("Successfully copy requirements to {0}".format(output))

    def generate_function(self):
        self.write_dockerfile()
        self.write_handler()
        self.write_server()
        self.write_functionfile()
        self.write_models()
        # if self.install_pip_requirements:
        #     self.write_requirements()

    def render(self, output):
        self.generate_function()
        try:
            logger.debug(
                f"Copying content of directory {self.temp_dir.path} into {output}"
            )
            self.temp_dir.copy(output)
        except FileExistsError:
            self.temp_dir.close()
            raise FileExistsError(f"{output} directory already exists")
        logger.info(f"Succcessfully generated function in directory {output}")
        self.temp_dir.close()
