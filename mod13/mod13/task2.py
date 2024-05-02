import sqlite3

deleted = """
    DELETE FROM table_fees
    WHERE truck_number=? AND timestamp= ?
"""


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str):
    truck_number, timestamp = wrong_fees_file.split()
    cursor.execute("SELECT COUNT(*) FROM table_fees WHERE truck_number=? AND timestamp=?", (truck_number, timestamp))
    if cursor.fetchone()[0] > 0:
        cursor.execute(deleted, (truck_number, timestamp))
        conn.commit()
        if cursor.rowcount > 0:
            return "Удаление выполнено успешно."
        else:
            return "Ничего не было удалено."


if __name__ == "__main__":
    with sqlite3.connect("hw2.db") as conn:
        print(delete_wrong_fees(conn.cursor(), input('Введите номер грузовика и дату через пробел: ')))
