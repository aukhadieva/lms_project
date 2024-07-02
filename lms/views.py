from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginators import LmsPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LmsPaginator

    def perform_create(self, serializer):
        """
        Привязывает курс к пользователю.
        """
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
        return super().get_permissions()

    def get_queryset(self):
        """
        Проверяет права и возвращает кверисет.
        """
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)


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
    pagination_class = LmsPaginator

    def get_queryset(self):
        """
        Проверяет права и возвращает кверисет.
        """
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
