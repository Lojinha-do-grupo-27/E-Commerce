from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartRetrieveView.as_view()),
    path("cart/<uuid:fk>/new/", views.CartCreateView.as_view()),
    path("cart/<uuid:product_id>/", views.CartDetailView.as_view()),
]
