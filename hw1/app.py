from flask import Flask
import random
import datetime
import re
import os

app = Flask(__name__)

carslist = ["Chevrolet", "Renault", "Ford", "Lada"]

catslist = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]

counter = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
file = open(BOOK_FILE, "r", encoding="utf-8")
data = file.read()


def get_rnd_word():
    words = re.findall(r'\b\w+\b', data)
    return random.choice(words)


@app.route('/hello_world')
def hello_world():
    return "Привет мир!"


@app.route('/cars')
def cars():
    return ", ".join(str(element) for element in carslist)


@app.route('/cats')
def cats():
    return random.choice(catslist)


@app.route('/get_time/now')
def time_now():
    time = f'{datetime.datetime.now():%H:%M:%S%z}'
    return ('Точное время: %s' % time)


@app.route('/get_time/future')
def time_future():
    time = f'{(datetime.timedelta(hours=1) + datetime.datetime.now()):%H:%M:%S%z}'
    return ('Точное время через час будет: %s' % time)


@app.route('/get_random_word')
def rnd_word():
    return get_rnd_word()


@app.route('/counter')
def get_counter():
    global counter
    counter += 1
    return str(counter)


if __name__ == '__main__':
  app.run(debug=True)