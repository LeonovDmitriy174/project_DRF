from django.db import models

from config.settings import AUTH_USER_MODEL
from users.models import User


class Course(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        help_text="Введите создателя курса",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    img = models.ImageField(
        upload_to="materials/course",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Добавьте превью курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        help_text="Введите создателя урока",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Введите к какому курсу относится урок",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    img = models.ImageField(
        upload_to="materials/lesson",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Добавьте превью урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )
    url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ссылка на урок",
        help_text="Введите ссылку на урок",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    CARD = "card"
    CACHE = "cache"
    PAYMENT_BY_CARD = {CARD: "оплата по карте", CACHE: "оплата наличными"}
    payment_by_card = models.CharField(
        max_length=5,
        verbose_name="способ оплаты",
        help_text="введите способ оплаты",
        choices=PAYMENT_BY_CARD,
        default=CARD,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        help_text="введите пользователя",
    )
    date = models.DateTimeField(
        verbose_name="дата оплаты", help_text="введите дату оплаты", auto_now_add=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
        help_text="введите оплаченный курс",
        null=True,
        blank=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
        help_text="введите оплаченный курс",
        null=True,
        blank=True,
    )
    amount = models.IntegerField(
        verbose_name="сумма оплаты",
        help_text="введите сумму оплаты",
        null=True,
        blank=True,
    )

    def is_upperclass(self):
        return self.payment_by_card in {self.CARD, self.CACHE}

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        help_text="введите пользователя",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        help_text="введите курс",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
