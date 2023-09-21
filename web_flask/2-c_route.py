#!/usr/bin/python3
"""hello route
"""
from flask import Flask


app = Flask("__main__")


@app.route('/', strict_slashes=False)
def hello():
    """return hello HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """return HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_C(text):
    """return C"""
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
