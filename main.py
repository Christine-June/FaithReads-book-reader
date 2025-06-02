from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Reader, Book, BookEntry

engine = create_engine("sqlite:///app.db")
Session = sessionmaker(bind=engine)
session = Session()

def list_readers():
    readers = session.query(Reader).all()
    for reader in readers:
        print(f"{reader.id}. {reader.name}")

def list_books():
    books = session.query(Book).all()
    for book in books:
        print(f"{book.id}. {book.title} by {book.author} ({book.category})")

def add_reader():
    name = input("Enter reader's name: ")
    if not name:
        print("Name cannot be empty.")
        return
    reader = Reader(name=name)
    session.add(reader)
    session.commit()
    print(f"Reader '{name}' added.")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    category = input("Enter book category: ")

    if not title or not author or not category:
        print("All fields are required.")
        return

    book = Book(title=title, author=author, category=category)
    session.add(book)
    session.commit()
    print(f"Book '{title}' added.")

def add_book_entry():
    list_readers()
    reader_id = input("Enter Reader ID: ")
    
    list_books()
    book_id = input("Enter Book ID: ")
    
    notes = input("Enter reading notes: ")
    
    entry = BookEntry(reader_id=reader_id, book_id=book_id, notes=notes)
    session.add(entry)
    session.commit()
    print("Book entry added.")

def show_entries_by_reader():
    list_readers()
    reader_id = input("Enter Reader ID to view their entries: ")
    
    reader = session.query(Reader).get(reader_id)
    if reader:
        print(f"\nEntries for {reader.name}:")
        for entry in reader.book_entries:
            print(f"- '{entry.book.title}' | Notes: {entry.notes}")
    else:
        print("Reader not found.")

def delete_entry():
    entries = session.query(BookEntry).all()
    if not entries:
        print("No entries found.")
        return

    print("\nAll Book Entries:")
    for entry in entries:
        print(f"{entry.id}. {entry.reader.name} read '{entry.book.title}' | Notes: {entry.notes}")

    entry_id = input("Enter the ID of the entry to delete: ")
    entry = session.query(BookEntry).get(entry_id)

    if entry:
        session.delete(entry)
        session.commit()
        print("Entry deleted.")
    else:
        print("Entry not found.")

def update_entry_notes():
    entries = session.query(BookEntry).all()
    if not entries:
        print("No entries found.")
        return

    print("\nAll Book Entries:")
    for entry in entries:
        print(f"{entry.id}. {entry.reader.name} read '{entry.book.title}' | Notes: {entry.notes}")

    entry_id = input("Enter the ID of the entry to update: ")
    entry = session.query(BookEntry).get(entry_id)

    if entry:
        new_notes = input("Enter new notes: ")
        entry.notes = new_notes
        session.commit()
        print("Notes updated.")
    else:
        print("Entry not found.")

def show_most_popular_book():
    result = Book.most_popular(session)
    if result:
        title, count = result
        print(f"\nMost Popular Book: '{title}' (Read {count} times)")
    else:
        print("No book entries found yet.")

def menu():
    while True:
        print("\nFaithReads CLI")
        print("1. List all readers")
        print("2. List all books")
        print("3. Add a book entry")
        print("4. Show entries by reader")
        print("5. Delete a book entry")     
        print("6. Update entry notes") 
        print("7. Add a new reader")
        print("8. Add a new book")
        print("9. Show most popular book")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_readers()
        elif choice == "2":
            list_books()
        elif choice == "3":
            add_book_entry()
        elif choice == "4":
            show_entries_by_reader()
        elif choice == "5":
            delete_entry()                  
        elif choice == "6":
            update_entry_notes()
        elif choice == "7":
            add_reader()
        elif choice == "8":
            add_book()
        elif choice == "9":
            show_most_popular_book()
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
