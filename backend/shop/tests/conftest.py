import pytest

from shop.models import (
    Country, Language, Author, Publication, Book
)

@pytest.fixture
def country():
    us = Country.objects.create(name="United States")
    us.save()
    return us


@pytest.fixture
def language():
    en = Language.objects.create(name='English')
    en.save()
    return en


@pytest.fixture
def author(country):
    some_author = Author.objects.create(
        name = 'Some Guy',
        nationality = country
    )
    some_author.save()
    return some_author


@pytest.fixture
def publication(country):
    pub = Publication.objects.create(title="Nice Publication", country=country)
    pub.save()
    return pub


@pytest.fixture
def book(language, author, publication):
    book_obj = Book.objects.create(
        title = "The Good Book",
        language = language,
        publisher = publication,
        original_language = language,
        page_count = 200,
    )
    book_obj.authors.set([author])
    book_obj.save()
    return book_obj