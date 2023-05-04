from django.shortcuts import render
from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, request, product_id):

        id = product_id
        name = request.name
        category = request.category

        if id:
            return Product.objects.filter(id=id)
        elif name:
            return Product.objects.filter(name=name)
        else:
            return Product.objects.filter(category=category)
