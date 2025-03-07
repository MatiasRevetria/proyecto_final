from django.urls import path
from django.contrib.auth.forms import UserCreationForm
from .views import *
#from . import views => views.<funcion>

urlpatterns = [
    path('',login_user),
]