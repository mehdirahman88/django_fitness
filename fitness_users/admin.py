from django.contrib import admin
from .models import FitnessUser


@admin.register(FitnessUser)
class FitnessUserAdmin(admin.ModelAdmin):
    pass
