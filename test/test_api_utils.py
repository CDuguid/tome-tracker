from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from src.tome_tracker.api_utils import (
    NoMatchingISBN,
    clean_book_info,
    get_book_by_volume_id,
    get_volume_id_by_isbn,
)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (
        args[0] == "https://www.googleapis.com/books/v1/volumes?q=isbn:9780575094147"
        or args[0] == "https://www.googleapis.com/books/v1/volumes?q=isbn:0575094141"
    ):
        json_data = {
            "totalItems": 1,
            "items": [
                {
                    "id": "qm2PPwAACAAJ",
                    "etag": "lElKHnQtAF4",
                    "selfLink": "https://www.googleapis.com/books/v1/volumes/qm2PPwAACAAJ",
                    "title": "The Forever War",
                    "authors": ["Joe Haldeman"],
                    "publisher": "Gollancz",
                    "publishedDate": "2010",
                    "description": "Private William Mandella is a hero in spite of himself--a reluctant conscript drafted into an elite military unit. He never wanted to go to war, but the leaders on Earth have drawn a line in the interstellar sand--despite the fact that their fierce alien enemy is unknowable, unconquerable, and very far away.",
                    "pageCount": 240,
                    "categories": [
                        "Fiction / General",
                        "Fiction / Classics",
                        "Fiction / Science Fiction / General",
                        "Fiction / Science Fiction / Hard Science Fiction",
                        "Fiction / Science Fiction / Space Opera",
                        "Fiction / Science Fiction / Military",
                        "Fiction / War & Military",
                    ],
                    "language": "en",
                    "isbn_10": "0575094141",
                    "isbn_13": "9780575094147",
                    "thumbnail": "http://books.google.com/books/content?id=qm2PPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70DYYMJU5XLUXS4f5ELvN5Yf-JF9Wfz5Hk6YvwbqNH4nhkpwAHRj_nVGWU93cpd5jUFVJDLd-H3ZYZW7FFmkz1-EcXOvsQlWv11GN0kzNX_oVp-QPVQ8nsi3k4HbWcvtN8fJ8xw&source=gbs_api",
                }
            ],
        }
        return MockResponse(json_data, 200)

    elif args[0] == "https://www.googleapis.com/books/v1/volumes?q=isbn:1234":
        return MockResponse({"totalItems": 0}, 200)

    elif args[0] == "https://www.googleapis.com/books/v1/volumes/qm2PPwAACAAJ":
        json_data = {
            "id": "qm2PPwAACAAJ",
            "etag": "eac0++rKPDY",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/qm2PPwAACAAJ",
            "volumeInfo": {
                "title": "The Forever War",
                "authors": ["Joe Haldeman"],
                "publisher": "Gollancz",
                "publishedDate": "2010",
                "description": "Private William Mandella is a hero in spite of himself--a reluctant conscript drafted into an elite military unit. He never wanted to go to war, but the leaders on Earth have drawn a line in the interstellar sand--despite the fact that their fierce alien enemy is unknowable, unconquerable, and very far away.",
                "industryIdentifiers": [
                    {"type": "ISBN_10", "identifier": "0575094141"},
                    {"type": "ISBN_13", "identifier": "9780575094147"},
                ],
                "pageCount": 240,
                "categories": [
                    "Fiction / General",
                    "Fiction / Classics",
                    "Fiction / Science Fiction / General",
                    "Fiction / Science Fiction / Hard Science Fiction",
                    "Fiction / Science Fiction / Space Opera",
                    "Fiction / Science Fiction / Military",
                    "Fiction / War & Military",
                ],
                "imageLinks": {
                    "thumbnail": "http://books.google.com/books/content?id=qm2PPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70agrzo1pLnXftR46paX3AvP0CXWYLkk4W4bWfewsI3ela9zDq16pqZXkvnrGmJuBJ91X1DHE89n4WHPY7huUMzOLHA3arBUs68hxEx3v1OWJCOLxB97AnsTemfHABmOP30CmB8&source=gbs_api"
                },
                "language": "en",
            },
        }
        return MockResponse(json_data, 200)

    elif args[0] == "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ":
        json_data = {
            "id": "pMyoPwAACAAJ",
            "etag": "WmUhbbR1UHg",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
            "volumeInfo": {
                "title": "Meditations",
                "publishedDate": "2004",
                "description": "A new translation of one of the most important texts of Western philosophy.",
                "industryIdentifiers": [
                    {"type": "ISBN_10", "identifier": "0753820161"},
                    {"type": "ISBN_13", "identifier": "9780753820162"},
                ],
                "pageCount": 200,
                "imageLinks": {
                    "thumbnail": "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api"
                },
                "language": "en",
            },
        }
        return MockResponse(json_data, 200)

    return MockResponse(None, 404)


@patch("src.tome_tracker.api_utils.requests.get", side_effect=mocked_requests_get)
class TestGetVolumeIdByISBN:
    def test_returns_volume_id_given_correct_isbn_13(self, mock_request):
        forever_war_isbn = "9780575094147"
        forever_war_id = "qm2PPwAACAAJ"
        assert get_volume_id_by_isbn(forever_war_isbn) == forever_war_id

    def test_returns_volume_id_given_correct_isbn_10(self, mock_request):
        forever_war_isbn = "0575094141"
        forever_war_id = "qm2PPwAACAAJ"
        assert get_volume_id_by_isbn(forever_war_isbn) == forever_war_id

    def test_raises_http_error_on_a_bad_request(self, mock_request):
        with pytest.raises(HTTPError):
            get_volume_id_by_isbn("network_failure")

    def test_raises_no_matching_isbn_error_given_incorrect_isbn(self, mock_request):
        with pytest.raises(NoMatchingISBN):
            get_volume_id_by_isbn("1234")


@patch("src.tome_tracker.api_utils.requests.get", side_effect=mocked_requests_get)
class TestGetBookByVolumeId:
    def test_returns_correctly_formatted_dictionary_given_volume_id(self, mock_request):
        expected = {
            "id": "qm2PPwAACAAJ",
            "etag": "eac0++rKPDY",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/qm2PPwAACAAJ",
            "title": "The Forever War",
            "authors": ["Joe Haldeman"],
            "publisher": "Gollancz",
            "publishedDate": "2010-01-01",
            "description": "Private William Mandella is a hero in spite of himself--a reluctant conscript drafted into an elite military unit. He never wanted to go to war, but the leaders on Earth have drawn a line in the interstellar sand--despite the fact that their fierce alien enemy is unknowable, unconquerable, and very far away.",
            "pageCount": 240,
            "categories": [
                "Fiction / General",
                "Fiction / Classics",
                "Fiction / Science Fiction / General",
                "Fiction / Science Fiction / Hard Science Fiction",
                "Fiction / Science Fiction / Space Opera",
                "Fiction / Science Fiction / Military",
                "Fiction / War & Military",
            ],
            "language": "en",
            "isbn_10": "0575094141",
            "isbn_13": "9780575094147",
            "thumbnail": "http://books.google.com/books/content?id=qm2PPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70agrzo1pLnXftR46paX3AvP0CXWYLkk4W4bWfewsI3ela9zDq16pqZXkvnrGmJuBJ91X1DHE89n4WHPY7huUMzOLHA3arBUs68hxEx3v1OWJCOLxB97AnsTemfHABmOP30CmB8&source=gbs_api",
        }
        assert get_book_by_volume_id("qm2PPwAACAAJ") == expected

    def test_raises_http_error_on_a_bad_request(self, mock_request):
        with pytest.raises(HTTPError):
            get_book_by_volume_id("network_failure")

    def test_handles_missing_book_info(self, mock_request):
        expected = {
            "id": "pMyoPwAACAAJ",
            "etag": "WmUhbbR1UHg",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/pMyoPwAACAAJ",
            "title": "Meditations",
            "authors": [],
            "publisher": None,
            "publishedDate": "2004-01-01",
            "description": "A new translation of one of the most important texts of Western philosophy.",
            "pageCount": 200,
            "categories": [],
            "language": "en",
            "isbn_10": "0753820161",
            "isbn_13": "9780753820162",
            "thumbnail": "http://books.google.com/books/content?id=pMyoPwAACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70wIuIPNQ8IJVGr-Er8MuUwDiPJE4xvb1UtvG3CZPDojWA3H05h1OnRPYbFjglMyKYHMc3_wEZ0EDgstcqmXUI9EjstHgvcCrcGLCjCVpcRpuNsDyuMRAbsQSQ5PopjBnrvLVW7&source=gbs_api",
        }
        assert get_book_by_volume_id("pMyoPwAACAAJ") == expected


class TestCleanBookInfo:
    def test_returns_dict_unchanged_given_full_date_info(self):
        book_info = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1789-07-14",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        assert clean_book_info(book_info) == book_info

    def test_adds_missing_day_value_to_published_date(self):
        book_info = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-06",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        expected = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-06-01",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        assert clean_book_info(book_info) == expected

    def test_adds_missing_month_and_day_value_to_published_date(self):
        book_info = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1862",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        expected = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1862-01-01",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        assert clean_book_info(book_info) == expected

    def test_handles_single_digit_month_and_day_values(self):
        single_month_book = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-7-08",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        single_day_book = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-07-8",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        single_month_and_day_book = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-7-8",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        expected = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": "1815-07-08",
            "thumbnail": None,
            "authors": ["Napoleon Bonaparte"],
        }
        assert (
            clean_book_info(single_month_book)
            == clean_book_info(single_day_book)
            == clean_book_info(single_month_and_day_book)
            == expected
        )

    def test_handles_date_value_being_none(self):
        book_info = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": None,
            "thumbnail": None,
            "authors": [],
        }
        assert clean_book_info(book_info) == book_info

    def test_capitalises_author_names(self):
        book_info = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": None,
            "authors": [
                "jane doe",
                "David Z. ALBERT",
            ],
        }
        expected = {
            "id": "abc",
            "title": "Test Book",
            "publishedDate": None,
            "authors": ["Jane Doe", "David Z. Albert"],
        }
        assert clean_book_info(book_info) == expected
