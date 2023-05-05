from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


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
        if request.method in permissions.SAFE_METHODS:
            return True
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
