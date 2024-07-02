import datetime

from django.urls import reverse
from rest_framework import test, status

from lms.models import Course, Lesson
from users.models import User, Payment


class UserTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru', password=12345)
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """
        Тест на создание пользователя.
        """
        url = reverse('users:create_user')
        data = {'email': 'test1@bk.ru', 'password': 123}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        """
        Тест на обновление пользователя.
        """
        url = reverse('users:edit_user', args=(self.user.pk,))
        data = {'email': 'test@bk.ru', 'password': 1234}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('password'), 1234)

    def test_user_list(self):
        """
        Тест на получение списка пользователей.
        """
        url = reverse('users:users')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                'id': self.user.pk,
                'last_login': None,
                'is_superuser': False,
                'first_name': '',
                'is_staff': False,
                'is_active': True,
                'date_joined': data[0]['date_joined'],
                'email': self.user.email,
                'phone_number': None,
                'city': None,
                'city': None,
                'avatar': None,
                'groups': [],
                'user_permissions': []
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_retrieve(self):
        """
        Тест на получение одного пользователя.
        """
        url = reverse('users:user', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), self.user.email)

    def test_user_delete(self):
        """
        Тест на удаление одного пользователя.
        """
        url = reverse('users:delete_user', args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)


class PaymentTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru', password=12345)
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            link='https://youtube.com/', course=self.course)
        self.payment = Payment.objects.create(user=self.user,
                                              payment_date=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
                                              course=self.course, lesson=self.lesson, sum=2000, payment_method='cash')

    def test_payment_list(self):
        """
        Тест на получение списка платежей.
        """
        url = reverse('users:payments')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                'id': self.payment.pk,
                'payment_date': data[0]['payment_date'],
                'sum': self.payment.sum,
                'payment_method': self.payment.payment_method,
                'user': self.user.pk,
                'course': self.course.pk,
                'lesson': self.lesson.pk
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
