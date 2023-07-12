from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/records', views.DietRecordList.as_view(), name='diet-records'),
    path('api/v1/records/<int:pk>', views.DietRecordRWD.as_view(), name='diet-records-info'),
    path('api/v1/records/add', views.DietRecordCreate.as_view(), name='diet-records-add'),

    path('api/v1/users/<int:user_id>/records', views.UserDietRecordList.as_view(), name='diet-user-records'),
]