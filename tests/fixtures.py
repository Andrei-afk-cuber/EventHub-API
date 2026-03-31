import pytest

# fixture for organizer
@pytest.fixture
def organizer_token(client, django_user_model):
    return get_token(client, django_user_model, True)

# fixture for default authenticated user
@pytest.fixture
def token(client, django_user_model):
    return get_token(client, django_user_model, False)

def get_token(client, django_user_model, is_organizer=False):
    username = 'test_user'
    password = '123'

    user = django_user_model.objects.create_user(
        username=username,
        password=password,
        email='',
        phone_number='+375268472847',
        date_of_birth='2006-01-26',
        is_organizer=is_organizer,
    )

    response = client.post(
        '/api/token/',
        data={
            'username': username,
            'password': password,
        },
        format='json'
    )

    return response.data['access'], user