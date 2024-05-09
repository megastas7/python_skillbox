import sqlite3
from datetime import datetime

from flask import jsonify
from requests import Response

ROOMS = [
    {"floor": 1, "beds": 1, "guestNum": 1, "price": 1000},
    {"floor": 2, "beds": 2, "guestNum": 2, "price": 2000},
]

BOOKINGS = [
    {'firstName': 'A', 'lastName': 'B', 'room_id': 1, 'checkIn': datetime.strptime('20240501', "%Y%m%d") , 'checkOut': datetime.strptime('20240510', "%Y%m%d")},
    {'firstName': 'AD', 'lastName': 'BA', 'room_id': 2, 'checkIn': datetime.strptime('20240501', "%Y%m%d"), 'checkOut': datetime.strptime('20240510', "%Y%m%d")}]


def init_table_room(cursor, initial):
    cursor.execute("DROP TABLE IF EXISTS 'table_room'")
    cursor.execute(
        "CREATE TABLE 'table_room'"
        "(roomId INTEGER PRIMARY KEY AUTOINCREMENT, floor, beds, guestNum, price)")
    data = [(j for j in i.values()) for i in initial]
    cursor.executemany(
        "INSERT INTO 'table_room'"
        "(floor, beds, guestNum, price) VALUES (?, ?, ?, ?)",
        data)


def init_table_booking(cursor, initial):
    cursor.execute("DROP TABLE IF EXISTS 'table_booking'")
    cursor.execute(
        "CREATE TABLE 'table_booking'"
        "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "firstName VARCHAR(255)"
        "lastName VARCHAR(255),"
        "checkIn DATETIME,"
        "checkOut DATETIME,"
        "roomId INTEGER)")
    data = [(j for j in i.values()) for i in initial]
    cursor.executemany(
        "INSERT INTO 'table_booking' "
        "(firstName, lastName, checkIn, checkOut, roomId) VALUES (?, ?, ?, ?, ?)",
        data)

def init_db():
    with sqlite3.connect("hotel.db") as conn:
        cursor = conn.cursor()
        init_table_room(cursor, ROOMS)
        init_table_booking(cursor, BOOKINGS)


def rooms_to_json(rooms, checkIn, checkOut):
    json_rooms = {"rooms": []}
    for i in rooms:
        json_rooms["rooms"].append({
            "roomId": i[0],
            "floor": i[1],
            "beds": i[2],
            "guestNum": i[3],
            "price": i[4],
            "bookingDates": {
                "checkIn": checkIn,
                "checkOut": checkOut,
            }
        })
    return jsonify(json_rooms)


def get_rooms(checkIn = None, checkOut = None):
    with sqlite3.connect('hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'table_room'")
        rooms = cursor.fetchall()
        return rooms_to_json(rooms, checkIn, checkOut)


def add_room_to_bd(room):
    with sqlite3.connect('hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO table_room (floor, beds, guestNum, price)"
            "VALUES (?, ?, ?, ?)",
            (room['floor'], room['beds'], room['guestNum'], room['price']))
    return jsonify({"id": room['id']})

def check_book(book):
    with sqlite3.connect('hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'table_booking' "
                       "WHERE checkIn >= ? AND checkIn <= ? AND roomId = ?",
                       (book['checkIn'], book['checkOut'], book['roomId']))
        return len(cursor.fetchall()) > 0

def add_book_to_bd(book):
    if check_book(book):
        return "Нельзя забронировать комнату в это время", 409

    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        checkIn = datetime.strptime(str(book["bookingDates"]["checkIn"]), "%Y%m%d"),
        checkOut = datetime.strptime(str(book["bookingDates"]["checkOut"]), "%Y%m%d"),
        cursor.execute(
            "INSERT INTO table_booking "
            "(firstName, lastName, checkIn, checkOut, roomId) VALUES (?, ?, ?, ?, ?)",
            (book['firstname'], book['lastName'], checkIn, checkOut, book['roomId']))
        return jsonify({"roomId": book['room_id']})



