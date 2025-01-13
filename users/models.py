from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
    gender = models.CharField(
        choices=[('M', 'Male'),
                 ('F', 'Female')],
        max_length=1)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    membership = models.ForeignKey('users.Membership',
                                   on_delete=models.PROTECT,
                                   null=True)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='coach')
    hourly_rate = models.FloatField()
    description = models.TextField(null=True)
    phone_number = models.IntegerField(null=True)

class Membership(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    price = models.FloatField()

class Review(models.Model):
    rating = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='reviews')

class Payment(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments')
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
            ('failed', 'Failed'),
            ('scheduled', 'Scheduled'),
        ],
        default='pending'
    )




# class UserAttributes(models.Model):
#     membership_type = models.CharField(max_length=20, default='none', choices=[
#             ('basic', 'basic'),
#             ('premium', 'premium'),
#             ('none', 'none')
#         ])
#
# class CoachAttributes(models.Model):
#     hourly_rate = models.FloatField()
#
# class User(AbstractUser):
#     class Role(models.TextChoices):
#         USER = 'u', 'user'
#         COACH = 'c', 'coach'
#         ADMIN = 'a', 'admin'
#
#     role = models.CharField(
#         max_length = 1,
#         default = Role.USER,
#         choices = Role.choices
#     )
#
#     userAttributes = models.ForeignKey(
#         UserAttributes,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='user')
#     coachAttributes = models.ForeignKey(
#         CoachAttributes,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='coach')

# class User(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=128)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.username
#
# class Client(User):
#     membership_type = models.CharField(max_length=20, default='none', choices=[
#         ('basic', 'basic'),
#         ('premium', 'premium'),
#         ('none', 'none')
#     ])
#
# class Coach(User):
#     hourly_rate = models.FloatField()