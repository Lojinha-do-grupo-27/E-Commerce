from django.http import Http404
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import (
    IsAccountOwnerOrAdm,
    IsAdminOrSeller,
    IsProductSellerOwner,
    IsAdminOrSellerOrOwner,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Order, StatusChoices
from .serializers import OrderSerializer
from users.models import User
from products.models import ProductCart


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
        cart_id = User.objects.get(id=kwargs["user_id"]).cart_id
        products_cart = ProductCart.objects.filter(cart_id=cart_id).select_related(
            "product"
        )

        products_by_seller = {}

        for product_cart in products_cart:
            product_dict = {
                "product_id": product_cart.product.id,
                "quantity": product_cart.quantity,
                "values": product_cart.values,
                "seller_id": product_cart.product.user_id,
            }

            seller_id = product_cart.product.user_id
            if seller_id not in products_by_seller:
                products_by_seller[seller_id] = []
            products_by_seller[seller_id].append(product_dict)

        orders = []
        user = get_object_or_404(User, id=kwargs["user_id"])
        for seller_id, seller_data in products_by_seller.items():
            products = [product_dict["product_id"] for product_dict in seller_data]
            order = Order.objects.create(
                seller_id=seller_id, user=user, status=StatusChoices.PEDIDO_REALIZADO
            )
            for product_dict in seller_data:
                order.products.add(product_dict["product_id"])
            orders.append(order)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


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
