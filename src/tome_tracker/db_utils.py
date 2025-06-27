import psycopg
from dotenv import load_dotenv
import datetime

load_dotenv()


def create_books_table(db_name: str):
    """Creates the `books` table in the passed database to store book info."""
    with psycopg.connect(f"dbname={db_name}") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id VARCHAR(20) PRIMARY KEY,
                etag VARCHAR(20),
                self_link TEXT,
                title TEXT,
                authors TEXT[],
                publisher TEXT,
                published_date DATE,
                description TEXT,
                page_count INT,
                categories TEXT[],
                language CHAR(2),
                isbn_10 CHAR(10),
                isbn_13 CHAR(13),
                thumbnail TEXT,
                read BOOLEAN,
                added DATE
            );
        """)


def add_book_to_db(db_name: str, book_info: dict, read: bool) -> bool:
    """
    Adds a single book to the `books` table of the passed database.
    If the book's `id` is already in the database, nothing happens.

    ### Args:
     - `db_name`: the name of the database with the `books` table.
     - `book_info`: a dictionary containing info on a single book.
     - `read`: a boolean flag tracking whether the book has been read.

    ### Returns:
    `True` if the book has been added to the database, `False` if it is already there.
    """
    added = datetime.date.today()

    if check_if_book_in_db(db_name, volume_id=book_info["id"]):
        return False

    with psycopg.connect(f"dbname={db_name}") as conn:
        conn.execute(
            """
            INSERT INTO books
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
            """,
            (
                book_info["id"],
                book_info["etag"],
                book_info["selfLink"],
                book_info["title"],
                book_info["authors"],
                book_info["publisher"],
                book_info["publishedDate"],
                book_info["description"],
                book_info["pageCount"],
                book_info["categories"],
                book_info["language"],
                book_info["isbn_10"],
                book_info["isbn_13"],
                book_info["thumbnail"],
                read,
                added,
            ),
        )
    return True


def check_if_book_in_db(
    db_name: str,
    volume_id: str | None = None,
    title: str | None = None,
    isbn: str | None = None,
) -> bool:
    """
    Checks if a given book is stored in the database.

    ### Args:
     - `db_name`: the name of the database with the `books` table.
     - `volume_id`: the id of the book to check.
     - `title`: the title of the book to check.
     - `isbn`: the ISBN of the book to check.

    ### Returns:
    `True` if the book is in the database, `False` otherwise.
    """
    with psycopg.connect(f"dbname={db_name}") as conn:
        if volume_id:
            response = conn.execute(
                """
                SELECT * FROM books
                WHERE id = %s
                """,
                (volume_id,),
            ).fetchall()
        if title:
            response = conn.execute(
                """
                SELECT * FROM books
                WHERE title = %s
                """,
                (title,),
            ).fetchall()
        if isbn:
            response = conn.execute(
                """
                SELECT * FROM books
                WHERE isbn_10 = %s OR isbn_13 = %s
                """,
                (isbn, isbn),
            ).fetchall()
    return len(response) > 0


def list_books_in_db(db_name: str, read_status: bool | None = None) -> list[str]:
    """
    Retrieves a list of book titles in the database.

    ### Args:
     - `db_name`: the name of the database with the `books` table.
     - `read_status`: whether the returned titles have been read or not. Defaults to `None`, which returns all titles.

    ### Returns:
    A list of book titles as strings.
    """
    with psycopg.connect(f"dbname={db_name}") as conn:
        response = conn.execute(
            """
            SELECT
                title
            FROM
                books
            WHERE
                read = COALESCE(%s, read)
            ORDER BY
                title ASC;
            """,
            (read_status,),
        ).fetchall()
    return [title[0] for title in response]


def delete_book_from_db(
    db_name: str, title: str | None = None, isbn: str | None = None
):
    """
    Deletes a single book from the database.
    If passed info doesn't match a stored book, or if neither `title` nor `isbn` are passed, does nothing.

    ### Args:
     - `db_name`: the name of the database with the `books` table.
     - `title`: the title of the book to delete.
     - `isbn`: either the ISBN 10 or ISBN 13 of the book to delete.

    ### Returns:
    `True` if the book has been deleted, `False` if it could not be found.
    """
    if title:
        if not check_if_book_in_db(db_name, title=title):
            return False
    if isbn:
        if not check_if_book_in_db(db_name, isbn=isbn):
            return False

    with psycopg.connect(f"dbname={db_name}") as conn:
        if title:
            conn.execute(
                """
                DELETE FROM
                    books
                WHERE
                    title = %s;
                """,
                (title,),
            )
        if isbn:
            conn.execute(
                """
                DELETE FROM
                    books
                WHERE
                    isbn_10 = %s OR isbn_13 = %s;
                """,
                (isbn, isbn),
            )
    return True


def update_book_in_db(db_name: str, title: str, toggle_read: bool):
    """
    Updates info on a single book in the database.

    ### Args:
     - `db_name`: the name of the database with the `books` table.
     - `title`: the title of the book to update.
     - `toggle_read`: if `True`, will flip a book's read status.

    ### Returns:
    `True` if the book has been updated, `False` if it could not be found.
    """
    if not check_if_book_in_db(db_name, title=title):
        return False

    if toggle_read:
        with psycopg.connect(f"dbname={db_name}") as conn:
            conn.execute(
                """
                UPDATE
                    books
                SET
                    read = NOT read
                WHERE
                    title = %s;
                """,
                (title,),
            )
    return True
