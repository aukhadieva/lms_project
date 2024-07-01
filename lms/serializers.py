from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_number_of_lessons(self, obj):
        """
        Возвращает количество уроков курса.
        """
        if obj.lesson_set.all().count():
            return obj.lesson_set.all().count()
        return 0
