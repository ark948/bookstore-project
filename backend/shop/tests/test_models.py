import pytest

from shop.models import *


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_country_fixture(country):
    print(country)
    print(country.pk)
    print(country.name)


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_langauge_fixtre(language):
    print(language)
    print(language.pk)
    print(language.name)


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_author_fixture(author):
    print(author.pk)
    print(author.name)
    print(author.nationality)


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_publication_fixture(publication):
    print(publication.pk)
    print(publication.title)
    print(publication.country)


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_book_fixture(book):
    print(book.pk)
    print(book.title)
    print(book.authors.all())


@pytest.mark.django_db
def test_book_author_relationship(author, book):
    assert book.authors.all()[0] == author
    assert book.authors.all()[0].pk == author.pk
    assert book.authors.all()[0].name == author.name


@pytest.mark.django_db
def test_author_books_count(author, book):
    assert author.books_count == 1


@pytest.mark.django_db
def test_author_book_relationship(author, book):
    assert author.books.all()[0] == book
    assert author.books.all()[0].pk == book.pk
    assert author.books.all()[0].title == book.title