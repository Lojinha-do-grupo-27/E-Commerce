from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("orders/<uuid:user_id>/", views.OrderView.as_view()),
    path("orders/<uuid:id>/edit/", views.OrderDetailView.as_view()),
]
