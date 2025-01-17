from django.db import models
from users.models import Coach, Client, User

class Workout(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coach_workouts')
    client = models.ManyToManyField(User, related_name='client_workouts')
    description = models.TextField()
    target = models.CharField(max_length=50)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    max_participans = models.IntegerField()

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        null=True,
    )

    class Weekdays(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    day = models.CharField(
        choices=Weekdays.choices,
        max_length=10,
        null=True,
    )

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
        max_length=10,
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
        max_length=10,
    )

class Visit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    enter_time = models.TimeField()

