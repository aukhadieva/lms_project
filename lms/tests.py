from django.urls import reverse
from rest_framework import test, status

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            link='https://youtube.com/', course=self.course)

    def test_course_create(self):
        """
        Тест на создание курса.
        """
        url = reverse('lms:course-list')
        data = {'name': 'курс #2', 'description': 'описание курса #2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.all().exists())

    def test_course_update(self):
        """
        Тест на обновление курса.
        """
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {"name": "курс #2", "description": "описание курса ##2"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('description'), 'описание курса ##2')

    def test_course_retrieve(self):
        """
        Тест на получение одного курса.
        """
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.course.name)

    def test_course_list(self):
        """
        Тест на получение списка курсов.
        """
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.pk,
                    'number_of_lessons': 1,
                    'lessons': [
                        {'id': self.lesson.pk,
                         'name': self.lesson.name,
                         'description': self.lesson.description,
                         'img': None,
                         'link': self.lesson.link,
                         'owner': self.user.pk,
                         'course': self.course.pk}
                    ],
                    'subscriptions': False,
                    'name': self.course.name,
                    'description': self.course.description,
                    'img': None,
                    'owner': self.user.pk}
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_course_delete(self):
        """
        Тест на удаление курса.
        """
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            link='https://youtube.com/', course=self.course)

    def test_lesson_create(self):
        """
        Тест на создание урока.
        """
        url = reverse('lms:crate_lesson')
        data = {'name': 'урок #2', 'description': 'описание урока #2', 'link': 'https://youtube.com/2/',
                'course': 7}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.all().exists())

    def test_lesson_update(self):
        """
        Тест на обновление урока.
        """
        url = reverse('lms:edit_lesson', args=(self.lesson.pk,))
        data = {'name': 'урок #2', 'description': 'описание урока ##2', 'link': 'https://youtube.com/2/'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('description'), 'описание урока ##2')

    def test_lesson_list(self):
        """
        Тест на получение списка уроков.
        """
        url = reverse('lms:lessons')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    {
                        'id': self.lesson.pk,
                        'name': self.lesson.name,
                        'description': self.lesson.description,
                        'img': None,
                        'link': self.lesson.link,
                        'owner': self.user.pk,
                        'course': self.course.pk
                     }
                ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_delete(self):
        url = reverse('lms:delete_lesson', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


    def test_lesson_retrieve(self):
        """
        Тест на получение одного урока.
        """
        url = reverse('lms:lesson', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

