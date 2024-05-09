from flask import Flask, request

from hw1.models import get_rooms, init_db, add_book_to_bd, add_room_to_bd

app = Flask(__name__)


@app.route("/room")
def all_rooms():
    rooms = get_rooms(request.args.get('checkIn'), request.args.get('checkOut'))
    return rooms


@app.route('/add-room', methods=['POST'])
def add_room():
    if request.method == "POST":
        room = request.get_json()
        return add_room_to_bd(room)


@app.route('/booking', methods=['POST'])
def booking():
    if request.method == "POST":
        book = request.get_json()
        return add_book_to_bd(book)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=5000)
