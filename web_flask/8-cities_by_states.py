#!/usr/bin/python3
"""Web framework for hbnb"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


# @app.route('/cities_by_states', strict_slashes=False)
# def state_list_by_cities():
#     state_objs = storage.all(State)
#     city_objs = storage.all(City)
#     state_list = sorted(state_objs.values(), key=lambda x: x.name)
#     lst = list()
#     final_states_list = list()
#     for state in state_list:
#         for city in city_objs:
#             if city.state_id == state.id:
#                 lst.append(city)
#         flst = sorted(lst, key=lambda x: x.name)
#         final_states_list.append((state, list(flst)))
#         lst.clear()
#         flst.clear()

#     return render_template('7-states_list.html', states=final_states_list)

@app.route('/cities_by_states', strict_slashes=False)
def state_list():
    objs = storage.all(State)
    lst_objs = sorted(objs.values(), key=lambda x: x.name)
    for item in lst_objs:
        item.cities = sorted(item.cities, key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=lst_objs)


@app.teardown_appcontext
def tear_down(exception):
    if storage:
        storage.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
