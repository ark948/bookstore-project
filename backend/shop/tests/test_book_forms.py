import pytest

from accounts.tests.conftest import user, custom_user, custom_employee
from shop.forms import NewBookForm


@pytest.mark.django_db
def test_books_forms_new_book_form(client, custom_employee, author, publication, language):
    client.force_login(custom_employee)
    
    form_data = {
        'title': 'A new book',
        'authors': [author.pk],
        'publisher': publication.pk,
        'language': [language.pk],
        'original_language': [language.pk],
        'page_count': 200
    }

    form = NewBookForm(data=form_data)
    assert not form.is_valid()