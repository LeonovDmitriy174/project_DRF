from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


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


class Payment(models.Model):
    CARD = "card"
    CACHE = "cache"
    PAYMENT_BY_CARD = {
        CARD: "оплата по карте",
        CACHE: "оплата наличными"
    }
    payment_by_card = models.CharField(
        max_length=5,
        verbose_name="способ оплаты",
        help_text="введите способ оплаты",
        choices=PAYMENT_BY_CARD,
        default=CARD
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="пользователь",
        help_text="введите пользователя"
    )
    date = models.DateTimeField(
        verbose_name="дата оплаты",
        help_text="введите дату оплаты",
        auto_now_add=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET('Данного курса больше не существует'),
        verbose_name="оплаченный курс",
        help_text="введите оплаченный курс",
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET('Данного урока больше не существует'),
        verbose_name="оплаченный курс",
        help_text="введите оплаченный курс",
        null=True,
        blank=True
    )
    amount = models.IntegerField(
        verbose_name="сумма оплаты",
        help_text="введите сумму оплаты",
        null=True,
        blank=True
    )

    def is_upperclass(self):
        return self.payment_by_card in {self.CARD, self.CACHE}

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
