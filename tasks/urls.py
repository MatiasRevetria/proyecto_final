from django.urls import path
from .views import *

urlpatterns = [
    path('home/',main_page),
    path('recetas/<int:id>',recetas),
    path('favoritas/',)
]