from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['delete'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response(
                {"error": "You can only cancel your own bookings!"},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status == 'cancelled':
            return Response(
                {"error": "This booking is already cancelled!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        return Response(BookingSerializer(instance=booking).data, status=status.HTTP_200_OK)