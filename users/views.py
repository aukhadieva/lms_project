from django.contrib.auth.hashers import make_password
from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.password = make_password(instance.password)
        instance.save()
