from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
