from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )  # Переопределение поля email, чтобы оно было уникальным для каждого пользователя

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )  # Проверка валидности номера
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )  # Поле с номером телефона пользователя
    is_owner = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.email)
