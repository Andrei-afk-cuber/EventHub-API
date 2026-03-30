from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bookings.serializers import BookingSerializer
from .models import Event, Review
from .serializers import EventSerializer, ReviewSerializer, EventRetrieveSerializer
from .permissions import IsOrganizerOrReadOnly

# Event viewset
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    ALLOWED_ORDERING_FIELDS = ['start_date', '-start_date','end_date', '-end_date', 'price', '-price']

    # override list action
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # filters
        queryset = self._apply_filters(request, queryset)

        # ordering
        queryset = self._apply_ordering(request, queryset)

        return Response(EventSerializer(queryset, many=True).data)

    def _apply_ordering(self, request, queryset):
        ordering = request.GET.get('ordering', None)

        if ordering and ordering in self.ALLOWED_ORDERING_FIELDS:
            queryset = queryset.order_by(ordering)

        return queryset

    def _apply_filters(self, request, queryset):
        date_from, date_to = request.GET.get('date_from', None), request.GET.get('date_to', None)
        organizer = request.GET.get('organizer', None)
        price_min, price_max = request.GET.get('price_min', None), request.GET.get('price_max', None)
        search = request.GET.get('search', None)

        # filters
        if date_from:
            queryset = queryset.filter(start_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(end_date__lte=date_to)
        if organizer:
            queryset = queryset.filter(organizer=organizer)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    # Override serializer getting
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventRetrieveSerializer
        else:
            return EventSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        reviews = Review.objects.filter(event=pk)
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