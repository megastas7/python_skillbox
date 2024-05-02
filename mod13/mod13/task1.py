import sqlite3

get_temp = """
SELECT temperature_in_celsius
FROM table_truck_with_vaccine
WHERE truck_number = ?
"""


def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    cursor.execute(get_temp, (truck_number,))
    result = cursor.fetchone()
    if result is not None:
        if 18 <= result[0] <= 20:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    with sqlite3.connect("hw1.db") as conn:
        print(check_if_vaccine_has_spoiled(conn.cursor(), input('Введите номер грузовика')))
