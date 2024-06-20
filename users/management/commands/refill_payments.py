import json

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):

    @staticmethod
    def read_payments() -> list[dict]:
        """
        Получает данные из фикстуры.
        """
        with open('fixtures/payment.json') as json_file:
            load_payments = json.load(json_file)
            return load_payments

    def handle(self, *args, **options):
        """
        Заполняет БД, предварительно зачистив ее от старых данных.
        """
        Payment.objects.all().delete()

        payment_for_create = []

        for payment in Command.read_payments():
            payment_for_create.append(Payment(id=payment['pk'],
                                              user=User.objects.get(pk=payment['fields']['user']),
                                              payment_date=payment['fields']['payment_date'],
                                              course=Course.objects.get(pk=payment['fields']['course']),
                                              lesson=Lesson.objects.get(pk=payment['fields']['lesson']),
                                              sum=payment['fields']['sum'],
                                              payment_method=payment['fields']['payment_method']))

        Payment.objects.bulk_create(payment_for_create)
