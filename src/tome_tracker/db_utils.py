import psycopg
from dotenv import load_dotenv
import datetime

load_dotenv()

def create_books_table(db_name: str):
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
                unread BOOLEAN,
                added DATE
            );
        """)

def add_book_to_db(db_name: str, book_info: dict, unread: bool):
    added = datetime.date.today()
    
    with psycopg.connect(f"dbname={db_name}") as conn:
        conn.execute("""
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
                unread,
                added
            )
        )
