from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return bool(user.is_authenticated and user.user_type=="staff")

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.user_type=="managers")

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)

class IsManagerOrStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and (user.user_type=="staff" or user.user_type=="managers") )

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)