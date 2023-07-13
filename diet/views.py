from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from diet import serializers, permissions as custom_permissions
from diet.constants import UserRoleChoice
from diet.models import DietRecord


class DietRecordListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DietRecordListCreateSerializer

    def get_queryset(self):
        if custom_permissions.is_manager_fitness_user(self.request.user) or self.request.user.is_staff:
            queryset = DietRecord.objects.all()
            return queryset
        raise PermissionDenied("You are not allowed to view all records.")

    def perform_create(self, serializer):
        fitness_user_id_in_request = serializer.validated_data['fitness_user_id']
        if fitness_user_id_in_request == self.request.user.id:
            serializer.save()
            return
        raise PermissionDenied("You are not allowed to create a DietRecord for another user.")


class DietRecordRWD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.IsDietRecordOwner]
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordRWDSerializer


class UserDietRecordList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DietRecordRWDSerializer

    def get_queryset(self):
        user_id_in_url = self.kwargs['user_id']
        logged_in_user = self.request.user
        if user_id_in_url == logged_in_user.id or custom_permissions.is_manager_fitness_user(logged_in_user):
            queryset = DietRecord.objects.filter(fitness_user_id=user_id_in_url)
            return queryset
        raise PermissionDenied("You are not allowed to view.")
