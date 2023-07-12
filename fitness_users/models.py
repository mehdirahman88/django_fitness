from django.contrib.auth.models import AbstractUser
from django.db import models


class FitnessUser(AbstractUser):
    REGULAR = 1
    TRAINER = 2
    MANAGER = 3

    ROLE_CHOICES = (
        (REGULAR, 'Regular'),
        (TRAINER, 'Premium'),
        (MANAGER, 'Manager'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=REGULAR, null=False)
