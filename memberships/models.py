from django.db import models
from users.models import User

class Payment(models.Model):
    date = models.DateField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ])
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('scheduled', 'Scheduled'),
        ],
        default='pending'
    )

class Membership(models.Model):
    name = models.CharField(max_length=50)
    price_1 = models.FloatField()
    price_6 = models.FloatField()
    price_12 = models.FloatField()
