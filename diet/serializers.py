from rest_framework import serializers

from diet.models import DietRecord


class DietRecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    fitness_user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DietRecord
        fields = ['id', 'fitness_user_id', 'diet_date',  'diet_time', 'diet_description', 'approximate_calorie']


class DietRecordListCreateSerializer(DietRecordSerializer):
    fitness_user_id = serializers.IntegerField(read_only=False)


class DietRecordRWDSerializer(DietRecordSerializer):
    pass
