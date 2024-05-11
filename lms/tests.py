from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Lesson, Course
from users.models import User, Subscription


class LessonTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.test',
            password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test',
            description='course description',
            owner=self.user
        )

    def test_create_lesson(self):
        """Создание урока"""
        data = {
            'name': 'test',
            'description': 'test description',
            'url': 'http://www.youtube.com/watch?v=tSOksGcGJCI&list',
            'owner': self.user.id,
            'course': self.course.id
        }
        # self.client.force_authenticate(user=self.user)

        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        """Вывод списка уроков"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/lesson/list/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Обновление данных урока"""

        lesson = Lesson.objects.create(
            owner=self.user,
            name='test name',
            description='test description',
            course=self.course,
            url='https://www.youtube.com/watch?v=video'
        )

        response = self.client.patch(
            f'/lesson/update/{lesson.id}/',
            data={
                'name': 'updated name',
                "description": 'updated description'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Удаление урока"""
        lesson = Lesson.objects.create(
            owner=self.user,
            name='test name',
            description='test description',
            course=self.course,
            url='https://www.youtube.com/watch?v=video'
        )

        response = self.client.delete(
            f'/lesson/delete/{lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.test',
            password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test',
            description='course description',
            owner=self.user
        )

    def test_subscription_enabled(self):
        data = {
            'course': self.course.id,
        }
        response = self.client.post(
            '/users/subscription/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "подписка добавлена"})

    def test_subscription_disabled(self):
        Subscription.objects.create(
            course=self.course,
            user=self.user,
            status=True
        )

        data = {
            "course": self.course.id,
        }

        response = self.client.post(
            '/users/subscription/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        )
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
