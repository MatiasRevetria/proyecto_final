from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('home/',MainPageView.as_view()),
    path('logout/',LogoutUserView.as_view()),
#   path('recetas/<int:id>',recetas),
    path('recetas/',RecetaListView.as_view(), name='recetas'),
    path('favoritas/',FavoritasView.as_view(), name='favoritas'),
    path('cocinadas/',CocinadasView.as_view(), name='cocinadas'),
    path('nueva/',CrearRecetaView.as_view()),
    path('editar/<int:pk>' , EditarRecetaView.as_view(), name='editar_receta'),
    path('eliminar/<int:pk>',EliminarRecetaView.as_view(), name='eliminar_receta'),
    path('mis_recetas/',MisRecetasView.as_view(), name = 'mis_recetas'),
    path('cocinado/<int:receta_id>', MarcarCocinadaView.as_view(), name= 'marcar_cocinada'),
    path('noconinada/<int:receta_id>',DesmarcarCocinadaView.as_view(), name= 'desmarcar_cocinada'),
    path('favorita/<int:receta_id>', MarcarFavoritaView.as_view(), name= 'marcar_favorita'),
    path('nofavorita/<int:receta_id>',DesmarcarFavoritaView.as_view(), name='desmarcar_favorita'),
    path('valorar/<int:receta_id>/', ValorarRecetaView.as_view(), name='valorar_receta'),
    path('lista_compra/', VerListaCompraView.as_view(), name='ver_lista_compra'),
    path('generar_lista/', GenerarListaCompraView.as_view(), name='generar_lista'),
    path('marcar_lista/', MarcarListaComoCompradaView.as_view(), name='marcar_lista'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)