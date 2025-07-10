from django.db import models

from .models import Author

class AuthorQuerySet(models.QuerySet):
    pass

class AuthorModelManager(models.Manager):
    pass