from mysql.connector import Error

from books import add_book, list_books
from db import get_connection
from students import add_student, list_students
from transactions import LibraryError, issue_book, list_active_loans, return_book


def read_int(prompt):
    return int(input(prompt).strip())


def show_books():
    books = list_books()
    if not books:
        print("Koi book nahi mili.")
        return
    print("\n--- Books ---")
    for book in books:
        print(
            f"ID: {book['book_id']} | {book['book_name']} | "
            f"Author: {book['author']} | Stock: {book['quantity']}"
        )


def show_students():
    students = list_students()
    if not students:
        print("Koi student nahi mila.")
        return
    print("\n--- Students ---")
    for student in students:
        print(
            f"ID: {student['student_id']} | {student['student_name']} | "
            f"Branch: {student['student_branch']} | Year: {student['student_year']}"
        )


def show_active_loans():
    loans = list_active_loans()
    if not loans:
        print("Abhi koi active loan nahi hai.")
        return
    print("\n--- Active Loans ---")
    for loan in loans:
        print(
            f"Transaction: {loan['transaction_id']} | Book: {loan['book_name']} | "
            f"Student: {loan['student_name']} ({loan['student_branch']}) | "
            f"Issue date: {loan['issue_date']}"
        )


def menu():
    while True:
        print(
            "\n--- Library Management ---\n"
            "1. Add book\n"
            "2. Add student\n"
            "3. Issue book\n"
            "4. Return book\n"
            "5. Show books\n"
            "6. Show students\n"
            "7. Show active loans\n"
            "8. Exit"
        )
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                book_id = add_book(
                    input("Book name: "),
                    input("Author: "),
                    read_int("Quantity: "),
                )
                print(f"Book add ho gayi. Book ID: {book_id}")
            elif choice == "2":
                student_id = add_student(
                    input("Student name: "),
                    input("Branch: "),
                    read_int("Year: "),
                )
                print(f"Student add ho gaya. Student ID: {student_id}")
            elif choice == "3":
                transaction_id = issue_book(
                    read_int("Book ID: "),
                    read_int("Student ID: "),
                )
                print(f"Book issue ho gayi. Transaction ID: {transaction_id}")
            elif choice == "4":
                return_book(read_int("Transaction ID: "))
                print("Book return ho gayi.")
            elif choice == "5":
                show_books()
            elif choice == "6":
                show_students()
            elif choice == "7":
                show_active_loans()
            elif choice == "8":
                print("Library system band ho raha hai.")
                break
            else:
                print("Invalid choice.")
        except (ValueError, Error) as error:
            print(f"Error: {error}")


def main():
    try:
        connection = get_connection()
        connection.close()
    except Error as error:
        print(f"Database connection failed: {error}")
        return
    print("Database successfully connected.")
    menu()


if __name__ == "__main__":
    main()
