from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User
from orders.models import Order
from products.models import ProductCart


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser


class IsSeller(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser) or (
            request.user.is_authenticated and request.user.is_seller
        )


class IsAdminOrSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_seller
        )


class IsAdminToListAndReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.is_seller
            )
        return True


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user


class IsAccountOwnerOrAdm(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return (request.user.is_authenticated and obj == request.user) or (
            request.user.is_authenticated and request.user.is_superuser
        )


class IsProductSellerOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Order):
        order_product = ProductCart.objects.filter(order_id=obj.id).first()

        if request.method == "GET":
            return True

        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return (
            request.user.is_authenticated
            and request.user.id == order_product.product.seller.id
        )


class IsAdminOrSellerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Order):
        if request.method == "PATCH":
            return True

        if (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_seller
        ):
            return True

        return request.user.is_authenticated and request.user.id == obj.client_id
