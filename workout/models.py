from django.db import models
from users.models import Coach, Client

class Workout(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='coach_workouts')
    clients = models.ManyToManyField(Client, related_name='client_workouts')
    description = models.TextField()
    target = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participans = models.IntegerField()

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
    )

    class Weekdays(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    day = models.CharField(
        choices=Weekdays.choices,
        max_length=10,
    )

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )



class Room(models.Model):
    name = models.CharField(max_length=100)

class WorkoutParticipation(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    status = models.CharField(
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

