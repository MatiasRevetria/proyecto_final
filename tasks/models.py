from django.db import models
from user_login.models import *

# Create your models here.
class Receta(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    cooked = models.BooleanField(default=False)
    favs = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + self.user.name
    
class Valoracion(models.Model):
    stars = models.IntegerChoices()
    comment = models.TextField()
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)


class Categoria(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Comentario(models.Model):
    txt = models.TextField()
    date = models.DateField()
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.receta + self.txt + self.date + self.user 

class Ingrediente(models.Model):
    name = models.CharField(max_length=255)
    unidad = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name + self.cantidad
    

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente,on_delete=models.CASCADE)

class Carrito(models.Model):
    total_ingredientes = models.IntegerField()

class CarritoIngrediente(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente,on_delete=models.CASCADE)

class Registro(models.Model):
    fecha = models.DateField()
    notas = models.TextField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)

class RecetaFavorita(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.name + self.receta.title

class Notificacion(models.Model):
    tipo = models.CharField(max_length=255)
    msj = models.TextField()
    fecha = models.DateField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)