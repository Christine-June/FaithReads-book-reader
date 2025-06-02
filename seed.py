# seed.py
from models import Reader, Book, BookEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///app.db")
Session = sessionmaker(bind=engine)
session = Session()

session.query(BookEntry).delete()
session.query(Reader).delete()
session.query(Book).delete()
session.commit()

readers = [
    Reader(name="Alice Johnson"),
    Reader(name="Brian Otieno"),
    Reader(name="Catherine Njeri")
]
session.add_all(readers)
session.commit()

books = [
    Book(title="The Ruthless Elimination of Hurry", author="John Mark Comer", category="Christian Living"),
    Book(title="Boundaries", author="Henry Cloud & John Townsend", category="Self-Help"),
    Book(title="Mere Christianity", author="C.S. Lewis", category="Apologetics")
]
session.add_all(books)
session.commit()

entries = [
    BookEntry(reader_id=readers[0].id, book_id=books[0].id, notes="Loved the clarity on sabbath rest."),
    BookEntry(reader_id=readers[1].id, book_id=books[1].id, notes="Helped me set healthier boundaries."),
    BookEntry(reader_id=readers[2].id, book_id=books[0].id, notes="Really made me rethink my pace of life."),
    BookEntry(reader_id=readers[0].id, book_id=books[2].id, notes="Powerful defense of faith.")
]
session.add_all(entries)
session.commit()

print("Database seeded successfully.")
