# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['faastapi',
 'faastapi.cli',
 'faastapi.databases',
 'faastapi.instrumentation',
 'faastapi.security']

package_data = \
{'': ['*'], 'faastapi': ['templates/*']}

install_requires = \
['fastapi>=0.33.0,<0.34.0', 'uvicorn>=0.8.6,<0.9.0']

extras_require = \
{'all': ['click>=7.0,<8.0',
         'pyyaml>=5.1,<6.0',
         'jinja2>=2.10,<3.0',
         'PyJWT>=1.7,<2.0',
         'passlib>=1.7,<2.0',
         'python-multipart>=0.0.5,<0.0.6',
         'bcrypt>=3.1,<4.0',
         'sqlalchemy>=1.3,<2.0',
         'mysqlclient>=1.4,<2.0',
         'psycopg2>=2.8,<3.0',
         'asyncpg>=0.18.3,<0.19.0',
         'aiomysql>=0.0.20,<0.0.21',
         'aiosqlite>=0.10.0,<0.11.0',
         'pymongo>=3.8,<4.0',
         'redis>=3.3,<4.0'],
 'async-mysql': ['databases>=0.2.5,<0.3.0', 'aiomysql>=0.0.20,<0.0.21'],
 'async-postgres': ['databases>=0.2.5,<0.3.0', 'asyncpg>=0.18.3,<0.19.0'],
 'async-sqlite': ['databases>=0.2.5,<0.3.0', 'aiosqlite>=0.10.0,<0.11.0'],
 'cli': ['click>=7.0,<8.0', 'pyyaml>=5.1,<6.0', 'jinja2>=2.10,<3.0'],
 'mongodb': ['pymongo>=3.8,<4.0'],
 'mysql': ['sqlalchemy>=1.3,<2.0', 'mysqlclient>=1.4,<2.0'],
 'oauth': ['PyJWT>=1.7,<2.0',
           'passlib>=1.7,<2.0',
           'python-multipart>=0.0.5,<0.0.6',
           'bcrypt>=3.1,<4.0'],
 'postgres': ['sqlalchemy>=1.3,<2.0', 'psycopg2>=2.8,<3.0'],
 'redis': ['redis>=3.3,<4.0'],
 'sqlite': ['sqlalchemy>=1.3,<2.0']}

entry_points = \
{'console_scripts': ['faastapi = faastapi.cli:entry_point']}

setup_kwargs = {
    'name': 'faastapi',
    'version': '0.3.4',
    'description': 'Easily create OpenFaas functions built on top of FastAPI Python framework',
    'long_description': '# FaastAPI\n\n> Easily create OpenFaas functions built on top of FastAPI Python framework\n\n### Warning:\n\nThis project is in its early phase. It might be subject to a lot of changes and many features might be added/removed.\n\n## Overview\n\n\n`FaastAPI` is built on top of [FastAPI](https://pypi.org/project/fastapi/) framework, [pydantic](https://pypi.org/project/pydantic/) library, and [jinja2](https://pypi.org/project/Jinja2/) library.\n\n\nIt allows developers to quickly generate [OpenFaas](https://www.openfaas.com/) functions.\n\nSeveral plugins can be used to quicly set up a rest API. A command line interface can be installed with the package so that functions can be tested locally.\n\n## Installation\n\nYou can install package using pip:\n\n```shell\npip install faastapi\n```\n\nBy default, the command line interface and plugins are not installed. You can choose to install the cli using the `cli` extra:\n\n```shell\npip install faastapi[cli]\n```\n\n## Example\n\nA simple Faastapi function file (by default Faastapi search files named `faastapi.yml`) can be as follow:\n\n```yaml\n---\napiversion: v1\n\nmeta:\n  name: hello-faastapi\n  version: 0.3.4\n\n  image: gcharbon/hello-fastapi\n  tags:\n    - test\n    - demo\n  description: A dummy function to demonstrate Faastapi\n\nbuild:\n  plugins:\n    basic-auth:\n      username: admin\n      password: password\n    mongodb:\n      host:  127.0.0.1\n      port: 27017\n      database: demo\n    sqlite:\n      uri: sqlite:///example.db\n    async-sqlite:\n    instrumentation:\n\nrun:\n  script: hello.py\n  function: say_hello\n  method: post\n  input:\n    name: \n      type: str\n      default: World\n  output:\n    message: str\n    date: datetime\n    drivers: Dict[str,str]\n```\n\nConsidering the file `hello.py` is present next to `faastapi.yml` with the following content:\n\n```python\nimport datetime\n\n\ndef say_hello(context, name):\n    return {\n        "message": f"Hello {name}",\n        "date": datetime.datetime.now(),\n        "drivers": {\n            "mongodb": str(context.mongodb),\n            "sqlite": str(context.sql),\n            "async-sqlite": str(context.async_sql),\n        },\n    }\n```\n\n> Note: As you can see function must always accept an argument named `context`. In this case, since `sqlite`, `async-sqlite` and `mongodb` plugins where specified, clients are available in the context.\n\nWhen the user run `faastapi function new -f faastapi.yml openfaas`, an OpenFaas function will be generated in the `openfaas` directory.\nThis function can then be deployed to OpenFaas with `faas-cli`:\n\n```shell\ncd openfaas/\nfaas-cli up -f function.yml\n```\n\nYou can then try the function on OpenFaas portal (`http://<OPENFAAS_URL>`):\n\n![Screenshot of OpenFaas portal](https://i.ibb.co/Jr9SwwD/screenshot-openfaas-faastapi.png)\n\n\nYou can also access the documentation of the function at `http://<OPENFAAS_URL>/function/hello-faastapi/docs`:\n\n![Screenshot of documentation](https://i.ibb.co/gySpPXg/screenshot-faastapi.png)\n\n## List of available plugins\n\n\n#### Security plugins:\n\n- `basic-auth`: Enables a basic authentication in your application.\n\n> Note: Username and password can be configured as in the above example\n\n- `oauth2-password`: Enable simple oauth2 with password and bearer.\n\n> Note: At this moment, configuration of user database is not possible, thus usage is limited to default values (username: `admin`, password: `secret`)\n\n#### Databases plugins:\n\n- `sqlite`: Injects an [sqlalchemy](https://www.sqlalchemy.org/) `Session` with `sqlite3` engine into the context by default.\n- `postgres`: Injects an sqlachemy `Session` with `psycopg2` engine into the context by default.\n- `mysql`: Injects an sqlalchemy `Session` with `mysqlclient` engine into the context by default.\n- `async-sqlite`: Injects a `databases.Database` instance with `aiosqlite` engine into the context by default.\n- `async-postgres`: Injects a `databases.Database` instance with `asyncpg` engine into the context by default.\n- `async-mysql`: Injects a `databases.Database` instance with `aiomysql` engine into the context by default.\n\n> Note: All those plugins accept a single configuration variable: `uri`\n\n- `mongodb`: Injects a `pymongo.Database` instance into the context.\n\n> Note: MongoDB plugin can be configured using the variables: `host` (default to `127.0.0.1`), `port` (default to `27017`) and `database` (default to `test`)\n\n- `redis`:  Injects a `Redis` instance into the context.\n\n> Note: Redis plugin can be configured using the variables: `host` (default to `127.0.0.1`), `port` (default to `6379`) and `db` (default to `0`)\n',
    'author': 'Carlos Benavides',
    'author_email': 'carlos.benavides@capgemini.com',
    'url': 'https://monsoon-gitlab.iti.gr/cap-dev/faastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
