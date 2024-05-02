import sqlite3

create_table_query = """
create table if not exists birds (
    bird_name text primary key,
    date_time text
)
"""

get_bird = """
select date_time
from birds
where bird_name = ?
"""


def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str,):
    cursor.execute("insert into birds (bird_name, date_time) values (?, ?)", (bird_name, date_time))
    cursor.connection.commit()


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    cursor.execute(get_bird, (bird_name, ))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


if __name__ == '__main__':
    with sqlite3.connect('birds_saw.db') as conn:
        c = conn.cursor()
        c.execute(create_table_query)
        log_bird(c, input('введите название птицы которую вы видели'),
                 input('введите дату когда вы ее видели(месяц в формате "00")'))
        print(check_if_such_bird_already_seen(c, input('введите имя птицы')))