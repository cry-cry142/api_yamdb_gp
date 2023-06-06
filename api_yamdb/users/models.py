from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Roles(models.IntegerChoices):
        USER = 1, 'user'
        MODERATOR = 2, 'moderator'
        ADMIN = 3, 'admin'

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    role = models.IntegerField(
        verbose_name='Права доступа',
        choices=Roles.choices,
        default=Roles.USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    is_moderator = models.BooleanField(
        verbose_name='Пользователь является модератором',
        default=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.is_moderator = (self.role == self.Roles.MODERATOR)
        self.is_staff = (self.role == self.Roles.ADMIN)
        super().save(*args, **kwargs)
