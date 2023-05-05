from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from users.permissions import IsAdminOrSeller, IsSeller


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrSeller]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrSeller]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductFilterView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category"]
    search_fields = ["name"]
    ordering_fields = ["name", "price"]
    ordering = ["name"]

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.query_params.get("name", None)
        category = self.request.query_params.get("category", None)
        id = self.request.query_params.get("id", None)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if category:
            queryset = queryset.filter(category__icontains=category)

        if id:
            queryset = queryset.filter(id=id)

        return queryset
