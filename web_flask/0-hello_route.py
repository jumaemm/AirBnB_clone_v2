#!/usr/bin/python3

"""Start Flask"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Default welcome page"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
