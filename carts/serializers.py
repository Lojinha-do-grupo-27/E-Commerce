from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from .models import Cart
from products.models import Product, ProductCart
from exceptions import NotInStock
from users.models import User

class CartSerializer(serializers.ModelSerializer):

    cart_item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_item"]
        read_only_fields = ["cart_item"]
    
    def get_cart_item(self, obj):
        return obj

    def create(self, validated_data: dict):
        user_id = self.context['request'].user.id
        user_obj = User.objects.get(id=user_id)
        
        fk = self.context['view'].kwargs['fk']

        product_obj = get_object_or_404(Product, pk=fk)

        product_dict = model_to_dict(product_obj)

        quantity = self.context['request'].data.get('quantity')

        if product_dict['stock'] < quantity:
            raise NotInStock()

        total_value = product_dict['price'] * quantity

        cart = user_obj.cart
        if not cart:
            cart = Cart.objects.create()
            user_obj.cart = cart
            user_obj.save()

        product_cart = ProductCart.objects.create(
        product=product_obj,
        cart=cart,
        quantity=quantity,
        values=total_value
        )

        return {
            "cart_id": product_cart.cart_id,
            "product_id": product_cart.product_id,
            "values": product_cart.values,
            "quantity": product_cart.quantity
        }

