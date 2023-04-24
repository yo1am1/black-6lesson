import sqlite3

import flask
from flask import Flask

from HW import data_create

app = Flask(__name__)


@app.route("/")
def index():
    data_create.create()
    return flask.render_template("index.html")


@app.route('/names/')
def unique_names():
    data_create.create()
    con = sqlite3.connect('music.db')
    c = con.cursor()
    names = c.execute("SELECT COUNT(DISTINCT first_name) FROM customers").fetchone()[0]
    con.close()
    return flask.render_template("task1.html", names=names)


@app.route('/tracks/')
def track_count():
    data_create.create()
    con = sqlite3.connect('music.db')
    c = con.cursor()
    track = c.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    con.close()
    return flask.render_template("task2.html", track=track)


@app.route('/tracks-sec/')
def track_lengths():
    data_create.create()
    con = sqlite3.connect('music.db')
    c = con.cursor()
    results = c.execute("SELECT (id+1), title, len_in_sec FROM tracks").fetchall()
    con.close()
    return flask.render_template("task3.html", track_sec=results)


@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("error.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
