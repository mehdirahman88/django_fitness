from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/users', views.FitnessUserListCreate.as_view(), name='fitness-users-list-create'),
    path('api/v1/users/<int:pk>', views.FitnessUserInfoRW.as_view(), name='fitness-users-info'),
]
