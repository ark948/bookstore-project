import factory
from datetime import datetime


from .models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.CustomUser'
        django_get_or_create = ('email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)