import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Команда для создания суперюзера.
        """
        superuser = User.objects.create(
            email="admin@bk.ru",
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        superuser.set_password(os.getenv("SU_PASSWORD"))
        superuser.save()
