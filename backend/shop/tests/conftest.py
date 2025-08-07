import pytest
import logging

from shop.models import (
    Country, Language, Author, Publication, Book, Genre
)

@pytest.fixture(autouse=True)
def disable_logging_for_forbidden_requests(caplog):
    logger = logging.getLogger('django.request')
    logger.setLevel(logging.CRITICAL)
    yield
    logger.setLevel(logging.WARNING)


@pytest.fixture
def book_obj():
    country = Country.objects.create(name="United States")
    language = Language.objects.create(name="English")
    author = Author.objects.create(en_name="Some Dude", nationality=country)
    publication = Publication.objects.create(title="Good Books Publications", country=country)
    genre = Genre.objects.create(title="Drama")
    book = Book.objects.create(
        title = "One Good Book",
        publisher = publication,
        language = language,
        original_language = language,
        page_count = 200,
    )
    book.authors.set([author])
    book.genres.set([genre])
    obj = {
        'country': country,
        'language': language,
        'author': author,
        'publication': publication,
        'genre': genre,
        'book': book
    }

    return obj