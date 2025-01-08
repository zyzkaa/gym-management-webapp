from django.urls import path
from . import views


urlpatterns = [
    path("<int:user_id>/", views.get_username, name="user_id"),
    path("register/", views.register, name="register"),
    path("users/", views.get_users, name="users"),
]