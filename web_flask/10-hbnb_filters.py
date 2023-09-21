#!/usr/bin/python3
"""state list
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask("__main__")


@app.teardown_appcontext
def teardown(exception):
    """calls in the storage close method"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def list_states():
    """return all states"""
    states = {s.name: s.cities for s in storage.all(State).values()}
    amenities = [amenity for amenity in storage.all(Amenity).values()]
    return render_template(
        '10-hbnb_filters.html',
        states=states,
        amenities=amenities
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
