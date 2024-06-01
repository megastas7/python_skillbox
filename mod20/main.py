from datetime import datetime, timedelta

from flask import Flask, request
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

engine = create_engine("sqlite:///mod20.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "table_books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(Base):
    __tablename__ = "table_authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Student(Base):
    __tablename__ = "table_students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls):
        return session.query(Student).filter(Student.scholarship == True).all()

    @classmethod
    def get_students_with_high_average_score(cls, average_score: float):
        return session.query(Student).filter(Student.average_score > average_score).all()

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBook(Base):
    __tablename__ = "table_receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def get_day_of_book(self):
        if self.date_of_return:
            return self.date_of_return - self.date_of_issue
        return datetime.now() - self.date_of_issue

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/books', methods=['GET'])
def get_all_books():
    books = []
    for i in session.query(Book).all():
        books.append(i.to_json())
    return books, 200


@app.route('/debtors', methods=['GET'])
def get_students_debtors():
    students_debtors = []
    for i in session.query(ReceivingBook).filter(
            ReceivingBook.date_of_issue < (datetime.now() - timedelta(days=14))).all():
        students_debtors.append(i.to_json())
    return students_debtors, 200


@app.route('/give-book', methods=['POST'])
def add_book_to_receiving_book():
    try:
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)

        new_r = ReceivingBook(book_id, student_id, datetime.now())
        session.add(new_r)
        return f"Книга выдана. Книга = \n {new_r.to_json()}", 200
    except Exception as e:
        return f"Произошла ошибка: {e}", 400


@app.route('/return-book', methods=['POST'])
def add_date_of_return_to_receiving_book():
    try:
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        book = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                   ReceivingBook.student_id == student_id).one()
        book.date_of_return = datetime.now()
        return f"Книгу вернули. Книга = \n {book.to_json()}", 200
    except Exception as e:
        return f"Произошла ошибка: {e}", 400


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
