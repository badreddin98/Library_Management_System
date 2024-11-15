import mysql.connector
from db_connection import connection

class User:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    @staticmethod
    def add_user():
        name = input("Enter user name: ")
        email = input("Enter user email: ")
        phone = input("Enter user phone: ")

        cursor = connection.cursor()
        query = '''
        INSERT INTO users (name, email, phone)
        VALUES (%s, %s, %s)
        '''
        values = (name, email, phone)
        try:
            cursor.execute(query, values)
            connection.commit()
            print("User added successfully.")
        except mysql.connector.Error as err:
            print(f"Error adding user: {err}")
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_id(user_id):
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as err:
            print(f"Error retrieving user: {err}")
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
                print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Phone: {user['phone']}")
        except mysql.connector.Error as err:
            print(f"Error displaying users: {err}")
        finally:
            cursor.close()

    @staticmethod
    def update_user():
        user_id = input("Enter user ID to update: ")
        name = input("Enter new name (press enter to skip): ")
        email = input("Enter new email (press enter to skip): ")
        phone = input("Enter new phone (press enter to skip): ")

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

            if not updates:
                print("No changes made.")
                return

            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            
            cursor.execute(query, tuple(values))
            connection.commit()
            if cursor.rowcount > 0:
                print("User updated successfully.")
            else:
                print("User not found.")
        except mysql.connector.Error as err:
            print(f"Error updating user: {err}")
        finally:
            cursor.close()

    @staticmethod
    def view_borrowed_books(user_id):
        cursor = connection.cursor(dictionary=True)
        query = '''
        SELECT b.title, b.isbn, bb.borrow_date, bb.return_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.user_id = %s
        '''
        try:
            cursor.execute(query, (user_id,))
            books = cursor.fetchall()
            if not books:
                print("No borrowed books found for this user.")
                return
            print("\nBorrowed Books:")
            for book in books:
                status = "Returned" if book['return_date'] else "Borrowed"
                print(f"Title: {book['title']}, ISBN: {book['isbn']}")
                print(f"Borrow Date: {book['borrow_date']}, Status: {status}")
        except mysql.connector.Error as err:
            print(f"Error retrieving borrowed books: {err}")
        finally:
            cursor.close()
