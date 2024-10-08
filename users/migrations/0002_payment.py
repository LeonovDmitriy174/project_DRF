# Generated by Django 5.0.7 on 2024-08-01 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="введите дату оплаты",
                        verbose_name="дата оплаты",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        blank=True,
                        help_text="введите сумму оплаты",
                        null=True,
                        verbose_name="сумма оплаты",
                    ),
                ),
                (
                    "payment_by_card",
                    models.BooleanField(
                        default=False,
                        help_text="оплата была произведена картой?",
                        verbose_name="оплата картой",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        help_text="введите оплаченный курс",
                        null=True,
                        on_delete=models.SET("Данного курса больше не существует"),
                        to="materials.course",
                        verbose_name="оплаченный курс",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        blank=True,
                        help_text="введите оплаченный курс",
                        null=True,
                        on_delete=models.SET("Данного урока больше не существует"),
                        to="materials.lesson",
                        verbose_name="оплаченный курс",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="введите пользователя",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
        ),
    ]
