import pytest

# test for /users/create/
@pytest.mark.django_db
def test_create_user(client):
    expected_data = {
        'id': 1,
        'username': 'new_test_user',
        'email': '',
        'phone_number': '+375292847284',
        'date_of_birth': '2006-01-26'
    }

    response = client.post(
        '/users/create/',
        data = {
            'username': 'new_test_user',
            'email': '',
            'phone_number': '+375292847284',
            'date_of_birth': '2006-01-26',
            'password': 'test_password'
        },
        format='json'
    )

    assert response.status_code == 201
    assert response.data == expected_data