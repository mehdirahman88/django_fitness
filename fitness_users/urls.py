from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/users', views.FitnessUserList.as_view(), name='fitness-users-list'),
    path('api/v1/users/<int:pk>', views.FitnessUserInfoRW.as_view(), name='fitness-users-info'),
    path('api/v1/users/add', views.FitnessUserCreate.as_view(), name='fitness-users-create'),
]