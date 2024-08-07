from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(name="Test Course", creator=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {"name": "Course Name", "creator": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.last().name, data["name"])

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data_ = {"name": "Course Name"}
        response = self.client.patch(url, data_)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), data_["name"])

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@test.ru")
        self.course = Course.objects.create(name="Test Course", creator=self.user)
        self.lesson = Lesson.objects.create(
            name="Test Lesson", course=self.course, creator=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        self.user.add_to_moderators_group()
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "name": "Lesson Name",
            "creator": self.user.pk,
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().name, data["name"])

    def test_lesson_update(self):
        self.user.add_to_moderators_group()
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data_ = {"name": "Lesson Name"}
        response = self.client.patch(url, data_)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), data_["name"])

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    url = reverse("materials:subscription_create")

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        another_user = User.objects.create(email="another_user@test.com")
        self.course = Course.objects.create(name="Test Course", creator=another_user)
        self.client.force_authenticate(user=self.user)

    def test_anonymous_user_failed_to_subscribe_on_course(self):
        self.client.logout()
        response = self.client.post(self.url, data={"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_failed_to_subscribe_on_not_existing_course(self):
        self.user.subscription_set.create(course=self.course)
        response = self.client.post(self.url, data={"course": 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_have_to_subscribe_on_course(self):
        response = self.client.post(self.url, data={"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_have_to_unsubscribe_on_course(self):
        self.user.subscription_set.create(course=self.course)
        response = self.client.post(self.url, data={"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
