import mysql.connector
from db_connection import connection

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
        try:
            cursor.execute(query, values)
            connection.commit()
            print("Author added successfully.")
        except mysql.connector.Error as err:
            print(f"Error adding author: {err}")
        finally:
            cursor.close()

    @staticmethod
    def get_author_by_id(author_id):
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM authors WHERE id = %s"
        try:
            cursor.execute(query, (author_id,))
            author = cursor.fetchone()
            return author
        except mysql.connector.Error as err:
            print(f"Error retrieving author: {err}")
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
                print(f"ID: {author['id']}, Name: {author['name']}, Biography: {author['biography']}")
        except mysql.connector.Error as err:
            print(f"Error displaying authors: {err}")
        finally:
            cursor.close()

    @staticmethod
    def update_author():
        author_id = input("Enter author ID to update: ")
        name = input("Enter new name (press enter to skip): ")
        biography = input("Enter new biography (press enter to skip): ")

        cursor = connection.cursor()
        try:
            if name and biography:
                query = "UPDATE authors SET name = %s, biography = %s WHERE id = %s"
                values = (name, biography, author_id)
            elif name:
                query = "UPDATE authors SET name = %s WHERE id = %s"
                values = (name, author_id)
            elif biography:
                query = "UPDATE authors SET biography = %s WHERE id = %s"
                values = (biography, author_id)
            else:
                print("No changes made.")
                return

            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount > 0:
                print("Author updated successfully.")
            else:
                print("Author not found.")
        except mysql.connector.Error as err:
            print(f"Error updating author: {err}")
        finally:
            cursor.close()
