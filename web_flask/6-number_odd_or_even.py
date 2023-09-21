#!/usr/bin/python3
"""hello route
"""
from flask import Flask, render_template


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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text='is cool'):
    """return python"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """return number"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_number_template(n):
    """return number template"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def display_number_odd_or_even(n):
    """return number template"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
