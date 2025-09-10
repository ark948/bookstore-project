import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.CustomUser'
        django_get_or_create = ('email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)


class CustomEmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ('email', )

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = "employee"
    email = factory.Sequence(lambda n: 'employee%d@email.com' % n)


class CustomManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ('email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = "manager"
    email = factory.Sequence(lambda n: 'manager%d@email.com' % n)


class CustomAdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ('email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = "admin"
    email = factory.Sequence(lambda n: 'admin%d@email.com' % n)