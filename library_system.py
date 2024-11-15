from library_db import Book, Author, User, close_connection

class LibraryManagementSystem:
    def __init__(self):
        pass

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
                close_connection()
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
            print("4. Display all books")
            print("5. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                Book.add_book()
            elif choice == "2":
                Book.borrow_book()
            elif choice == "3":
                Book.return_book()
            elif choice == "4":
                Book.display_books()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self):
        while True:
            print("\nUser Operations:")
            print("1. Add a new user")
            print("2. Update user details")
            print("3. Display all users")
            print("4. View user's borrowed books")
            print("5. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                User.add_user()
            elif choice == "2":
                User.update_user()
            elif choice == "3":
                User.display_users()
            elif choice == "4":
                user_id = input("Enter user ID: ")
                User.view_borrowed_books(user_id)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def author_menu(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add a new author")
            print("2. Update author details")
            print("3. Display all authors")
            print("4. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                Author.add_author()
            elif choice == "2":
                Author.update_author()
            elif choice == "3":
                Author.display_authors()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.main_menu()
