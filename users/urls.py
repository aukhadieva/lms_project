from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (UserUpdateAPIView, PaymentListAPIView, PaymentCreateAPIView, UserListAPIView,
                         UserCreateAPIView, UserRetrieveAPIView, UserDestroyAPIView, PaymentDetailView)

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='create_user'),
    path('user/edit/<int:pk>/', UserUpdateAPIView.as_view(), name='edit_user'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('api/token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='create_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='refresh_token'),

    path('payment/success/<int:pk>/', PaymentDetailView.as_view(), name='success_url')
]
