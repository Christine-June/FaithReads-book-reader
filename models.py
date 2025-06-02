from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import create_engine


Base = declarative_base()

engine = create_engine("sqlite:///app.db")

class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    book_entries = relationship("BookEntry", back_populates="reader", cascade="all, delete")

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Reader name cannot be empty.")
        return name

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category = Column(String)

    book_entries = relationship("BookEntry", back_populates="book", cascade="all, delete")

    @validates('title', 'author')
    def validate_not_empty(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError(f"{key.capitalize()} cannot be empty.")
        return value

    @classmethod
    def most_popular(cls, session):
        return session.query(cls.title, func.count(BookEntry.id).label('count'))\
            .join(BookEntry)\
            .group_by(cls.title)\
            .order_by(func.count(BookEntry.id).desc())\
            .first()

class BookEntry(Base):
    __tablename__ = 'book_entries'

    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey('readers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    notes = Column(String)

    reader = relationship("Reader", back_populates="book_entries")
    book = relationship("Book", back_populates="book_entries")
