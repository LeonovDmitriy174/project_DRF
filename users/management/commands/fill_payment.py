import json
import os

from django.core.management import BaseCommand
from django.db import connection

from config.settings import BASE_DIR
from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    @staticmethod
    def json_read():
        with open(
            os.path.join(BASE_DIR, "fixtures", "payment.json"), encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
        return data

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE users_payment RESTART IDENTITY CASCADE;")

        Payment.objects.all().delete()

        payment = Command.json_read()

        for_create = []

        for i in payment:
            if i["model"] == "users.payment":
                fields = i.get("fields", {})
                user_id = fields.get("user")
                user = User.objects.get(pk=user_id)
                date = fields.get("date")
                amount = fields.get("amount")
                payment_by_card = fields.get("payment_by_card")

                course_tmp = fields.get("course")
                if type(course_tmp) is int:
                    course = Course.objects.get(pk=course_tmp)
                else:
                    course = fields.get("course")

                lesson_tmp = fields.get("lesson")
                if type(lesson_tmp) is int:
                    lesson = Lesson.objects.get(pk=lesson_tmp)
                else:
                    lesson = fields.get("lesson")

                for_create.append(
                    Payment(
                        user=user,
                        date=date,
                        course=course,
                        lesson=lesson,
                        amount=amount,
                        payment_by_card=payment_by_card,
                    )
                )

        Payment.objects.bulk_create(for_create)
