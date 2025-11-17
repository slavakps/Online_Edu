from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.ru')
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            title='Тестовый курс',
            owner=self.user
        )

    def test_lesson_create_authenticated(self):
        """Тест создания урока авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=test'
        }
        response = self.client.post('/api/materials/lessons/create/', data)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, 'Новый урок')


    def test_lesson_create_unauthenticated(self):
        """Тест создания урока без авторизации"""
        data = {
            'title': 'Новый урок',
            'course': self.course.id
        }
        response = self.client.post('/api/materials/lessons/create/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@test.ru'
        )
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            title='Тестовый курс',
            owner=self.user
        )

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(user=self.user)

        data = {'course_id': self.course.id}
        response = self.client.post('/api/materials/subscription/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertIn('Подписка добавлена', response.data['message'])

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        self.client.force_authenticate(user=self.user)

        # Сначала создаём подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Потом удаляем её
        data = {'course_id': self.course.id}
        response = self.client.post('/api/materials/subscription/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertIn('Подписка удалена', response.data['message'])