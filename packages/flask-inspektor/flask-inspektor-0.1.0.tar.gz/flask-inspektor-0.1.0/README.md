[![CircleCI](https://circleci.com/gh/getbyrd/inspektor/tree/master.svg?style=svg)](https://circleci.com/gh/getbyrd/inspektor/tree/master)

# Flask-Inspektor
SQLAlchemy querying metrics collection and reporting extension for Flask.
Heavily influenced by [flask-queryinspect](https://github.com/noise/flask-queryinspect).

[![image](./icon.jpg)](https://www.flickr.com/photos/veryveryquiet)

## Installation

For now you have to use the Git repository:

```bash
pip install git+https://github.com/getbyrd/inspektor.git#egg=flask-inspektor
```


## Usage

Using eagerly configured Flask application:

```python
from flask import Flask
from flask_inspektor import QueryInspector

app = Flask(__name__)
qi = QueryInspector(app)
```

Using lazy configuration or application factory pattern:

```python
from flask import Flask
from flask_inspektor import QueryInspector


qi = QueryInspector()


def create_app():
    app = Flask(__name__)
    qi.init_app(app)
```


## Configuration

*Note*: Query inspector is not enabled by default.

Variable               | Default | Description
--------               | ------- | -----------
QUERYINSPECT_ENABLED   | False   | Activate the extension / react to SQL queries.
QUERYINSPECT_HEADERS   | True    | Enable reporting in HTTP response header.
QUERYINSPECT_LOG       | True    | Enable reporting in INFO level log message.
QUERYINSPECT_LOG_DUPES | False   | Enable logging of duplicated SQL queries.


------

Delivered to you by [developers](mailto:developers@getbyrd.com) of [Byrd](https://getbyrd.com).
