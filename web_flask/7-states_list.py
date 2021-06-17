#!/usr/bin/python3
"""Web framework for hbnb"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list')
def state_list():
    objs = storage.all(State)
    lst_objs = sorted(objs.values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=lst_objs)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
