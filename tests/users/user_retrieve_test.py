import pytest

@pytest.mark.django_db
def test_user_retrieve(client, user, token):
    expected_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_organizer': user.is_organizer,
        'email': user.email,
        'phone_number': user.phone_number,
        'date_of_birth': user.date_of_birth,
    }

    response = client.get(
        f'/users/{user.id}/',
        HTTP_AUTHORIZATION=f"Bearer " + token,
    )

    assert response.status_code == 200
    assert response.data == expected_data