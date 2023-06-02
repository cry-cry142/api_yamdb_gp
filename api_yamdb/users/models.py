from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\z')],
    )
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


    def __str__(self):
        return self.username

    def has_moderator_access(self):
        '''Возвращает True, если права доступа не ниже модератора.'''
        return self.role >= self.MODERATOR

    def is_admin(self):
        '''Возвращает True, если права доступа соответствуют администратору.'''
        return self.role == self.ADMIN
