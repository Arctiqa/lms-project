from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_payment_history(self, instance):
        payments_filtered_set = Payment.objects.filter(user=instance.pk)
        history = PaymentSerializer(payments_filtered_set, many=True).data
        return history

    class Meta:
        model = User
        fields = '__all__'
        required = ['email', 'password']
        write_only_fields = ['password']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
