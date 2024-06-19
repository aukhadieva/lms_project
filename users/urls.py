from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/edit/<int:pk>/', UserUpdateAPIView.as_view(), name='edit_user'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
]
