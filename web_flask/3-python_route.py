#!/usr/bin/python3

"""Start Flask"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Default welcome page"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """just print HBNB"""
    return "HBNB"


@app.route('/c/<string:text>', strict_slashes=False)
def c_text(text):
    """Print C followed by some text"""
    text = text.replace("_", " ")
    return "C %s" % text


@app.route('/python/<string:text>', strict_slashes=False)
def python_text(text="is_cool"):
    """Print some text after Python"""
    text = text.replace("_", " ")
    return "Python %s" % text


if __name__ == "__main__":
    app.run(host="0.0.0.0")
