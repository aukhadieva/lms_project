from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserViewSerializer


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


class PaymentListAPIView(generics.ListAPIView):
    """
    Payment list endpoint.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)
