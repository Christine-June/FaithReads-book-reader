from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Reader, Book, BookEntry, Base

# 1. Connect to the SQLite DB
engine = create_engine('sqlite:///app.db')

# 2. Bind a session to the engine
Session = sessionmaker(bind=engine)
session = Session()

# 3. Create test data
reader = Reader(name="Hery Excel")
book = Book(title="Python Power", author="Alex Dev", category="Programming")
entry = BookEntry(notes="Learned OOP", reader=reader, book=book)

# 4. Add objects to session
session.add_all([reader, book, entry])

# 5. Commit to save changes
session.commit()

print("✅ Database seeded successfully!")

# 6. Optional: Query and print to verify
for r in session.query(Reader).all():
    print(f"Reader: {r.name}")
    for entry in r.book_entries:
        print(f"  - Read '{entry.book.title}' by {entry.book.author} with notes: {entry.notes}")
