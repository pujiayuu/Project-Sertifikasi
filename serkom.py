from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from prettytable import PrettyTable
import json
import os

Base = declarative_base()

# MySQL connection
engine = create_engine('mysql+mysqlconnector://root@127.0.0.1/serkom', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(100))
    author = Column(String(100))

    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

    def __repr__(self):
        return f"<Item(id='{self.id}', title='{self.title}', author='{self.author}')>"

class Book(Item): 
    __tablename__ = 'books'
    year = Column(Integer)

    def __init__(self, id, title, author, year):
        super().__init__(id, title, author)
        self.year = year

    def __repr__(self):
        return f"<Book(id='{self.id}', title='{self.title}', author='{self.author}', year='{self.year}')>"

class Magazine(Item):
    __tablename__ = 'magazines'
    issue = Column(String(100))

    def __init__(self, id, title, author, issue):
        super().__init__(id, title, author)
        self.issue = issue

    def __repr__(self):
        return f"<Magazine(id='{self.id}', title='{self.title}', author='{self.author}', issue='{self.issue}')>"

Base.metadata.create_all(engine)

class LibraryDatabase:
    def add(self, item):
        try:
            existing_item = session.query(type(item)).filter_by(id=item.id).first()
            if existing_item:
                print(f"Item with ID {item.id} already exists.")
                return
            session.add(item)
            session.commit()
            print("Item added successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

    def list(self, item_type):
        return session.query(item_type).all()

    def update(self, item_id, item_type, title, author, specific_attr):
        item = session.query(item_type).filter(item_type.id == item_id).first()
        if item:
            item.title = title
            item.author = author
            if isinstance(item, Book):
                item.year = specific_attr
            elif isinstance(item, Magazine):
                item.issue = specific_attr
            session.commit()
            return True
        return False

    def delete(self, item_id, item_type):
        item = session.query(item_type).filter(item_type.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
            return True
        return False

class LibraryInterface:
    def __init__(self):
        self.db = LibraryDatabase()

    def add_item(self):
        item_type = input("Enter item type (book/magazine): ").lower()
        if item_type not in ['book', 'magazine']:
            print("Invalid item type!")
            return

        item_id = int(input("Enter item ID: "))
        title = input("Enter item title: ")
        author = input("Enter item author: ")

        if item_type == 'book':
            year = int(input("Enter book year: "))
            item = Book(id=item_id, title=title, author=author, year=year)
        elif item_type == 'magazine':
            issue = input("Enter magazine issue: ")
            item = Magazine(id=item_id, title=title, author=author, issue=issue)

        self.db.add(item)

    def list_items(self):
        item_type = input("Enter item type to list (book/magazine): ").lower()
        if item_type not in ['book', 'magazine']:
            print("Invalid item type!")
            return

        if item_type == 'book':
            items = self.db.list(Book)
        elif item_type == 'magazine':
            items = self.db.list(Magazine)

        if items:
            table = PrettyTable()
            if item_type == 'book':
                table.field_names = ["ID", "Title", "Author", "Year"]
            else:
                table.field_names = ["ID", "Title", "Author", "Issue"]
            for item in items:
                if item_type == 'book':
                    table.add_row([item.id, item.title, item.author, item.year])
                else:
                    table.add_row([item.id, item.title, item.author, item.issue])
            print(table)
        else:
            print(f"No {item_type}s available.")

    def update_item(self):
        item_type = input("Enter item type (book/magazine): ").lower()
        if item_type not in ['book', 'magazine']:
            print("Invalid item type!")
            return

        item_id = int(input("Enter item ID to update: "))
        title = input("Enter new item title: ")
        author = input("Enter new item author: ")

        if item_type == 'book':
            year = int(input("Enter new book year: "))
            success = self.db.update(item_id, Book, title, author, year)
        elif item_type == 'magazine':
            issue = input("Enter new magazine issue: ")
            success = self.db.update(item_id, Magazine, title, author, issue)

        if success:
            print("Item updated successfully!")
        else:
            print("Item ID not found.")

    def delete_item(self):
        item_type = input("Enter item type (book/magazine): ").lower()
        if item_type not in ['book', 'magazine']:
            print("Invalid item type!")
            return

        item_id = int(input("Enter item ID to delete: "))

        if item_type == 'book':
            success = self.db.delete(item_id, Book)
        elif item_type == 'magazine':
            success = self.db.delete(item_id, Magazine)

        if success:
            print("Item deleted successfully!")
        else:
            print("Item ID not found.")

    def save_to_file(self):
        books = self.db.list(Book)
        magazines = self.db.list(Magazine)
        
        data = {
            'books': [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year} for book in books],
            'magazines': [{'id': magazine.id, 'title': magazine.title, 'author': magazine.author, 'issue': magazine.issue} for magazine in magazines]
        }

        with open('library_data.json', 'w') as f:
            json.dump(data, f)
        print("Data saved to library_data.json")

    def load_from_file(self):
        if not os.path.exists('library_data.json'):
            print("No saved data found.")
            return

        with open('library_data.json', 'r') as f:
            data = json.load(f)

        for book_data in data.get('books', []):
            book = Book(id=book_data['id'], title=book_data['title'], author=book_data['author'], year=book_data['year'])
            self.db.add(book)

        for magazine_data in data.get('magazines', []):
            magazine = Magazine(id=magazine_data['id'], title=magazine_data['title'], author=magazine_data['author'], issue=magazine_data['issue'])
            self.db.add(magazine)

        print("Data loaded from library_data.json")

    def main_menu(self):
        while True:
            print("\nLibrary Management System")
            print("1. Add Item")
            print("2. List Items")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Save to File")
            print("6. Load from File")
            print("7. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.list_items()
            elif choice == '3':
                self.update_item()
            elif choice == '4':
                self.delete_item()
            elif choice == '5':
                self.save_to_file()
            elif choice == '6':
                self.load_from_file()
            elif choice == '7':
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    interface = LibraryInterface()
    interface.main_menu()
