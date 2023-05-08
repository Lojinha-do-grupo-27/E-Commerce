from products.models import ProductCart
from products.serializers import ProductCartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .serializers import CartSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from users.permissions import IsAccountOwner
from rest_framework.permissions import IsAuthenticated

class CartView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CartSerializer
    lookup_url_kwarg = "fk"


class CartDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        user = self.request.user
        cart_id = user.cart_id
        queryset = ProductCart.objects.filter(cart_id=cart_id)
        serializer = ProductCartSerializer(queryset, many=True)
        return serializer.data