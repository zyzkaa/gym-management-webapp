from django.urls import path
from . import views

app_name = 'workout'

urlpatterns = [
    path('add/', views.add_workout, name='add_workout'),
    path('schedule/', views.schedule, name='schedule'),
    path('join/', views.join_workout, name='join_workout'),
    path('leave/', views.leave_workout, name='leave_workout'),
    path('delete/', views.delete_workout, name='delete_workout'),
    path('edit/', views.edit_workout, name='edit_workout'),
    path('details/<int:workout_id>', views.details_workout, name='details_workout'),
    path('remove_from_workout/',  views.remove_client_from_workout, name='remove_client'),
]