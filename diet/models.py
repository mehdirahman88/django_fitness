from django.db import models
from django.utils import timezone

from fitness_users.models import FitnessUser


class DietRecord(models.Model):
    fitness_user_id = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, related_name='diet_records', null=False)
    diet_date = models.DateField(null=False)
    diet_time = models.TimeField(null=False)
    diet_description = models.TextField(null=False)
    approximate_calorie = models.IntegerField(default=0)

    record_created = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.fitness_user} | {self.diet_date} | {self.diet_time} | {self.approximate_calorie}"
    