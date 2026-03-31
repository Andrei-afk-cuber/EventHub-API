import factory
import random

from users.models import User
from events.models import Event, Review
from bookings.models import Booking


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = 'test_password'
    phone_number = factory.Sequence(lambda n: f'+37529{n:07d}')
    date_of_birth = '2006-01-26'

class OrganizerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = 'test_password'
    # phone_number = factory.Sequence(lambda n: f'+37529{n:07d}')
    phone_number = factory.Faker('numerify', text='+37529#######')
    date_of_birth = '2006-01-26'
    is_organizer = True

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Event title"
    description = "Event description"
    start_date = "2025-01-01"
    end_date = "2025-12-31"
    location = "Location"
    max_members = 20
    current_members = 19
    price = 100
    organizer = factory.SubFactory(OrganizerFactory)
    is_published = True

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
    date = "2025-01-02"
    status = "confirmed"
    number_of_seats = 1

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
    rating = 5.0
    text = "Review text"
    date = "2025-01-02"