from django.db import models
from django.utils import timezone
from django.db.models import Avg
from user_login.models import *


DIFICULTADES = [
    ('Facil', 'Facil'),
    ('Media', 'Media'),
    ('Dificil','Dificil')
]

CATEGORIAS = [
    ('Desayuno', 'Desayuno'),
    ('Almuerzo', 'Almuerzo'),
    ('Merienda', 'Merienda'),
    ('Cena','Cena')
]
    
VALORACION = [
    (1,'⭐'),
    (2,'⭐⭐'),
    (3,'⭐⭐⭐'),
    (4,'⭐⭐⭐⭐'),
    (5,'⭐⭐⭐⭐⭐')
]
# Create your models here.

class Receta(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    coccion = models.IntegerField(default=0)
    cooked = models.BooleanField(default=False)
    favs = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to="recetas_image/", null=True, blank=True)
    categoria = models.CharField(max_length=10,choices=CATEGORIAS, default= 'Sin categoria')
    dificultad = models.CharField(max_length=10, choices=DIFICULTADES, default='Fácil')

    @property
    def promedio_valoracion(self):
        return self.valoraciones.aggregate(prom=Avg('puntaje'))['prom'] or 0
    
    def __str__(self):
        return self.title + ' - ' + self.user.name
    
class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()


    class Meta:
        unique_together = ('receta', 'user')  # un usuario no puede valorar la misma receta más de una vez

    def __str__(self):
        return f"{self.user.name} valoró {self.receta.title} con {self.puntaje} estrellas"



class Comentario(models.Model):
    txt = models.TextField()
    date = models.DateField(default=timezone.now)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.receta + self.txt + self.date + self.user 

class Ingrediente(models.Model):
    name = models.CharField(max_length=255)
    unidad = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name + self.unidad
    

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="ingredientes")
    nombre = models.CharField(max_length=255)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.nombre} - {self.cantidad} {self.unidad}"


class Carrito(models.Model):
    total_ingredientes = models.IntegerField()

class CarritoIngrediente(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente,on_delete=models.CASCADE)

class Registro(models.Model):
    fecha = models.DateField(default=timezone.now)
    notas = models.TextField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)

class RecetaFavorita(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.name + self.receta.title
    
class RecetaCocinada(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + self.receta.title

class Notificacion(models.Model):
    tipo = models.CharField(max_length=255)
    msj = models.TextField()
    fecha = models.DateField(default=timezone.now)
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)

class ListaCompra(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    creada = models.DateTimeField(auto_now_add=True)
    comprada = models.BooleanField(default=False)

    def vaciar(self):
        self.items.all().delete()
        self.comprada = True
        self.save()

    def __str__(self):
        return f"Lista de {self.user.name} - {'Comprada' if self.comprada else 'Pendiente'}"

class ItemListaCompra(models.Model):
    lista = models.ForeignKey(ListaCompra, on_delete=models.CASCADE, related_name='items')
    nombre = models.CharField(max_length=255)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} {self.unidad}"