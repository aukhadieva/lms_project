import smtplib

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Course
from subscription.models import Subscription


@shared_task
def send_mail_about_updates(pk):
    """
    Отложенная задача. При обновлении курса отправляет
    письмо пользователю, подписанному на курс.
    """
    course = Course.objects.get(pk=pk)
    subscriptions = Subscription.objects.filter(course=course, is_subscribed=True)
    emails = list(subscriptions.values_list('user__email', flat=True))
    try:
        send_mail(
            subject=f'Обновление курса {course.name}',
            message=f'Информация курса {course.name} обновилась, заходи на сайт, чтобы увидеть изменения!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False
        )
    except smtplib.SMTPException as error:
        raise error
