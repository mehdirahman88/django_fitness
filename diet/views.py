from rest_framework import generics

from diet import serializers
from diet.models import DietRecord


class DietRecordCreate(generics.CreateAPIView):
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordCreateSerializer


class DietRecordRWD(generics.RetrieveUpdateDestroyAPIView):
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordRWDSerializer


class DietRecordList(generics.ListAPIView):
    queryset = DietRecord.objects.all()
    serializer_class = serializers.DietRecordListSerializer


class UserDietRecordList(generics.ListAPIView):
    serializer_class = serializers.DietRecordListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = DietRecord.objects.filter(fitness_user_id=user_id)
        return queryset
