from rest_framework.permissions import BasePermission

from diet.constants import UserRoleChoice


class IsManagerFitnessUser(BasePermission):
    """
    Allows access only to manager FitnessUsers.
    """

    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role') and request.user.role == UserRoleChoice.MANAGER)


class IsDietRecordOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fitness_user == request.user
