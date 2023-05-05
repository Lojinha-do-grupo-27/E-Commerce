from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from .models import Cart
from products.models import Product
from exceptions import NotInStock
from users.models import User
from products.serializers import ProductCartSerializer

class CartSerializer(serializers.ModelSerializer):

    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "quantity"]
        read_only_fields = ["id", "quantity"]
    
    def get_quantity(self, obj):
        return obj

    def create(self, validated_data: dict):
        user_id = self.context['request'].user.id
        user_obj = User.objects.get(id=user_id)
        user_dict = model_to_dict(user_obj)

        fk = self.context['view'].kwargs['fk']

        product = get_object_or_404(Product, pk=fk)

        product_dict = model_to_dict(product)

        quantity = self.context['request'].data.get('quantity')

        if product_dict['stock'] <= quantity:
            raise NotInStock()

        total_value = product_dict['price'] * quantity
        
        if not user_dict['cart']:
            cart = Cart.objects.create(user=user_obj)
        else:
            cart = user_dict['cart']
        
        print('cart')

        # dict = {
        #     "cart": cart,
        #     "product": product,
        #     "quantity": quantity,
        #     "values": total_value
        # }

        # cart = ProductCartSerializer.validated_data(dict)
        # ProductCartSerializer.is_valid(cart, raise_exception=True)
        # cart_obj = ProductCartSerializer.save(cart)
        # cart_dict = model_to_dict(cart_obj)

        return 'user_obj'
        # return 'Product has add at cart.'

    def update(self, instance: Cart, validated_data: dict) -> Cart:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
