from django.urls import path
from .views import *

urlpatterns = [
    path('home/',main_page),
    path('logout/',logout_user),
#   path('recetas/<int:id>',recetas),
    path('recetas/',recetas),
    path('favoritas/',favoritas),
    path('nueva/',crear_receta),
    path('editar/<int:id>' , editar_receta, name='editar_receta'),
    path('receta/<int:id>',eliminar_receta, name='eliminar_receta')
]