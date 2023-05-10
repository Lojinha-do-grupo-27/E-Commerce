from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Product, ProductCart


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Product.objects.all())],
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "category",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "user_id",
        ]

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user.id
        return Product.objects.create(**validated_data)


class ProductCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCart
        fields = ["id", "cart_id", "product_id", "values", "quantity"]

        def create(self, validated_data: dict):
            ProductCart.objects.create(**validated_data)

