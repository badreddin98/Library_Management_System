import mysql.connector

# Database connection configuration
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="callofdutY4#",
    database="library_management"
)

def get_connection():
    """Returns the database connection object"""
    return connection

def close_connection():
    """Closes the database connection"""
    if connection.is_connected():
        connection.close()
        print("Database connection closed.")
