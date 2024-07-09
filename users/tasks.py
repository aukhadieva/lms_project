from datetime import datetime

import pytz
from celery import shared_task

from dateutil.relativedelta import relativedelta

from config import settings
from users.models import User


@shared_task
def check_last_login():
    """
    Периодическая задача. Меняет статус пользователей,
    которые заходили в учетную запись более месяца на неактивный.
    """
    users = User.objects.filter(is_active=True)

    for user in users:
        filtered_user = User.objects.get(pk=user.pk)

        current_date_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user_last_login = filtered_user.last_login
        not_active = user_last_login + relativedelta(months=1)

        if current_date_time > not_active:
            filtered_user.is_active = False
            filtered_user.save()
