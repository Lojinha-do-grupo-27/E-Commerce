from django.urls import path
from . import views

urlpatterns = [
    path("cart/<uuid:fk>/", views.CartView.as_view()),
    path("cart/", views.CartDetailView.as_view()),
]
