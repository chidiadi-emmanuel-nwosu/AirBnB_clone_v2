#!/usr/bin/python3
"""state list
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask("__main__")


@app.route('/states', strict_slashes=False)
def states():
    """return all states"""
    states = {state.id: state.name for state in storage.all(State).values()}
    return render_template(
        '9-states.html',
        title="HBNB",
        table="States",
        states=states
    )


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """return all states"""
    s_id = [s for s in storage.all(State).values() if s.id == str(id)]
    cities = [(s.id, s.name, s.cities) for s in s_id]
    return render_template(
        '9-states.html',
        title="HBNB",
        table="States",
        cities=cities
    )


@app.teardown_appcontext
def teardown(exception):
    """calls in the storage close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
