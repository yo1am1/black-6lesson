import sqlite3

import flask
from faker import Faker
from flask import Flask

fake = Faker()


try:
    con = sqlite3.connect('music.db')
    c = con.cursor()
    c.execute('''CREATE TABLE customers
                 (id INTEGER,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT)''')

    for i in range(200):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        c.execute(f"INSERT INTO customers (id, first_name, last_name, email) VALUES ({i}, '{first_name}', '{last_name}', '{email}')")

    c.execute('''CREATE TABLE tracks
                 (id INTEGER,
                  title TEXT,
                  artist TEXT,
                  len_in_sec INTEGER)''')

    for i in range(200):
        title = fake.text(40)
        artist = fake.name()
        len_in_sec = fake.random_int(min=90, max=240)
        c.execute(f"INSERT INTO tracks (id, title, artist, len_in_sec) VALUES ({i}, '{title}', '{artist}', {len_in_sec})")

    con.commit()
    con.close()
except (Exception,):
    pass


app = Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route('/names/')
def unique_names():
    con = sqlite3.connect('music.db')
    c = con.cursor()
    names = c.execute("SELECT COUNT(DISTINCT first_name) FROM customers").fetchone()[0]
    con.close()
    return flask.render_template("task1.html", names=names)


@app.route('/tracks/')
def track_count():
    con = sqlite3.connect('music.db')
    c = con.cursor()
    track = c.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    con.close()
    return flask.render_template("task2.html", track=track)


@app.route('/tracks-sec/')
def track_lengths():
    con = sqlite3.connect('music.db')
    c = con.cursor()
    results = c.execute("SELECT title, len_in_sec FROM tracks").fetchall()
    con.close()
    return flask.render_template("task3.html", track_sec=results)


@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("error.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
