from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import OrderSerializer


class OrderView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
