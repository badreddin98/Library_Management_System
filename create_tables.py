import mysql.connector

# First, create the database if it doesn't exist
root_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@@@@"
)

def create_database():
    cursor = root_connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_management")
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        root_connection.close()

# Now connect to the library_management database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@@@@",
    database="library_management"
)

def drop_tables():
    cursor = connection.cursor()
    try:
        # Drop tables in reverse order of dependencies
        cursor.execute("DROP TABLE IF EXISTS borrowed_books")
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS authors")
        connection.commit()
        print("Tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")
    finally:
        cursor.close()

def create_tables():
    cursor = connection.cursor()
    try:
        # Create authors table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            biography TEXT
        )
        ''')

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20)
        )
        ''')

        # Create books table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author_id INT,
            isbn VARCHAR(13) UNIQUE,
            publication_date DATE,
            availability BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (author_id) REFERENCES authors(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
        ''')

        # Create borrowed_books table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
        ''')

        connection.commit()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    print("Creating database if it doesn't exist...")
    create_database()
    
    print("\nDropping existing tables...")
    drop_tables()
    
    print("\nCreating new tables...")
    create_tables()
    
    connection.close()
    print("\nDatabase setup completed!")
