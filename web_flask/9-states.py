#!/usr/bin/python3
"""Web framework for hbnb"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state_list():
    objs = storage.all(State)
    lst_objs = sorted(objs.values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=lst_objs)


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    state = None
    cities = None
    state_objs = storage.all(State)
    for obj in state_objs.values():
        if id == obj.id:
            state = obj.name
            cities = sorted(obj.cities, key=lambda x: x.name)
    return render_template('9-states.html', states=state, hcities=cities)


@app.teardown_appcontext
def tear_down(exception):
    if storage:
        storage.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
