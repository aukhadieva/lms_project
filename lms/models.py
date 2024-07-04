from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    img = models.ImageField(upload_to='course/', verbose_name='превью (картинка)', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость курса', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    img = models.ImageField(upload_to='lesson/', verbose_name='превью (картинка)', **NULLABLE)
    link = models.URLField(max_length=200, verbose_name='ссылка на видео')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='курс')
    amount = models.PositiveIntegerField(verbose_name='стоимость урока', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
