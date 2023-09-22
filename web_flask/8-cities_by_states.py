#!/usr/bin/python3
"""state list
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask("__main__")


@app.route('/cities_by_states', strict_slashes=False)
def states_cities():
    """return all states"""
    states = storage.all(State)
    return render_template(
        '8-cities_by_states.html',
        title="HBNB",
        table="States",
        states=states
    )


@app.teardown_appcontext
def teardown(exception):
    """calls in the storage close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
