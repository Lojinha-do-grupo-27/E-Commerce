from rest_framework import serializers

from .models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'seller_id']
        read_only_fields = ['id', 'status', 'seller_id', 'products']
