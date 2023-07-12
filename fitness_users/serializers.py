from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from fitness_users.models import FitnessUser


class FitnessUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = FitnessUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


class FitnessUserCreateSerializer(FitnessUserSerializer):
    pass


class FitnessUserRWSerializer(FitnessUserSerializer):
    role = serializers.ReadOnlyField()




