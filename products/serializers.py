from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Product.objects.all())],
    )

    class Meta:
        model = Product
        fields = ["id", "description", "price", "quantity", "is_available", "category"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)