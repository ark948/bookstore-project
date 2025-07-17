import pytest

from shop.models import *


@pytest.mark.django_db
def test_country_fixture(country):
    assert isinstance(country, Country) == True
    assert country.pk == 1
    assert country.name == "United States"


@pytest.mark.django_db
def test_langauge_fixtre(language):
    assert isinstance(language, Language) == True
    assert language.pk == 1
    assert language.name == "English"


@pytest.mark.django_db
def test_author_fixture(author):
    assert isinstance(author, Author) == True
    assert author.en_name == "Some Guy"
    assert author.nationality.pk == 1


@pytest.mark.django_db
def test_publication_fixture(publication):
    assert publication.pk == 1
    assert publication.title == "Nice Publication"
    assert publication.country.pk == 1


@pytest.mark.django_db
def test_book_fixture(author, book):
    assert book.pk == 1
    assert book.title == "The Good Book"
    assert list(book.authors.all()) == [author]


@pytest.mark.django_db
def test_book_author_relationship(author, book):
    assert book.authors.all()[0] == author
    assert book.authors.all()[0].pk == author.pk
    assert book.authors.all()[0].en_name == author.en_name


@pytest.mark.django_db
def test_author_books_count(author, book):
    assert author.books_count == 1


@pytest.mark.django_db
def test_author_book_relationship(author, book):
    assert author.books.all()[0] == book
    assert author.books.all()[0].pk == book.pk
    assert author.books.all()[0].title == book.title