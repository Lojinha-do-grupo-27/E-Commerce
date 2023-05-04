from .models import Cart
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CartSerializer
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from users.permissions import IsAccountOwner


class CartView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    




class CartDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_url_kwarg = "pk"

    

