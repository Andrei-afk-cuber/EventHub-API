import pytest


@pytest.mark.django_db
class TestEventCreate:
    data = {
        "title": "Event title",
        "description": "Event description",
        "start_date": "2021-01-10",
        "end_date": "2021-01-20",
        "location": "Location",
        "max_members": 20,
        "current_members": 19,
        "price": 100,
        "is_published": True
    }

    def test_correct_create(self, client, organizer_token):
        expected_data = {
            "id": 1,
            "title": "Event title",
            "description": "Event description",
            "start_date": "2021-01-10",
            "end_date": "2021-01-20",
            "location": "Location",
            "max_members": 20,
            "current_members": 19,
            "price": 100,
            "is_published": True
        }

        response = client.post(
            '/events/',
            data = self.data,
            HTTP_AUTHORIZATION = f'Bearer {organizer_token[0]}',
            format = 'json'
        )
        expected_data['organizer'] = response.data['organizer']
        expected_data['id'] = response.data['id']

        assert response.status_code == 201
        assert response.data == expected_data

    def test_incorrect_create(self, client, organizer_token):
        incorrect_data = self.data.copy()
        incorrect_data['start_date'], incorrect_data['end_date'] = incorrect_data['end_date'], incorrect_data['start_date']

        response = client.post(
            '/events/',
            data=incorrect_data,
            HTTP_AUTHORIZATION=f'Bearer {organizer_token[0]}',
            format='json'
        )

        assert response.status_code == 400

    def test_not_organizer_create(self, client, token):
        response = client.post(
            '/events/',
            data={
                "title": "Event title",
                "description": "Event description",
                "end_date": "2021-01-10",
                "start_date": "2021-01-20",
                "location": "Location",
                "max_members": 20,
                "current_members": 19,
                "price": 100,
                "is_published": True
            },
            HTTP_AUTHORIZATION=f'Bearer {token[0]}',
            format='json'
        )

        assert response.status_code == 403