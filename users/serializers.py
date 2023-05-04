from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from addresses.serializers import AddressSerializer
from addresses.models import Address


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    address = AddressSerializer(required=True)

    def create(self, validated_data: dict) -> User:
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        if validated_data["is_superuser"]:
            user = User.objects.create_superuser(address=address, **validated_data)
        else:
            user = User.objects.create_user(address=address, **validated_data)
        return user

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
            "is_seller",
            "address",
        ]
        read_only_fields = ["id"]
