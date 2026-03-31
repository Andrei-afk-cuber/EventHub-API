import pytest

from tests.factories import BookingFactory, EventFactory, UserFactory
from bookings.serializers import BookingSerializer

@pytest.mark.django_db
class TestGetBooking:
    def test_list_bookings(self, client, token):
        # get user
        user = token[1]
        # create event
        event1 = EventFactory()
        # create booking by user
        booking_by_user = BookingFactory.create(event=event1, user=user)
        # create other bookings
        BookingFactory.create_batch(9)

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': BookingSerializer([booking_by_user, ], many=True).data
        }
        response = client.get(
            '/bookings/',
            HTTP_AUTHORIZATION=f'Bearer {token[0]}'
        )

        assert response.status_code == 200
        assert response.data == expected_data

    def test_retrieve_booking(self, client, token):
        token_string, user = token
        booking = BookingFactory(user=user)

        expected_data = {
            'id': booking.id,
            'user': booking.user.id,
            'event': booking.event.id,
            'date': booking.date,
            'status': booking.status,
            'number_of_seats': booking.number_of_seats,
        }

        response = client.get(
            f'/bookings/{booking.id}/',
            HTTP_AUTHORIZATION=f'Bearer {token_string}'
        )

        assert response.status_code == 200
        assert response.data == expected_data