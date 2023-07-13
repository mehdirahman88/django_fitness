from rest_framework import generics

from fitness_users import serializers
from fitness_users.models import FitnessUser


class FitnessUserListCreate(generics.ListCreateAPIView):
    queryset = FitnessUser.objects.all()
    serializer_class = serializers.FitnessUserListCreateSerializer


class FitnessUserInfoRW(generics.RetrieveUpdateAPIView):
    queryset = FitnessUser.objects.all()
    serializer_class = serializers.FitnessUserRWSerializer
