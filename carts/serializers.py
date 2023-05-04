from rest_framework import serializers
from .models import Cart
from products.models import Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Cart:
        product_availability = Product.objects.get("is_available")
        if not product_availability:
            raise ValueError("This item is no longer in stock")

        return Cart.objects.create(**validated_data)

    def update(self, instance: Cart, validated_data: dict) -> Cart:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
