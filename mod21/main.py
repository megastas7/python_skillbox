from datetime import datetime, date, timedelta

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, Float, String, Boolean, Date, ForeignKey, DateTime, create_engine, func, \
    extract, desc
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///mod20.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    __tablename__ = "table_authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    __tablename__ = 'table_books'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    receiving = relationship('ReceivingBook', back_populates='book', cascade="all, delete-orphan", lazy="select")
    students = association_proxy('receiving', 'student')

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBook(Base):
    __tablename__ = "table_receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    book = relationship("Book", back_populates="receiving")
    student = relationship("Student", back_populates="receiving")

    @hybrid_property
    def get_day_of_book(self):
        if self.date_of_return:
            return self.date_of_return - self.date_of_issue
        return datetime.now() - self.date_of_issue

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    __tablename__ = "table_students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    receiving = relationship('ReceivingBook', back_populates='student')
    books = association_proxy('receiving', 'book')

    @classmethod
    def get_students_with_scholarship(cls):
        return session.query(Student).filter(Student.scholarship is True).all()

    @classmethod
    def get_students_with_high_average_score(cls, average_score: float):
        return session.query(Student).filter(Student.average_score > average_score).all()

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/books', methods=['GET'])
def get_all_books():
    books = []
    for i in session.query(Book).all():
        books.append(i.to_json())
    return jsonify(books), 200


@app.route('/debtors', methods=['GET'])
def get_students_debtors():
    students_debtors = []
    for i in session.query(ReceivingBook).filter(
            ReceivingBook.date_of_issue < (datetime.now() - timedelta(days=14))).all():
        students_debtors.append(i.to_json())
    return jsonify(students_debtors), 200


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


@app.route('/count-remain-books-by-author/<int:author_id>', methods=['GET'])
def count_remain_books_by_author(author_id):
    book_count = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
    return jsonify(book_count), 200


@app.route('/get-book-which-not-read/<int:student_id>', methods=['GET'])
def get_book_which_student_not_read(student_id):
    authors_id = session.query(ReceivingBook.book_id).distinct().filter(ReceivingBook.student_id == student_id).subquery()
    query_books = session.query(Book).filter(Book.author_id in authors_id).all()
    books = []
    for i in query_books():
        books.append(i.to_json())
    return jsonify(books), 200


@app.route('/avg-count-book-by-student/', methods=['GET'])
def avg_count_book_by_student(student_id):
    books_count = session.query(func.count(ReceivingBook.id)).filter(
        datetime.now().month == extract('month', ReceivingBook.date_of_issue)).scalar()
    student_count = session.query(func.count(Student.id)).scalar()
    if student_count:
        avg_count_books = books_count / student_count
    else:
        avg_count_books = 0
    return jsonify(avg_count_books), 200


@app.route('/popular-book', methods=['GET'])
def get_popular_book():
    query = session.query(Student).filter(Student.average_score > 4.0).all()
    book_counts = {}
    for student in query:
        for book in student.books:
            book_counts[book.id] = book_counts.get(book.id, 0) + 1

    most_popular_book_id = max(book_counts, key=book_counts.get) if book_counts else None
    most_popular_book = session.query(Book).filter(Book.id == most_popular_book_id).first()

    return jsonify(most_popular_book.to_json()), 200


@app.route('/top_readers', methods=['GET'])
def get_top_readers():
    query = session.query(Student).order_by(desc(Student.books_count)).limit(10).all()
    top_readers = []
    for i in query:
        top_readers.append(i.to_json())
    return jsonify(top_readers), 200


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
