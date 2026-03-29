from rest_framework import serializers

from .models import Booking

# default booking serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def validate(self, attrs):
        user = self.context['request'].user
        event = attrs.get('event')

        if user and event and user == event.organizer:
            raise serializers.ValidationError("Organizer can't create booking for own event")

        if user and event:
            active_bookings = Booking.objects.filter(
                user=user,
                event=event,
                status__in=['confirmed']
            )

            if active_bookings.exists():
                raise serializers.ValidationError("User already have booking on this event")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)