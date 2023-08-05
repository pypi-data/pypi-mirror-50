# Flask-AntiJs

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