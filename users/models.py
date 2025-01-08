from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Client(User):
    membership_type = models.CharField(max_length=20, choices=[
        ('basic', 'basic'),
        ('premium', 'premium'),
    ])

class Coach(User):
    hourly_rate = models.FloatField()