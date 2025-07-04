import datetime

import psycopg
import pytest

from src.tome_tracker.db_utils import (
    add_book_to_db,
    check_if_book_in_db,
    create_books_table,
    delete_book_from_db,
    list_books_in_db,
    update_book_in_db,
)

DBNAME = "test_tome_tracker"

MEDITATIONS_INFO = {
    "id": "pMyoPwAACAAJ",
    "etag": "WmUhbbR1UHg",
    "selfLink": "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
    "title": "Meditations",
    "authors": ["Marcus Aurelius"],
    "publisher": "Phoenix",
    "publishedDate": "2004-01-01",
    "description": "A new translation of one of the most important texts of Western philosophy.",
    "pageCount": 200,
    "categories": None,
    "language": "en",
    "isbn_10": "0753820161",
    "isbn_13": "9780753820162",
    "thumbnail": "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api",
}

CIRCE_INFO = {
    "id": "d6kyEAAAQBAJ",
    "etag": "hsBy3rTbPTA",
    "selfLink": "https://www.googleapis.com/books/v1/volumes/d6kyEAAAQBAJ",
    "title": "Circe",
    "authors": ["Madeline Miller"],
    "publisher": "Bloomsbury Publishing",
    "publishedDate": "2019-01-01",
    "description": '<b>"A bold and subversive retelling of the goddess\'s story," this #1 <i>New York Times</i> bestseller is "both epic and intimate in its scope, recasting the most infamous female figure from the Odyssey as a hero in her own right" (Alexandra Alter, <i>The New York Times</i>).</b> <p> In the house of Helios, god of the sun and mightiest of the Titans, a daughter is born. But Circe is a strange child -- not powerful, like her father, nor viciously alluring like her mother. Turning to the world of mortals for companionship, she discovers that she does possess power -- the power of witchcraft, which can transform rivals into monsters and menace the gods themselves. <p> Threatened, Zeus banishes her to a deserted island, where she hones her occult craft, tames wild beasts and crosses paths with many of the most famous figures in all of mythology, including the Minotaur, Daedalus and his doomed son Icarus, the murderous Medea, and, of course, wily Odysseus. <p> But there is danger, too, for a woman who stands alone, and Circe unwittingly draws the wrath of both men and gods, ultimately finding herself pitted against one of the most terrifying and vengeful of the Olympians. To protect what she loves most, Circe must summon all her strength and choose, once and for all, whether she belongs with the gods she is born from, or the mortals she has come to love. <p> With unforgettably vivid characters, mesmerizing language, and page-turning suspense, Circe is a triumph of storytelling, an intoxicating epic of family rivalry, palace intrigue, love and loss, as well as a celebration of indomitable female strength in a man\'s world. <p><b>#1 <i>New York Times</i> Bestseller -- named one of the Best Books of the Year by NPR, the <i>Washington Post</i>, <i>People</i>, <i>Time</i>, Amazon, <i>Entertainment Weekly</i>, <i>Bustle<i>, <i>Newsweek</i>, the A.V. Club, <i>Christian Science Monitor</i>, <i>Refinery 29</i>, Buzzfeed, Paste, Audible, <i>Kirkus</i>, <i>Publishers Weekly</i>, Thrillist, NYPL, <i>Self</i>, <i>Real Simple</i>, Goodreads, <i>Boston Globe</i>, Electric Literature, BookPage, <i>the Guardian</i>, Book Riot, <i>Seattle Times</i>, and <i>Business Insider</i>.</b>',
    "pageCount": 336,
    "categories": [
        "Fiction / General",
        "Fiction / Fantasy / General",
        "Fiction / Fantasy / Epic",
        "Fiction / Fantasy / Historical",
        "Fiction / Fairy Tales, Folk Tales, Legends & Mythology",
        "Fiction / Historical / General",
        "Fiction / Historical / Ancient",
        "Fiction / Literary",
        "Fiction / Feminist",
    ],
    "language": "en",
    "isbn_10": "1408890046",
    "isbn_13": "9781408890042",
    "thumbnail": "http://books.google.com/books/publisher/content?id=d6kyEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73ccYINFvS7a-QJzZ4qrB099pJfw6YP6a4CikzGMzGvaICvuZlJeiViTKuZzIAe49cf8WVAU3i5gxfm8nlx9djaa_Lv-Ly-oo5aUZp_SOPVuSoohpBI-7xO6SGD_wm3LUG4ayUL&source=gbs_api",
}

TIME_AND_CHANCE_INFO = {
    "id": "lnlAnwEACAAJ",
    "etag": "mAkz3LO1yO8",
    "selfLink": "https://www.googleapis.com/books/v1/volumes/lnlAnwEACAAJ",
    "title": "Time and Chance",
    "authors": ["David Z. ALBERT"],
    "publisher": "Harvard University Press",
    "publishedDate": "2003-01-01",
    "description": "<p> This book is an attempt to get to the bottom of an acute and perennial tension between our best scientific pictures of the fundamental physical structure of the world and our everyday empirical experience of it. The trouble is about the direction of time. The situation (very briefly) is that it is a consequence of almost every one of those fundamental scientific pictures--and that it is at the same time radically at odds with our common sense--that whatever can happen can just as naturally happen backwards. </p><p> Albert provides an unprecedentedly clear, lively, and systematic new account--in the context of a Newtonian-Mechanical picture of the world--of the ultimate origins of the statistical regularities we see around us, of the temporal irreversibility of the Second Law of Thermodynamics, of the asymmetries in our epistemic access to the past and the future, and of our conviction that by acting now we can affect the future but not the past. Then, in the final section of the book, he generalizes the Newtonian picture to the quantum-mechanical case and (most interestingly) suggests a very deep potential connection between the problem of the direction of time and the quantum-mechanical measurement problem. <p> The book aims to be both an original contribution to the present scientific and philosophical understanding of these matters at the most advanced level, and something in the nature of an elementary textbook on the subject accessible to interested high-school students. </p><br><br>Table of Contents: <br><p> Preface </p><p> 1. Time-Reversal Invariance <br> 2. Thermodynamics <br> 3. Statistical Mechanics <br> 4. The Reversibility Objections and the Past-Hypothesis <br> 5. The Scope of Thermodynamics <br> 6. The Asymmetries of Knowledge and Intervention <br> 7. Quantum Mechanics <br> Appendix: Gedankenexperiments with Heat Engines </p><p> Index </p><br><br>Reviews of this book: <br>The foundations of statistical mechanisms are often presented in physics textbooks in a rather obscure and confused way. By challenging common ways of thinking about this subject, <i>Time and Chance</i> can do quite a lot to improve this situation.<br>--Jean Bricmont, Science<br><br>Albert is perfecting a style of foundational analysis that is uniquely his own...It has a surgical precision...and it is ruthless with pretensions. The foundations of thermodynamics is a topic that has accumulated a good deal of dead wood; this is a fire that will burn and burn.<br>--Simon W. Saunders, Oxford University<br><br>As usual with Albert's work, the exposition is brisk and to the point, and exceptionally clear...The book will be an extremely valuable contribution to the literature on the subject of philosophical issues in thermodynamics and statistical mechanics, a literature which has been thin on the ground but is now growing as it deserves to.<br>--Lawrence Sklar, University of Michigan",
    "pageCount": 192,
    "categories": [
        "Science / Philosophy & Social Aspects",
        "Science / Mechanics / Thermodynamics",
        "Science / Physics / Quantum Theory",
    ],
    "language": "en",
    "isbn_10": "0674011325",
    "isbn_13": "9780674011328",
    "thumbnail": "http://books.google.com/books/content?id=lnlAnwEACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE71B-YLU51M_7EeirZY85MtDvZBrsz6F70CpYVzTGjK581a5WnlFiakR6ZCHsKjNhniE2HaKc7pGdocS4sYxFyWlnUTlssrjIZeLbZfb4BowWIRfEK2R8J5UOxVjV8kM19C1ug4Y&source=gbs_api",
}


@pytest.fixture(autouse=True)
def clean_test_db():
    with psycopg.connect(f"dbname={DBNAME}") as conn:
        conn.execute("""
            DROP TABLE IF EXISTS books;
        """)


@pytest.fixture
def table_creation():
    create_books_table(DBNAME)


class TestCreateBooksTable:
    def test_creates_table_with_correct_name_and_columns(self):
        create_books_table(DBNAME)
        with psycopg.connect(f"dbname={DBNAME}") as conn:
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
            "read",
            "added",
        ]
        assert actual_columns == expected_columns


class TestAddBookToDB:
    def test_adds_a_book_to_the_database(self, table_creation):
        response = add_book_to_db(DBNAME, MEDITATIONS_INFO, True)

        with psycopg.connect(f"dbname={DBNAME}") as conn:
            table_rows = conn.execute("""
                SELECT * FROM books;
                """).fetchall()

        expected = [
            (
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
                datetime.date.today(),
            )
        ]
        assert table_rows == expected
        assert response

    def test_does_not_duplicate_books_already_in_database(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        response = add_book_to_db(DBNAME, MEDITATIONS_INFO, False)

        with psycopg.connect(f"dbname={DBNAME}") as conn:
            table_rows = conn.execute("""
                SELECT * FROM books;
                """).fetchall()

        expected = [
            (
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
                datetime.date.today(),
            )
        ]
        assert table_rows == expected
        assert not response


class TestListBooksInDB:
    def test_returns_list_of_all_book_titles_in_db(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        add_book_to_db(DBNAME, TIME_AND_CHANCE_INFO, False)
        expected = ["Circe", "Meditations", "Time and Chance"]
        actual = list_books_in_db(DBNAME)
        assert actual == expected

    def test_returns_list_of_all_read_books(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        add_book_to_db(DBNAME, TIME_AND_CHANCE_INFO, False)
        expected = ["Circe", "Meditations"]
        actual = list_books_in_db(DBNAME, True)
        assert actual == expected

    def test_returns_list_of_all_unread_books(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        add_book_to_db(DBNAME, TIME_AND_CHANCE_INFO, False)
        expected = ["Time and Chance"]
        actual = list_books_in_db(DBNAME, False)
        assert actual == expected


class TestCheckIfBookInDB:
    def test_returns_true_if_book_id_is_in_database(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        assert check_if_book_in_db(DBNAME, volume_id=MEDITATIONS_INFO["id"])

    def test_returns_false_if_book_id_is_not_in_database(self, table_creation):
        assert not check_if_book_in_db(DBNAME, volume_id=MEDITATIONS_INFO["id"])

    def test_returns_true_if_book_title_is_in_database(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        assert check_if_book_in_db(DBNAME, title=MEDITATIONS_INFO["title"])

    def test_returns_false_if_book_title_is_not_in_database(self, table_creation):
        assert not check_if_book_in_db(DBNAME, title=MEDITATIONS_INFO["title"])

    def test_returns_true_if_book_isbn_is_in_database(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        assert check_if_book_in_db(DBNAME, isbn=MEDITATIONS_INFO["isbn_10"])

    def test_returns_false_if_book_isbn_is_not_in_database(self, table_creation):
        assert not check_if_book_in_db(DBNAME, isbn=MEDITATIONS_INFO["isbn_10"])


class TestDeleteBookFromDB:
    def test_deletes_title_from_database_if_present(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        response = delete_book_from_db(DBNAME, title=MEDITATIONS_INFO["title"])
        remaining_books = list_books_in_db(DBNAME)
        assert len(remaining_books) == 0
        assert response

    def test_does_nothing_if_title_not_present(self, table_creation):
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        response = delete_book_from_db(DBNAME, title=MEDITATIONS_INFO["title"])
        remaining_books = list_books_in_db(DBNAME)
        assert len(remaining_books) == 1
        assert not response

    def test_deletes_isbn_from_database_if_present(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        delete_book_from_db(DBNAME, isbn=MEDITATIONS_INFO["isbn_10"])
        delete_book_from_db(DBNAME, isbn=CIRCE_INFO["isbn_13"])
        remaining_books = list_books_in_db(DBNAME)
        assert len(remaining_books) == 0

    def test_does_nothing_if_isbn_not_present(self, table_creation):
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        response_1 = delete_book_from_db(DBNAME, isbn=MEDITATIONS_INFO["isbn_10"])
        response_2 = delete_book_from_db(DBNAME, isbn=MEDITATIONS_INFO["isbn_13"])
        remaining_books = list_books_in_db(DBNAME)
        assert len(remaining_books) == 1
        assert not response_1
        assert not response_2


class TestUpdateBookInDB:
    def test_changes_an_unread_book_to_read(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, False)
        add_book_to_db(DBNAME, CIRCE_INFO, False)
        response = update_book_in_db(DBNAME, MEDITATIONS_INFO["title"], True)
        assert len(list_books_in_db(DBNAME, True)) == 1
        assert len(list_books_in_db(DBNAME, False)) == 1
        assert response

    def test_changes_a_read_book_to_unread(self, table_creation):
        add_book_to_db(DBNAME, MEDITATIONS_INFO, True)
        response = update_book_in_db(DBNAME, MEDITATIONS_INFO["title"], True)
        assert len(list_books_in_db(DBNAME, True)) == 0
        assert len(list_books_in_db(DBNAME, False)) == 1
        assert response

    def test_does_nothing_if_attempting_to_update_a_nonpresent_book(
        self, table_creation
    ):
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        response = update_book_in_db(DBNAME, MEDITATIONS_INFO["title"], True)
        assert len(list_books_in_db(DBNAME, True)) == 1
        assert len(list_books_in_db(DBNAME, False)) == 0
        assert not response

    @pytest.mark.skip(
        reason="current implementation toggles read status, rather than setting it to a specific value"
    )
    def test_does_nothing_if_attempting_to_set_read_status_to_current_value(
        self, table_creation
    ):
        add_book_to_db(DBNAME, CIRCE_INFO, True)
        update_book_in_db(DBNAME, MEDITATIONS_INFO["title"], True)
        assert len(list_books_in_db(DBNAME, True)) == 1
        assert len(list_books_in_db(DBNAME, False)) == 0
