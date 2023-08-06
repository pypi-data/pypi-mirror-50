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
         'pymongo>=3.8,<4.0'],
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
 'sql': ['sqlalchemy>=1.3,<2.0'],
 'sqlite': ['databases>=0.2.5,<0.3.0', 'aiosqlite>=0.10.0,<0.11.0']}

entry_points = \
{'console_scripts': ['faastapi = faastapi.cli.cli:entry_point']}

setup_kwargs = {
    'name': 'faastapi',
    'version': '0.1.5',
    'description': 'Easily create OpenFaas functions built on top of FastAPI Python framework',
    'long_description': '# FaastAPI\n\n> Easily create OpenFaas functions built on top of FastAPI Python framework\n\n### Warning:\n\nThis project is in its early phase. It might be subject to a lot of changes and many features might be added/removed.\n',
    'author': 'Guillaume Charbonnier',
    'author_email': 'guillaume.charbonnier@capgemini.com',
    'url': 'https://monsoon-gitlab.iti.gr/cap-dev/faastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
