from rest_framework import permissions


class IsADMIN(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.role == "admin" and request.method == "DELETE":
            return True
        if (
            user.role == "admin" or user.role == "senior" and request.method == "PUT" # noqa
        ):  # noqa
            # return request.user.is_staff
            return True
        return False
