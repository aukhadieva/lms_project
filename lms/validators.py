import re

from rest_framework.exceptions import ValidationError


class LinkValidator:
    """
    Кастомный валидатор, который проверяет, на отсутствие в материалах
    ссылок на сторонние ресурсы, кроме youtube.com.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        regular_expression = re.compile('https://youtube.com/')
        tmp_value = dict(value).get(self.field)
        if not bool(regular_expression.match(tmp_value)):
            raise ValidationError('Можно указывать ссылку только на видео, размещенное на youtube')
