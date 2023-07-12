from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from diet import serializers, permissions as custom_permissions
from diet.constants import UserRoleChoice
from diet.models import DietRecord


class DietRecordCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordCreateSerializer

    def perform_create(self, serializer):
        fitness_user_id_in_request = serializer.validated_data['fitness_user_id']
        if fitness_user_id_in_request != self.request.user.id:
            raise PermissionDenied("You are not allowed to create a DietRecord for another user.")
        serializer.save()


class DietRecordRWD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.IsDietRecordOwner]
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordRWDSerializer


class DietRecordList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser | custom_permissions.IsManagerFitnessUser]
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordListSerializer


class UserDietRecordList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DietRecordListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if user_id != self.request.user.id and self.request.user.role != UserRoleChoice.MANAGER:
            raise PermissionDenied("You are not allowed to view.")
        queryset = DietRecord.objects.filter(fitness_user_id=user_id)
        return queryset
