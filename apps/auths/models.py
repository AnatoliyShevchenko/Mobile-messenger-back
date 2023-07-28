# Django
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

# Third-Party
from typing import Any


class ClientManager(BaseUserManager):
    """Manager for user model."""

    def create_user(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        phone_number: str,
        image: Any = None
    ) -> 'Client':
        """Create user."""

        user: 'Client' = self.model(
            email=self.normalize_email(email),
        )
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.image = image or None
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> 'Client':
        """Create admin."""

        user: 'Client' = self.model(
            email=self.normalize_email(email),
        )
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser, PermissionsMixin):
    """User model."""

    username = models.CharField(
        verbose_name='имя пользователя',
        unique=True,
        max_length=32,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=50,
        unique=True
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия'
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )
    friends = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list,
        verbose_name='список друзей'
    )
    image = models.ImageField(
        upload_to='users/images',
        null=True,
        blank=True,
        verbose_name='фото'
    )
    is_active = models.BooleanField(
        verbose_name='активный',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='менеджер',
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name='админ',
        default=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = ClientManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def save(
        self,
        *args: tuple,
        **kwargs: dict
    ) -> None:
        """Custom method for generate activation code."""

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.email} | {self.username} | {self.phone_number}'
    
    