from django.urls import path
from .views import ProductView, ProductDetailView, ProductFilterView

urlpatterns = [
    path("products/", ProductView.as_view(), name="product-list"),
    path("products/<uuid:pk>/", ProductDetailView.as_view()),
    path("products/filter/", ProductFilterView.as_view(), name="product-list"),
]
