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
def var_text(text):
    return "c %s" % text.replace("_", " ")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
