from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        """
        Привязывает курс к пользователю.
        """
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        """
        Привязывает урок к пользователю.
        """
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [~IsModerator | IsOwner]
