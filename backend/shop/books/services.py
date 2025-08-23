from django.db import transaction

from shop.models import Book


class BookService:
    @staticmethod
    @transaction.atomic
    def create_book(data: dict) -> Book:
        book = Book.objects.create(**data)
        return book