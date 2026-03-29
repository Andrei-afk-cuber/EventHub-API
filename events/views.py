from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from bookings.serializers import BookingSerializer
from .models import Event, Review
from .serializers import EventSerializer, ReviewSerializer, EventRetrieveSerializer


# Event viewset
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Override serializer getting
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventRetrieveSerializer
        else:
            return EventSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def get_all_reviews(self, request, pk=None):
        reviews = Review.objects.filter(event=pk).all()
        return Response(ReviewSerializer(instance=reviews, many=True).data)

    @action(detail=True, methods=['post'], url_path='book')
    def create_book(self, request, pk=None):
        data = request.data

        serializer = BookingSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Review view set
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]