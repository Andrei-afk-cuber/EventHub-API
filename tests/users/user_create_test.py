import pytest
from rest_framework.exceptions import ErrorDetail


# test for /users/create/
@pytest.mark.django_db
class TestCreateUser:
    def test_create_user(self, client):
        expected_data = {
            'id': 1,
            'username': 'new_test_user',
            'email': '',
            'phone_number': '+375292847284',
            'date_of_birth': '2006-01-26',
            'is_organizer': False
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

    def test_invalid_phone(self, client):
        expected_data = {'phone_number':
                             [ErrorDetail(string='Incorrect phone number, correct format: +375xxxxxxxxx', code='invalid')]
                         }

        response = client.post(
            '/users/create/',
            data={
                'username': 'new_test_user',
                'email': '',
                'phone_number': '+3752928472846',
                'date_of_birth': '2006-01-26',
                'password': 'test_password'
            },
            format='json'
        )
        assert response.status_code == 400
        assert response.data == expected_data