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