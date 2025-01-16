from django.urls import path
from . import views

app_name = 'workout'

urlpatterns = [
    path('add/', views.add_workout, name='add_workout'),
    path('schedule/', views.schedule, name='schedule'),
    path('join/', views.join_workout, name='join_workout'),
]