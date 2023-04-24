import random
import sqlite3

from faker import Faker


def create():
    try:
        fake = Faker()
        con = sqlite3.connect('music.db')
        c = con.cursor()
        c.execute('''CREATE TABLE customers
                     (id INTEGER,
                      first_name TEXT,
                      last_name TEXT,
                      email TEXT)''')

        for i in range(random.randint(100, 400)):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            c.execute(
                f"INSERT INTO customers (id, first_name, last_name, email) VALUES ({i}, '{first_name}', '{last_name}', '{email}')")

        c.execute('''CREATE TABLE tracks
                     (id INTEGER,
                      title TEXT,
                      artist TEXT,
                      len_in_sec INTEGER)''')

        for i in range(random.randint(100, 250)):
            title = fake.text(random.randint(10, 50))
            artist = fake.name()
            len_in_sec = fake.random_int(min=90, max=240)
            c.execute(
                f"INSERT INTO tracks (id, title, artist, len_in_sec) VALUES ({i}, '{title}', '{artist}', {len_in_sec})")

        con.commit()
        con.close()
    except (Exception,):
        pass


if __name__ == '__main__':
    create()
