from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, LessonDestroyAPIView, PaymentListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView, PaymentUpdateAPIView, PaymentDestroyAPIView, SubscriptionAPIView


app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
                  path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
                  path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
                  path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
                  path('payment/<int:pk>/update/', PaymentUpdateAPIView.as_view(), name='payment_update'),
                  path('payment/<int:pk>/delete/', PaymentDestroyAPIView.as_view(), name='payment_delete'),

                  path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons_retrieve'),
                  path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons_update'),
                  path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons_delete'),

                  path('subscription/create/', SubscriptionAPIView.as_view(), name='subscription_create')
] + router.urls
