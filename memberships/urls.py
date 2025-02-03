from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path("show/", views.show_memberships, name="show_memberships"),
    path("cancel_membership", views.cancel_membership, name="cancel_membership"),
]