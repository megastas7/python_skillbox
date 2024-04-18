import requests
import sqlite3
import time
import threading


def load_characters():
    response = requests.get('https://www.swapi.tech/api/people/')
    data = response.json()['results']

    conn = sqlite3.connect('star_wars_characters_2.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS characters
                     (name TEXT, gender TEXT, age TEXT)''')

    for character in data:
        name = character['name']
        gender = character.get('gender', None)
        age = int(character.get('age', '0')) if character.get('age', '0').isdigit() else None

        c.execute("INSERT INTO characters (name, gender, age) VALUES (?, ?, ?)",
                  (name, gender, age))

    conn.commit()
    conn.close()


def load_characters_with_threads():
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=load_characters)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


start_time = time.time()
load_characters()
print("Time taken without threads:", time.time() - start_time)

start_time=time.time()
load_characters_with_threads()
print("Time taken with threads:", time.time() - start_time)


