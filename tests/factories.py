import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = 'test_password'
    phone_number = '+375292847284'
    date_of_birth = '2006-01-26'