from django.db import models
from users.models import Client, Coach

class Workout(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='coach_workouts')
    clients = models.ManyToManyField(Client, related_name='client_workouts')
