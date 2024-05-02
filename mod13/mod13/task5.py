import sqlite3

create_group = """
create table if not exists groups (
    number int,
    name text,
    country text,
    level text
)
"""

create_play = """
create table if not exists play(
    groups int,
    number int,
    name text,
    country text,
    level text
)
"""


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int):
    c1 = 1
    c2 = 2
    c3 = 3
    c4 = 4
    while number_of_groups > 0:
        cursor.execute(f"insert into groups (number, name, country, level) values ({c1}, '{c1}', '{c1}', 'сильная')")
        cursor.execute(f"insert into groups (number, name, country, level) values ({c2}, '{c2}', '{c2}', 'средняя')")
        cursor.execute(f"insert into groups (number, name, country, level) values ({c3}, '{c3}', '{c3}', 'средняя')")
        cursor.execute(f"insert into groups (number, name, country, level) values ({c4}, '{c4}', '{c4}', 'слабая')")
        c1 += 4
        c2 += 4
        c3 += 4
        c4 += 4
        cursor.execute("insert into play (groups, number, name, country, level) "
                       f"select {number_of_groups}, number, name, country, level "
                       "from groups")
        number_of_groups -= 1


if __name__ == '__main__':
    with sqlite3.connect('uefa.db') as conn:
        c = conn.cursor()
        c.execute(create_group)
        c.execute(create_play)
        generate_test_data(c, 5)
