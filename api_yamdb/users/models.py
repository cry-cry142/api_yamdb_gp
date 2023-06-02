from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Класс пользователя.'''
    USER = 1
    MODERATOR = 2
    ADMIN = 3
    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    password = None
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    role = models.IntegerField(
        verbose_name='Права доступа',
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.is_staff = (self.role == self.ADMIN)
        super().save(*args, **kwargs)

    def has_moderator_access(self):
        '''Возвращает True, если права доступа не ниже модератора.'''
        return self.role >= self.MODERATOR

    def is_admin(self):
        '''Возвращает True, если права доступа соответствуют администратору.'''
        return self.role == self.ADMIN
