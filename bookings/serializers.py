from rest_framework import serializers

from .models import Booking

# serializer for creating booking
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['__all__']

    def validate(self, attrs):
        user = attrs.get('user')
        event = attrs.get('event')

        if user and event and user == event.organizer:
            raise serializers.ValidationError("Organizer cant create booking for own event")

        if user and event:
            active_bookings = Booking.objects.filter(
                user=user,
                event=event,
                status_in=['confirmed']
            )

            if active_bookings.exists():
                raise serializers.ValidationError("User already have booking on this event")