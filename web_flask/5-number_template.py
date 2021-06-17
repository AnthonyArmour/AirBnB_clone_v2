#!/usr/bin/python3
"""Web framework for hbnb"""


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<string:text>', strict_slashes=False)
def c_text(text):
    return "C %s" % text.replace("_", " ")


@app.route('/python/<string:text>')
@app.route('/python/')
def python_text(text="is cool"):
    return "Python %s" % text.replace('_', ' ')


@app.route('/number/<int:n>')
def n_num(n):
    return "%d is a number" % n


@app.route('/number_template/<int:n>')
def num_template(n):
    return render_template('5-number.html', value=n)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
