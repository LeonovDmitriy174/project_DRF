from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Payment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailsSerializer(ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True, source='lesson_set')
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['name', 'img', 'description', 'lessons_count', 'lessons']


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
