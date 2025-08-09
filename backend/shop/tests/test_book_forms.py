import pytest

from accounts.tests.conftest import custom_employee
from shop.forms import NewBookForm

@pytest.mark.skip
@pytest.mark.django_db
def test_books_forms_new_book_form(client, custom_employee, book_obj):
    client.force_login(custom_employee)
    
    form_data = {
        'title': 'A new book',
        'authors': [book_obj['author'].pk],
        'publisher': book_obj['publication'].pk,
        'language': [book_obj['language'].pk],
        'original_language': [book_obj['language'].pk],
        'page_count': 200
    }

    form = NewBookForm(data=form_data)
    assert not form.is_valid()