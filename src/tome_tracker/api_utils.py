import requests
from requests.exceptions import HTTPError


class NoMatchingISBN(Exception):
    pass


def get_volume_id_by_isbn(isbn: str) -> str:
    """
    Calls the Google Books API with the passed ISBN.
    If a single match is found, returns the volume id.
    If either no matches or multiple matches are found, raises a NoMatchingISBN exception.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url, timeout=3.05)
    if response.status_code == 200:
        response_body = response.json()
        if response_body["totalItems"] == 1:
            return response_body["items"][0]["id"]
        else:
            raise NoMatchingISBN()
        
    raise HTTPError(f"Non-success status code: {response.status_code}")



def get_book_by_volume_id(volume_id:str) -> dict:
    """
    Calls the Google Books API with the passed volume id.
    Returns desired info about the book as a dictionary.
    Should only be called after a volume id is confirmed to ensure a match is present.
    """
    url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"
    response = requests.get(url, timeout=3.05)
    if response.status_code == 200:
        response_body = response.json()

        # Need to handle keys in separate blocks due to different locations in the JSON
        # KeyErrors will occur if the response body is missing info
        book_info = {}
        keys = ["id", "etag", "selfLink"]
        volume_info_keys = ["title", "authors", "publisher", "publishedDate", "description", "pageCount", "categories", "language"]
        
        for key in keys:
            try:
                book_info[key] = response_body[key]
            except KeyError:
                book_info[key] = None
        
        for key in volume_info_keys:
            try:
                book_info[key] = response_body["volumeInfo"][key]
            except KeyError:
                book_info[key] = None

        try:
            book_info["isbn_10"] = None
            book_info["isbn_13"] = None
            
            for identifier in response_body["volumeInfo"]["industryIdentifiers"]:
                if identifier["type"] == "ISBN_10":
                    book_info["isbn_10"] = identifier["identifier"]
                elif identifier["type"] == "ISBN_13":
                    book_info["isbn_13"] = identifier["identifier"]
                # do I want to check for issn here?
        except KeyError:
            pass
        
        try:
            book_info["thumbnail"] = response_body["volumeInfo"]["imageLinks"]["thumbnail"]
        except KeyError:
            book_info["thumbnail"] = None
        
        return book_info
    
    raise HTTPError(f"Non-success status code: {response.status_code}")


if __name__ == "__main__":
    soul_music = "0552140295"
    meditations = "9780753820162"
    circe = "9781408890042"
    forever_war = "9780575094147"
    volume_id = get_volume_id_by_isbn(forever_war)
    print(volume_id)
    book_info = get_book_by_volume_id(volume_id)
    print(book_info)
    
