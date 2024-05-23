import sqlite3

if __name__ == '__main__':
    with open('create_schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()