from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field import modelfields

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}
PAYMENT_METHOD = [
    ('cash', 'наличные'),
    ('transaction', 'перевод на счет'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    phone_number = modelfields.PhoneNumberField(verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatar', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок')
    sum = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        return f'payment for {self.lesson} ({self.course}) / {self.user}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
