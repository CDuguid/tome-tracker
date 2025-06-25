from src.tome_tracker.db_utils import create_books_table, add_book_to_db
import psycopg
import pytest
import datetime

@pytest.fixture(autouse=True)
def clean_test_db():
    with psycopg.connect("dbname=test_tome_tracker") as conn:
        conn.execute("""
            DROP TABLE IF EXISTS books;
        """)

@pytest.fixture
def meditations_info():
    return {
        "id": "pMyoPwAACAAJ",
        "etag": "WmUhbbR1UHg",
        "selfLink": "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
        "title": "Meditations",
        "authors": [
            "Marcus Aurelius"
        ],
        "publisher": "Phoenix",
        "publishedDate": "2004-01-01",
        "description": "A new translation of one of the most important texts of Western philosophy.",
        "pageCount": 200,
        "categories": None,
        "language": "en",
        "isbn_10": "0753820161",
        "isbn_13": "9780753820162",
        "thumbnail": "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api"
    }


class TestCreateBooksTable:
    
    def test_creates_table_with_correct_name_and_columns(self):
        create_books_table("test_tome_tracker")
        with psycopg.connect("dbname=test_tome_tracker") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        *
                    FROM
                        books;
                """)
                actual_columns = [col.name for col in cur.description]
        expected_columns = [
            "id",
            "etag",
            "self_link",
            "title",
            "authors",
            "publisher",
            "published_date",
            "description",
            "page_count",
            "categories",
            "language",
            "isbn_10",
            "isbn_13",
            "thumbnail",
            "unread",
            "added"
        ]
        assert actual_columns == expected_columns


class TestAddBookToDB:
    
    def test_adds_a_book_to_the_database(self, meditations_info):
        create_books_table("test_tome_tracker")
        add_book_to_db("test_tome_tracker", meditations_info, True)
        
        with psycopg.connect("dbname=test_tome_tracker") as conn:
            table_rows = conn.execute("""
                SELECT * FROM books;
                """).fetchall()
        
        expected = [(
            "pMyoPwAACAAJ",
            "WmUhbbR1UHg",
            "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
            "Meditations",
            ["Marcus Aurelius"],
            "Phoenix",
            datetime.date(2004, 1, 1),
            "A new translation of one of the most important texts of Western philosophy.",
            200,
            None,
            "en",
            "0753820161",
            "9780753820162",
            "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api",
            True,
            datetime.date.today()
        )]
        assert table_rows == expected

    @pytest.mark.skip(reason="need to implement checking for which books are in db first -- duplicate id on primary key")
    def test_does_not_duplicate_books_already_in_database(self, meditations_info):
        create_books_table("test_tome_tracker")
        add_book_to_db("test_tome_tracker", meditations_info, True)
        add_book_to_db("test_tome_tracker", meditations_info, False)
        
        with psycopg.connect("dbname=test_tome_tracker") as conn:
            table_rows = conn.execute("""
                SELECT * FROM books;
                """).fetchall()
        
        expected = [(
            "pMyoPwAACAAJ",
            "WmUhbbR1UHg",
            "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
            "Meditations",
            ["Marcus Aurelius"],
            "Phoenix",
            datetime.date(2004, 1, 1),
            "A new translation of one of the most important texts of Western philosophy.",
            200,
            None,
            "en",
            "0753820161",
            "9780753820162",
            "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api",
            True,
            datetime.date.today()
        )]
        assert table_rows == expected
