from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("my_profile/", views.current_profile, name="current_profile"),
    path("logout/", views.logout_user, name="logout"),
    path("add_visit/<int:user_id>/", views.add_visit, name="add_visit"),
    path("coaches/", views.show_coaches, name="coaches"),
]