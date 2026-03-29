from django.db import models
from django.core.exceptions import ValidationError


# Booking class
class Booking(models.Model):
    # choices for status field
    STATUS_CHOICES = [
        ('canceled', 'отменено'),
        ('confirmed', 'подтверждено')
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, default='canceled', max_length=15)
    number_of_seats = models.IntegerField()

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return self.user.username + " | " + self.event.title

    def clean(self):
        if self.number_of_seats > self.event.free_seats:
            raise ValidationError(f"Incorrect number of seats. Free seats: {self.event.free_seats}")