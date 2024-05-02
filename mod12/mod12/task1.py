import logging
import multiprocessing
import sqlite3
import time
import requests
from multiprocessing.pool import ThreadPool

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)
url = 'https://swapi.dev/api/people/'


def get_links():
    links = []
    for i in range(1, 22):
        links.append(url+str(i))
    return links


def get_hero(url):
    response = requests.get(url, timeout=(5, 15))
    data = response.json()
    name = data.get('name', None)
    birth_year = data.get('birth_year', None)
    gender = data.get('gender', None)
    return name, birth_year, gender


def load_heroes_pool():
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(get_hero, get_links())
    pool.close()
    pool.join()
    logger.info(f'время работы с pool- {time.time() - start}')
    return result


def load_heroes_threadpool():
    pool = ThreadPool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(get_hero, get_links())
    pool.close()
    pool.join()
    logger.info(f'время работы с pool- {time.time() - start}')
    return result


def save_to_db(heroes):
    with sqlite3.connect('star_wars.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            create table if not exists heroes 
            (id integer primary key autoincrement, name text, 
            age text, gender text)
                       """)
        for hero in heroes:
            if hero[0] is not None:
                cursor.execute(f"insert into heroes (name, age, gender) values (?, ?, ?)", hero)


if __name__ == '__main__':
    heroes_pool = load_heroes_pool()
    save_to_db(heroes_pool)
    heroes_threadpool = load_heroes_threadpool()
    save_to_db(heroes_threadpool)


