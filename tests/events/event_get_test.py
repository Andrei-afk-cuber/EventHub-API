import pytest

from tests.factories import EventFactory
from events.serializers import EventListSerializer


@pytest.mark.django_db
class TestEventGet:
    def test_events_list(self, client):
        events = EventFactory.create_batch(10)

        expected_data = {
            "count": 10,
            "next": None,
            "previous": None,
            "results": EventListSerializer(events, many=True).data
        }

        response = client.get(
            '/events/'
        )
        assert response.status_code == 200
        assert response.data == expected_data

    def test_event_retrieve(self, client, event):
        expected_data = {
            "id": event.id,
            "title": "Event title",
            "description": "Event description",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "location": "Location",
            "max_members": 20,
            "current_members": 19,
            "available_seats": 1,
            "price": 100,
            "organizer": event.organizer.id,
            "is_published": True
        }

        response = client.get(
            f'/events/{event.id}/'
        )
        assert response.status_code == 200
        assert response.data == expected_data