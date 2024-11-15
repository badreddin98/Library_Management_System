import mysql.connector
from datetime import datetime
from db_connection import connection

class Book:
    def __init__(self, title, author_id, isbn, publication_date):
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publication_date = publication_date
        self.available = True

    def save_to_db(self):
        cursor = connection.cursor()
        try:
            query = '''
            INSERT INTO books (title, author_id, isbn, publication_date, availability)
            VALUES (%s, %s, %s, %s, %s)
            '''
            values = (self.title, self.author_id, self.isbn, self.publication_date, self.available)
            cursor.execute(query, values)
            connection.commit()
            print(f"Book '{self.title}' added successfully!")
        except Exception as e:
            print(f"Error adding book: {e}")
        finally:
            cursor.close()

    @staticmethod
    def display_books():
        cursor = connection.cursor(dictionary=True)
        try:
            query = '''
            SELECT b.*, a.name as author_name 
            FROM books b 
            LEFT JOIN authors a ON b.author_id = a.id
            '''
            cursor.execute(query)
            books = cursor.fetchall()
            if not books:
                print("No books found in the library.")
                return
            
            print("\nList of Books:")
            for book in books:
                status = "Available" if book['availability'] else "Borrowed"
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author_name']}")
                print(f"ISBN: {book['isbn']}, Status: {status}")
                print("-" * 50)
        except Exception as e:
            print(f"Error displaying books: {e}")
        finally:
            cursor.close()

    @staticmethod
    def borrow_book(book_id, user_id):
        cursor = connection.cursor()
        try:
            # Check if book is available
            cursor.execute("SELECT availability FROM books WHERE id = %s", (book_id,))
            result = cursor.fetchone()
            if not result or not result[0]:
                print("Book is not available for borrowing.")
                return False

            # Update book availability
            cursor.execute("UPDATE books SET availability = FALSE WHERE id = %s", (book_id,))
            
            # Record the borrowing
            borrow_date = datetime.now().date()
            cursor.execute('''
                INSERT INTO borrowed_books (user_id, book_id, borrow_date)
                VALUES (%s, %s, %s)
            ''', (user_id, book_id, borrow_date))
            
            connection.commit()
            print("Book borrowed successfully!")
            return True
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def return_book(book_id, user_id):
        cursor = connection.cursor()
        try:
            # Update book availability
            cursor.execute("UPDATE books SET availability = TRUE WHERE id = %s", (book_id,))
            
            # Update borrowed_books record
            return_date = datetime.now().date()
            cursor.execute('''
                UPDATE borrowed_books 
                SET return_date = %s 
                WHERE book_id = %s AND user_id = %s AND return_date IS NULL
            ''', (return_date, book_id, user_id))
            
            connection.commit()
            if cursor.rowcount > 0:
                print("Book returned successfully!")
                return True
            else:
                print("No active borrowing record found for this book and user.")
                return False
        except Exception as e:
            print(f"Error returning book: {e}")
            return False
        finally:
            cursor.close()

class Author:
    def __init__(self, name, biography=None):
        self.name = name
        self.biography = biography

    def save_to_db(self):
        cursor = connection.cursor()
        try:
            query = '''
            INSERT INTO authors (name, biography)
            VALUES (%s, %s)
            '''
            values = (self.name, self.biography)
            cursor.execute(query, values)
            connection.commit()
            print(f"Author '{self.name}' added successfully!")
        except Exception as e:
            print(f"Error adding author: {e}")
        finally:
            cursor.close()

    @staticmethod
    def get_author_by_id(author_id):
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM authors WHERE id = %s"
            cursor.execute(query, (author_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving author: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def display_authors():
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM authors")
            authors = cursor.fetchall()
            if not authors:
                print("No authors found.")
                return
            print("\nList of Authors:")
            for author in authors:
                print(f"ID: {author['id']}, Name: {author['name']}")
                if author['biography']:
                    print(f"Biography: {author['biography']}")
                print("-" * 50)
        except Exception as e:
            print(f"Error displaying authors: {e}")
        finally:
            cursor.close()

    @staticmethod
    def update_author(author_id, name=None, biography=None):
        if not name and not biography:
            print("No updates provided.")
            return

        cursor = connection.cursor()
        try:
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if biography:
                updates.append("biography = %s")
                values.append(biography)
            
            values.append(author_id)
            query = f"UPDATE authors SET {', '.join(updates)} WHERE id = %s"
            
            cursor.execute(query, tuple(values))
            connection.commit()
            if cursor.rowcount > 0:
                print("Author updated successfully!")
            else:
                print("Author not found.")
        except Exception as e:
            print(f"Error updating author: {e}")
        finally:
            cursor.close()

class User:
    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def save_to_db(self):
        cursor = connection.cursor()
        try:
            query = '''
            INSERT INTO users (name, email, phone)
            VALUES (%s, %s, %s)
            '''
            values = (self.name, self.email, self.phone)
            cursor.execute(query, values)
            connection.commit()
            print(f"User '{self.name}' added successfully!")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_id(user_id):
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def display_users():
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            if not users:
                print("No users found.")
                return
            print("\nList of Users:")
            for user in users:
                print(f"ID: {user['id']}, Name: {user['name']}")
                print(f"Email: {user['email']}, Phone: {user['phone'] or 'N/A'}")
                print("-" * 50)
        except Exception as e:
            print(f"Error displaying users: {e}")
        finally:
            cursor.close()

    @staticmethod
    def update_user(user_id, name=None, email=None, phone=None):
        if not any([name, email, phone]):
            print("No updates provided.")
            return

        cursor = connection.cursor()
        try:
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if phone:
                updates.append("phone = %s")
                values.append(phone)
            
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            
            cursor.execute(query, tuple(values))
            connection.commit()
            if cursor.rowcount > 0:
                print("User updated successfully!")
            else:
                print("User not found.")
        except Exception as e:
            print(f"Error updating user: {e}")
        finally:
            cursor.close()

    @staticmethod
    def view_borrowed_books(user_id):
        cursor = connection.cursor(dictionary=True)
        try:
            query = '''
            SELECT b.title, b.isbn, bb.borrow_date, bb.return_date,
                   a.name as author_name
            FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.id
            JOIN authors a ON b.author_id = a.id
            WHERE bb.user_id = %s
            ORDER BY bb.borrow_date DESC
            '''
            cursor.execute(query, (user_id,))
            books = cursor.fetchall()
            if not books:
                print("No borrowed books found for this user.")
                return
            print("\nBorrowed Books:")
            for book in books:
                status = "Returned" if book['return_date'] else "Currently Borrowed"
                print(f"Title: {book['title']} by {book['author_name']}")
                print(f"ISBN: {book['isbn']}")
                print(f"Borrowed on: {book['borrow_date']}")
                if book['return_date']:
                    print(f"Returned on: {book['return_date']}")
                print(f"Status: {status}")
                print("-" * 50)
        except Exception as e:
            print(f"Error retrieving borrowed books: {e}")
        finally:
            cursor.close()
