from products.models import ProductCart, Product
from products.serializers import ProductCartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .serializers import CartSerializer
from .models import Cart
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from exceptions import NotInStock


class CartRetrieveView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        user = self.request.user
        cart_id = user.cart_id
        queryset = ProductCart.objects.filter(cart_id=cart_id)
        serializer = ProductCartSerializer(queryset, many=True)
        return serializer.data


class CartCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_url_kwarg = "fk"


class CartDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = ProductCart.objects.all()
    lookup_url_kwarg = "product_id"

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        cart_id = user.cart_id
        product_id = kwargs["product_id"]
        product_cart_obj = ProductCart.objects.filter(cart_id=cart_id, product_id=product_id).first()        
        new_quantity = request.data['quantity']
        product_obj = Product.objects.get(id=product_id)
        if new_quantity > product_obj.stock:
            raise NotInStock()
        
        serializer = ProductCartSerializer(product_cart_obj, data={'quantity': new_quantity}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        cart_id = user.cart_id
        product_id = kwargs["product_id"]
        product_cart_obj = ProductCart.objects.filter(cart_id=cart_id, product_id=product_id).first()
        ProductCart.delete(product_cart_obj)
        return Response(status=204)