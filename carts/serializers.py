from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Cart
from products.models import Product

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id"]
        read_only_fields = ["id"]

    def create(self, request, validated_data, pk: int):
        product = get_object_or_404(Product, pk=pk)

        if not product['quantity'] <= request.data['quantity']:
            raise ValueError("We don't have this quantity in stock")
        
        total_value = product['price'] * request.data['quantity']

        dict = {
            "name": product['name'],
            "value": total_value
        }

        cart = Cart.objects.create(**validated_data, product=product)

        return dict

    def update(self, instance: Cart, validated_data: dict) -> Cart:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
