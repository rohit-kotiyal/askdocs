from rest_framework.permissions import BasePermission


class IsOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return bool(
            user.is_authenticated
            and user.organization_id
            and user.role == "admin"
        )
