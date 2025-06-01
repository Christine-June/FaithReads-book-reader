# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    book_entries = relationship('BookEntry', back_populates='reader')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    book_entries = relationship('BookEntry', back_populates='book')

class BookEntry(Base):
    __tablename__ = 'book_entries'
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    notes = Column(String, nullable=False)
    
    reader = relationship('Reader', back_populates='book_entries')
    book = relationship('Book', back_populates='book_entries')
