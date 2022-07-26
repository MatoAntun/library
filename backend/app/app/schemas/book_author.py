from typing import List

from .author import AuthorInDB
from .book import BookInDB


class BookSchema(BookInDB):
    authors: List[AuthorInDB]


class AuthorSchema(AuthorInDB):
    books: List[BookInDB]
