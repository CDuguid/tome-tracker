from api_utils import get_volume_id_by_isbn, get_book_by_volume_id, NoMatchingISBN
from db_utils import (
    create_books_table,
    add_book_to_db,
    list_books_in_db,
    delete_book_from_db,
    update_book_in_db,
)
from barcode_scanner import scan_barcode


class UserInterface:
    def __init__(self):
        self.db_name = "tome_tracker"
        create_books_table(self.db_name)

    def main_loop(self):
        self.print_intro_message()

        while True:
            command = input("\n> ").casefold()
            if command == "a":
                self.add_book()
            elif command == "l":
                self.list_stored_books()
            elif command == "d":
                self.delete_book()
            elif command == "u":
                self.update_book()
            elif command == "q":
                break
            else:
                print("Command not recognised. Choose one of a/l/d/u/q.")

    def print_intro_message(self):
        print("\nWelcome to Tome Tracker!")
        print("\nChoose from one of the following options:")
        print(" - [a]dd a book to storage")
        print(" - [l]ist stored books")
        print(" - [d]elete a stored book")
        print(" - [u]pdate a stored book")
        print(" - [q]uit")

    def add_book(self):
        addition_type = input(
            "Press 's' to scan a barcode or any other key to manually enter an ISBN:\n> "
        )
        if addition_type == "s":
            isbn = scan_barcode()
        else:
            isbn = input("Please provide the book's ISBN:\n> ")
        try:
            volume_id = get_volume_id_by_isbn(isbn)
            book_info = get_book_by_volume_id(volume_id)
            print(f"{book_info['title']} has been found.")
        except NoMatchingISBN:
            print("No book with that ISBN could be found!")
            return

        read_status = input("Press 'y' if you have read this book:\n> ")
        read_status = read_status == "y"
        response = add_book_to_db(self.db_name, book_info, read_status)
        if response:
            print("Book successfully added!")
        else:
            print("Book has already been added!")

    def list_stored_books(self):
        read_status = input(
            "Press 'r' to see all read books, 'u' to see all unread books, and any other key to see all books:\n> "
        )
        if read_status == "r":
            stored_books = list_books_in_db(self.db_name, True)
        elif read_status == "u":
            stored_books = list_books_in_db(self.db_name, False)
        else:
            stored_books = list_books_in_db(self.db_name)

        print("Currently stored books:")
        for book in stored_books:
            print(f" - {book}")

    def delete_book(self):
        deletion_command = input(
            "Press 't' to delete by title, 'i' to delete by ISBN, or any other key to cancel deletion:\n> "
        )
        if deletion_command == "t":
            title = input("Please enter the title exactly:\n> ")
            response = delete_book_from_db(self.db_name, title=title)
            if response:
                print("Book deleted from storage!")
            else:
                print("Book could not be found!")
        elif deletion_command == "i":
            isbn = input("Please enter the ISBN without dashes or spaces:\n> ")
            response = delete_book_from_db(self.db_name, isbn=isbn)
            if response:
                print("Book deleted from storage!")
            else:
                print("Book could not be found!")

    def update_book(self):
        print("This will toggle whether a book is marked as read or not.")
        title = input("Please enter the title of the book to update:\n> ")
        response = update_book_in_db(self.db_name, title, True)
        if response:
            print("Book updated!")
        else:
            print("Book could not be found!")


if __name__ == "__main__":
    UserInterface().main_loop()
