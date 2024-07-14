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
    которые не заходили в учетную запись более месяца на неактивный.
    """
    users = User.objects.filter(is_active=True)

    for user in users:
        current_date_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user_last_login = user.last_login

        if user_last_login < (current_date_time - relativedelta(months=1)):
            user.is_active = False
            user.save()
