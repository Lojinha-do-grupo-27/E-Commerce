from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

from .models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "seller_id"]
        read_only_fields = ["id", "seller_id", "products"]

    def update(self, instance, validated_data):
        user_email = instance.user.email
        send_mail(
            subject="Your order has a new update",
            message=f'Your order status has been updated to *{validated_data["status"]}*.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )

        return super().update(instance, validated_data)
