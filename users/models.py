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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='transaction', verbose_name='способ оплаты')
    session_id = models.CharField(max_length=255, verbose_name='id сессии', **NULLABLE)
    payment_link = models.URLField(max_length=400, verbose_name='ссылка на оплату', **NULLABLE)
    payment_status = models.CharField(max_length=30, verbose_name='статус платежа', **NULLABLE)

    def __str__(self):
        return f'payment for {self.lesson if self.lesson else self.course} / {self.user}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
