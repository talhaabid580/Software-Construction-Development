from validation import validate_copies
from book_operations import get_book_status
from display import display_book


def main():
    # to get book information


    title = input("Enter book title: ")
    author = input("Enter author name: ")
    copies = int(input("Enter number of copies: "))

    # to validate number of copies


    while not validate_copies(copies):
        print("Invalid copies. Enter 0 or more.")
        copies = int(input("Enter number of copies: "))

    # to determine book status


    status = get_book_status(copies)

    # to display book information
    display_book(title, author, copies, status)


main()