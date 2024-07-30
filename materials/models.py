from django.db import models


class Course(models.Model):
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
