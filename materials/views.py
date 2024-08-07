from datetime import datetime, timezone

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from materials.models import Course, Lesson, Payment, Subscription
from materials.paginators import BasePagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailsSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
)
from materials.services import (
    create_stripe_prise,
    create_stripe_session,
    create_stripe_product,
)
from users.permissions import IsModerator, IsMyMaterials
from materials.tasks import send_update_course_mail


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailsSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [~IsModerator, IsMyMaterials]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModerator | IsMyMaterials]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save(last_update=datetime.now(timezone.utc))
        course_id = course.id
        send_update_course_mail.delay(course_id)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save(creator=self.request.user)
        courses = Course.objects.all().filter(pk=lesson.course_id)
        for course in courses:
            print(course)
            course.last_update = datetime.now(timezone.utc)
            course.save()


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

    def perform_update(self, serializer):
        lesson = serializer.save(last_update=datetime.now(timezone.utc))
        courses = Course.objects.all().filter(pk=lesson.course_id)
        for course in courses:
            course.last_update = datetime.now(timezone.utc)
            course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["date"]
    filterset_fields = ("course", "lesson", "payment_by_card")


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_prise(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.product_id = product_id
        payment.link = payment_link
        payment.session_id = session_id
        payment.save()


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
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        user = serializer.validated_data["user"]

        try:
            subscription = Subscription.objects.get(user=user, course=course)
        except Subscription.DoesNotExist:
            Subscription.objects.create(user=user, course=course)
            status_code = status.HTTP_201_CREATED
        else:
            subscription.delete()
            status_code = status.HTTP_204_NO_CONTENT

        return Response(status=status_code)
