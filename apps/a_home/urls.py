from django.urls import path
#from a_home.views import *
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
]
