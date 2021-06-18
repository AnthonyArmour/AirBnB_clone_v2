#!/usr/bin/python3
"""Web framework for hbnb"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def state_list():
    state_objs = storage.all(State)
    amenity_objs = storage.all(Amenity)
    a_lst = sorted(amenity_objs.values(), key=lambda x: x.name)
    lst_objs = sorted(state_objs.values(), key=lambda x: x.name)
    for item in lst_objs:
        cities = sorted(item.cities, key=lambda x: x.name)
        setattr(item, "sorted_cities", cities)
    return render_template('10-hbnb_filters.html',
                           states=lst_objs, amenities=a_lst)


@app.teardown_appcontext
def tear_down(exception):
    if storage:
        storage.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
