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
    current_date_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
    inactive = current_date_time - relativedelta(months=1)
    users = User.objects.get(last_login__lte=inactive)

    for user in users:
        user.is_active = False
        user.save()
