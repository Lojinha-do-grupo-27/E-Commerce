from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id","street","number","complement","city","state","zip_code","neighborhood"]
        read_only_fields = ['id']