from library_db import Book, Author, User

def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Quit")
        choice = input("Select an option: ")

        if choice == '1':
            book_operations()
        elif choice == '2':
            user_operations()
        elif choice == '3':
            author_operations()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid option. Try again.")

def book_operations():
    while True:
        print("\nBook Operations")
        print("1. Add a new book")
        print("2. Display all books")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Go back to the main menu")
        choice = input("Select an option: ")

        if choice == '1':
            # First check if there are any authors
            print("\nAvailable Authors:")
            Author.display_authors()
            
            # Get author ID
            try:
                author_id = int(input("\nEnter author ID (or 0 to add a new author first): "))
                if author_id == 0:
                    print("\nLet's add a new author first:")
                    name = input("Enter author name: ")
                    biography = input("Enter author biography (optional): ")
                    new_author = Author(name, biography)
                    new_author.save_to_db()
                    print("\nNow let's add the book. Available Authors:")
                    Author.display_authors()
                    author_id = int(input("\nEnter author ID for the book: "))
                
                # Now add the book
                title = input("Enter the book title: ")
                isbn = input("Enter ISBN: ")
                publication_date = input("Enter publication date (YYYY-MM-DD): ")
                book = Book(title, author_id, isbn, publication_date)
                book.save_to_db()
            except ValueError:
                print("Invalid input. Please enter a valid number for author ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            Book.display_books()
        elif choice == '3':
            Book.display_books()
            try:
                book_id = int(input("\nEnter book ID to borrow: "))
                User.display_users()
                user_id = int(input("\nEnter your user ID: "))
                Book.borrow_book(book_id, user_id)
            except ValueError:
                print("Invalid input. Please enter valid numbers for book ID and user ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            Book.display_books()
            try:
                book_id = int(input("\nEnter book ID to return: "))
                User.display_users()
                user_id = int(input("\nEnter your user ID: "))
                Book.return_book(book_id, user_id)
            except ValueError:
                print("Invalid input. Please enter valid numbers for book ID and user ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '5':
            break
        else:
            print("Invalid option. Try again.")

def user_operations():
    while True:
        print("\nUser Operations")
        print("1. Add a new user")
        print("2. Display all users")
        print("3. Update user details")
        print("4. View borrowed books")
        print("5. Go back to the main menu")
        choice = input("Select an option: ")

        if choice == '1':
            try:
                name = input("Enter user name: ")
                email = input("Enter user email: ")
                phone = input("Enter user phone (optional): ")
                if not phone.strip():
                    phone = None
                user = User(name, email, phone)
                user.save_to_db()
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            User.display_users()
        elif choice == '3':
            User.display_users()
            try:
                user_id = int(input("\nEnter user ID to update: "))
                name = input("Enter new name (or press enter to skip): ")
                email = input("Enter new email (or press enter to skip): ")
                phone = input("Enter new phone (or press enter to skip): ")
                User.update_user(user_id, 
                               name if name.strip() else None,
                               email if email.strip() else None,
                               phone if phone.strip() else None)
            except ValueError:
                print("Invalid input. Please enter a valid number for user ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            User.display_users()
            try:
                user_id = int(input("\nEnter user ID to view borrowed books: "))
                User.view_borrowed_books(user_id)
            except ValueError:
                print("Invalid input. Please enter a valid number for user ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '5':
            break
        else:
            print("Invalid option. Try again.")

def author_operations():
    while True:
        print("\nAuthor Operations")
        print("1. Add a new author")
        print("2. Display all authors")
        print("3. Update author details")
        print("4. Go back to the main menu")
        choice = input("Select an option: ")

        if choice == '1':
            try:
                name = input("Enter author name: ")
                biography = input("Enter author biography (optional): ")
                if not biography.strip():
                    biography = None
                author = Author(name, biography)
                author.save_to_db()
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            Author.display_authors()
        elif choice == '3':
            Author.display_authors()
            try:
                author_id = int(input("\nEnter author ID to update: "))
                name = input("Enter new name (or press enter to skip): ")
                biography = input("Enter new biography (or press enter to skip): ")
                Author.update_author(author_id,
                                  name if name.strip() else None,
                                  biography if biography.strip() else None)
            except ValueError:
                print("Invalid input. Please enter a valid number for author ID.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
