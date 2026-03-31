from rest_framework import serializers

from events.models import Event, Review


# serializer for list
class EventListSerializer(serializers.ModelSerializer):
    free_seats = serializers.SerializerMethodField()
    organizer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Event
        fields = ('organizer', 'free_seats')

    def get_free_seats(self, obj):
        return obj.free_seats

# serializer for review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# serializer for retrieve
class EventRetrieveSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    available_seats = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'

    def get_available_seats(self, obj):
        count_of_bookings = obj.bookings.filter(status__in=['confirmed']).count()
        return obj.free_seats - count_of_bookings

# default serializer for event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'organizer')

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError()

        return attrs

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)