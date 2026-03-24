from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, date_of_birth, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        user = self.model(username=username, date_of_birth=date_of_birth, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, date_of_birth='2000-12-12', phone_number='+375255555555', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.model(username=username, date_of_birth=date_of_birth, phone_number=phone_number,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

# validator for user phone number
def validate_phone_number(phone_number):
    if not phone_number.startswith('+375') or len(phone_number) != 13:
        raise ValidationError('Incorrect phone number, correct format: +375xxxxxxxxx')

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=16, unique=True, validators=[validate_phone_number])
    date_of_birth = models.DateField()
    is_organizer = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'