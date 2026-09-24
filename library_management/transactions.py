from db import db_session


class LibraryError(ValueError):
    pass


def issue_book(book_id, student_id):
    with db_session() as connection:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,),
        )
        if cursor.fetchone() is None:
            raise LibraryError("Student ID nahi mila.")

        cursor.execute(
            "SELECT book_id, quantity FROM books WHERE book_id = %s FOR UPDATE",
            (book_id,),
        )
        book = cursor.fetchone()
        if book is None:
            raise LibraryError("Book ID nahi mila.")
        if book["quantity"] <= 0:
            raise LibraryError("Book stock mein available nahi hai.")

        cursor.execute(
            """
            SELECT transaction_id
            FROM transactions
            WHERE book_id = %s AND student_id = %s AND status = 'issued'
            """,
            (book_id, student_id),
        )
        if cursor.fetchone() is not None:
            raise LibraryError("Ye book is student ko pehle se issue hai.")

        cursor.execute(
            "UPDATE books SET quantity = quantity - 1 WHERE book_id = %s",
            (book_id,),
        )
        cursor.execute(
            """
            INSERT INTO transactions (book_id, student_id, issue_date, status)
            VALUES (%s, %s, CURDATE(), 'issued')
            """,
            (book_id, student_id),
        )
        transaction_id = cursor.lastrowid
        cursor.close()
        return transaction_id


def return_book(transaction_id):
    with db_session() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT transaction_id, book_id, status
            FROM transactions
            WHERE transaction_id = %s
            FOR UPDATE
            """,
            (transaction_id,),
        )
        transaction = cursor.fetchone()
        if transaction is None:
            raise LibraryError("Transaction ID nahi mila.")
        if transaction["status"] == "returned":
            raise LibraryError("Ye book pehle hi return ho chuki hai.")

        cursor.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE book_id = %s",
            (transaction["book_id"],),
        )
        cursor.execute(
            """
            UPDATE transactions
            SET return_date = CURDATE(), status = 'returned'
            WHERE transaction_id = %s
            """,
            (transaction_id,),
        )
        cursor.close()


def list_active_loans():
    with db_session() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                t.transaction_id,
                b.book_name,
                s.student_name,
                s.student_branch,
                t.issue_date
            FROM transactions AS t
            JOIN books AS b ON b.book_id = t.book_id
            JOIN students AS s ON s.student_id = t.student_id
            WHERE t.status = 'issued'
            ORDER BY t.issue_date, t.transaction_id
            """
        )
        loans = cursor.fetchall()
        cursor.close()
        return loans
