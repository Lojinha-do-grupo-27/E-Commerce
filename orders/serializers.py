from rest_framework import serializers

from .models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'products_ids', 'statu', 'seller_id', 'products', 'seller', 'user']
        write_only_fields = ['products_ids', 'seller_id']
        read_only_fields = ['products', 'seller']

    def create(self, request, view):
        user = User.objects.get(pk=request.user.id)
        print(user)

    def get():
        ...
