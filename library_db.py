import mysql.connector
from datetime import datetime

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="callofdutY4#",
    database="library_management"
)

class Book:
    def __init__(self, title, author_id, isbn, publication_date):
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publication_date = publication_date

    @staticmethod
    def add_book():
        title = input("Enter book title: ")
        author_id = int(input("Enter author ID: "))
        isbn = input("Enter ISBN: ")
        publication_date = input("Enter publication date (YYYY-MM-DD): ")

        cursor = connection.cursor()
        query = '''
        INSERT INTO books (title, author_id, isbn, publication_date, availability)
        VALUES (%s, %s, %s, %s, %s)
        '''
        values = (title, author_id, isbn, publication_date, True)
        cursor.execute(query, values)
        connection.commit()
        print("Book added successfully.")

    @staticmethod
    def borrow_book():
        book_id = int(input("Enter book ID to borrow: "))
        user_id = int(input("Enter your user ID: "))
        borrow_date = datetime.now().date()

        cursor = connection.cursor()
        cursor.execute("SELECT availability FROM books WHERE id = %s", (book_id,))
        availability = cursor.fetchone()[0]
        if availability:
            cursor.execute("UPDATE books SET availability = 0 WHERE id = %s", (book_id,))
            cursor.execute(
                "INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, %s)",
                (user_id, book_id, borrow_date)
            )
            connection.commit()
            print("Book borrowed successfully.")
        else:
            print("Book is not available.")

    @staticmethod
    def return_book():
        book_id = int(input("Enter book ID to return: "))
        user_id = int(input("Enter your user ID: "))
        return_date = datetime.now().date()

        cursor = connection.cursor()
        cursor.execute("UPDATE books SET availability = 1 WHERE id = %s", (book_id,))
        cursor.execute(
            "UPDATE borrowed_books SET return_date = %s WHERE book_id = %s AND user_id = %s",
            (return_date, book_id, user_id)
        )
        connection.commit()
        print("Book returned successfully.")

    @staticmethod
    def display_books():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        for book in cursor.fetchall():
            print(book)

class Author:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    @staticmethod
    def add_author():
        name = input("Enter author name: ")
        biography = input("Enter author biography: ")

        cursor = connection.cursor()
        query = '''
        INSERT INTO authors (name, biography)
        VALUES (%s, %s)
        '''
        values = (name, biography)
        cursor.execute(query, values)
        connection.commit()
        print("Author added successfully.")

    @staticmethod
    def display_authors():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors")
        for author in cursor.fetchall():
            print(author)

class User:
    def __init__(self, name, library_id):
        self.name = name
        self.library_id = library_id

    @staticmethod
    def add_user():
        name = input("Enter user name: ")
        library_id = input("Enter user library ID: ")

        cursor = connection.cursor()
        query = '''
        INSERT INTO users (name, library_id)
        VALUES (%s, %s)
        '''
        values = (name, library_id)
        cursor.execute(query, values)
        connection.commit()
        print("User added successfully.")

    @staticmethod
    def display_users():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        for user in cursor.fetchall():
            print(user)

def close_connection():
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")
