from datetime import datetime

import pytz
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from config import settings
from lms.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserViewSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, checkout_session


class UserCreateAPIView(generics.CreateAPIView):
    """
    User create endpoint.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Хэширует создаваемый при регистрации пароль.
        """
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.last_login = datetime.now(pytz.timezone(settings.TIME_ZONE))
        instance.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    User update endpoint.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]

    def perform_update(self, serializer):
        """
        Хэширует редактируемый пароль.
        """
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserListAPIView(generics.ListAPIView):
    """
    User list endpoint.
    """
    serializer_class = UserViewSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    User retrieve endpoint.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора, который будет использоваться для сериализации объекта.
        """
        if self.request.user.email == self.get_object().email:
            return UserSerializer
        else:
            return UserViewSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    User destroy endpoint.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class PaymentListAPIView(generics.ListAPIView):
    """
    Payment list endpoint.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Payment create endpoint.
    """
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """
        Привязывает платеж (с использованием stripe) к пользователю.
        """
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get('course')
        lesson_id = self.request.data.get('lesson')
        if course_id:
            course_product = create_stripe_product(Course.objects.get(pk=course_id).name)
            course_price = create_stripe_price(instance.course.amount, course_product)
            session_id, payment_link = create_stripe_session(course_price, instance.pk)
        else:
            lesson_product = create_stripe_product(Lesson.objects.get(pk=lesson_id).name)
            lesson_price = create_stripe_price(instance.lesson.amount, lesson_product)
            session_id, payment_link = create_stripe_session(lesson_price, instance.pk)

        payment_status = checkout_session(session_id)
        instance.payment_status = payment_status
        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()


class PaymentDetailView(DetailView):
    """
    Представление для платежа.
    """
    model = Payment
