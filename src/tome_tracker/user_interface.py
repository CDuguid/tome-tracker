class UserInterface:
    def __init__(self):
        pass

    def main_loop(self):
        self.print_intro_message()

        while True:
            command = input("\n> ").casefold()
            if command == "a":
                self.add_book()
            elif command == "l":
                pass
            elif command == "d":
                pass
            elif command == "u":
                pass
            elif command == "q":
                break
            else:
                print("Command not recognised. Choose one of a/l/d/u/q.")

    def print_intro_message(self):
        print("\nWelcome to Tome Tracker!")
        print("\nChoose from one of the following options:")
        print(" - [a]dd a book to storage")
        print(" - [l]ist all stored books")
        print(" - [d]elete a stored book")
        print(" - [u]pdate a stored book")
        print(" - [q]uit")

    def add_book(self):
        # isbn = input("Please provide the book's ISBN:\n> ")
        pass


if __name__ == "__main__":
    UserInterface().main_loop()
