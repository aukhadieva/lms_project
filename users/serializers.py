from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment
from users.services import checkout_session


class PaymentSerializer(serializers.ModelSerializer):
    payment_status = SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_status(self, obj):
        """
        Получает статус платежа.
        """
        session = obj.session_id
        status = checkout_session(session)
        return status


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_name',)
