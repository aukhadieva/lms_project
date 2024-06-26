from django.urls import path

from users.apps import UsersConfig
from users.views import (UserUpdateAPIView, PaymentListAPIView, UserListAPIView, UserCreateAPIView, UserRetrieveAPIView,
                         UserDestroyAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='create_user'),
    path('user/edit/<int:pk>/', UserUpdateAPIView.as_view(), name='edit_user'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
]
