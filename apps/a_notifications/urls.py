from django.urls import path
from .views import *

urlpatterns = [
    path("notifications", notification_view, name="notifications"),
]
