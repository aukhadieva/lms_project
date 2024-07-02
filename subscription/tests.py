from django.urls import reverse
from rest_framework import test, status

from lms.models import Course, Lesson
from subscription.models import Subscription
from users.models import User


class SubscriptionTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            link='https://youtube.com/', course=self.course)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course, is_subscribed=False)

    def test_subscription_create(self):
        """
        Тест функционала работы подписки на обновления курса.
        """
        url = reverse('subscription:create_subscription')
        data = {'owner': self.user.pk, 'course': self.course.pk, 'is_subscribed': True}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 2)
        self.assertEqual(data.get('message'), 'подписка добавлена')
