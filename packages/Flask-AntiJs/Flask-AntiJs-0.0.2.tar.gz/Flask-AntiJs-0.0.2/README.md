# Flask-AntiJs
[![PyPI](https://img.shields.io/pypi/v/Flask-AntiJs.svg)](https://pypi.python.org/pypi/Flask-AntiJs)
[![Build Status](https://travis-ci.com/michaelbukachi/flask-antijs.svg?branch=master)](https://travis-ci.com/michaelbukachi/flask-antijs)

Flask-AntiJs is a Flask extension the protects endpoints against
'undefined' javascript values by checking the URL, query params and payloads
and return a 400 (Bad request) response.

### Install

```
$ pip install Flask-AntiJs
```

### Usage
```
from flask import Flask
from flask_antijs import AntiJs

app = Flask(__name__)
AntiJs(app)
```

### Issues
Feel free to raise any issue [here](https://github.com/michaelbukachi/flask-antijs/issues).

### Contributions
All contributions are welcome:smile:.