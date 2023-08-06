# FaastAPI

> Easily create OpenFaas functions built on top of FastAPI Python framework

### Warning:

This project is in its early phase. It might be subject to a lot of changes and many features might be added/removed.

## Overview


`FaastAPI` is built on top of [FastAPI](https://pypi.org/project/fastapi/) framework, [pydantic](https://pypi.org/project/pydantic/) library, and [jinja2](https://pypi.org/project/Jinja2/) library.


It allows developers to quickly generate [OpenFaas](https://www.openfaas.com/) functions.

Several plugins can be used to quicly set up a rest API. A command line interface can be installed with the package so that functions can be tested locally.

## Installation

You can install package using pip:

```shell
pip install faastapi
```

By default, the command line interface and plugins are not installed. You can choose to install the cli using the `cli` extra:

```shell
pip install faastapi[cli]
```

## Example

A simple Faastapi function file (by default Faastapi search files named `faastapi.yml`) can be as follow:

```yaml
---
apiversion: v1

meta:
  name: hello-faastapi
  version: 0.3.3

  image: gcharbon/hello-fastapi
  tags:
    - test
    - demo
  description: A dummy function to demonstrate Faastapi

build:
  plugins:
    basic-auth:
      username: admin
      password: password
    mongodb:
      host:  127.0.0.1
      port: 27017
      database: demo
    sqlite:
      uri: sqlite:///example.db
    async-sqlite:
    instrumentation:

run:
  script: hello.py
  function: say_hello
  method: post
  input:
    name: 
      type: str
      default: World
  output:
    message: str
    date: datetime
    drivers: Dict[str,str]
```

Considering the file `hello.py` is present next to `faastapi.yml` with the following content:

```python
import datetime


def say_hello(context, name):
    return {
        "message": f"Hello {name}",
        "date": datetime.datetime.now(),
        "drivers": {
            "mongodb": str(context.mongodb),
            "sqlite": str(context.sql),
            "async-sqlite": str(context.async_sql),
        },
    }
```

> Note: As you can see function must always accept an argument named `context`. In this case, since `sqlite`, `async-sqlite` and `mongodb` plugins where specified, clients are available in the context.

When the user run `faastapi function new -f faastapi.yml openfaas`, an OpenFaas function will be generated in the `openfaas` directory.
This function can then be deployed to OpenFaas with `faas-cli`:

```shell
cd openfaas/
faas-cli up -f function.yml
```

## List of available plugins


#### Security plugins:

- `basic-auth`: Enables a basic authentication in your application.

> Note: Username and password can be configured as in the above example

- `oauth2-password`: Enable simple oauth2 with password and bearer.

> Note: At this moment, configuration of user database is not possible, thus usage is limited to default values (username: `admin`, password: `secret`)

#### Databases plugins:

- `sqlite`: Injects an [sqlalchemy](https://www.sqlalchemy.org/) `Session` with `sqlite3` engine into the context by default.
- `postgres`: Injects an sqlachemy `Session` with `psycopg2` engine into the context by default.
- `mysql`: Injects an sqlalchemy `Session` with `mysqlclient` engine into the context by default.
- `async-sqlite`: Injects a `databases.Database` instance with `aiosqlite` engine into the context by default.
- `async-postgres`: Injects a `databases.Database` instance with `asyncpg` engine into the context by default.
- `async-mysql`: Injects a `databases.Database` instance with `aiomysql` engine into the context by default.

> Note: All those plugins accept a single configuration variable: `uri`

- `mongodb`: Injects a `pymongo.Database` instance into the context.

> Note: MongoDB plugin can be configured using the variables: `host` (default to `127.0.0.1`), `port` (default to `27017`) and `database` (default to `test`)

- `redis`:  Injects a `Redis` instance into the context.

> Note: Redis plugin can be configured using the variables: `host` (default to `127.0.0.1`), `port` (default to `6379`) and `db` (default to `0`)
