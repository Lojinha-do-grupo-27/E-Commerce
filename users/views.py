from .models import User
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [Colocar permission aqui]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "pk"
