from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
    def get_number_of_lessons(self, obj):
        if obj.lesson_set.all().count():
            return obj.lesson_set.all().count()
        return 0


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
