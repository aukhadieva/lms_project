from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginators import LmsPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_mail_about_updates


@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Warning: Course delete endpoint."))
class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course.
    """
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

    def perform_update(self, serializer):
        """
        Запускает отложенную задачу send_mail_about_updates при обновлении курса.
        """
        instance = serializer.save()
        send_mail_about_updates.delay(instance.pk)
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
    """
    Lesson create endpoint.
    """
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
    """
    Lesson list endpoint.
    """
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
    """
    Lesson retrieve endpoint.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Lesson update endpoint.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Lesson destroy endpoint.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
