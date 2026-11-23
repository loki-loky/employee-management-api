
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EmployeeManagementPermission(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        # User must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Superusers have full access
        if user.is_superuser:
            return True

        # Check user groups
        user_groups = user.groups.values_list(
            'name',
            flat=True
        )

        # Admin role
        if 'Admin' in user_groups:
            return True

        # HR role
        if 'HR' in user_groups:
            return True

        # Employee role - read-only access
        if 'Employee' in user_groups:
            return request.method in SAFE_METHODS

        return False
