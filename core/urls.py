from django.urls import path

from workout.urls import app_name
from . import views

app_name='core'

urlpatterns = [
    path('', views.home, name='home'),
]
