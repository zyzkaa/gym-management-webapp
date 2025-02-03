from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_coach = models.BooleanField()
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        default='profile_pictures/default.png')
    gender = models.CharField(
        choices=[('M', 'Male'),
                 ('F', 'Female')],
        max_length=1)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    membership = models.ForeignKey('memberships.Membership',
                                   on_delete=models.PROTECT,
                                   null=True)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='coach')
    hourly_rate = models.FloatField()
    description = models.TextField(null=True)
    phone_number = models.IntegerField(null=True)

class Visit(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    enter_time = models.TimeField()