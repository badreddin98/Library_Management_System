from book import Book
from user import User
from author import Author

class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.authors = []

    def main_menu(self):
        while True:
            print("\nWelcome to the Library Management System!")
            print("Main Menu:")
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.book_menu()
            elif choice == "2":
                self.user_menu()
            elif choice == "3":
                self.author_menu()
            elif choice == "4":
                print("Thank you for using the Library Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_menu(self):
        while True:
            print("\nBook Operations:")
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Search for a book")
            print("5. Display all books")
            print("6. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.borrow_book()
            elif choice == "3":
                self.return_book()
            elif choice == "4":
                self.search_book()
            elif choice == "5":
                self.display_books()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self):
        while True:
            print("\nUser Operations:")
            print("1. Add a new user")
            print("2. View user details")
            print("3. Display all users")
            print("4. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_user()
            elif choice == "2":
                self.view_user_details()
            elif choice == "3":
                self.display_users()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def author_menu(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add a new author")
            print("2. View author details")
            print("3. Display all authors")
            print("4. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_author()
            elif choice == "2":
                self.view_author_details()
            elif choice == "3":
                self.display_authors()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_book(self):
        title = input("Enter the book title: ")
        author = input("Enter the author: ")
        genre = input("Enter the genre: ")
        publication_date = input("Enter the publication date: ")
        new_book = Book(title, author, genre, publication_date)
        self.books.append(new_book)
        print(f"Book '{title}' added successfully!")

    def borrow_book(self):
        title = input("Enter the title of the book to borrow: ")
        for book in self.books:
            if book.get_title() == title and book.is_available():
                book.borrow()
                print(f"You have successfully borrowed '{title}'.")
                return
        print(f"The book '{title}' is not available or does not exist.")

    def return_book(self):
        title = input("Enter the title of the book to return: ")
        for book in self.books:
            if book.get_title() == title and not book.is_available():
                book.return_book()
                print(f"You have successfully returned '{title}'.")
                return
        print(f"The book '{title}' is not borrowed or does not exist.")

    def search_book(self):
        title = input("Enter the title of the book to search: ")
        for book in self.books:
            if book.get_title() == title:
                status = "Available" if book.is_available() else "Borrowed"
                print(f"Title: {book.get_title()}, Author: {book.get_author()}, Genre: {book.get_genre()}, Status: {status}")
                return
        print(f"The book '{title}' is not found.")

    def display_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("\nList of books:")
        for book in self.books:
            status = "Available" if book.is_available() else "Borrowed"
            print(f"Title: {book.get_title()}, Author: {book.get_author()}, Status: {status}")

    def add_user(self):
        name = input("Enter the user's name: ")
        library_id = input("Enter the library ID: ")
        new_user = User(name, library_id)
        self.users.append(new_user)
        print(f"User '{name}' added successfully!")

    def view_user_details(self):
        library_id = input("Enter the library ID: ")
        for user in self.users:
            if user.get_library_id() == library_id:
                print(f"Name: {user.get_name()}, Borrowed Books: {user.get_borrowed_books()}")
                return
        print(f"User with ID '{library_id}' not found.")

    def display_users(self):
        if not self.users:
            print("No users found in the system.")
            return
        print("\nList of users:")
        for user in self.users:
            print(f"Name: {user.get_name()}, Library ID: {user.get_library_id()}")

    def add_author(self):
        name = input("Enter the author's name: ")
        biography = input("Enter a short biography: ")
        new_author = Author(name, biography)
        self.authors.append(new_author)
        print(f"Author '{name}' added successfully!")

    def view_author_details(self):
        name = input("Enter the author's name: ")
        for author in self.authors:
            if author.get_name() == name:
                print(f"Name: {author.get_name()}, Biography: {author.get_biography()}")
                return
        print(f"Author '{name}' not found.")

    def display_authors(self):
        if not self.authors:
            print("No authors found in the system.")
            return
        print("\nList of authors:")
        for author in self.authors:
            print(f"Name: {author.get_name()}, Biography: {author.get_biography()}")

# Entry point for the program
if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.main_menu()
