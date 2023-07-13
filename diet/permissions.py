from rest_framework.permissions import BasePermission

from diet.constants import UserRoleChoice


class IsManagerFitnessUser(BasePermission):
    """
    Allows access only to manager FitnessUsers.
    """

    def has_permission(self, request, view):
        return bool(request.user and is_manager_fitness_user(request.user))


class IsDietRecordOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fitness_user == request.user


def is_manager_fitness_user(user):
    return hasattr(user, 'role') and user.role == UserRoleChoice.MANAGER
