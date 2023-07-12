from rest_framework import serializers

from diet.models import DietRecord


class DietRecordSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = DietRecord
        fields = ['id', 'fitness_user_id', 'diet_date',  'diet_time', 'diet_description', 'approximate_calorie']


class DietRecordCreateSerializer(DietRecordSerializer):
    pass


class DietRecordRWDSerializer(DietRecordSerializer):
    fitness_user_id = serializers.ReadOnlyField()


class DietRecordListSerializer(DietRecordSerializer):
    pass
