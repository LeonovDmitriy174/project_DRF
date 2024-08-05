from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, get_object_or_404)

from materials.models import Course, Lesson, Payment, Subscription
from materials.paginators import BasePagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailsSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
)
from users.models import User
from users.permissions import IsModerator, IsMyMaterials


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailsSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModerator,
                IsMyMaterials,
            )
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsMyMaterials,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = BasePagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["date"]
    filterset_fields = ("course", "lesson", "payment_by_card")


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(
            data=request.data, context={'request': request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            user = self.request.user
            course_id = self.request.data.get("course")
            course = get_object_or_404(Course, pk=course_id)
        else:
            course = serializer.validated_data['course']
            user = serializer.validated_data['user']
        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Subscription.objects.create(user=user, course=course)
            return Response(status=status.HTTP_201_CREATED)
