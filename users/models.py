from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="введите почту", max_length=255
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    phone = PhoneNumberField(
        verbose_name="телефон", help_text="введите телефон", blank=True, null=True
    )
    city = models.CharField(
        max_length=255,
        verbose_name="город",
        help_text="введите город",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
