from django.conf import settings
from django.conf.urls.static import static
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
    path('eliminar/<int:id>',eliminar_receta, name='eliminar_receta'),
    path('mis_recetas/',mis_recetas, name = 'mis_recetas'),
    path('cocinado/<int:receta_id>', marcar_cocinada, name= 'marcar_cocinada'),
    path('noconinada/<int:receta_id>',desmarcar_cocinada, name= 'desmarcar_cocinada'),
    path('favorita/<int:receta_id>', marcar_favorita, name= 'marcar_favorita'),
    path('nofavorita/<int:receta_id>',desmarcar_favorita, name='desmarcar_favorita'),
    path('valorar/<int:receta_id>/', valorar_receta, name='valorar_receta')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)