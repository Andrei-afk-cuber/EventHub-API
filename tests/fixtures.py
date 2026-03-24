import pytest

# fixture for token getting
@pytest.fixture
def token(client, django_user_model):
    username = 'test_user'
    password = '123'

    django_user_model.objects.create_user(
        username=username,
        password=password,
        email='',
        phone_number='+375268472847',
        date_of_birth='2006-01-26'
    )

    response = client.post(
        '/api/token/',
        data={
            'username': username,
            'password': password,
        },
        format='json'
    )

    return response.data['access']