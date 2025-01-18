from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("profile/", views.user_current_profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("add_visit/<int:user_id>/", views.add_visit, name="add_visit"),
    path("memberships/", views.show_memberships, name="membership"),
    path("coaches/", views.show_coaches, name="coaches"),
    path("payment_<int:membership_id>/", views.payment, name="payment"),
    path("cancel_membership", views.cancel_membership, name="cancel_membership"),
]