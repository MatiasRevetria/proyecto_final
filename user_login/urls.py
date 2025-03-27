from django.urls import path
from django.contrib.auth.forms import UserCreationForm
from .views import *
#from . import views => views.<funcion>

urlpatterns = [
    path('register/',create_user),
    path('login/',login_user),
]