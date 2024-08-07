from django.contrib import admin

from materials.models import Lesson, Course, Payment, Subscription


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "course", "img", "url")
    search_fields = ("name", "description")
    list_filter = ("course",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "img")
    search_fields = ("name", "description")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "lesson",
        "amount",
        "date",
        "payment_by_card",
    )
    search_fields = ("course", "lesson")
    list_filter = ("user", "course", "lesson")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status")
    search_fields = ("course", "user")
    list_filter = ("user", "course")
