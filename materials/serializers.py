from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault,
)

from materials.models import Course, Lesson, Payment, Subscription
from materials.validators import UrlValidator


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="url")]


class CourseDetailsSerializer(ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True, source="lesson_set")
    lessons_count = SerializerMethodField()
    subscription = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    def get_subscription(self, instance):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return instance.subscription_set.filter(user=user).exists()

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = "__all__"
