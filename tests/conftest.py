from pytest_factoryboy import register

from tests.factories import UserFactory, OrganizerFactory, EventFactory, BookingFactory, ReviewFactory


pytest_plugins = ['tests.fixtures']

register(UserFactory)
register(OrganizerFactory)
register(EventFactory)
register(BookingFactory)
register(ReviewFactory)