# Generated by Django 5.0.7 on 2024-08-03 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_payment_payment_by_card"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
