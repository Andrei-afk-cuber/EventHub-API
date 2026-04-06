from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer

@extend_schema_view(
    list=extend_schema(description='List all bookings', summary='List all bookings'),
    retrieve=extend_schema(description='Get detail of a booking', summary='Retrieve booking'),
    partial_update=extend_schema(description='Update a booking', summary='Update a booking'),
)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            return Booking.objects.filter(event__organizer=user)
        else:
            return Booking.objects.filter(user=user)

    @extend_schema(description='Cancel book', summary='Cancel book')
    @action(detail=True, methods=['patch'], url_path='cancel')
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