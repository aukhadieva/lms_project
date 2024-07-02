from django.db import models

from config import settings
from lms.models import Course


class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='курс')
    is_subscribed = models.BooleanField(default=False, verbose_name='признак подписки')

    def __str__(self):
        return f'{self.user} subscription to {self.course}: {self.is_subscribed}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
