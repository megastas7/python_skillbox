import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS table_users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)")
        cursor.execute("INSERT INTO table_users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()


def hack() -> None:
    username: str = "i_like"
    password: str = (
        """sql injection'); delete from table_users; 
        create table if not exists table_users2 (id integer primary key, username text not null,
         password text not null); insert into table_users2 (username, password) values ('you database', 'is hacked'); --"""
    )
    register(username, password)


if __name__=='__main__':
    hack()

