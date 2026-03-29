from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# event model
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    max_members = models.IntegerField()
    current_members = models.IntegerField(default=0)
    price = models.FloatField()
    organizer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_published = models.BooleanField()

    # count of free seats
    @property
    def free_seats(self):
        return self.max_members - self.current_members

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be earlier than end date.')

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title

# review model
class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    text = models.TextField(null=False)
    date = models.DateField()

    # user check
    def clean(self):
        has_booking = self.event.bookings.filter(
            user=self.user,
            status__in=['confirmed']
        )

        if not has_booking:
            raise ValidationError('User dont have booking for this event.')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.user.username + " | " + self.event.title