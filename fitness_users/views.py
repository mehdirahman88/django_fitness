from rest_framework import generics

from fitness_users import serializers
from fitness_users.models import FitnessUser


class FitnessUserCreate(generics.CreateAPIView):
    queryset = FitnessUser.objects.all()
    serializer_class = serializers.FitnessUserCreateSerializer


class FitnessUserInfoRW(generics.RetrieveUpdateAPIView):
    queryset = FitnessUser.objects.all()
    serializer_class = serializers.FitnessUserRWSerializer


class FitnessUserList(generics.ListAPIView):
    queryset = FitnessUser.objects.all()
    serializer_class = serializers.FitnessUserRWSerializer
