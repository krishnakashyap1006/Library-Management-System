from db import db_session


def add_book(book_name, author, quantity):
    if not book_name.strip() or not author.strip():
        raise ValueError("Book name aur author required hain.")
    if quantity < 0:
        raise ValueError("Quantity negative nahi ho sakti.")

    with db_session() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO books (book_name, author, quantity)
            VALUES (%s, %s, %s)
            """,
            (book_name.strip(), author.strip(), quantity),
        )
        book_id = cursor.lastrowid
        cursor.close()
        return book_id


def list_books():
    with db_session() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT book_id, book_name, author, quantity
            FROM books
            ORDER BY book_id
            """
        )
        books = cursor.fetchall()
        cursor.close()
        return books
