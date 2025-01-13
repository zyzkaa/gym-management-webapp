from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addWorkout, name='add_workout'),
]