from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from lms.models import Course
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Удаляет или добавляет подписку в зависимости от ее наличия в БД
        и возвращает соответствующее сообщение пользователю.
        """
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item, is_subscribed=True)
        if not created:
            subscription.delete()
            message = 'подписка удалена'
        else:
            message = 'подписка добавлена'

        # Возвращает ответ в API
        return Response({"message": message})
