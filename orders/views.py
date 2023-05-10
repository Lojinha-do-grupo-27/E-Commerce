from django.http import Http404
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import (
    IsAccountOwnerOrAdm,
    IsProductSellerOwner,
    IsAdminOrSellerOrOwner,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .models import Order, StatusChoices
from .serializers import OrderSerializer
from users.models import User
from products.models import Product, ProductCart
from carts.models import Cart
from exceptions import EmptyCart, NotInStock


class OrderView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdm]
    serializer_class = OrderSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        queryset = Order.objects.filter(user_id=user_id)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.list(serializer.data)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["user_id"])
        cart_id = User.objects.get(id=kwargs["user_id"]).cart_id

        if not cart_id:
            raise EmptyCart

        products_cart = ProductCart.objects.filter(cart_id=cart_id).select_related(
            "product"
        )

        products_by_seller = []
        orders = []
        for product_cart in products_cart:            
            if not product_cart.product.user_id in products_by_seller:
                seller_order = {
                    "seller_id": product_cart.product.user_id,
                    "products": [],
                    "status": "Pedido realizado",
                    "total_value": product_cart.values
                }

                product_dict = {
                    "product_id": product_cart.product.id,
                    "name": product_cart.product.name,
                    "quantity": product_cart.quantity,
                    "price": product_cart.product.price,
                    "total_value": product_cart.values,
                }

                seller_order["products"].append(product_dict)
                products_by_seller.append(product_cart.product.user_id)
                orders.append(seller_order)
            else:
                for seller_order in orders:
                    if seller_order['seller_id'] == product_cart.product.user_id:
                        product_dict = {
                            "product_id": product_cart.product.id,
                            "name": product_cart.product.name,
                            "quantity": product_cart.quantity,
                            "price": product_cart.product.price,
                            "total_value": product_cart.values,
                        }
                        seller_order['products'].append(product_dict)
                        seller_order['total_value'] += product_cart.values


        for order_dict in orders:
            order = Order.objects.create(
                seller_id=order_dict["seller_id"], user=user, status=StatusChoices.PEDIDO_REALIZADO
            )
            
            for product_dict in order_dict["products"]:
                product_obj = Product.objects.get(id=product_dict["product_id"])

                if not product_obj.is_available:
                    message = f" there isn't enought {product_dict['name']} in stock, the quantity available is just {product_obj.stock}"
                    raise NotInStock(message)

                order.products.add(product_dict["product_id"])
            
                product_obj.stock -= product_dict["quantity"]

                if product_obj.stock == 0:
                    product_obj.is_available = False
                
                product_obj.save()
            
            order.save()
            user_email = user.email
            send_mail(
                subject="Your order has generated.",
                message=f'You order has generated at {order.created_at}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )
        
        cart = Cart.objects.get(id=cart_id)
        cart.delete()

        return Response(orders)


class OrderDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProductSellerOwner, IsAdminOrSellerOrOwner]
    serializer_class = OrderSerializer

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    lookup_url_kwarg = "id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = queryset.filter(**filter_kwargs).first()
        if obj is None:
            raise Http404("No order found matching the given query.")
        return obj
