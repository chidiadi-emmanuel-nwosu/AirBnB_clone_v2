#!/usr/bin/python3
"""state list
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask("__main__")


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_id(id=None):
    """return all states"""
    states = storage.all(State)
    if id:
        for state in states.values():
            if state.id == id:
                return render_template('9-states.html', state=state)
        return render_template('9-states.html')
    else:
        return render_template('9-states.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """calls in the storage close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
