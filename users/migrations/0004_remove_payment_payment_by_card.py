# Generated by Django 5.0.7 on 2024-08-02 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_payment_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="payment_by_card",
        ),
    ]
