from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("profile/", views.user_current_profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
]