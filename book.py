from db_connection import connection
from datetime import datetime

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
